# -*- coding: utf-8 -*-
"""

Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: ellen.teradata@teradata.com
Secondary Owner:

This file implements the teradataml dataframe.
A teradataml dataframe maps virtually to teradata tables and views.
"""
import decimal
import inspect
import numbers
import pandas as pd
import re
import sqlalchemy
import sys
import teradataml.context.context as tdmlctx

from collections import OrderedDict
from sqlalchemy.sql import ClauseElement
from teradataml.dataframe.sql import _MetaExpression
from teradataml.dataframe.sql_interfaces import ColumnExpression

from teradataml.series.series import Series

from teradatasqlalchemy.types import BIGINT, INTEGER, PERIOD_TIMESTAMP
from teradataml.common.utils import UtilFuncs
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes

from teradataml.common.constants import AEDConstants
from teradataml.common.constants import SourceType, PythonTypes, TeradataConstants,\
    TeradataTypes, PTITableConstants, TableOperatorConstants
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.dataframe.indexer import _LocationIndexer
from teradataml.common.aed_utils import AedUtils
from teradataml.options.display import display
from teradataml.dataframe.copy_to import copy_to_sql
from teradataml.dataframe.setop import concat
from teradataml.utils.dtypes import _Dtypes
from teradataml.utils.validators import _Validators
from teradataml.table_operators.table_operator_util import _TableOperatorUtils
from teradatasqlalchemy.dialect import preparer, dialect as td_dialect
from teradatasql import OperationalError

#TODO use logger when available on master branch
#logger = teradatapylog.getLogger()

in_schema = UtilFuncs._in_schema

class DataFrame():
    """
    The teradataml DataFrame enables data manipulation, exploration, and analysis
    on tables, views, and queries on Teradata Vantage.
    """

    def __init__(self, table_name=None, index=True, index_label=None, query=None, materialize=False):
        """
        Constructor for TerdataML DataFrame.

        PARAMETERS:
            table_name:
                Optional Argument.
                The table name or view name in Teradata Vantage referenced by this DataFrame.
                Types: str

            index:
                Optional Argument.
                True if using index column for sorting, otherwise False.
                Default Value: True
                Types: bool

            index_label:
                Optional Argument.
                Column/s used for sorting.
                Types: str OR list of Strings (str)

            query:
                Optional Argument.
                SQL query for this Dataframe. Used by class method from_query.
                Types: str

            materialize:
                Optional Argument.
                Whether to materialize DataFrame or not when created.
                Used by class method from_query.

                One should use enable materialization, when the query  passed to from_query(),
                is expected to produce non-deterministic results, when it is executed multiple
                times. Using this option will help user to have deterministic results in the
                resulting teradataml DataFrame.
                Default Value: False (No materialization)
                Types: bool

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame("mytab")
            df = DataFrame("myview")
            df = DataFrame("myview", False)
            df = DataFrame("mytab", True, "Col1, Col2")

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        self._table_name = None
        self._query = None
        self._column_names_and_types = None
        self._td_column_names_and_types = None
        self._td_column_names_and_sqlalchemy_types = None
        self._nodeid = None
        self._metaexpr = None
        self._index = index
        self.__index_label = index_label if isinstance(index_label, list) or index_label is None else [index_label]
        # This attribute instructs the _index_label property to query or not query the database
        # to find the index of the table/view for a DataFrame.
        self._index_query_required = True if index_label is None else False
        self._aed_utils = AedUtils()
        self._source_type = None
        self._orderby = None
        self._undropped_index = None
        # This attribute added to add setter for columns property,
        # it is required when setting columns from groupby
        self._columns = None

        # Below matrix is list of list, where in each row contains following elements:
        # Let's take an example of following, just to get an idea:
        #   [element1, element2, element3, element4, element5, element6]
        #   e.g.
        #       ["join", join, True, (str), True, concat_join_permitted_values]

        #   1. element1 --> Argument Name, a string. ["join" in above example.]
        #   2. element2 --> Argument itself. [join]
        #   3. element3 --> Specifies a flag that mentions argument is optional or not.
        #                   False, means required and True means optional.
        #   4. element4 --> Tuple of accepted types. (str) in above example.
        #   5. element5 --> True, means validate for empty value. Error will be raised, if empty values is passed.
        #                   If not specified, means same as specifying False.
        #   6. element6 --> A list of permitted values, an argument can accept.
        #                   If not specified, it is as good as passing None. If a list is passed, validation will be
        #                   performed for permitted values.
        awu_matrix = []
        awu_matrix.append(["table_name", table_name, True, (str), True])
        awu_matrix.append(["index", index, True, (bool)])
        awu_matrix.append(["index_label", index_label, True, (str, list)])
        awu_matrix.append(["query", query, True, (str), True])
        awu_matrix.append(["materialize", materialize, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        try:
            if table_name is not None:
                self._table_name = UtilFuncs._quote_table_names(table_name)
                self._source_type = SourceType.TABLE.value
                self._nodeid = self._aed_utils._aed_table(self._table_name)

            elif query is not None:
                self._query = query
                self._source_type = SourceType.QUERY.value

                if materialize:
                    # If user requests to materialize the the query, then we should create a
                    # table instead of view and add the same in the GarbageCollector.
                    temp_table_name = UtilFuncs._generate_temp_table_name(prefix="_frmqry_t", use_default_database=True,
                                                                          quote=False,
                                                                          table_type=TeradataConstants.TERADATA_TABLE)
                else:
                    temp_table_name = UtilFuncs._generate_temp_table_name(prefix="_frmqry_v", use_default_database=True,
                                                                          quote=False)

                self._table_name = UtilFuncs._quote_table_names(temp_table_name)
                try:
                    if materialize:
                        UtilFuncs._create_table(self._table_name, self._query)
                    else:
                        UtilFuncs._create_view(self._table_name, self._query)
                except OperationalError as oe:
                    if "[Error 3707] Syntax error" in str(oe):
                        raise ValueError(Messages.get_message(
                            MessageCodes.FROM_QUERY_SELECT_SUPPORTED).format("Only \"SELECT\" queries are supported."))
                    elif "[Error 3706] Syntax error: ORDER BY is not allowed in subqueries." in str(oe):
                        raise ValueError(Messages.get_message(
                            MessageCodes.FROM_QUERY_SELECT_SUPPORTED).format("ORDER BY is not allowed in the query."))
                    elif "[Error 3706] Syntax error" in str(oe):
                        raise ValueError(Messages.get_message(
                            MessageCodes.FROM_QUERY_SELECT_SUPPORTED).format("Check the syntax."))
                    raise ValueError(Messages.get_message(
                            MessageCodes.FROM_QUERY_SELECT_SUPPORTED))

                self._nodeid = self._aed_utils._aed_query(self._query, temp_table_name)

            else:
                if inspect.stack()[1][3] not in ['_from_node', '__init__']:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_CREATE_FAIL),
                                              MessageCodes.TDMLDF_CREATE_FAIL)

            if table_name or query:
                self._metaexpr = self._get_metaexpr()
                self._get_metadata_from_metaexpr(self._metaexpr)

            self._loc = _LocationIndexer(self)
            self._iloc = _LocationIndexer(self, integer_indexing=True)

        except TeradataMlException:
            raise
        except ValueError:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_CREATE_FAIL),
                                      MessageCodes.TDMLDF_CREATE_FAIL) from err

    @classmethod
    def from_table(cls, table_name, index=True, index_label=None):
        """
        Class method for creating a DataFrame from a table or a view.

        PARAMETERS:
            table_name:
                Required Argument.
                The table name in Teradata Vantage referenced by this DataFrame.
                Types: str

            index:
                Optional Argument.
                True if using index column for sorting otherwise False.
                Default Value: True
                Types: bool

            index_label:
                Optional
                Column/s used for sorting.
                Types: str

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            df = DataFrame.from_table("sales", False)
            df = DataFrame.from_table("sales", True, "accounts")

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        return cls(table_name, index, index_label)

    @classmethod
    def from_query(cls, query, index=True, index_label=None, materialize=False):
        """
        Class method for creating a DataFrame from a table or view.

        PARAMETERS:
            query:
                Required Argument.
                Specifies the Teradata Vantage SQL query referenced by this DataFrame.
                Only "SELECT" queries are supported. Exception will be
                raised, if any other type of query is passed.
                Unsupported queries include:
                    1. DDL Queries like CREATE, DROP, ALTER etc.
                    2. DML Queries like INSERT, UPDATE, DELETE etc. except SELECT.
                    3. SELECT query with ORDER BY clause is not supported.
                Types: str

            index:
                Optional Argument.
                True if using index column for sorting otherwise False.
                Default Value: True
                Types: bool

            index_label:
                Optional Argument.
                Column/s used for sorting.
                Types: str

            materialize:
                Optional Argument.
                Whether to materialize DataFrame or not when created.

                One should use enable materialization, when the query  passed to from_query(),
                is expected to produce non-deterministic results, when it is executed multiple
                times. Using this option will help user to have deterministic results in the
                resulting teradataml DataFrame.
                Default Value: False (No materialization)
                Types: bool

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            load_example_data("dataframe","sales")
            df = DataFrame.from_query("select accounts, Jan, Feb from sales")
            df = DataFrame.from_query("select accounts, Jan, Feb from sales", False)
            df = DataFrame.from_query("select * from sales", True, "accounts")

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        return cls(index=index, index_label=index_label, query=query, materialize=materialize)

    @classmethod
    def _from_node(cls, nodeid, metaexpr, index_label=None, undropped_index=None):
        """
        Private class method for creating a DataFrame from a nodeid and parent metadata.

        PARAMETERS:
            nodeid:
                Required Argument.
                Node ID for the DataFrame.

            metaexpr:
                Required Argument.
                Parent metadata (_MetaExpression Object).

            index_label:
                Optional Argument.
                List specifying index column(s) for the DataFrame.

            undropped_index:
                Optional Argument.
                List specifying index column(s) to be retained as columns for printing.

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame._from_node(1234, metaexpr)
            df = DataFrame._from_node(1234, metaexpr, ['col1'], ['col2'])

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        df = cls()
        df._nodeid = nodeid
        df._source_type = SourceType.TABLE.value
        df._get_metadata_from_metaexpr(metaexpr)

        if isinstance(index_label, str):
            index_label = [index_label]

        if index_label is not None and all(elem in [col.name for col in metaexpr.c] for elem in index_label):
            df._index_label = index_label
        elif index_label is not None and all(UtilFuncs._teradata_quote_arg(elem, "\"", False)
                                             in [col.name for col in metaexpr.c] for elem in index_label):
            df._index_label = index_label

        # Set the flag suggesting that the _index_label is set,
        # and that a database lookup wont be required even when it is None.
        df._index_query_required = False

        if isinstance(undropped_index, str):
            undropped_index = [undropped_index]

        if undropped_index is not None and all(elem in [col.name for col in metaexpr.c] for elem in undropped_index):
            df._undropped_index = undropped_index
        elif undropped_index is not None and all(UtilFuncs._teradata_quote_arg(elem, "\"", False)
                                             in [col.name for col in metaexpr.c] for elem in undropped_index):
             df._undropped_index = undropped_index

        return df

    def __execute_node_and_set_table_name(self, nodeid, metaexpr = None):
        """
        Private method for executing node and setting _table_name,
        if not set already.

        PARAMETERS:
            nodeid:
                Required Argument.
                nodeid to execute.

            metaexpression:
                Optional Argument.
                Updated _metaexpr to validate

        EXAMPLES:
             __execute_node_and_set_table_name(nodeid)
             __execute_node_and_set_table_name(nodeid, metaexpr)

        """
        if self._table_name is None:
            self._table_name = df_utils._execute_node_return_db_object_name(nodeid, metaexpr)

    def _get_metadata_from_metaexpr(self, metaexpr):
        """
        Private method for setting _metaexpr and retrieving column names and types.

        PARAMETERS:
            metaexpr - Parent meta data (_MetaExpression object).

        RETURNS:
            None

        RAISES:
            None

        """
        self._metaexpr = metaexpr
        self._column_names_and_types = []
        self._td_column_names_and_types = []
        self._td_column_names_and_sqlalchemy_types = {}
        for col in metaexpr.c:
            if isinstance(col.type, sqlalchemy.sql.sqltypes.NullType):
                tdtype = TeradataTypes.TD_NULL_TYPE.value
            else:
                tdtype = "{}".format(col.type)

            self._column_names_and_types.append((str(col.name), UtilFuncs._teradata_type_to_python_type(col.type)))
            self._td_column_names_and_types.append((str(col.name), tdtype))
            self._td_column_names_and_sqlalchemy_types[(str(col.name)).lower()] = col.type

    def _get_metaexpr(self):
        """
        Private method that returns a TableExpression object for this dataframe.

        RETURNS:
            TableExpression object

        EXAMPLES:
            table_meta = self._get_metaexpr()

            # you can access the columns with the 'c' attribute
            table_meta.c

        """
        eng = tdmlctx.get_context()
        meta = sqlalchemy.MetaData(eng)
        db_schema = UtilFuncs._extract_db_name(self._table_name)
        db_table_name = UtilFuncs._extract_table_name(self._table_name)

        #Remove quotes because sqlalchemy.Table() does not like the quotes.
        if db_schema is not None:
            db_schema = db_schema[1:-1]
        db_table_name = db_table_name[1:-1]

        t = sqlalchemy.Table(db_table_name, meta, schema=db_schema, autoload=True, autoload_with=eng)
        return _MetaExpression(t)

    def __getattr__(self, name):
        """
        Returns an attribute of the DataFrame

        PARAMETERS:
          name: the name of the attribute

        RETURNS:
          Return the value of the named attribute of object (if found).

        EXAMPLES:
          df = DataFrame('table')

          # you can access a column from the DataFrame
          df.c1

        RAISES:
          Attribute Error when the named attribute is not found
        """

        # look in the underlying _MetaExpression for columns
        for col in self._metaexpr.c:
            if col.name == name:
                return col

        raise AttributeError("'DataFrame' object has no attribute %s" % name)

    def __getitem__(self, key):
        """
        Return a column from the DataFrame or filter the DataFrame using an expression
        The following operators are supported:
          comparison: ==, !=, <, <=, >, >=
          boolean: & (and), | (or), ~ (not), ^ (xor)

        Operands can be python literals and instances of ColumnExpressions from the DataFrame

        EXAMPLES:
          df = DataFrame('table')

          # filter the DataFrame df
          df[df.c1 > df.c2]

          df[df.c1 >= 1]

          df[df.c1 == 'string']

          df[1 != df.c2]

          df[~(1 < df.c2)]

          df[(df.c1 > 0) & (df.c2 > df.c1)]

          # retrieve column c1 from df
          df['c1']

        PARAMETERS:
          key: A column name as a string or filter expression (ColumnExpression)

        RETURNS:
          DataFrame or ColumnExpression instance

        RAISES:
          1. KeyError   - If key is not found
          2. ValueError - When columns of different dataframes are given in ColumnExpression.
        """

        try:
            # get the ColumnExpression from the _MetaExpression
            if isinstance(key, str):
                return self.__getattr__(key)

            if isinstance(key, ClauseElement):
                from teradataml.dataframe.sql import _SQLColumnExpression
                key = _SQLColumnExpression(key)
                
            # apply the filter expression
            if isinstance(key, ColumnExpression):

                if self._metaexpr is None:
                    msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
                    raise TeradataMlException(msg, MessageCodes.TDMLDF_INFO_ERROR)

                if key.get_flag_has_multiple_dataframes():
                    raise ValueError("Combining Columns from different dataframes is unsupported "
                                     "for filter [] operation.")

                clause_exp = key.compile()
                new_nodeid = self._aed_utils._aed_filter(self._nodeid, clause_exp)

                # Get the updated metaexpr
                new_metaexpr = UtilFuncs._get_metaexpr_using_parent_metaexpr(new_nodeid, self._metaexpr)
                return DataFrame._from_node(new_nodeid, new_metaexpr, self._index_label)

        except TeradataMlException:
            raise

        except ValueError:
             raise

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode) from err

        raise KeyError('Unable to find key: %s' % str(key))

    def keys(self):
        """
        RETURNS:
            a list containing the column names

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df.keys()
            ['accounts', 'Feb', 'Jan', 'Mar', 'Apr', 'datetime']
        """
        if self._column_names_and_types is not None:
            return [i[0] for i in self._column_names_and_types]
        else:
            return []

    @property
    def columns(self):
        """
        RETURNS:
            a list containing the column names

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df.columns
            ['accounts', 'Feb', 'Jan', 'Mar', 'Apr', 'datetime']
        """
        return self.keys()

    @property
    def _index_label(self):
        """
        RETURNS:
            The index_label for the DataFrame.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame.from_table('admissions_train')
            >>> df._index_label
            ['id']
        """
        if not self._index_query_required:
            return self.__index_label
        else:
            try:
                self.__index_label = df_utils._get_primary_index_from_table(self._table_name)
            except Exception as err:
                # DataFrames generated from views (top node), _index_label is None when PI fetch fails.
                self.__index_label = None
            finally:
                self._index_query_required = False

            return self.__index_label

    @property
    def loc(self):
        """
        Access a group of rows and columns by label(s) or a boolean array.

        VALID INPUTS:

            - A single label, e.g. ``5`` or ``'a'``, (note that ``5`` is
            interpreted as a label of the index, it is not interpreted as an
            integer position along the index).

            - A list or array of column or index labels, e.g. ``['a', 'b', 'c']``.

            - A slice object with labels, e.g. ``'a':'f'``.
            Note that unlike the usual python slices where the stop index is not included, both the
                start and the stop are included

            - A conditional expression for row access.

            - A boolean array of the same length as the column axis for column access.

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES
        --------
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame('sales')
            >>> df
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # Retrieve row using a single label.
            >>> df.loc['Blue Inc']
                    Feb Jan Mar  Apr    datetime
            accounts
            Blue Inc  90.0  50  95  101  04/01/2017

            # List of labels. Note using ``[[]]``
            >>> df.loc[['Blue Inc', 'Jones LLC']]
                        Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  04/01/2017
            Jones LLC  200.0  150  140  180  04/01/2017

            # Single label for row and column (index)
            >>> df.loc['Yellow Inc', 'accounts']
            Empty DataFrame
            Columns: []
            Index: [Yellow Inc]

            # Single label for row and column
            >>> df.loc['Yellow Inc', 'Feb']
                Feb
            0  90.0

            # Single label for row and column access using a tuple
            >>> df.loc[('Yellow Inc', 'Feb')]
                Feb
            0  90.0

            # Slice with labels for row and single label for column. As mentioned
            # above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'accounts']
            Empty DataFrame
            Columns: []
            Index: [Orange Inc, Jones LLC, Red Inc]

            # Slice with labels for row and single label for column. As mentioned
            # above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'Jan']
                Jan
            0  None
            1   150
            2   150

            # Slice with labels for row and labels for column. As mentioned
            # above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'accounts':'Apr']
                        Mar   Jan    Feb   Apr
            accounts
            Orange Inc  None  None  210.0   250
            Red Inc      140   150  200.0  None
            Jones LLC    140   150  200.0   180

            # Empty slice for row and labels for column.
            >>> df.loc[:, :]
                        Feb   Jan   Mar    datetime   Apr
            accounts
            Jones LLC   200.0   150   140  04/01/2017   180
            Blue Inc     90.0    50    95  04/01/2017   101
            Yellow Inc   90.0  None  None  04/01/2017  None
            Orange Inc  210.0  None  None  04/01/2017   250
            Alpha Co    210.0   200   215  04/01/2017   250
            Red Inc     200.0   150   140  04/01/2017  None

            # Conditional expression
            >>> df.loc[df['Feb'] > 90]
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017

            # Conditional expression with column labels specified
            >>> df.loc[df['Feb'] > 90, ['accounts', 'Jan']]
                        Jan
            accounts
            Jones LLC    150
            Red Inc      150
            Alpha Co     200
            Orange Inc  None

            # Conditional expression with multiple column labels specified
            >>> df.loc[df['accounts'] == 'Jones LLC', ['accounts', 'Jan', 'Feb']]
                    Jan    Feb
            accounts
            Jones LLC  150  200.0

            # Conditional expression and slice with column labels specified
            >>> df.loc[df['accounts'] == 'Jones LLC', 'accounts':'Mar']
                    Mar  Jan    Feb
            accounts
            Jones LLC  140  150  200.0

            # Conditional expression and boolean array for column access
            >>> df.loc[df['Feb'] > 90, [True, True, False, False, True, True]]
                      Feb   Apr    datetime
            accounts
            Alpha Co    210.0   250  04/01/2017
            Jones LLC   200.0   180  04/01/2017
            Red Inc     200.0  None  04/01/2017
            Orange Inc  210.0   250  04/01/2017
            >>>
        """
        return self._loc

    @property
    def iloc(self):
        """
        Access a group of rows and columns by integer values or a boolean array.
        VALID INPUTS:
            - A single integer values, e.g. 5.

            - A list or array of integer values, e.g. ``[1, 2, 3]``.

            - A slice object with integer values, e.g. ``1:6``.
              Note: The stop value is excluded.

            - A boolean array of the same length as the column axis for column access,

            Note: For integer indexing on row access, the integer index values are
            applied to a sorted teradataml DataFrame on the index column or the first column if
            there is no index column.

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES
        --------
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame('sales')
            >>> df
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # Retrieve row using a single integer.
            >>> df.iloc[1]
                    Feb Jan Mar  Apr    datetime
            accounts
            Blue Inc  90.0  50  95  101  04/01/2017

            # List of integers. Note using ``[[]]``
            >>> df.iloc[[1, 2]]
                        Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  04/01/2017
            Jones LLC  200.0  150  140  180  04/01/2017

            # Single integer for row and column
            >>> df.iloc[5, 0]
            Empty DataFrame
            Columns: []
            Index: [Yellow Inc]

            # Single integer for row and column
            >>> df.iloc[5, 1]
                Feb
            0  90.0

            # Single integer for row and column access using a tuple
            >>> df.iloc[(5, 1)]
                Feb
            0  90.0

            # Slice for row and single integer for column access. As mentioned
            # above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 0]
            Empty DataFrame
            Columns: []
            Index: [Orange Inc, Jones LLC, Red Inc]

            # Slice for row and a single integer for column access. As mentioned
            # above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 2]
                Jan
            0  None
            1   150
            2   150

            # Slice for row and column access. As mentioned
            # above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 0:5]
                        Mar   Jan    Feb   Apr
            accounts
            Orange Inc  None  None  210.0   250
            Red Inc      140   150  200.0  None
            Jones LLC    140   150  200.0   180

            # Empty slice for row and column access.
            >>> df.iloc[:, :]
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # List of integers and boolean array for column access
            >>> df.iloc[[0, 2, 3, 4], [True, True, False, False, True, True]]
                          Feb   Apr    datetime
            accounts
            Orange Inc  210.0   250  04/01/2017
            Red Inc     200.0  None  04/01/2017
            Jones LLC   200.0   180  04/01/2017
            Alpha Co    210.0   250  04/01/2017
        """
        return self._iloc

    @columns.setter
    def columns(self, columns):
        """
        Assigns self._columns for the passed columns

        PARAMETERS:
            columns

        EXAMPLES:
            df.columns

        """
        self._columns = columns

    @_index_label.setter
    def _index_label(self, index_label):
        """
        Assigns self.__index_label for the passed column or list of columns.

        PARAMETERS:
            index_label:
                The columns or list of columns to set as the DataFrame's index_label.
                Types: str or List of str

        EXAMPLES:
            df._index_labels = index_label
        """
        self.__index_label = index_label
        self._index_query_required = False

    @property
    def dtypes(self):
        """
        Returns a MetaData containing the column names and types.

        PARAMETERS:

        RETURNS:
            MetaData containing the column names and Python types

        RAISES:

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> print(df.dtypes)
            accounts              str
            Feb                 float
            Jan                   int
            Mar                   int
            Apr                   int
            datetime    datetime.date
            >>>

        """
        return MetaData(self._column_names_and_types)

    @property
    def tdtypes(self):
        """
        DESCRIPTION:
            Get the teradataml DataFrame metadata containing column names and
            corresponding teradatasqlalchemy types.

        RETURNS:
            MetaData containing the column names and Teradata types

        RAISES:
            None.

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> print(df.tdtypes)
            accounts    VARCHAR(length=20, charset='LATIN')
            Feb                                     FLOAT()
            Jan                                    BIGINT()
            Mar                                    BIGINT()
            Apr                                    BIGINT()
            datetime                                 DATE()
            >>>
        """
        # String representation of teradatasqlalchemy.types.VARCHAR is only VARCHAR
        # but repr representation is VARCHAR(length=5, charset='LATIN')
        td_metadata = [(column.name, repr(column.type)) for column in self._metaexpr.c]
        return MetaData(td_metadata)

    def info(self, verbose=True, buf=None, max_cols=None, null_counts=False):
        """
        DESCRIPTION:
            Print a summary of the DataFrame.

        PARAMETERS:
            verbose:
                Optional Argument.
                Print full summary if True. Print short summary if False.
                Default Value: True
                Types: bool

            buf:
                Optional Argument.
                The writable buffer to send the output to. By default, the output is
                sent to sys.stdout.

            max_cols:
                Optional Argument.
                The maximum number of columns allowed for printing the full summary.
                Types: int

            null_counts:
                Optional Argument.
                Whether to show the non-null counts.
                Display the counts if True, otherwise do not display the counts.
                Default Value: False
                Types: bool

        RETURNS:

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df.info()
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            accounts              str
            Feb                 float
            Jan                   int
            Mar                   int
            Apr                   int
            datetime    datetime.date
            dtypes: datetime.date(1), float(1), str(1), int(3)
            >>>
            >>> df.info(null_counts=True)
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            accounts    6 non-null str
            Feb         6 non-null float
            Jan         4 non-null int
            Mar         4 non-null int
            Apr         4 non-null int
            datetime    6 non-null datetime.date
            dtypes: datetime.date(1), float(1), str(1), int(3)
            >>>
            >>> df.info(verbose=False)
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            dtypes: datetime.date(1), float(1), str(1), int(3)
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["verbose", verbose, True, (bool)])
        awu_matrix.append(["max_cols", max_cols, True, (int)])
        awu_matrix.append(["null_counts", null_counts, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        try:
            output_buf = sys.stdout
            if buf is not None:
                output_buf = buf

            num_columns = len(self._column_names_and_types)
            suffix = ""
            if num_columns > 1:
                suffix = "s"

            col_names = [i[0] for i in self._column_names_and_types]
            col_types = [i[1] for i in self._column_names_and_types]

            # Print the class name for self.
            print(str(type(self)), file=output_buf)
            # Print the total number of columns
            print("Data columns (total {0} column{1}):".format(num_columns, suffix), file=output_buf)

            # If max_cols and the number of columns exceeds max_cols, do not print the column names and types
            if max_cols is not None and len(col_names) > max_cols:
                verbose = False

            # If verbose, print the column names and types.
            if verbose:
                # If null_counts, print the number of non-null values for each column if this is not an empty dataframe.
                if null_counts and self._table_name is not None:
                    null_count_str = UtilFuncs._get_non_null_counts(col_names, self._table_name)
                    zipped = zip(col_names, col_types, null_count_str)
                    column_names_and_types = list(zipped)
                    null_count = True
                # Else just print the column names and types
                else:
                    column_names_and_types = self._column_names_and_types
                    null_count = False
                print("{}".format(df_utils._get_pprint_dtypes(column_names_and_types, null_count)), file=output_buf)

            # Print the dtypes and count of each dtypes
            unique_types = list(set(col_types))
            for i in range(0, len(unique_types)):
                unique_types[i] = "{0}({1})".format(unique_types[i], col_types.count(unique_types[i]))
            print("dtypes: {}".format(", ".join(unique_types)), file=output_buf)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def head(self, n=display.max_rows):
        """
        DESCRIPTION:
            Print the first n rows of the sorted teradataml DataFrame.
            Note: The DataFrame is sorted on the index column or the first column if
            there is no index column. The column type must support sorting.
            Unsupported types: ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        PARAMETERS:
            n:
                Optional Argument.
                Specifies the number of rows to select.
                Default Value: 10.
                Types: int

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame.from_table('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  Advanced    Advanced        1
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            26     yes  3.57  Advanced    Advanced        1
            5       no  3.44    Novice      Novice        0
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0
            
            >>> df.head()
               masters   gpa     stats programming admitted
            id
            3       no  3.70    Novice    Beginner        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            8       no  3.60  Beginner    Advanced        1
            4      yes  3.50  Beginner      Novice        1
            2      yes  3.76  Beginner    Beginner        0
            1      yes  3.95  Beginner    Beginner        0
            
            >>> df.head(15)
               masters   gpa     stats programming admitted
            id
            3       no  3.70    Novice    Beginner        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            11      no  3.13  Advanced    Advanced        1
            12      no  3.65    Novice      Novice        1
            13      no  4.00  Advanced      Novice        1
            14     yes  3.45  Advanced    Advanced        0
            15     yes  4.00  Advanced    Advanced        1
            8       no  3.60  Beginner    Advanced        1
            4      yes  3.50  Beginner      Novice        1
            2      yes  3.76  Beginner    Beginner        0
            1      yes  3.95  Beginner    Beginner        0
            
            >>> df.head(5)
               masters   gpa     stats programming admitted
            id
            3       no  3.70    Novice    Beginner        1
            5       no  3.44    Novice      Novice        0
            4      yes  3.50  Beginner      Novice        1
            2      yes  3.76  Beginner    Beginner        0
            1      yes  3.95  Beginner    Beginner        0
        """
        # Validate argument types
        _Validators._validate_function_arguments([["n", n, True, (int)]])

        # Validate n is a positive int.
        _Validators._validate_positive_int(n, "n")

        try:
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                          MessageCodes.TDMLDF_INFO_ERROR)

            sort_col = self._get_sort_col()
            return df_utils._get_sorted_nrow(self, n, sort_col[0], asc=True)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def tail(self, n=display.max_rows):
        """
        DESCRIPTION:
            Print the last n rows of the sorted teradataml DataFrame.
            Note: The Dataframe is sorted on the index column or the first column if
            there is no index column. The column type must support sorting.
            Unsupported types: ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        PARAMETERS:
            n:
                Optional Argument.
                Specifies the number of rows to select.
                Default Value: 10.
                Types: int

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame.from_table('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  Advanced    Advanced        1
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            26     yes  3.57  Advanced    Advanced        1
            5       no  3.44    Novice      Novice        0
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            >>> df.tail()
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  Advanced    Beginner        1
            36      no  3.00  Advanced      Novice        0
            35      no  3.68    Novice    Beginner        1
            34     yes  3.85  Advanced    Beginner        0
            32     yes  3.46  Advanced    Beginner        0
            31     yes  3.50  Advanced    Beginner        1
            33      no  3.55    Novice      Novice        1
            37      no  3.52    Novice      Novice        1
            39     yes  3.75  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            >>> df.tail(3)
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  Advanced    Beginner        1
            39     yes  3.75  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            >>> df.tail(15)
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  Advanced    Beginner        1
            36      no  3.00  Advanced      Novice        0
            35      no  3.68    Novice    Beginner        1
            34     yes  3.85  Advanced    Beginner        0
            32     yes  3.46  Advanced    Beginner        0
            31     yes  3.50  Advanced    Beginner        1
            30     yes  3.79  Advanced      Novice        0
            29     yes  4.00    Novice    Beginner        0
            28      no  3.93  Advanced    Advanced        1
            27     yes  3.96  Advanced    Advanced        0
            26     yes  3.57  Advanced    Advanced        1
            33      no  3.55    Novice      Novice        1
            37      no  3.52    Novice      Novice        1
            39     yes  3.75  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0
        """
        # Validate argument types
        _Validators._validate_function_arguments([["n", n, True, (int)]])

        # Validate n is a positive int.
        _Validators._validate_positive_int(n, "n")

        try:
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

            sort_col = self._get_sort_col()
            return df_utils._get_sorted_nrow(self, n, sort_col[0], asc=False)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def _get_axis(self, axis):
        """
        Private method to retrieve axis value, 0 for index or 1 for columns

        PARAMETERS:
            axis - 0 or 'index' for index labels
                   1 or 'columns' for column labels

        RETURNS:
            0 or 1

        RAISE:
            TeradataMlException

        EXAMPLES:
            a = self._get_axis(0)
            a = self._get_axis(1)
            a = self._get_axis('index')
            a = self._get_axis('columns')
        """
        if isinstance(axis, str):
            if axis == "index":
                return 0
            elif axis == "columns":
                return 1
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)
        elif isinstance(axis, numbers.Integral):
            if axis in [0, 1]:
                return axis
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)

    def _get_sort_col(self):
        """
        Private method to retrieve sort column.
        If _index_labels is not None, return first column and type in _index_labels.
        Otherwise return first column and type in _metadata.

        PARAMETERS:

        RETURNS:
            A tuple containing the column name and type in _index_labels or first column in _metadata.

        RAISE:

        EXAMPLES:
            sort_col = self._get_sort_col()
        """
        unsupported_types = ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        if self._index_label is not None:
            if isinstance(self._index_label, list):
                col_name = self._index_label[0]
            else:
                col_name = self._index_label
        else: #Use the first column from metadata
            col_name = self.columns[0]

        col_type = PythonTypes.PY_NULL_TYPE.value
        for name, py_type in self._column_names_and_types:
            if col_name == name:
                col_type = py_type

        if col_type == PythonTypes.PY_NULL_TYPE.value:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

        sort_col_sqlalchemy_type = (self._metaexpr.t.c[col_name].type)
        # convert types to string from sqlalchemy type for the columns entered for sort
        sort_col_type = repr(sort_col_sqlalchemy_type).split("(")[0]
        if sort_col_type in unsupported_types:
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, sort_col_type, "ANY, except following {}".format(unsupported_types)), MessageCodes.UNSUPPORTED_DATATYPE)

        return (col_name, col_type)

    def drop(self, labels=None, axis=0, columns=None):
        """
        DESCRIPTION:
            Drop specified labels from rows or columns.

            Remove rows or columns by specifying label names and corresponding
            axis, or by specifying the index or column names directly.

        PARAMETERS:
            labels:
                Optional Argument. Required when columns is not provided.
                Single label or list-like. Can be Index or column labels to drop depending on axis.
                Types: str OR list of Strings (str)

            axis:
                Optional Argument.
                0 or 'index' for index labels
                1 or 'columns' for column labels
                Default Values: 0
                Permitted Values: 0, 1, 'index', 'columns'
                Types: int OR str

            columns:
                Optional Argument. Required when labels is not provided.
                Single label or list-like. This is an alternative to specifying axis=1 with labels.
                Cannot specify both labels and columns.
                Types: str OR list of Strings (str)

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            5       no  3.44    Novice      Novice        0
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            19     yes  1.98  Advanced    Advanced        0
            36      no  3.00  Advanced      Novice        0
            15     yes  4.00  Advanced    Advanced        1
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            # Drop columns
            >>> df.drop(['stats', 'admitted'], axis=1)
               programming masters   gpa
            id
            5       Novice      no  3.44
            34    Beginner     yes  3.85
            13      Novice      no  4.00
            40    Beginner     yes  3.95
            22    Beginner     yes  3.46
            19    Advanced     yes  1.98
            36      Novice      no  3.00
            15    Advanced     yes  4.00
            7       Novice     yes  2.33
            17    Advanced      no  3.83

            >>> df.drop(columns=['stats', 'admitted'])
               programming masters   gpa
            id
            5       Novice      no  3.44
            34    Beginner     yes  3.85
            13      Novice      no  4.00
            19    Advanced     yes  1.98
            15    Advanced     yes  4.00
            40    Beginner     yes  3.95
            7       Novice     yes  2.33
            22    Beginner     yes  3.46
            36      Novice      no  3.00
            17    Advanced      no  3.83

            # Drop a row by index
            >>> df1 = df[df.gpa == 4.00]
            >>> df1
               masters  gpa     stats programming admitted
            id
            13      no  4.0  Advanced      Novice        1
            29     yes  4.0    Novice    Beginner        0
            15     yes  4.0  Advanced    Advanced        1
            >>> df1.drop([13,15], axis=0)
               masters  gpa   stats programming admitted
            id
            29     yes  4.0  Novice    Beginner        0
            >>>
        """

        # Argument validations
        awu_matrix = []
        awu_matrix.append(["axis", axis, True, (int, str), False, [0, 1, 'index', 'columns']])
        awu_matrix.append(["columns", columns, True, (str, list), True])

        # Make sure either columns or labels is provided.
        if (labels is None and columns is None) or (labels is not None and columns is not None):
            raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT, "labels",
                                                           "columns"),
                                      MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

        # Validate argument types
        _Validators._validate_input_columns_not_empty(labels, "labels")
        _Validators._validate_missing_required_arguments(awu_matrix)
        _Validators._validate_function_arguments(awu_matrix)

        try:
            column_labels = None
            index_labels = None

            if labels is not None:
                if self._get_axis(axis) == 0:
                    index_labels = labels
                else:
                    column_labels = labels
            else: # Columns is not None
                column_labels = columns

            if index_labels is not None:
                sort_col = self._get_sort_col()
                df_utils._validate_sort_col_type(sort_col[1], index_labels)

                if isinstance(index_labels, list):
                    if len(index_labels) == 0:
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

                    if sort_col[1] == PythonTypes.PY_STRING_TYPE.value:
                        index_labels = ["'{}'".format(x) for x in index_labels]
                    index_expr = ",".join(map(str, (index_labels)))
                else:
                    if sort_col[1] == PythonTypes.PY_STRING_TYPE.value:
                        index_expr = "'{}'".format(index_labels)
                    else:
                        index_expr = index_labels

                filter_expr = "{0} not in ({1})".format(sort_col[0], index_expr)
                new_nodeid= self._aed_utils._aed_filter(self._nodeid, filter_expr)
                # Get the updated metaexpr
                new_metaexpr = UtilFuncs._get_metaexpr_using_parent_metaexpr(new_nodeid, self._metaexpr)
                return DataFrame._from_node(new_nodeid, new_metaexpr, self._index_label)
            else: # Column labels
                select_cols = []
                cols = [x.name for x in self._metaexpr.columns]
                if isinstance(column_labels, list):
                    if len(column_labels) == 0:
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

                    if not all(isinstance(n, str) for n in column_labels):
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
                    drop_cols = [x for x in column_labels]
                elif isinstance(column_labels, (tuple, dict)):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)
                else:
                    if not isinstance(column_labels, str):
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
                    drop_cols = [column_labels]

                for drop_name in drop_cols:
                    if drop_name not in cols:
                        msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL).format(drop_name, cols)
                        raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_COL)

                for colname in cols:
                    if colname not in drop_cols:
                        select_cols.append(colname)
                if len(select_cols) > 0:
                    return self.select(select_cols)
                else: # no columns selected
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ALL_COLS), MessageCodes.TDMLDF_DROP_ALL_COLS)

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def dropna(self, how='any', thresh=None, subset=None):
        """
        DESCRIPTION:
            Removes rows with null values.

        PARAMETERS:
            how:
                Optional Argument.
                Specifies how rows are removed.
                'any' removes rows with at least one null value.
                'all' removes rows with all null values.
                Default Value: 'any'
                Permitted Values: 'any' or 'all'
                Types: str

            thresh:
                Optional Argument.
                Specifies the minimum number of non null values in a row to include.
                Types: int

            subset:
                Optional Argument.
                Specifies list of column names to include, in array-like format.
                Types: str OR list of Strings (str)

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame('sales')
            >>> df
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # Drop the rows where at least one element is null.
            >>> df.dropna()
                         Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  04/01/2017
            Jones LLC  200.0  150  140  180  04/01/2017
            Alpha Co   210.0  200  215  250  04/01/2017

            # Drop the rows where all elements are nulls for columns 'Jan' and 'Mar'.
            >>> df.dropna(how='all', subset=['Jan','Mar'])
                         Feb  Jan  Mar   Apr    datetime
            accounts
            Alpha Co   210.0  200  215   250  04/01/2017
            Jones LLC  200.0  150  140   180  04/01/2017
            Red Inc    200.0  150  140  None  04/01/2017
            Blue Inc    90.0   50   95   101  04/01/2017

            # Keep only the rows with at least 4 non null values.
            >>> df.dropna(thresh=4)
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  04/01/2017
            Blue Inc     90.0    50    95   101  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # Keep only the rows with at least 5 non null values.
            >>> df.dropna(thresh=5)
                         Feb  Jan  Mar   Apr    datetime
            accounts
            Alpha Co   210.0  200  215   250  04/01/2017
            Jones LLC  200.0  150  140   180  04/01/2017
            Blue Inc    90.0   50   95   101  04/01/2017
            Red Inc    200.0  150  140  None  04/01/2017
        """

        # Argument validations
        awu_matrix = []
        awu_matrix.append(["how", how, True, (str), True, ['any', 'all']])
        awu_matrix.append(["thresh", thresh, True, (int)])
        awu_matrix.append(["subset", subset, True, (str, list), True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Validate n is a positive int.
        _Validators._validate_positive_int(thresh, "thresh")

        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(subset, self._metaexpr)

        try:
            col_names = [item.lower() for item in self.keys()]
            if subset is not None:
                col_filters = subset
            else:
                col_filters = col_names

            col_filters_decode = ["decode(\"{}\", null, 0, 1)".format(col_name) for col_name in col_filters]
            fmt_filter = " + ".join(col_filters_decode)

            if thresh is not None:
                filter_expr = "{0} >= {1}".format(fmt_filter, thresh)
            elif how == 'any':
                filter_expr = "{0} = {1}".format(fmt_filter, len(col_filters))
            else: # how == 'all'
                filter_expr = "{0} > 0".format(fmt_filter)

            new_nodeid= self._aed_utils._aed_filter(self._nodeid, filter_expr)

            # Get the updated metaexpr
            new_metaexpr = UtilFuncs._get_metaexpr_using_parent_metaexpr(new_nodeid, self._metaexpr)
            return DataFrame._from_node(new_nodeid, new_metaexpr, self._index_label)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def sort(self, columns, ascending=True):
        """
        DESCRIPTION:
            Get Sorted data by one or more columns in either ascending or descending order for a Dataframe.
            Unsupported column types for sorting: ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        PARAMETERS:
            columns:
                Required Argument.
                Column names as a string or a list of strings to sort on.
                Types: str OR list of Strings (str)

            ascending:
                Optional Argument.
                Order ASC or DESC to be applied for each column.
                True for ascending order and False for descending order.
                Default value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            22     yes  3.46    Novice    Beginner        0
            37      no  3.52    Novice      Novice        1
            35      no  3.68    Novice    Beginner        1
            12      no  3.65    Novice      Novice        1
            4      yes  3.50  Beginner      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            27     yes  3.96  Advanced    Advanced        0
            39     yes  3.75  Advanced    Beginner        0
            7      yes  2.33    Novice      Novice        1
            40     yes  3.95    Novice    Beginner        0
            >>> df.sort("id")
               masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1
            4      yes  3.50  Beginner      Novice        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            8       no  3.60  Beginner    Advanced        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            >>> df.sort(["id"])
               masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1
            4      yes  3.50  Beginner      Novice        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            8       no  3.60  Beginner    Advanced        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            >>> df.sort(["masters","gpa"])
               masters   gpa     stats programming admitted
            id
            24      no  1.87  Advanced      Novice        1
            36      no  3.00  Advanced      Novice        0
            11      no  3.13  Advanced    Advanced        1
            5       no  3.44    Novice      Novice        0
            37      no  3.52    Novice      Novice        1
            33      no  3.55    Novice      Novice        1
            8       no  3.60  Beginner    Advanced        1
            12      no  3.65    Novice      Novice        1
            35      no  3.68    Novice    Beginner        1
            16      no  3.70  Advanced    Advanced        1
            >>> # In next example, sort dataframe with masters column in Ascending ('True')
            >>> # order and gpa column with Descending (False)
            >>> df.sort(["masters","gpa"], ascending=[True,False])
               masters   gpa     stats programming admitted
            id
            13      no  4.00  Advanced      Novice        1
            25      no  3.96  Advanced    Advanced        1
            28      no  3.93  Advanced    Advanced        1
            21      no  3.87    Novice    Beginner        1
            17      no  3.83  Advanced    Advanced        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            3       no  3.70    Novice    Beginner        1
            16      no  3.70  Advanced    Advanced        1
            35      no  3.68    Novice    Beginner        1
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["columns", columns, True, (str, list), True])
        awu_matrix.append(["ascending", ascending, True, (bool, list)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(columns, self._metaexpr)

        try:
            orderexpr=""
            type_expr=[]
            invalid_types = []
            unsupported_types = ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

            if (isinstance(columns, str)):
                columns=[columns]
            if isinstance(ascending, bool):
                ascending=[ascending] * len(columns)

            # Validating lengths of passed arguments which are passed i.e. length of columns
            # must be same as ascending
            if ascending and len(columns) != len(ascending):
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_LENGTH_ARGS,
                                                               '"columns" and "ascending"'),
                                          MessageCodes.INVALID_LENGTH_ARGS)

            # Let's get the column types for the columns passed to 'columns' argument.
            for col in columns:
                type_expr.append(self._metaexpr.t.c[col].type)

            # Convert types to string from sqlalchemy type for the columns entered for sort
            columns_types = [repr(type_expr[i]).split("(")[0] for i in range(len(type_expr))]

            # Checking each element in passed columns_types to be valid a data type for sort
            # and create a list of invalid_types
            for col_type in columns_types:
                if col_type in unsupported_types:
                    invalid_types.append(col_type)
            if len(invalid_types) > 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_types,
                                                               "ANY, except following {}".format(unsupported_types)),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            columns_expr = UtilFuncs._teradata_quote_arg(columns, "\"", False)
            if (len(ascending) != 0):
                val=['ASC' if i==True else 'DESC' for i in ascending]
                for c,v in zip(columns_expr,val):
                    orderexpr='{}{} {}, '.format(orderexpr,c,v)
                orderexpr=orderexpr[:-2]
            else:
                orderexpr=", ".join(columns_expr)

            # We are just updating orderby clause in exisitng teradataml dataframe
            # and returning new teradataml dataframe.
            sort_df = DataFrame._from_node(self._nodeid, self._metaexpr, self._index_label)
            sort_df._orderby = orderexpr

            # Assigning self attributes to newly created dataframe.
            sort_df._table_name = self._table_name
            sort_df._index = self._index
            sort_df._index_label = self._index_label
            return sort_df
        except TeradataMlException:
            raise

    def filter(self, items = None, like = None, regex = None, axis = 1, **kw):
        """
        DESCRIPTION:
            Filter rows or columns of dataframe according to labels in the specified index.
            The filter is applied to the columns of the index when axis is set to 'rows'.

            Must use one of the parameters 'items', 'like', and 'regex' only.

        PARAMETERS:
            axis:
                Optional Argument.
                Specifies the axis to filter on.
                1 denotes column axis (default). Alternatively, 'columns' can be specified.
                0 denotes row axis. Alternatively, 'rows' can be specified.
                Default Values: 1
                Permitted Values: 0, 1, 'rows', 'columns'
                Types: int OR str

            items:
                Optional Argument.
                List of values that the info axis should be restricted to
                When axis is 1, items is a list of column names
                When axis is 0, items is a list of literal values
                Types: list of Strings (str) or literals

            like:
                Optional Argument.
                When axis is 1, substring pattern for matching column names
                When axis is 0, substring pattern for checking index values with REGEXP_SUBSTR
                Types: str

            regex:
                Optional Argument.
                Specified a regular expression pattern.
                When axis is 1, regex pattern for re.search(regex, column_name)
                When axis is 0, regex pattern for checking index values with REGEXP_SUBSTR
                Types: str

            **kw: optional keyword arguments

                varchar_size:
                    An integer to specify the size of varchar-casted index.
                    Used when axis = 0/'rows' and index must be char-like in "like" and "regex" filtering
                    Default Value: configure.default_varchar_size
                    Types: int

                match_arg: string
                    argument to pass if axis is 0/'rows' and regex is used

                    Valid values for match_arg are:
                    - 'i' = case-insensitive matching.
                    - 'c' = case sensitive matching.
                    - 'n' = the period character (match any character) can match the newline character.
                    - 'm' = index value is treated as multiple lines instead of as a single line. With this option, the
                            '^' and '$' characters apply to each line in source_string instead of the entire index value.
                    - 'l' = if index value exceeds the current maximum allowed size (currently 16 MB), a NULL is returned
                            instead of an error.
                            This is useful for long-running queries where you do not want long strings
                            causing an error that would make the query fail.
                    - 'x' = ignore whitespace.

            The 'match_arg' argument may contain more than one character.
            If a character in 'match_arg' is not valid, then that character is ignored.

            See Teradata® Database SQL Functions, Operators, Expressions, and Predicates, Release 16.20
            for more information on specifying arguments for REGEXP_SUBSTR.

            NOTES:
                - Using 'regex' or 'like' with axis equal to 0 will attempt to cast the values in the index to a VARCHAR.
                  Note that conversion between BYTE data and other types is not supported.
                  Also, LOBs are not allowed to be compared.

                - When using 'like' or 'regex', datatypes are casted into VARCHAR.
                  This may alter the format of the value in the column(s)
                  and thus whether there is a match or not. The size of the VARCHAR may also
                  play a role since the casted value is truncated if the size is not big enough.
                  See varchar_size under **kw: optional keyword arguments.

        RETURNS:
            teradataml DataFrame

        RAISES:
            ValueError if more than one parameter: 'items', 'like', or 'regex' is used.
            TeradataMlException if invalid argument values are given.

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            22     yes  3.46    Novice    Beginner        0
            37      no  3.52    Novice      Novice        1
            35      no  3.68    Novice    Beginner        1
            12      no  3.65    Novice      Novice        1
            4      yes  3.50  Beginner      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            27     yes  3.96  Advanced    Advanced        0
            39     yes  3.75  Advanced    Beginner        0
            7      yes  2.33    Novice      Novice        1
            40     yes  3.95    Novice    Beginner        0
            >>>
            >>> # retrieve columns masters, gpa, and stats in df
            ... df.filter(items = ['masters', 'gpa', 'stats'])
              masters   gpa     stats
            0     yes  4.00  Advanced
            1     yes  3.45  Advanced
            2     yes  3.50  Advanced
            3     yes  4.00    Novice
            4     yes  3.59  Advanced
            5      no  3.87    Novice
            6     yes  3.50  Beginner
            7     yes  3.79  Advanced
            8      no  3.00  Advanced
            9     yes  1.98  Advanced
            >>>
            >>> # retrieve rows where index matches ‘2’, ‘4’
            ... df.filter(items = ['2', '4'], axis = 0)
               masters   gpa     stats programming admitted
            id
            2      yes  3.76  Beginner    Beginner        0
            4      yes  3.50  Beginner      Novice        1
            >>>
            >>> df = DataFrame('admissions_train', index_label="programming")
            >>> df
                         id masters   gpa     stats admitted
            programming
            Beginner     22     yes  3.46    Novice        0
            Novice       37      no  3.52    Novice        1
            Beginner     35      no  3.68    Novice        1
            Novice       12      no  3.65    Novice        1
            Novice        4     yes  3.50  Beginner        1
            Beginner     38     yes  2.65  Advanced        1
            Advanced     27     yes  3.96  Advanced        0
            Beginner     39     yes  3.75  Advanced        0
            Novice        7     yes  2.33    Novice        1
            Beginner     40     yes  3.95    Novice        0
            >>>
            >>> # retrieve columns with a matching substring
            ... df.filter(like = 'masters')
              masters
            0     yes
            1     yes
            2     yes
            3     yes
            4     yes
            5      no
            6     yes
            7     yes
            8      no
            9     yes
            >>>
            >>> # retrieve rows where index values have ‘vice’ as a subtring
            ... df.filter(like = 'vice', axis = 'rows')
                         id masters   gpa     stats admitted
            programming
            Novice       12      no  3.65    Novice        1
            Novice        5      no  3.44    Novice        0
            Novice       24      no  1.87  Advanced        1
            Novice       36      no  3.00  Advanced        0
            Novice       23     yes  3.59  Advanced        1
            Novice       13      no  4.00  Advanced        1
            Novice       33      no  3.55    Novice        1
            Novice       30     yes  3.79  Advanced        0
            Novice        4     yes  3.50  Beginner        1
            Novice       37      no  3.52    Novice        1
            >>>
            >>> # give a regular expression to match column names
            ... df.filter(regex = '^a.+')
              admitted
            0        0
            1        1
            2        1
            3        1
            4        1
            5        1
            6        0
            7        0
            8        1
            9        0
            >>>
            >>> # give a regular expression to match values in index
            ... df.filter(regex = '^B.+', axis = 0)
                         id masters   gpa     stats admitted
            programming
            Beginner     39     yes  3.75  Advanced        0
            Beginner     38     yes  2.65  Advanced        1
            Beginner      3      no  3.70    Novice        1
            Beginner     31     yes  3.50  Advanced        1
            Beginner     21      no  3.87    Novice        1
            Beginner     34     yes  3.85  Advanced        0
            Beginner     32     yes  3.46  Advanced        0
            Beginner     29     yes  4.00    Novice        0
            Beginner     35      no  3.68    Novice        1
            Beginner     22     yes  3.46    Novice        0
            >>>
            >>> # case-insensitive, ignore white space when matching index values
            ... df.filter(regex = '^A.+', axis = 0, match_args = 'ix')
                         id masters   gpa     stats admitted
            programming
            Advanced     20     yes  3.90  Advanced        1
            Advanced      8      no  3.60  Beginner        1
            Advanced     25      no  3.96  Advanced        1
            Advanced     19     yes  1.98  Advanced        0
            Advanced     14     yes  3.45  Advanced        0
            Advanced      6     yes  3.50  Beginner        1
            Advanced     17      no  3.83  Advanced        1
            Advanced     11      no  3.13  Advanced        1
            Advanced     15     yes  4.00  Advanced        1
            Advanced     18     yes  3.81  Advanced        1
            >>>
            >>> # case-insensitive/ ignore white space/ match up to 32 characters
            ... df.filter(regex = '^A.+', axis = 0, match_args = 'ix', varchar_size = 32)
                         id masters   gpa     stats admitted
            programming
            Advanced     20     yes  3.90  Advanced        1
            Advanced      8      no  3.60  Beginner        1
            Advanced     25      no  3.96  Advanced        1
            Advanced     19     yes  1.98  Advanced        0
            Advanced     14     yes  3.45  Advanced        0
            Advanced      6     yes  3.50  Beginner        1
            Advanced     17      no  3.83  Advanced        1
            Advanced     11      no  3.13  Advanced        1
            Advanced     15     yes  4.00  Advanced        1
            Advanced     18     yes  3.81  Advanced        1
            >>>
        """

        # Argument validations
        awu_matrix = []
        awu_matrix.append(["axis", axis, True, (int, str), False, [0, 1, 'columns', 'rows']])
        awu_matrix.append(["like", like, True, (str)])
        awu_matrix.append(["regex", regex, True, (str)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if self._index_label is None and axis in (0, 'rows'):
            raise AttributeError('DataFrame must have index_label set to a valid column')

        axis = 1 if axis == 'columns' or axis == 1 else 0
        errcode = MessageCodes.UNSUPPORTED_DATATYPE

        # validate items, like, regex type and value
        op = ''

        if items is not None:
            op += 'items'
            valid_value = (type(items) is list) and len(set(map(lambda x: type(x), items))) == 1

        if like is not None:
            op += 'like'
            valid_value = type(like) is str

        if regex is not None:
            op += 'regex'
            valid_value = type(regex) is str

        if op not in('items', 'like', 'regex'):
            raise ValueError('Must use exactly one of the parameters items, like, and regex.')

        if not valid_value:
            msg = 'The "items" parameter must be list of strings or tuples of column labels/index values. ' +\
                'The "regex" parameter and "like" parameter must be strings.'
            raise TeradataMlException(msg, errcode)

        # validate multi index labels for items
        if op == 'items' and axis == 0:

            num_col_indexes = len(self._index_label)
            if num_col_indexes > 1 and not all(map(lambda entry: len(entry) == num_col_indexes, items)):
                raise ValueError('tuple length in items must match length of multi index: %d' % num_col_indexes)

        # validate the optional keyword args
        if kw is not None and 'match_arg' in kw:
            if not isinstance(kw['match_arg'], str):
                msg = Messages.get_message(errcode, type(kw['match_arg']), 'match_arg', 'string')
                raise TeradataMlException(msg, errcode)

        if kw is not None and 'varchar_size' in kw:
            if not isinstance(kw['varchar_size'], int):
                msg = Messages.get_message(errcode, type(kw['varchar_size']), 'varchar_size', 'int')
                raise TeradataMlException(msg, errcode)

        # generate the sql expression
        expression = self._metaexpr._filter(axis, op, self._index_label,
                                            items=items,
                                            like=like,
                                            regex=regex,
                                            **kw)

        if axis == 1 and isinstance(expression, list):
            return self.select(expression)

        elif axis == 0 and isinstance(expression, ColumnExpression):
            return self.__getitem__(expression)

        else:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode)

    def describe(self, percentiles=[.25, .5, .75], include=None, verbose=False, distinct=False):
        """
        DESCRIPTION:
            Generates statistics for numeric columns. This function can be used in two modes:
                1. Regular Aggregate Mode.
                    It computes the count, mean, std, min, percentiles, and max for numeric columns.
                    Default statistics include:
                        "count", "mean", "std", "min", "percentile", "max"
                2. Time Series Aggregate Mode.
                    It computes max, mean, min, std, median, mode, and percentiles for numeric columns.
                    Default statistics include:
                        'max', 'mean', 'min', 'std'

            Note:
                Regular Aggregate Mode: If describe() is used on the output of any DataFrame API or groupby(),
                                        then describe() is used as regular aggregation.
                Time Series Aggregate Mode: If describe() is used on the output of groupby_time(), then describe()
                                            is a time series aggregate, where time series aggregates are used
                                            to calculate the statistics.

        PARAMETERS:
            percentiles:
                Optional Argument.
                A list of values between 0 and 1. Applicable for both modes.
                By default, percentiles are calculated for statistics for 'Regular Aggregate Mode', whereas
                for 'Time Series Aggregate Mode', percentiles are calculated when verbose is set to True.
                Default Values: [.25, .5, .75], which returns the 25th, 50th, and 75th percentiles.
                Types: float or List of floats

            include:
                Optional Argument.
                Values can be either None or "all".
                If the value is "all", then both numeric and non-numeric columns are included.
                Computes count, mean, std, min, percentiles, and max for numeric columns.
                Computes count and unique for non-numeric columns.
                If the value is None, only numeric columns are used for collecting statistics.
                Note:
                    Value 'all' is not applicable for 'Time Series Aggregate Mode'.
                Default Values: None
                Types: str

            verbose:
                Optional Argument.
                Specifies a boolean value to be used for time series aggregation, stating whether to get
                verbose output or not.
                When this argument is set to 'True', function calculates median, mode, and percentile values
                on top of its default statistics.
                Note:
                    verbose as 'True' is not applicable for 'Regular Aggregate Mode'.
                Default Values: False
                Types: bool

            distinct:
                Optional Argument.
                Specifies a boolean value to decide whether to consider duplicate rows in statistic
                calculation or not. By default, duplicate values are considered for statistic calculation.
                When this is set to True, only distinct rows are considered for statistic calculation.
                Default Values: False
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame('sales')
            >>> print(df)
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017

            # Computes count, mean, std, min, percentiles, and max for numeric columns.
            >>> df.describe()
                      Apr      Feb     Mar     Jan
            func
            count       4        6       4       4
            mean   195.25  166.667   147.5   137.5
            std    70.971   59.554  49.749  62.915
            min       101       90      95      50
            25%    160.25    117.5  128.75     125
            50%       215      200     140     150
            75%       250    207.5  158.75   162.5
            max       250      210     215     200

            # Computes count, mean, std, min, percentiles, and max for numeric columns with 30th and 60th percentiles.
            >>> df.describe(percentiles=[.3, .6])
                      Apr      Feb     Mar     Jan
            func
            count       4        6       4       4
            mean   195.25  166.667   147.5   137.5
            std    70.971   59.554  49.749  62.915
            min       101       90      95      50
            30%     172.1      145   135.5     140
            60%       236      200     140     150
            max       250      210     215     200

            # Computes count, mean, std, min, percentiles, and max for numeric columns group by "datetime" and "Feb".
            >>> df1 = df.groupby(["datetime", "Feb"])
            >>> df1.describe()
                                     Jan   Mar   Apr
            datetime   Feb   func
            04/01/2017 90.0  25%      50    95   101
                             50%      50    95   101
                             75%      50    95   101
                             count     1     1     1
                             max      50    95   101
                             mean     50    95   101
                             min      50    95   101
                             std    None  None  None
                       200.0 25%     150   140   180
                             50%     150   140   180
                             75%     150   140   180
                             count     2     2     1
                             max     150   140   180
                             mean    150   140   180
                             min     150   140   180
                             std       0     0  None
                       210.0 25%     200   215   250
                             50%     200   215   250
                             75%     200   215   250
                             count     1     1     2
                             max     200   215   250
                             mean    200   215   250
                             min     200   215   250
                             std    None  None     0

            # Computes count, mean, std, min, percentiles, and max for numeric columns and
            # computes count and unique for non-numeric columns
            >>> df.describe(include="all")
                   accounts      Feb     Jan     Mar     Apr datetime
            func
            25%        None    117.5     125  128.75  160.25     None
            75%        None    207.5   162.5  158.75     250     None
            count         6        6       4       4       4        6
            mean       None  166.667   137.5   147.5  195.25     None
            max        None      210     200     215     250     None
            min        None       90      50      95     101     None
            50%        None      200     150     140     215     None
            std        None   59.554  62.915  49.749  70.971     None
            unique        6     None    None    None    None        1

            #
            # Examples for describe() function as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> ocean_buoys_grpby = ocean_buoys.groupby_time(timebucket_duration="2cy", value_expression="buoyid", fill="NULLS")
            >>>

            #
            # Example 1: Get the basic statistics for time series aggregation for all the numeric columns.
            #            This returns max, mean, min and std values.
            #
            >>> ocean_buoys_grpby.describe()
                                                                                                       temperature salinity
            TIMECODE_RANGE                                     GROUP BY TIME(CAL_YEARS(2)) buoyid func
            ('2014-01-01 00:00:00.000000-00:00', '2016-01-0... 2                           0      max          100       55
                                                                                                  mean       54.75       55
                                                                                                  min           10       55
                                                                                                  std       51.674        0
                                                                                           1      max           79       55
                                                                                                  mean        74.5       55
                                                                                                  min           70       55
                                                                                                  std        3.937        0
                                                                                           2      max           82       55
                                                                                                  mean          81       55
                                                                                                  min           80       55
                                                                                                  std            1        0
                                                                                           44     max           56       55
                                                                                                  mean      48.077       55
                                                                                                  min           43       55
                                                                                                  std        5.766        0
            >>>

            #
            # Example 2: Get the verbose statistics for time series aggregation for all the numeric columns.
            #            This returns max, mean, min, std, median, mode, 25th, 50th and 75th percentile.
            #
            >>> ocean_buoys_grpby.describe(verbose=True)
                                                                                                         temperature salinity
            TIMECODE_RANGE                                     GROUP BY TIME(CAL_YEARS(2)) buoyid func
            ('2014-01-01 00:00:00.000000-00:00', '2016-01-0... 2                           0      25%             10       55
                                                                                                  50%           54.5       55
                                                                                                  75%          99.25       55
                                                                                                  max            100       55
                                                                                                  mean         54.75       55
                                                                                                  median        54.5       55
                                                                                                  min             10       55
                                                                                                  mode            10       55
                                                                                                  std         51.674        0
                                                                                           1      25%          71.25       55
                                                                                                  50%           74.5       55
                                                                                                  75%          77.75       55
                                                                                                  max             79       55
                                                                                                  mean          74.5       55
                                                                                                  median        74.5       55
                                                                                                  min             70       55
                                                                                                  mode            71       55
                                                                                                  mode            72       55
                                                                                                  mode            77       55
                                                                                                  mode            78       55
                                                                                                  mode            79       55
                                                                                                  mode            70       55
                                                                                                  std          3.937        0
                                                                                           2      25%           80.5       55
                                                                                                  50%             81       55
                                                                                                  75%           81.5       55
                                                                                                  max             82       55
                                                                                                  mean            81       55
                                                                                                  median          81       55
                                                                                                  min             80       55
                                                                                                  mode            80       55
                                                                                                  mode            81       55
                                                                                                  mode            82       55
                                                                                                  std              1        0
                                                                                           44     25%             43       55
                                                                                                  50%             43       55
                                                                                                  75%             53       55
                                                                                                  max             56       55
                                                                                                  mean        48.077       55
                                                                                                  median          43       55
                                                                                                  min             43       55
                                                                                                  mode            43       55
                                                                                                  std          5.766        0
            >>>

            #
            # Example 3: Get the basic statistics for time series aggregation for all the numeric columns,
            #            consider only unique values.
            #            This returns max, mean, min and std values.
            #
            >>> ocean_buoys_grpby.describe(distinct=True)
                                                                                                       temperature salinity
            TIMECODE_RANGE                                     GROUP BY TIME(CAL_YEARS(2)) buoyid func
            ('2014-01-01 00:00:00.000000-00:00', '2016-01-0... 2                           0      max          100       55
                                                                                                  mean      69.667       55
                                                                                                  min           10       55
                                                                                                  std       51.675     None
                                                                                           1      max           79       55
                                                                                                  mean        74.5       55
                                                                                                  min           70       55
                                                                                                  std        3.937     None
                                                                                           2      max           82       55
                                                                                                  mean          81       55
                                                                                                  min           80       55
                                                                                                  std            1     None
                                                                                           44     max           56       55
                                                                                                  mean        52.2       55
                                                                                                  min           43       55
                                                                                                  std        5.263     None
            >>>

            #
            # Example 4: Get the verbose statistics for time series aggregation for all the numeric columns.
            #            This select non-default percentiles 33rd and 66th.
            #            This returns max, mean, min, std, median, mode, 33rd, and 66th percentile.
            #
            >>> ocean_buoys_grpby.describe(verbose=True, percentiles=[0.33, 0.66])
                                                                                                         temperature salinity
            TIMECODE_RANGE                                     GROUP BY TIME(CAL_YEARS(2)) buoyid func
            ('2014-01-01 00:00:00.000000-00:00', '2016-01-0... 2                           0      33%             10       55
                                                                                                  66%          97.22       55
                                                                                                  max            100       55
                                                                                                  mean         54.75       55
                                                                                                  median        54.5       55
                                                                                                  min             10       55
                                                                                                  mode            10       55
                                                                                                  std         51.674        0
                                                                                           1      33%          71.65       55
                                                                                                  66%           77.3       55
                                                                                                  max             79       55
                                                                                                  mean          74.5       55
                                                                                                  median        74.5       55
                                                                                                  min             70       55
                                                                                                  mode            70       55
                                                                                                  mode            71       55
                                                                                                  mode            77       55
                                                                                                  mode            78       55
                                                                                                  mode            79       55
                                                                                                  mode            72       55
                                                                                                  std          3.937        0
                                                                                           2      33%          80.66       55
                                                                                                  66%          81.32       55
                                                                                                  max             82       55
                                                                                                  mean            81       55
                                                                                                  median          81       55
                                                                                                  min             80       55
                                                                                                  mode            80       55
                                                                                                  mode            81       55
                                                                                                  mode            82       55
                                                                                                  std              1        0
                                                                                           44     33%             43       55
                                                                                                  66%             53       55
                                                                                                  max             56       55
                                                                                                  mean        48.077       55
                                                                                                  median          43       55
                                                                                                  min             43       55
                                                                                                  mode            43       55
                                                                                                  std          5.766        0
            >>>
        """

        # Argument validations
        awu_matrix = []
        awu_matrix.append(["percentiles", percentiles, True, (float, list)])
        awu_matrix.append(["include", include, True, (str), True, [None, "all"]])
        awu_matrix.append(["verbose", verbose, True, (bool)])
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Validate argument values.
        if isinstance(percentiles, float):
            percentiles = [percentiles]

        # Percentiles must be a list of values between 0 and 1.
        if not isinstance(percentiles, list) or not all(p > 0 and p < 1 for p in percentiles):
            raise ValueError(Messages.get_message(MessageCodes.INVALID_ARG_VALUE, percentiles, "percentiles",
                                                           "percentiles must be a list of values between 0 and 1"))

        # Argument 'include' with value 'all' is not allowed for DataFrameGroupByTime
        if include is not None and include.lower() == "all" and isinstance(self, DataFrameGroupByTime):
            raise ValueError(Messages.get_message(MessageCodes.ARG_VALUE_CLASS_DEPENDENCY).format(
                'include', 'Aggregation', 'all', 'describe()', 'DataFrame or DataFrameGroupBy'))

        # Argument 'verbose' with value True is not allowed for non DataFrameGroupByTime objects.
        if verbose and not isinstance(self, DataFrameGroupByTime):
            raise ValueError(Messages.get_message(MessageCodes.ARG_VALUE_CLASS_DEPENDENCY).format(
                'verbose', 'Aggregation', 'True', 'describe()', 'DataFrameGroupByTime'))

        function_label = "func"
        try:
            self.__execute_node_and_set_table_name(self._nodeid)

            groupby_column_list = None
            if isinstance(self, DataFrameGroupBy):
                groupby_column_list = self.groupby_column_list

            if isinstance(self, DataFrameGroupByTime):
                groupby_column_list = self.groupby_column_list
                # Construct the aggregate query.
                agg_query = df_utils._construct_describe_query(df=self, metaexpr=self._metaexpr,
                                                               percentiles=percentiles, function_label=function_label,
                                                               groupby_column_list=groupby_column_list, include=include,
                                                               is_time_series_aggregate=True, verbose=verbose,
                                                               distinct=distinct,
                                                               timebucket_duration=self._timebucket_duration,
                                                               value_expression=self._value_expression,
                                                               timecode_column=self._timecode_column,
                                                               sequence_column=self._sequence_column,
                                                               fill=self._fill)
            else:
                # Construct the aggregate query.
                agg_query = df_utils._construct_describe_query(df=self, metaexpr=self._metaexpr,
                                                               percentiles=percentiles, function_label=function_label,
                                                               groupby_column_list=groupby_column_list, include=include,
                                                               is_time_series_aggregate=False, verbose=verbose,
                                                               distinct=distinct)

            if groupby_column_list is not None:
                sort_cols = [i for i in groupby_column_list]
                sort_cols.append(function_label)
                df = DataFrame.from_query(agg_query, index_label=sort_cols)
                df2 = df.sort(sort_cols)
                df2._metaexpr._n_rows = 100
                return df2
            else:
                return DataFrame.from_query(agg_query, index_label=function_label)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def kurtosis(self, distinct=False):
        """
        DESCRIPTION:
            Returns column-wise kurtosis value of the dataframe.
            Kurtosis is the fourth moment of the distribution of the standardized (z) values.
            It is a measure of the outlier (rare, extreme observation) character of the distribution as
            compared with the normal (or Gaussian) distribution.
                * The normal distribution has a kurtosis of 0.
                * Positive kurtosis indicates that the distribution is more outlier-prone than the
                  normal distribution.
                * Negative kurtosis indicates that the distribution is less outlier-prone than the
                  normal distribution.

            Notes:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.
                3. Following conditions will produce null result:
                    a. Fewer than three non-null data points in the data used for the computation.
                    b. Standard deviation for a column is equal to 0.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating the kurtosis value.
                Default Values: False
                Types: bool

        RETURNS:
            teradataml DataFrame object with kurtosis()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If kurtosis() operation fails to
               generate the column-wise kurtosis value of the dataframe.

               Possible error message:
               Unable to perform 'kurtosis()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the kurtosis() operation
               doesn't support all the columns in the dataframe.

               Possible error message:
               No results. Below is/are the error message(s):
               All selected columns [(col2 -  PERIOD_TIME), (col3 -
               BLOB)] is/are unsupported for 'kurtosis' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["admissions_train"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("admissions_train")
            >>> print(df1.sort("id"))
               masters   gpa     stats programming  admitted
            id
            1      yes  3.95  Beginner    Beginner         0
            2      yes  3.76  Beginner    Beginner         0
            3       no  3.70    Novice    Beginner         1
            4      yes  3.50  Beginner      Novice         1
            5       no  3.44    Novice      Novice         0
            6      yes  3.50  Beginner    Advanced         1
            7      yes  2.33    Novice      Novice         1
            8       no  3.60  Beginner    Advanced         1
            9       no  3.82  Advanced    Advanced         1
            10      no  3.71  Advanced    Advanced         1
            >>>

            # Prints kurtosis value of each column
            >>> df1.kurtosis()
               kurtosis_id  kurtosis_gpa  kurtosis_admitted
            0         -1.2      4.052659            -1.6582
            >>>

            #
            # Using kurtosis() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            #
            # Time Series Aggregate Example 1: Executing kurtosis() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the kurtosis values.
            #
            # To use kurtosis() as Time Series Aggregate we must run groupby_time() first, followed by kurtosis().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.kurtosis().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid kurtosis_salinity  kurtosis_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0              None             -5.998128
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1              None             -2.758377
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2              None                   NaN
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44              None             -2.195395
            >>>

            #
            # Time Series Aggregate Example 2: Executing kurtosis() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT values for the
            #                                  columns while calculating the kurtosis value.
            #
            # To use kurtosis() as Time Series Aggregate we must run groupby_time() first, followed by kurtosis().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.kurtosis(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid kurtosis_salinity  kurtosis_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0              None                   NaN
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1              None             -2.758377
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2              None                   NaN
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44              None              4.128426
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return self._get_dataframe_aggregate(operation='kurtosis', distinct=distinct)

    def min(self, distinct=False):
        """
        DESCRIPTION:
            Returns column-wise minimum value of the dataframe.
            Note:
                Null values are not included in the result computation.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating the minimum value.
                Default Values: False
                Types: bool

        RETURNS:
            teradataml DataFrame object with min()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If min() operation fails to
                generate the column-wise minimum value of the dataframe.

                Possible error message:
                Unable to perform 'min()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the min() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'min' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Prints minimum value of each column(with supported data types).
            >>> df1.min()
              min_employee_no min_first_name min_marks min_dob min_joined_date
            0             100           abcd      None    None        02/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            # Prints minimum value of each column(with supported data types).
            >>> df3 = df1.select(['employee_no', 'first_name', 'joined_date'])
            >>> df3.min()
              min_employee_no min_first_name min_joined_date
            0             100           abcd        02/12/05
            >>>

            #
            # Using min() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            #
            # Time Series Aggregate Example 1: Executing min() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the minimum values.
            #
            # To use min() as Time Series Aggregate we must run groupby_time() first, followed by min().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.min().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid             min_TD_TIMECODE  min_salinity  min_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0  2014-01-06 08:00:00.000000            55               10
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1  2014-01-06 09:01:25.122200            55               70
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2  2014-01-06 21:01:25.122200            55               80
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44  2014-01-06 10:00:24.000000            55               43
            >>>

            #
            # Time Series Aggregate Example 2: Executing min() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT values for the
            #                                  columns while calculating the minimum value.
            #
            # To use min() as Time Series Aggregate we must run groupby_time() first, followed by min().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.min(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid             min_TD_TIMECODE  min_salinity  min_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0  2014-01-06 08:00:00.000000            55               10
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1  2014-01-06 09:01:25.122200            55               70
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2  2014-01-06 21:01:25.122200            55               80
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44  2014-01-06 10:00:24.000000            55               43
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return self._get_dataframe_aggregate(operation='min', distinct=distinct)

    def max(self, distinct=False):
        """
        DESCRIPTION:
            Returns column-wise maximum value of the dataframe.
            Note:
                Null values are not included in the result computation.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating the maximum value.
                Default Values: False
                Types: bool

        RETURNS:
            teradataml DataFrame object with max()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If max() operation fails to
                generate the column-wise maximum value of the dataframe.

                Possible error message:
                Unable to perform 'max()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the max() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'max' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Prints maximum value of each column(with supported data types).
            >>> df1.max()
              max_employee_no max_first_name max_marks max_dob max_joined_date
            0             112          abcde      None    None        18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df3 = df1.select(['employee_no', 'first_name', 'joined_date'])

            # Prints maximum value of each column(with supported data types).
            >>> df3.max()
              max_employee_no max_first_name max_joined_date
            0             112          abcde        18/12/05
            >>>

            #
            # Using max() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            #
            # Time Series Aggregate Example 1: Executing max() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the maximum values.
            #
            # To use max() as Time Series Aggregate we must run groupby_time() first, followed by max().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.max().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid             max_TD_TIMECODE  max_salinity  max_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0  2014-01-06 08:10:00.000000            55              100
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1  2014-01-06 09:03:25.122200            55               79
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2  2014-01-06 21:03:25.122200            55               82
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44  2014-01-06 10:52:00.000009            55               56
            >>>

            #
            # Time Series Aggregate Example 2: Executing max() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT values for the
            #                                  columns while calculating the maximum value.
            #
            # To use max() as Time Series Aggregate we must run groupby_time() first, followed by max().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.max(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid             max_TD_TIMECODE  max_salinity  max_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0  2014-01-06 08:10:00.000000            55              100
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1  2014-01-06 09:03:25.122200            55               79
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2  2014-01-06 21:03:25.122200            55               82
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44  2014-01-06 10:52:00.000009            55               56
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return self._get_dataframe_aggregate(operation='max', distinct=distinct)

    def mean(self, distinct=False):
        """
        DESCRIPTION:
            Returns column-wise mean value of the dataframe.
            Notes:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating the mean.
                Default Values: False

        RETURNS:
            teradataml DataFrame object with mean()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If mean() operation fails to
                generate the column-wise mean value of the dataframe.

                Possible error message:
                Unable to perform 'mean()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the mean() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'mean' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df2 = df1.select(['employee_no', 'marks', 'first_name'])

            # Prints mean value of each column(with supported data types).
            >>> df2.mean()
               mean_employee_no mean_marks
            0        104.333333       None
            >>>

            #
            # Using mean() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            #
            # Time Series Aggregate Example 1: Executing mean() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the mean values.
            #
            # To use mean() as Time Series Aggregate we must run groupby_time() first, followed by mean().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.mean().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  mean_salinity  mean_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0           55.0         54.750000
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1           55.0         74.500000
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2           55.0         81.000000
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44           55.0         48.076923
            >>>

            #
            # Time Series Aggregate Example 2: Executing mean() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT values for the
            #                                  columns while calculating the mean value.
            #
            # To use mean() as Time Series Aggregate we must run groupby_time() first, followed by mean().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.mean(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  mean_salinity  mean_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0           55.0         69.666667
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1           55.0         74.500000
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2           55.0         81.000000
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44           55.0         52.200000
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return self._get_dataframe_aggregate(operation='mean', distinct = distinct)

    def skew(self, distinct=False):
        """
        DESCRIPTION:
            Returns column-wise skewness of the distribution of the dataframe.
            Skewness is the third moment of a distribution. It is a measure of the asymmetry of the
            distribution about its mean compared with the normal (or Gaussian) distribution.
                * The normal distribution has a skewness of 0.
                * Positive skewness indicates a distribution having an asymmetric tail
                  extending toward more positive values.
                * Negative skewness indicates an asymmetric tail extending toward more negative values.

            Notes:
                1. This function is valid only on columns with numeric types.
                2. Nulls are not included in the result computation.
                3. Following conditions will produce null result:
                    a. Fewer than three non-null data points in the data used for the computation.
                    b. Standard deviation for a column is equal to 0.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating the skewness of the distribution.
                Default Values: False
                Types: bool

        RETURNS:
            teradataml DataFrame object with skew()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If the skew() operation fails to
                generate the column-wise skew value of the dataframe.

                Possible error message:
                Unable to perform 'skew()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the skew() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'skew' operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", ["admissions_train"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("admissions_train")
            >>> print(df1.sort('id'))
               masters   gpa     stats programming  admitted
            id
            1      yes  3.95  Beginner    Beginner         0
            2      yes  3.76  Beginner    Beginner         0
            3       no  3.70    Novice    Beginner         1
            4      yes  3.50  Beginner      Novice         1
            5       no  3.44    Novice      Novice         0
            6      yes  3.50  Beginner    Advanced         1
            7      yes  2.33    Novice      Novice         1
            8       no  3.60  Beginner    Advanced         1
            9       no  3.82  Advanced    Advanced         1
            10      no  3.71  Advanced    Advanced         1
            >>>

            # Prints skew value of each column(with supported data types).
            >>> df1.skew()
               skew_id  skew_gpa  skew_admitted
            0      0.0 -2.058969      -0.653746
            >>>

            #
            # Using skew() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            #
            # Time Series Aggregate Example 1: Executing skew() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the skew values.
            #
            # To use skew() as Time Series Aggregate we must run groupby_time() first, followed by skew().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.skew().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid skew_salinity  skew_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0          None          0.000324
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1          None          0.000000
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2          None          0.000000
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44          None          0.246084
            >>>

            #
            # Time Series Aggregate Example 2: Executing skew() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT values for the
            #                                  columns while calculating the skew value.
            #
            # To use skew() as Time Series Aggregate we must run groupby_time() first, followed by skew().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.skew(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid skew_salinity  skew_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0          None         -1.731321
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1          None          0.000000
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2          None          0.000000
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44          None         -1.987828
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return self._get_dataframe_aggregate(operation='skew', distinct=distinct)

    def sum(self, distinct=False):
        """
        DESCRIPTION:
            Returns column-wise sum value of the dataframe.
            Notes:
                1. teradataml doesn't support sum operation on columns of str, datetime types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating the sum.
                Default Value: False 
                Types: bool

        RETURNS:
            teradataml DataFrame object with sum()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If sum() operation fails to
                generate the column-wise summation value of the dataframe.

                Possible error message:
                Unable to perform 'sum()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the sum() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'sum' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Prints sum of the values of each column(with supported data types).
            >>> df1.sum()
              sum_employee_no sum_marks
            0             313      None
            >>>

            #
            # Using sum() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>

            #
            # Time Series Aggregate Example 1: Executing sum() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the sum value.
            #
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            # To use sum() as Time Series Aggregate we must run groupby_time() first, followed by sum().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.sum().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  sum_salinity  sum_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0           275              219
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1           330              447
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2           165              243
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44           715              625
            >>>

            #
            # Time Series Aggregate Example 2: Executing sum() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT values for the
            #                                  columns while calculating the sum value.
            #
            # To use sum() as Time Series Aggregate we must run groupby_time() first, followed by sum().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.sum(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  sum_salinity  sum_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0            55              209
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1            55              447
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2            55              243
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44            55              261
            >>>

        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return self._get_dataframe_aggregate(operation='sum', distinct=distinct)

    def count(self, distinct=False):
        """
        DESCRIPTION:
            Returns column-wise count of the dataframe.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating the count.
                Default Value: False
                Types: bool

        RETURNS:
            teradataml DataFrame object with count() operation
            performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If count() operation fails to
                generate the column-wise count of the dataframe.

                Possible error message:
                Unable to perform 'count()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the count() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'count' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df2 = df1.select(['employee_no', 'first_name', 'marks'])

            # Prints count of the values in all the selected columns
            # (excluding None types).
            >>> df2.count()
              count_employee_no count_first_name count_marks
            0                 3                2           0
            >>>

            #
            # Using count() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys_seq"])
            >>>

            #
            # Time Series Aggregate Example 1: Executing count() function on DataFrame created on
            #                                  sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the count.
            #
            >>> ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            44      2014-01-06 10:00:25.122200         6        55           43  2014-06-06
            44      2014-01-06 10:01:25.122200         8        55           53  2014-08-08
            44      2014-01-06 10:01:25.122200        20        55           54  2015-08-20
            1       2014-01-06 09:01:25.122200        11        55           70  2014-11-11
            1       2014-01-06 09:02:25.122200        12        55           71  2014-12-12
            1       2014-01-06 09:02:25.122200        24        55           78  2015-12-24
            1       2014-01-06 09:03:25.122200        13        55           72  2015-01-13
            1       2014-01-06 09:03:25.122200        25        55           79  2016-01-25
            1       2014-01-06 09:01:25.122200        23        55           77  2015-11-23
            44      2014-01-06 10:00:26.122200         7        55           43  2014-07-07
            >>>

            # To use count() as Time Series Aggregate we must run groupby_time() first, followed by count().
            >>> ocean_buoys_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="2cy", value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.count().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  count_TD_TIMECODE  count_TD_SEQNO  count_salinity  count_temperature  count_dates
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                  5               5               5                  4            5
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                  6               6               6                  6            6
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                  3               3               3                  3            3
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      22                  1               1               1                  1            1
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                 13              13              13                 13           13
            >>>

            #
            # Time Series Aggregate Example 2: Executing count() function on DataFrame created on
            #                                  sequenced PTI table. We will consider DISTINCT rows for the
            #                                  columns while calculating the count.
            #
            # To use count() as Time Series Aggregate we must run groupby_time() first, followed by count().
            >>> ocean_buoys_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="2cy",value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.count(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  count_TD_TIMECODE  count_TD_SEQNO  count_salinity  count_temperature  count_dates
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                  4               5               1                  3            5
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                  3               6               1                  6            6
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                  3               3               1                  3            3
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      22                  1               1               1                  1            1
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                 10              13               1                  5           13
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        return self._get_dataframe_aggregate(operation='count', distinct=distinct)

    def std(self, distinct=False, population=False):
        """
        DESCRIPTION:
            Returns column-wise sample or population standard deviation value of the
            dataframe. The standard deviation is the second moment of a distribution.
                * For a sample, it is a measure of dispersion from the mean of that sample.
                * For a population, it is a measure of dispersion from the mean of that population.
            The computation is more conservative for the population standard deviation
            to minimize the effect of outliers on the computed value.
            Note:
                1. When there are fewer than two non-null data points in the sample used
                   for the computation, then std returns None.
                2. Null values are not included in the result computation.
                3. If data represents only a sample of the entire population for the
                   columns, Teradata recommends to calculate sample standard deviation,
                   otherwise calculate population standard deviation.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating
                the standard deviation.
                Default Value: False
                Types: bool

            population:
                Optional Argument.
                Specifies whether to calculate standard deviation on entire population or not.
                Set this argument to True only when the data points represent the complete
                population. If your data represents only a sample of the entire population for the
                columns, then set this variable to False, which will compute the sample standard
                deviation. As the sample size increases, even though the values for sample
                standard deviation and population standard deviation approach the same number,
                you should always use the more conservative sample standard deviation calculation,
                unless you are absolutely certain that your data constitutes the entire population
                for the columns.
                Default Value: False
                Types: bool

        RETURNS:
            teradataml DataFrame object with std() operation performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If std() operation fails to
                generate the column-wise standard deviation of the
                dataframe.

                Possible error message:
                Unable to perform 'std()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the std() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'std' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df2 = df1.select(['employee_no', 'first_name', 'marks', 'joined_date'])

            # Prints sample standard deviation of each column(with supported data types).
            >>> df2.std()
               std_employee_no std_marks std_joined_date
            0         6.658328      None        82/03/09
            >>>

            # Prints population standard deviation of each column(with supported data types).
            >>> df2.std(population=True)
               std_employee_no std_marks std_joined_date
            0         5.436502      None        58/02/28
            >>>

            #
            # Using std() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>

            #
            # Time Series Aggregate Example 1: Executing std() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the standard deviation.
            #
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            # To use std() as Time Series Aggregate we must run groupby_time() first, followed by std().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.std().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  std_salinity  std_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0           0.0        51.674462
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1           0.0         3.937004
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2           0.0         1.000000
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44           0.0         5.765725
            >>>

            #
            # Time Series Aggregate Example 2: Executing std() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT rows for the
            #                                  columns while calculating the standard deviation.
            #
            # To use std() as Time Series Aggregate we must run groupby_time() first, followed by std().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.std(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid std_salinity  std_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0         None        51.675268
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1         None         3.937004
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2         None         1.000000
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44         None         5.263079
            >>>

            #
            # Time Series Aggregate Example 3: Executing std() function on DataFrame created on
            #                                  non-sequenced PTI table. We shall calculate the
            #                                  standard deviation on entire population, with
            #                                  all non-null data points considered for calculations.
            #
            # To use std() as Time Series Aggregate we must run groupby_time() first, followed by std().
            # To calculate population standard deviation we must set population=True.
            #
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.std(population=True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  std_salinity  std_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0           0.0        44.751397
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1           0.0         3.593976
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2           0.0         0.816497
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44           0.0         5.539530
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])
        awu_matrix.append(["population", population, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        return self._get_dataframe_aggregate(operation='std', distinct=distinct, population=population)

    def median(self, distinct=False):
        """
        DESCRIPTION:
            Returns column-wise median value of the dataframe.
            Notes:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating the median.
                Note:
                    This is allowed only when median() is used as Time Series Aggregate function, i.e.,
                    this can be set to True, only when median() is operated on DataFrameGroupByTime object.
                    Otherwise, an exception will be raised.
                Default Values: False

        RETURNS:
            teradataml DataFrame object with median() operation
            performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If median() operation fails to
                generate the column-wise median value of the dataframe.

                Possible error message:
                Unable to perform 'median()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the median() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'median' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Prints median value of each column(with supported data types).
            >>> df1.median()
              median_employee_no median_marks
            0                101         None
            >>>

            #
            # Using median() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>

            #
            # Time Series Aggregate Example 1: Executing median() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the median value.
            #
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            # To use median() as Time Series Aggregate we must run groupby_time() first, followed by median().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.median().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  median_temperature  median_salinity
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                54.5             55.0
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                74.5             55.0
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                81.0             55.0
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                43.0             55.0
            >>>

            #
            # Time Series Aggregate Example 2: Executing median() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT rows for the
            #                                  columns while calculating the median value.
            #
            # To use median() as Time Series Aggregate we must run groupby_time() first, followed by median().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.median(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  median_temperature  median_salinity
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                99.0             55.0
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                74.5             55.0
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                81.0             55.0
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                54.0             55.0
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if distinct and not isinstance(self, DataFrameGroupByTime):
            raise ValueError(Messages.get_message(MessageCodes.ARG_VALUE_CLASS_DEPENDENCY).format('distinct', 'Aggregation',
                                                                                         'True', 'median()',
                                                                                         'DataFrameGroupByTime'))

        return self._get_dataframe_aggregate(operation = 'median', distinct = distinct)

    def var(self, distinct=False, population=False):
        """
        DESCRIPTION:
            Returns column-wise sample or population variance of the columns in a
            dataframe.
                * The variance of a population is a measure of dispersion from the
                  mean of that population.
                * The variance of a sample is a measure of dispersion from the mean
                  of that sample. It is the square of the sample standard deviation.
            Note:
                1. When there are fewer than two non-null data points in the sample used
                   for the computation, then var returns None.
                2. Null values are not included in the result computation.
                3. If data represents only a sample of the entire population for the
                   columns, Teradata recommends to calculate sample variance,
                   otherwise calculate population variance.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate column values while calculating the
                variance value.
                Default Values: False
                Types: bool

            population:
                Optional Argument.
                Specifies whether to calculate variance on entire population or not.
                Set this argument to True only when the data points represent the complete
                population. If your data represents only a sample of the entire population
                for the columns, then set this variable to False, which will compute the
                sample variance. As the sample size increases, even though the values for
                sample variance and population variance approach the same number, but you
                should always use the more conservative sample standard deviation calculation,
                unless you are absolutely certain that your data constitutes the entire
                population for the columns.
                Default Value: False
                Types: bool
            
        RETURNS:
            teradataml DataFrame object with var() operation performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If var() operation fails to
                generate the column-wise variance of the dataframe.

                Possible error message:
                Unable to perform 'var()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the var() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'var' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info", "sales"])

            # Example 1 - Applying var on table 'employee_info' that has all
            #             NULL values in marks and dob columns which are
            #             captured as None in variance dataframe.

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df3 = df1.select(["employee_no", "first_name", "dob", "marks"])

            # Prints unbiased variance of each column(with supported data types).
            >>> df3.var()
                   var_employee_no var_dob var_marks
                0        44.333333    None      None

            # Example 2 - Applying var on table 'sales' that has different
            #             types of data like floats, integers, strings
            #             some of which having NULL values which are ignored.

            # Create teradataml dataframe.
            >>> df1 = DataFrame("sales")
            >>> print(df1)
                              Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017

            # Prints unbiased sample variance of each column(with supported data types).
            >>> df3 = df1.select(["accounts","Feb","Jan","Mar","Apr"])
            >>> df3.var()
                   var_Feb      var_Jan  var_Mar      var_Apr
            0  3546.666667  3958.333333   2475.0  5036.916667
            >>>

            # Prints population variance of each column(with supported data types).
            >>> df3.var(population=True)
                   var_Feb  var_Jan  var_Mar    var_Apr
            0  2955.555556  2968.75  1856.25  3777.6875
            >>>

            #
            # Using var() as Time Series Aggregate.
            #
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])
            >>>

            #
            # Time Series Aggregate Example 1: Executing var() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider all rows for the
            #                                  columns while calculating the variance value.
            #
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            # To use var() as Time Series Aggregate we must run groupby_time() first, followed by var().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.var().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  var_salinity  var_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0           0.0       2670.25000
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1           0.0         15.50000
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2           0.0          1.00000
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44           0.0         33.24359
            >>>

            #
            # Time Series Aggregate Example 2: Executing var() function on DataFrame created on
            #                                  non-sequenced PTI table. We will consider DISTINCT rows for the
            #                                  columns while calculating the variance value.
            #
            # To use var() as Time Series Aggregate we must run groupby_time() first, followed by var().
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.var(distinct = True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid var_salinity  var_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0         None      2670.333333
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1         None        15.500000
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2         None         1.000000
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44         None        27.700000
            >>>

            #
            # Time Series Aggregate Example 3: Executing var() function on DataFrame created on
            #                                  non-sequenced PTI table. We shall calculate the
            #                                  variance on entire population, with all non-null
            #                                  data points considered for calculations.
            #
            # To use var() as Time Series Aggregate we must run groupby_time() first, followed by var().
            # To calculate population variance we must set population=True.
            #
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.var(population=True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  var_salinity  var_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0           0.0      2002.687500
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1           0.0        12.916667
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2           0.0         0.666667
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44           0.0        30.686391
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["distinct", distinct, True, (bool)])
        awu_matrix.append(["population", population, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return self._get_dataframe_aggregate(operation='var', distinct=distinct, population=population)

    def agg(self, func = None):
        """
        DESCRIPTION:
            Perform aggregates using one or more operations.

        PARAMETERS:
            func:
                Required Argument.
                Specifies the function(s) to apply on DataFrame columns.

                Valid values for func are:
                    'count', 'sum', 'min', 'max', 'mean', 'std', 'percentile', 'unique',
                    'median', 'var'

                Acceptable formats for function(s) are
                    string, dictionary or list of strings/functions.

                Accepted combinations are:
                    1. String function name
                    2. List of string functions
                    3. Dictionary containing column name as key and
                       aggregate function name (string or list of
                       strings) as value

        RETURNS:
            teradataml DataFrame object with operations
            mentioned in parameter 'func' performed on specified
            columns.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If operations on given columns
                fail to generate aggregate dataframe.

                Possible error message:
                Unable to perform 'agg()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the provided
                aggregate operations do not support specified columns.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col1 - VARCHAR)] is/are
                unsupported for 'sum' operation.

            3. TDMLDF_INVALID_AGGREGATE_OPERATION - If the aggregate
                operation(s) received in parameter 'func' is/are
                invalid.

                Possible error message:
                Invalid aggregate operation(s): minimum, counter.
                Valid aggregate operation(s): count, max, mean, min,
                std, sum.

            4. TDMLDF_AGGREGATE_INVALID_COLUMN - If any of the columns
                specified in 'func' is not present in the dataframe.

                Possible error message:
                Invalid column(s) given in parameter func: col1.
                Valid column(s) : A, B, C, D.

            5. MISSING_ARGS - If the argument 'func' is missing.

                Possible error message:
                Following required arguments are missing: func.

            6. UNSUPPORTED_DATATYPE - If the argument 'func' is not of
                valid datatype.

                Possible error message:
                Invalid type(s) passed to argument 'func', should be:"\
                             "['str', 'list', 'dict'].

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info", "sales"])

            # Create teradataml dataframe.
            >>> df = DataFrame("employee_info")
            >>> print(df)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Dictionary of column names to string function/list of string functions as parameter.
            >>> df.agg({'employee_no' : ['min', 'sum', 'var'], 'first_name' : ['min', 'mean']})
                  min_employee_no sum_employee_no  var_employee_no min_first_name
                0             100             313        44.333333           abcd

            # List of string functions as parameter.
            >>> df.agg(['min', 'sum'])
                  min_employee_no sum_employee_no min_first_name min_marks sum_marks min_dob min_joined_date
                0             100             313           abcd      None      None    None      1902-05-12

            # A string function as parameter.
            >>> df.agg('mean')
               mean_employee_no mean_marks mean_dob mean_joined_date
            0        104.333333       None     None         60/12/04

            # Select only subset of columns from the DataFrame.
            >>> df1 = df.select(['employee_no', 'first_name', 'joined_date'])

            # List of string functions as parameter.
            >>> df1.agg(['mean', 'unique'])
               mean_employee_no unique_employee_no unique_first_name mean_joined_date unique_joined_date
            0        104.333333                  3                 2         60/12/04                  2

            >>> df.agg('percentile')
                  percentile_employee_no percentile_marks
                0                    101             None

            # Using another table 'sales' (having repeated values) to demonstrate operations
            # 'unique' and 'percentile'.

            # Create teradataml dataframe.
            >>> df = DataFrame('sales')
            >>> df
                              Feb   Jan   Mar   Apr    datetime
                accounts
                Yellow Inc   90.0  None  None  None  2017-04-01
                Alpha Co    210.0   200   215   250  2017-04-01
                Jones LLC   200.0   150   140   180  2017-04-01
                Orange Inc  210.0  None  None   250  2017-04-01
                Blue Inc     90.0    50    95   101  2017-04-01
                Red Inc     200.0   150   140  None  2017-04-01

            >>> df.agg('percentile')
                   percentile_Feb percentile_Jan percentile_Mar percentile_Apr
                0           200.0            150            140            215

            >>> df.agg('unique')
                  unique_accounts unique_Feb unique_Jan unique_Mar unique_Apr unique_datetime
                0               6          3          3          3          3               1
        """

        if func is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS, "func"),
                                      MessageCodes.MISSING_ARGS)

        if not isinstance(func, str) and not isinstance(func, list) and not isinstance(func, dict):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE,
                                'func', ['str', 'list', 'dict']), MessageCodes.UNSUPPORTED_DATATYPE)

        return self._get_dataframe_aggregate(func)

    def _get_dataframe_aggregate(self, operation, **kwargs):
        """
        Returns the DataFrame given the aggregate operation or list of
        operations or dictionary of column names -> operations.

        PARAMETERS:
            operation - Required Argument. Specifies the function(s) to be
                    applied on teradataml DataFrame columns.
                    Acceptable formats for function(s) are string,
                    dictionary or list of strings/functions.
                    Accepted combinations are:
                    1. String function name
                    2. List of string functions
                    3. Dictionary containing column name as key and
                       aggregate function name (string or list of
                       strings) as value

            **kwargs: Keyword arguments. Mainly used for Time Series Aggragates.

        RETURNS:
            teradataml DataFrame object with required
            operations mentioned in 'operation' parameter performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If operations on given columns
                fail to generate output dataframe.

                Possible error message:
                Unable to perform 'agg()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the provided
                aggregate operations do not support specified columns.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col1 - VARCHAR)] is/are
                unsupported for 'sum' operation.

            3. TDMLDF_INVALID_AGGREGATE_OPERATION - If the aggregate
                operation(s) received in parameter 'operation' is/are
                invalid.

                Possible error message:
                Invalid aggregate operation(s): minimum, counter.
                Valid aggregate operation(s): count, max, mean, min,
                std, sum.

            4. TDMLDF_AGGREGATE_INVALID_COLUMN - If any of the columns
                specified in the parameter 'operation' is not present
                in the dataframe.

                Possible error message:
                Invalid column(s) given in parameter func: col1.
                Valid column(s) : A, B, C, D.

        EXAMPLES :
            df = _get_dataframe_aggregate(operation = 'mean')
            or
            df = _get_dataframe_aggregate(operation = ['mean', 'min'])
            or
            df = _get_dataframe_aggregate(operation = {'col1' :
                                    ['mean', 'min'], 'col2' : 'count'})
        """
        if isinstance(self, DataFrameGroupByTime) and self._timebucket_duration == "*" and operation != 'delta_t':
            raise ValueError(Messages.get_message(
                MessageCodes.INVALID_ARG_VALUE).format("*", 'timebucket_duration while grouping time series data',
                                                       'a valid timebucket duration, as mentioned in user guide. '
                                                       'DELTA_T is the only aggregate function that can be used with '
                                                       'timebucket_duration as \'*\''))

        try:
            # Check if aggregation is to be performed on specific set of columns or not.
            columns = kwargs['columns'] if "columns" in kwargs.keys() else None
            if columns is not None:
                col_names = []
                col_types = []
                if isinstance(columns, str):
                    columns = [columns]
                for col in columns:
                    col_names.append(col)
                    col_types.append(self[col].type)
            else:
                # Retrieve the column names and types from the metaexpr.
                col_names, col_types = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)

            # Remove columns from metaexpr before passing to stated aggr func if self
            # is of DataFrameGroupBy or DataFrameGroupByTime type so that no duplicate
            # columns shown in result
            groupby_col_names = []
            groupby_col_types = []
            pti_default_cols_proj = []
            pti_default_cols_types = []
            is_time_series_aggregate = True if isinstance(self, DataFrameGroupByTime) else False
            if isinstance(self, DataFrameGroupBy) or isinstance(self, DataFrameGroupByTime):
                for col in self.groupby_column_list:
                    if "GROUP BY TIME" not in col and col != "TIMECODE_RANGE":
                        # If group by columns are not time series specific columns, then process
                        # these group by columns, so that they are removed from the actual projection
                        # list and aggregate operation will not performed on those.
                        groupby_col_names.append(col)
                        groupby_col_types.append(self[col].type)

                        if col in col_names:
                            # If group by column is not specified in the columns argument,
                            # then, we should ignore this processing, otherwise we
                            # should process it in the same way to remove the reference
                            # for grouping column from aggregation list.
                            colindex = col_names.index(col)

                            # Remove the grouping column and it's type from the lists.
                            del col_names[colindex]
                            del col_types[colindex]
                    else:
                        # If grouping columns are timeseries columns, then process those
                        # and generate a separate list of columns and their types.
                        pti_default_cols_proj.append(col)
                        if "GROUP BY TIME" not in col:
                            ctypes = PERIOD_TIMESTAMP
                        else:
                            ctypes = BIGINT
                        pti_default_cols_types.append(ctypes)

            # Return Empty DataFrame if all the columns are selected in groupby as parent has
            if len(col_names) == 0:
                aggregate_expression, new_column_names, new_column_types = \
                        df_utils._construct_sql_expression_for_aggregations(self,
                            groupby_col_names, groupby_col_types, operation,
                            as_time_series_aggregate = is_time_series_aggregate, **kwargs)
                self._index_label = new_column_names
            else:
                aggregate_expression, new_column_names, new_column_types = \
                        df_utils._construct_sql_expression_for_aggregations(self,
                            col_names, col_types, operation, as_time_series_aggregate = is_time_series_aggregate,
                            **kwargs)
                new_column_names = pti_default_cols_proj + groupby_col_names + new_column_names
                new_column_types = pti_default_cols_types + groupby_col_types + new_column_types

            if isinstance(operation, dict) or isinstance(operation, list):
                operation = 'agg'

            aggregate_node_id = self._aed_utils._aed_aggregate(self._nodeid, aggregate_expression,
                                                               operation)

            new_metaexpr = UtilFuncs._get_metaexpr_using_columns(aggregate_node_id,
                                                                 zip(new_column_names,
                                                                     new_column_types))
            return DataFrame._from_node(aggregate_node_id, new_metaexpr, self._index_label)

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(
                MessageCodes.TDMLDF_AGGREGATE_FAILED, str(err.exception)).format(operation),
                                      MessageCodes.TDMLDF_AGGREGATE_FAILED) from err

    def __repr__(self):
        """
        Returns the string representation for a teradataml DataFrame instance.
        The string contains:
            1. Column names of the dataframe.
            2. At most the first no_of_rows rows of the dataframe.
            3. A default index for row numbers.

        NOTES:
          - This makes an explicit call to get rows from the database.
          - To change number of rows to be printed set the max_rows option in options.display.display
          - Default value of max_rows is 10

        EXAMPLES:
            df = DataFrame.from_table("table1")
            print(df)

            df = DataFrame.from_query("select col1, col2, col3 from table1")
            print(df)
        """
        try:

            # Generate/Execute AED nodes
            self.__execute_node_and_set_table_name(self._nodeid, self._metaexpr)

            query = repr(self._metaexpr) + ' FROM ' + self._table_name

            if self._orderby is not None:
                query += ' ORDER BY ' + self._orderby

            # Execute the query and get the results in a list and create a Pandas DataFrame from the same.
            data, columns = UtilFuncs._execute_query(query=query, fetchWarnings=True)
            pandas_df = pd.DataFrame.from_records(data, columns=columns, coerce_float=True)

            if self._index_label:
                pandas_df.set_index(self._index_label, inplace=True)

            if self._undropped_index is not None:
                for col in self._undropped_index:
                    pandas_df.insert(0, col, pandas_df.index.get_level_values(col).tolist(), allow_duplicates = True)

            return pandas_df.to_string()

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR) + str(err),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    def select(self, select_expression):
        """
        DESCRIPTION:
            Select required columns from DataFrame using an expression.
            Returns a new teradataml DataFrame with selected columns only.

        PARAMETERS:

            select_expression:
                Required Argument.
                String or List representing columns to select.
                Types: str OR List of Strings (str)

                The following formats (only) are supported for select_expression:

                A] Single Column String: df.select("col1")
                B] Single Column List: df.select(["col1"])
                C] Multi-Column List: df.select(['col1', 'col2', 'col3'])
                D] Multi-Column List of List: df.select([["col1", "col2", "col3"]])

                Column Names ("col1", "col2"..) are Strings representing Teradata Vantage table Columns.
                All Standard Teradata Data-Types for columns supported: INTEGER, VARCHAR(5), FLOAT.

                Note: Multi-Column selection of the same column such as df.select(['col1', 'col1']) is not supported.

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException (TDMLDF_SELECT_INVALID_COLUMN, TDMLDF_SELECT_INVALID_FORMAT,
                                 TDMLDF_SELECT_DF_FAIL, TDMLDF_SELECT_EXPR_UNSPECIFIED,
                                 TDMLDF_SELECT_NONE_OR_EMPTY)

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            5       no  3.44    Novice      Novice        0
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            19     yes  1.98  Advanced    Advanced        0
            36      no  3.00  Advanced      Novice        0
            15     yes  4.00  Advanced    Advanced        1
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            A] Single String Column
            >>> df.select("id")
            Empty DataFrame
            Columns: []
            Index: [22, 34, 13, 19, 15, 38, 26, 5, 36, 17]

            B] Single Column List
            >>> df.select(["id"])
            Empty DataFrame
            Columns: []
            Index: [15, 26, 5, 40, 22, 17, 34, 13, 7, 38]

            C] Multi-Column List
            >>> df.select(["id", "masters", "gpa"])
               masters   gpa
            id
            5       no  3.44
            36      no  3.00
            15     yes  4.00
            17      no  3.83
            13      no  4.00
            40     yes  3.95
            7      yes  2.33
            22     yes  3.46
            34     yes  3.85
            19     yes  1.98

            D] Multi-Column List of List
            >>> df.select([['id', 'masters', 'gpa']])
               masters   gpa
            id
            5       no  3.44
            34     yes  3.85
            13      no  4.00
            40     yes  3.95
            22     yes  3.46
            19     yes  1.98
            36      no  3.00
            15     yes  4.00
            7      yes  2.33
            17      no  3.83
        """
        try:
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

            # If invalid, appropriate exception raised; Processing ahead only for valid expressions
            select_exp_col_list = self.__validate_select_expression(select_expression)

            # Constructing New Column names & Types for selected columns ONLY using Parent _metaexpr
            col_names_types = df_utils._get_required_columns_types_from_metaexpr(self._metaexpr, select_exp_col_list)

            # Create a node in AED using _aed_select
            column_expression = ','.join(select_exp_col_list)
            sel_nodeid = self._aed_utils._aed_select(self._nodeid, column_expression)

            # Constructing new Metadata (_metaexpr) without DB; using dummy select_nodeid and underlying table name.
            new_metaexpr = UtilFuncs._get_metaexpr_using_columns(sel_nodeid, col_names_types.items())
            return DataFrame._from_node(sel_nodeid, new_metaexpr, self._index_label)

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_DF_FAIL, str(err.exception)),
                                      MessageCodes.TDMLDF_SELECT_DF_FAIL) from err

    def __validate_select_expression(self, select_expression):
        """
        This is an internal function used to validate the select expression for the Select API.
        When the select expression is valid, a list of valid columns to be selected is returned.
        Appropriate TeradataMlException is raised when validation fails.

        PARAMETERS:
            select_expression - The expression to be validated.
            Types: Single String or List of Strings or List of List (single-level)
            Required: Yes

        RETURNS:
            List of column name strings, when valid select_expression is passed.

        RAISES:
            TeradataMlException, when parameter validation fails.

        EXAMPLES:
            self.__validate_select_expression(select_expression = 'col1')
            self.__validate_select_expression(select_expression = ["col1"])
            self.__validate_select_expression(select_expression = [['col1', 'col2', 'col3']])
        """
        tdp = preparer(td_dialect)

        if select_expression is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_EXPR_UNSPECIFIED),
                                      MessageCodes.TDMLDF_SELECT_EXPR_UNSPECIFIED)

        else:
            # _extract_select_string returns column list only if valid; else raises appropriate exception
            select_exp_col_list = df_utils._extract_select_string(select_expression)
            df_column_list = [tdp.quote("{0}".format(column.name)) for column in self._metaexpr.c]

            # TODO: Remove this check when same column multiple selection enabled
            if len(select_exp_col_list) > len(df_column_list):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_INVALID_COLUMN, ', '.join(df_column_list)),
                                          MessageCodes.TDMLDF_SELECT_INVALID_COLUMN)

            all_cols_exist =  all(col in df_column_list for col in select_exp_col_list)

            if not all_cols_exist:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_INVALID_COLUMN, ', '.join(df_column_list)),
                                          MessageCodes.TDMLDF_SELECT_INVALID_COLUMN)

            return select_exp_col_list

    def to_pandas(self, index_column = None, num_rows = 99999, all_rows = False):
        """
        DESCRIPTION:
            Returns a Pandas DataFrame for the corresponding teradataml DataFrame Object.

        PARAMETERS:
            index_column:
                Optional Argument.
                Specifies column(s) to be used as Pandas index.
                When the argument is provided, the specified column is used as the Pandas index.
                Otherwise, the teradataml DataFrame's index (if exists) is used as the Pandas index
                or the primary index of the table on Vantage is used as the Pandas index.
                The default integer index is used if none of the above indexes exists.
                Default Value: Integer index
                Types: str OR list of Strings (str)

            num_rows:
                Optional Argument.
                The number of rows to retrieve from DataFrame while creating Pandas Dataframe.
                Default Value: 99999
                Types: int
                Note:
                    This argument is ignored if "all_rows" is set to True.

            all_rows:
                Optional Argument.
                Specifies whether all rows from teradataml DataFrame should be retrieved while creating
                Pandas DataFrame.
                Default Value: False
                Types: bool

        RETURNS:
            Pandas DataFrame

            Note:
                Column types of the resulting Pandas DataFrame depends on pandas.read_sql_query(). 

        RAISES:
            TeradataMlException

        EXAMPLES:

            Teradata supports the following formats:

            A] No parameter(s): df.to_pandas()
            B] Single index_column parameter: df.to_pandas(index_column = "col1")
            C] Multiple index_column (list) parameters: df.to_pandas(index_column = ['col1', 'col2'])
            D] Only num_rows parameter specified:  df.to_pandas(num_rows = 100)
            E] Both index_column & num_rows specified: df.to_pandas(index_column = 'col1', num_rows = 100)
            F] Only all_rows parameter specified:  df.to_pandas(all_rows = True)

            Column names ("col1", "col2"..) are strings representing Teradata Vantage table Columns.
            It supports all standard Teradata data types for columns: INTEGER, VARCHAR(5), FLOAT etc.
            df is a Teradata DataFrame object: df = DataFrame.from_table('admissions_train')

            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming admitted
            id
            22     yes  3.46    Novice    Beginner        0
            37      no  3.52    Novice      Novice        1
            35      no  3.68    Novice    Beginner        1
            12      no  3.65    Novice      Novice        1
            4      yes  3.50  Beginner      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            27     yes  3.96  Advanced    Advanced        0
            39     yes  3.75  Advanced    Beginner        0
            7      yes  2.33    Novice      Novice        1
            40     yes  3.95    Novice    Beginner        0
            >>> pandas_df = df.to_pandas()
            >>> pandas_df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            14     yes  3.45  Advanced    Advanced         0
            31     yes  3.50  Advanced    Beginner         1
            29     yes  4.00    Novice    Beginner         0
            23     yes  3.59  Advanced      Novice         1
            21      no  3.87    Novice    Beginner         1
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            32     yes  3.46  Advanced    Beginner         0
            11      no  3.13  Advanced    Advanced         1
            ...

            >>> pandas_df = df.to_pandas(index_column = 'id')
            >>> pandas_df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            14     yes  3.45  Advanced    Advanced         0
            31     yes  3.50  Advanced    Beginner         1
            29     yes  4.00    Novice    Beginner         0
            23     yes  3.59  Advanced      Novice         1
            21      no  3.87    Novice    Beginner         1
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            32     yes  3.46  Advanced    Beginner         0
            11      no  3.13  Advanced    Advanced         1
            28      no  3.93  Advanced    Advanced         1
            ...

            >>> pandas_df = df.to_pandas(index_column = 'gpa')
            >>> pandas_df
                  id masters     stats programming  admitted
            gpa
            4.00  15     yes  Advanced    Advanced         1
            3.45  14     yes  Advanced    Advanced         0
            3.50  31     yes  Advanced    Beginner         1
            4.00  29     yes    Novice    Beginner         0
            3.59  23     yes  Advanced      Novice         1
            3.87  21      no    Novice    Beginner         1
            3.83  17      no  Advanced    Advanced         1
            3.85  34     yes  Advanced    Beginner         0
            4.00  13      no  Advanced      Novice         1
            3.46  32     yes  Advanced    Beginner         0
            3.13  11      no  Advanced    Advanced         1
            3.93  28      no  Advanced    Advanced         1
            ...

            >>> pandas_df = df.to_pandas(index_column = ['masters', 'gpa'])
            >>> pandas_df
                          id     stats programming  admitted
            masters gpa
            yes     4.00  15  Advanced    Advanced         1
                    3.45  14  Advanced    Advanced         0
                    3.50  31  Advanced    Beginner         1
                    4.00  29    Novice    Beginner         0
                    3.59  23  Advanced      Novice         1
            no      3.87  21    Novice    Beginner         1
                    3.83  17  Advanced    Advanced         1
            yes     3.85  34  Advanced    Beginner         0
            no      4.00  13  Advanced      Novice         1
            yes     3.46  32  Advanced    Beginner         0
            no      3.13  11  Advanced    Advanced         1
                    3.93  28  Advanced    Advanced         1
            ...

            >>> pandas_df = df.to_pandas(index_column = 'gpa', num_rows = 3)
            >>> pandas_df
                  id masters   stats programming  admitted
            gpa
            3.46  22     yes  Novice    Beginner         0
            2.33   7     yes  Novice      Novice         1
            3.95  40     yes  Novice    Beginner         0

            >>> pandas_df = df.to_pandas(all_rows = True)
            >>> pandas_df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            14     yes  3.45  Advanced    Advanced         0
            31     yes  3.50  Advanced    Beginner         1
            29     yes  4.00    Novice    Beginner         0
            23     yes  3.59  Advanced      Novice         1
            21      no  3.87    Novice    Beginner         1
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            32     yes  3.46  Advanced    Beginner         0
            11      no  3.13  Advanced    Advanced         1
            ...

        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["index_column", index_column, True, (str, list), True])
        awu_matrix.append(["num_rows", num_rows, True, (int)])
        awu_matrix.append(["all_rows", all_rows, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(index_column, self._metaexpr)

        # Validate n is a positive int.
        _Validators._validate_positive_int(num_rows, "num_rows")

        if self._metaexpr is not None:
            df_column_list = [col.name.lower() for col in self._metaexpr.c]
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

        # Check if TDML DF has appropriate index_label set when required
        df_index_label = self._index_label

        if df_index_label is not None:
            if isinstance(df_index_label, str):
                if df_index_label.lower() not in df_column_list:
                    raise TeradataMlException(Messages.get_message(MessageCodes.DF_LABEL_MISMATCH), MessageCodes.DF_LABEL_MISMATCH)

            elif isinstance(df_index_label, list):
                for index_label in df_index_label:
                    if index_label.lower() not in df_column_list:
                        raise TeradataMlException(Messages.get_message(MessageCodes.DF_LABEL_MISMATCH), MessageCodes.DF_LABEL_MISMATCH)

        try:
            pandas_df = None

            # Un-executed - Generate/Execute Nodes & Set Table Name
            if self._nodeid:
                self.__execute_node_and_set_table_name(self._nodeid, self._metaexpr)
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TO_PANDAS_FAILED),
                                          MessageCodes.TO_PANDAS_FAILED)

            pandas_df = df_utils._get_pandas_dataframe(self._table_name, index_column,
                                                       self._index_label, num_rows, self._orderby, all_rows)
            if pandas_df is not None:
                return pandas_df
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.DF_WITH_NO_COLUMNS),
                                          MessageCodes.DF_WITH_NO_COLUMNS)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TO_PANDAS_FAILED) + str(err),
                                      MessageCodes.TO_PANDAS_FAILED) from err

    def join(self, other, on=None, how="left", lsuffix=None, rsuffix=None):
        """
        DESCRIPTION:
            Joins two different teradataml DataFrames together based on column comparisons
            specified in argument 'on' and type of join is specified in the argument 'how'.
            Supported join operations are:
            • Inner join: Returns only matching rows, non matching rows are eliminated.
            • Left outer join: Returns all matching rows plus non matching rows from the left table.
            • Right outer join: Returns all matching rows plus non matching rows from the right table.
            • Full outer join: Returns all rows from both tables, including non matching rows.
            • Cross join: Returns all rows from both tables where each row from the first table
                          is joined with each row from the second table. The result of the join
                          is a cartesian cross product.
                          Note: For a cross join, the 'on' argument is ignored.
            Supported join operators are =, ==, <, <=, >, >=, <> and != (= and <> operators are
            not supported when using DataFrame columns as operands).

            Note:
                1.  When multiple join conditions are given, they are joined using AND boolean
                    operator. Other boolean operators are not supported.
                2.  Nesting of join on conditions in column expressions using & and | is not
                    supported. The example for unsupported nested join on conditions is:
                    on = [(df1.a == df1.b) & (df1.c == df1.d)]

                    One can use [df1.a == df1.b, df1.c == df1.d] in place of
                    [(df1.a == df1.b) & (df1.c == df1.d)].

        PARAMETERS:

            other:
                Required Argument.
                Specifies right teradataml DataFrame on which join is to be performed.
                Types: teradataml DataFrame

            on:
                Optional argument when "how" is "cross", otherwise required.
                If specified when "how" is "cross", it is ignored.
                Specifies list of conditions that indicate the columns to be join keys.

                It can take the following forms:
                • String comparisons, in the form of "col1 <= col2", where col1 is
                  the column of left dataframe df1 and col2 is the column of right
                  dataframe df2.
                  Examples:
                    1. ["a","b"] indicates df1.a = df2.a and df1.b = df2.b.
                    2. ["a = b", "c == d"] indicates df1.a = df2.b and df1.c = df2.d.
                    3. ["a <= b", "c > d"] indicates df1.a <= df2.b and df1.c > df2.d.
                    4. ["a < b", "c >= d"] indicates df1.a < df2.b and df1.c >= df2.d.
                    5. ["a <> b"] indicates df1.a != df2.b. Same is the case for ["a != b"].
                • Column comparisons, in the form of df1.col1 <= df2.col2, where col1
                  is the column of left dataframe df1 and col2 is the column of right
                  dataframe df2.
                  Examples:
                    1. [df1.a == df2.a, df1.b == df2.b] indicates df1.a = df2.a and df1.b = df2.b.
                    2. [df1.a == df2.b, df1.c == df2.d] indicates df1.a = df2.b and df1.c = df2.d.
                    3. [df1.a <= df2.b and df1.c > df2.d] indicates df1.a <= df2.b and df1.c > df2.d.
                    4. [df1.a < df2.b and df1.c >= df2.d] indicates df1.a < df2.b and df1.c >= df2.d.
                    5. df1.a != df2.b indicates df1.a != df2.b.
                • The combination of both string comparisons and comparisons as column expressions.
                  Examples:
                    1. ["a", df1.b == df2.b] indicates df1.a = df2.a and df1.b = df2.b.
                    2. [df1.a <= df2.b, "c > d"] indicates df1.a <= df2.b and df1.c > df2.d.

                Types: str (or) ColumnExpression (or) List of strings(str) or ColumnExpressions

            how:
                Optional Argument.
                Specifies the type of join to perform.
                Default value is "left".
                Permitted Values : "inner", "left", "right", "full" and "cross"
                Types: str

            lsuffix:
                Optional Argument.
                Specifies the suffix to be added to the left table columns.
                Default Value: None.
                Types: str

            rsuffix:
                Optional Argument.
                Specifies the suffix to be added to the right table columns.
                Default Value: None.
                Types: str

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Load the data to run the example.
            >>> from teradataml import load_example_data
            >>> load_example_data("dataframe", ["join_table1", "join_table2"])
            >>> load_example_data("glm", "admissions_train") # used in cross join

            >>> df1 = DataFrame("join_table1")
            >>> df2 = DataFrame("join_table2")

            # Print dataframe.
            >>> df1
                       col2  col3 col5
            col1
            2     analytics   2.3    b
            1      teradata   1.3    a
            3      platform   3.3    c

            # Print dataframe.
            >>> df2
                       col4  col3 col7
            col1
            2     analytics   2.3    b
            1      teradata   1.3    a
            3       are you   4.3    d

            # Both on conditions as strings.
            >>> df1.join(other = df2, on = ["col2=col4", "col1"], how = "inner", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4 col7
            0       2       2  analytics      2.3      2.3    b  analytics    b
            1       1       1   teradata      1.3      1.3    a   teradata    a

            # One on condition is ColumnExpression and other is string having two columns with left
            # outer join.
            >>> df1.join(df2, on = [df1.col2 == df2.col4,"col5 = col7"], how = "left", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4  col7
            0       3    None   platform      3.3      NaN    c       None  None
            1       2       2  analytics      2.3      2.3    b  analytics     b
            2       1       1   teradata      1.3      1.3    a   teradata     a

            # One on condition is ColumnExpression and other is string having only one column.
            >>> df1.join(other = df2, on = [df1.col2 == df2.col4,"col3"], how = "inner", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4 col7
            0       2       2  analytics      2.3      2.3    b  analytics    b
            1       1       1   teradata      1.3      1.3    a   teradata    a

            # One on condition is ColumnExpression and other is string having two columns with
            # full join.
            >>> df1.join(other = df2, on = ["col2=col4",df1.col5 == df2.col7], how = "full", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3  col5       col4  col7
            0       3    None   platform      3.3      NaN     c       None  None
            1    None       3       None      NaN      4.3  None    are you     d
            2       1       1   teradata      1.3      1.3     a   teradata     a
            3       2       2  analytics      2.3      2.3     b  analytics     b

            # Using not equal operation in ColumnExpression condition.
            >>> df1.join(other = df2, on = ["col5==col7",df1.col2 != df2.col4], how = "full", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3  col5       col4  col7
            0       1    None   teradata      1.3      NaN     a       None  None
            1       2    None  analytics      2.3      NaN     b       None  None
            2    None       2       None      NaN      2.3  None  analytics     b
            3    None       1       None      NaN      1.3  None   teradata     a
            4       3    None   platform      3.3      NaN     c       None  None
            5    None       3       None      NaN      4.3  None    are you     d

            # Using only one string expression with <> operation.
            >>> df1.join(other = df2, on = "col2<>col4", how = "left", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4 col7
            0       2       3  analytics      2.3      4.3    b    are you    d
            1       2       1  analytics      2.3      1.3    b   teradata    a
            2       3       2   platform      3.3      2.3    c  analytics    b
            3       1       2   teradata      1.3      2.3    a  analytics    b
            4       3       1   platform      3.3      1.3    c   teradata    a
            5       1       3   teradata      1.3      4.3    a    are you    d
            6       3       3   platform      3.3      4.3    c    are you    d

            # Using only one ColumnExpression in on conditions.
            >>> df1.join(other = df2, on = df1.col5 != df2.col7, how = "full", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4 col7
            0       1       3   teradata      1.3      4.3    a    are you    d
            1       3       1   platform      3.3      1.3    c   teradata    a
            2       1       2   teradata      1.3      2.3    a  analytics    b
            3       3       2   platform      3.3      2.3    c  analytics    b
            4       2       1  analytics      2.3      1.3    b   teradata    a
            5       3       3   platform      3.3      4.3    c    are you    d
            6       2       3  analytics      2.3      4.3    b    are you    d

            # Both on conditions as ColumnExpressions.
            >>> df1.join(df2, on = [df1.col2 == df2.col4, df1.col5 > df2.col7], how = "right", lsuffix = "t1", rsuffix ="t2")
              t1_col1 t2_col1  col2 t1_col3  t2_col3  col5       col4 col7
            0    None       2  None    None      2.3  None  analytics    b
            1    None       1  None    None      1.3  None   teradata    a
            2    None       3  None    None      4.3  None    are you    d

            # cross join "admissions_train" with "admissions_train".
            >>> df1 = DataFrame("admissions_train").head(3).sort("id")
            >>> print(df1)
            masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1

            >>> df2 = DataFrame("admissions_train").head(3).sort("id")
            >>> print(df2)
            masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1

            >>> df3 = df1.join(other=df2, how="cross", lsuffix="l", rsuffix="r")
            >>> df3.set_index("l_id").sort("l_id")
                 l_programming   r_stats r_id  r_gpa r_programming  l_gpa   l_stats r_admitted l_admitted l_masters r_masters
            l_id
            1         Beginner    Novice    3   3.70      Beginner   3.95  Beginner          1          0       yes        no
            1         Beginner  Beginner    1   3.95      Beginner   3.95  Beginner          0          0       yes       yes
            1         Beginner  Beginner    2   3.76      Beginner   3.95  Beginner          0          0       yes       yes
            2         Beginner  Beginner    1   3.95      Beginner   3.76  Beginner          0          0       yes       yes
            2         Beginner  Beginner    2   3.76      Beginner   3.76  Beginner          0          0       yes       yes
            2         Beginner    Novice    3   3.70      Beginner   3.76  Beginner          1          0       yes        no
            3         Beginner  Beginner    1   3.95      Beginner   3.70    Novice          0          1        no       yes
            3         Beginner  Beginner    2   3.76      Beginner   3.70    Novice          0          1        no       yes
            3         Beginner    Novice    3   3.70      Beginner   3.70    Novice          1          1        no        no
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["other", other, False, (DataFrame)])
        awu_matrix.append(["on", on, True, (str, ColumnExpression, list)])
        awu_matrix.append(["how", how, True, (str), False, TeradataConstants.TERADATA_JOINS.value])
        awu_matrix.append(["lsuffix", lsuffix, True, (str), True])
        awu_matrix.append(["rsuffix", rsuffix, True, (str), True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        how_lc = how.lower()

        if on is None and how_lc != "cross":
            raise TeradataMlException(
                Messages.get_message(MessageCodes.MISSING_ARGS, "on"),
                MessageCodes.MISSING_ARGS)

        # Get the lowercase column names for the DataFrames involved in the operation.
        self_columns_lower_actual_map = {}
        other_columns_lower_actual_map = {}
        for col in self.columns:
            self_columns_lower_actual_map[col.lower()] = col

        for col in other.columns:
            other_columns_lower_actual_map[col.lower()] = col

        for column in self_columns_lower_actual_map.keys():
            if column in other_columns_lower_actual_map.keys():
                if lsuffix is None or rsuffix is None:
                    raise TeradataMlException(
                        Messages.get_message(MessageCodes.TDMLDF_REQUIRED_TABLE_ALIAS),MessageCodes.TDMLDF_REQUIRED_TABLE_ALIAS)

        if lsuffix is None:
            lsuffix = "df1"

        if rsuffix is None:
            rsuffix = "df2"

        # Both suffix shuold not be equal to perform join
        if lsuffix == rsuffix:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_INVALID_TABLE_ALIAS, "'lsuffix' and 'rsuffix'"),
                MessageCodes.TDMLDF_INVALID_TABLE_ALIAS)

        if how_lc != "cross":
            if isinstance(on, str) or isinstance(on, ColumnExpression):
                on = [on]

            all_join_conditions = []
            invalid_join_conditions = []
            # Forming join condition
            for condition in on:
                ori_condition = condition

                if not isinstance(condition, (ColumnExpression, str)):
                    invalid_join_conditions.append(condition)
                    continue

                # Process only when the on condition is string or a ColumnExpression
                if isinstance(condition, ColumnExpression):
                    columns = condition.original_column_expr
                    condition = condition.compile()

                for op in TeradataConstants.TERADATA_JOIN_OPERATORS.value:
                    if op in condition:
                        conditional_separator = op
                        break
                else:
                    # If no join condition is mentioned, default is taken as equal.
                    # If on is ['a'], then it is equal to 'df1.a = df2.a'
                    columns = [condition, condition]
                    condition = "{0} = {0}".format(condition)
                    conditional_separator = "="

                if isinstance(ori_condition, str):
                    columns = [column.strip() for column in condition.split(sep=conditional_separator)
                            if len(column) > 0]

                if len(columns) != 2:
                    invalid_join_conditions.append(condition)
                else:
                    left_col = self.__add_alias_to_column(columns[0], self, lsuffix)
                    right_col = self.__add_alias_to_column(columns[1], other, rsuffix)
                    if conditional_separator == "!=":
                        # "!=" is python way of expressing 'not equal to'. "<>" is Teradata way of
                        # expressing 'not equal to'. Adding support for "!=".
                        conditional_separator = "<>"
                    all_join_conditions.append('{0} {1} {2}'.format(left_col, conditional_separator, right_col))

            if len(invalid_join_conditions) > 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_JOIN_CONDITION,
                            ", ".join(invalid_join_conditions)), MessageCodes.TDMLDF_INVALID_JOIN_CONDITION)

            join_condition = " and ".join(all_join_conditions)
        else:
            join_condition = ""

        df1_columns_types = df_utils._get_required_columns_types_from_metaexpr(self._metaexpr)
        df2_columns_types = df_utils._get_required_columns_types_from_metaexpr(other._metaexpr)

        select_columns = []
        new_metaexpr_columns_types = OrderedDict()

        for column in self.columns:
            if df_utils._check_column_exists(column.lower(), other_columns_lower_actual_map.keys()):
                # Check if column found in other DataFrame has same case or different.
                # Return the column name from the other DataFrame.
                other_column = other_columns_lower_actual_map[column.lower()]

                df1_column_with_suffix = self.__check_and_return_new_column_name(lsuffix, other_column,
                                                                                 other_columns_lower_actual_map.keys(),
                                                                                 "right")
                select_columns.append("{0} as {1}".format(self.__add_suffix(other_column, lsuffix),
                                                          df1_column_with_suffix))

                df2_column_with_suffix = self.__check_and_return_new_column_name(rsuffix, column,
                                                                                 self_columns_lower_actual_map.keys(),
                                                                                 "left")
                select_columns.append("{0} as {1}".format(self.__add_suffix(column, rsuffix),
                                                          df2_column_with_suffix))

                # As we are creating new column name, adding it to new metadata dict for new dataframe from join
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                                    UtilFuncs._teradata_unquote_arg(df1_column_with_suffix, "\""),
                                                    column, df1_columns_types)

                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                                    UtilFuncs._teradata_unquote_arg(df2_column_with_suffix, "\""),
                                                    other_column, df2_columns_types)
            else:
                # As column not present in right DataFrame, directly adding column to new metadata dict.
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types, column, column, df1_columns_types)
                select_columns.append(UtilFuncs._teradata_quote_arg(column, "\"", False))

        for column in other.columns:
            if not df_utils._check_column_exists(column.lower(), self_columns_lower_actual_map.keys()):
                # As column not present in left DataFrame, directly adding column to new metadata dict.
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types, column, column, df2_columns_types)
                select_columns.append(UtilFuncs._teradata_quote_arg(column, "\"", False))

        # Create a node in AED using _aed_join
        join_node_id = self._aed_utils._aed_join(self._nodeid, other._nodeid, ", ".join(select_columns), how_lc,
                                                 join_condition, lsuffix, rsuffix)

        # Constructing new Metadata (_metaexpr) without DB; using dummy select_nodeid and underlying table name.
        new_metaexpr = UtilFuncs._get_metaexpr_using_columns(join_node_id, new_metaexpr_columns_types.items())

        return DataFrame._from_node(join_node_id, new_metaexpr, self._index_label)

    def __add_alias_to_column(self, column, df, alias):
        """
        This function check column exists in list of columns, if exists add suffix to column and
        adds to join columns list.

        PARAMETERS:
            column  - Column name.
            df - DataFrame to look into for columns.
            alias - alias to be added to column.

        EXAMPLES:
            df1 = DataFrame("table1")
            df2 = DataFrame("table2")
            __add_alias_to_column("a", df1, "t1")

        RAISES:
            ValueError - If column not found in DataFrame
        """
        # Checking each element in passed columns to be valid column in dataframe
        column_name = column
        if isinstance(column, ColumnExpression):
            column_name = column.name
        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(column_name, df._metaexpr, True)

        return self.__add_suffix(column, alias)

    def __add_suffix(self, column, alias):
        """
        Adds alias to column

        PARAMETERS:
            column  - Column name.
            alias - alias to be appended to column.

        EXAMPLES:
            __add_suffix("a", "t1")

        RAISES:
            None
        """
        # Process only when the column is ColumneExpression
        if isinstance(column, ColumnExpression):
            column_name = column.name
            column = column.compile()
            if column_name != column:
                # Process it only when the ColumnExpression has a label.
                # E.g. if df.id.label(..) then column is "label(id as ..)" and column_name is "id".
                return column.replace("(" + column_name, "({0}.{1}".format(
                    UtilFuncs._teradata_quote_arg(alias, "\"", False),
                    UtilFuncs._teradata_quote_arg(column_name, "\"", False)))

        return "{0}.{1}".format(UtilFuncs._teradata_quote_arg(alias, "\"", False),
                                UtilFuncs._teradata_quote_arg(column, "\"", False))

    def __check_and_return_new_column_name(self, suffix, column, col_list, df_side):
        """
         Check new column name alias with column exists in col_list or not, if exists throws exception else
         returns new column name.

         PARAMETERS:
             suffix  - alias to be added to column.
             column - column name.
             col_list - list of columns to check in which new column is exists or not.
             df_side - Side of the dataframe.

         EXAMPLES:
             df = DataFrame("t1")
             __check_and_return_new_column_name("df1", "column_name", df.columns, "right")

         RAISES:
             None
         """
        df1_column_with_suffix = "{0}_{1}".format(suffix,
                                                  UtilFuncs._teradata_unquote_arg(column, "\""))
        if df_utils._check_column_exists(df1_column_with_suffix.lower(), col_list):
            if df_side == "right":
                suffix_side = "lsuffix"
            else:
                suffix_side = "rsuffix"
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_COLUMN_ALREADY_EXISTS, df1_column_with_suffix, df_side,
                                     suffix_side),
                MessageCodes.TDMLDF_COLUMN_ALREADY_EXISTS)
        return UtilFuncs._teradata_quote_arg(df1_column_with_suffix, "\"", False)

    def __add_column_type_item_to_dict(self, new_metadata_dict, new_column,column, column_types):
        """
        Add a column as key and datatype as a value to dictionary

        PARAMETERS:
            new_metadata_dict  - Dictionary to which new item to be added.
            new_column - key fo new item.
            column - column to which datatype to be get.
            column_types - datatypes of the columns.
        EXAMPLES:
            __add_to_column_types_dict( metadata_dict, "col1","integer")

        RAISES:
            None
        """
        try:
            new_metadata_dict[new_column] = column_types[column]
        except KeyError:
            try:
                new_metadata_dict[new_column] = column_types[UtilFuncs._teradata_quote_arg(column, "\"", False)]
            except KeyError:
                new_metadata_dict[new_column] = column_types[UtilFuncs._teradata_unquote_arg(column, "\"")]

    def __get_sorted_list(self, colnames_list, ascending, kind):
        """
        Private method to return sorted list with different algoritms in either ascending or decending order.
        
        PARAMETERS:
            colnames_list - List of values to be sorted
            ascending - Specifies a flag to sort columns in either ascending (True) or descending (False).
            kind - Type of sorting algorithm to be applied upon.            
        
        EXAMPLES:
            __get_sorted_list(colnames_list, False, 'mergesort')
            
        RAISES:
            None
            
        RETURNS:
            Sorted list of column names
        """
        if kind == 'quicksort':
            less = []
            equal = []
            greater = []
            if len(colnames_list) > 1:
                pivot = colnames_list[0]
                for col in colnames_list:
                    if col < pivot:
                        less.append(col)
                    elif col == pivot:
                        equal.append(col)
                    else:
                        greater.append(col)
                greater = self.__get_sorted_list(greater, ascending=ascending, kind=kind)
                less = self.__get_sorted_list(less, ascending=ascending, kind=kind)
                if ascending:
                    final = less + equal + greater
                else:
                    final = greater + equal + less
                return final
            else:
                return colnames_list
            
        elif kind == 'mergesort':
            if ascending == True:
                return sorted(colnames_list)
            else:
                return sorted(colnames_list, reverse=True)     
            
        elif kind == 'heapsort':
            end = len(colnames_list)  
            start = end // 2 - 1
            for i in range(start, -1, -1):   
                self.__get_heap(colnames_list, end, i)   
            for i in range(end-1, 0, -1):  
                #swap(i, 0)  
                colnames_list[i], colnames_list[0] = colnames_list[0], colnames_list[i]
                colnames_list = self.__get_heap(colnames_list, i, 0)
            if ascending == True:
                return colnames_list
            else:
                return colnames_list[::-1]

    def __get_heap(self, colnames_list, n, i):
        """
        Private method to make a subtree rooted at index i.
        
        PARAMETERS:
            colnames_list - List of values for which heap is to be created.
            n - Size of the heap.
            i - Index to be taken as a root.
            
        EXAMPLES:
            __get_heap(colnames_list, 5, 3)
            
        RAISES:
            None
            
        RETURNS:
            Sorted list of column names indexed at i
        """
        l=2 * i + 1
        r=2 * (i + 1) 
        max=i
        if l < n and colnames_list[i] < colnames_list[l]:
            max = l
        if r < n and colnames_list[max] < colnames_list[r]:
            max = r
        if max != i:
            colnames_list[i], colnames_list[max] = colnames_list[max], colnames_list[i]
            self.__get_heap(colnames_list, n, max)
        return colnames_list

    def to_sql(self, table_name, if_exists='fail', primary_index=None, temporary=False, schema_name=None, types = None,
               primary_time_index_name=None, timecode_column=None, timebucket_duration=None,
               timezero_date=None, columns_list=None, sequence_column=None, seq_max=None, set_table=False):
        """
        DESCRIPTION:
            Writes records stored in a teradataml DataFrame to Teradata Vantage.

        PARAMETERS:

            table_name:
                Required Argument.
                Specifies the name of the table to be created in Teradata Vantage.
                Types: str

            schema_name:
                Optional Argument.
                Specifies the name of the SQL schema in Teradata Vantage to write to.
                Default Value: None (Use default Teradata Vantage schema).
                Types: str

                Note: schema_name will be ignored when temporary=True.

            if_exists:
                Optional Argument.
                Specifies the action to take when table already exists in Teradata Vantage.
                Default Value: 'fail'
                Permitted Values: 'fail', 'replace', 'append'
                    - fail: If table exists, do nothing.
                    - replace: If table exists, drop it, recreate it, and insert data.
                    - append: If table exists, insert data. Create if does not exist.
                Types: str

                Note: Replacing a table with the contents of a teradataml DataFrame based on
                      the same underlying table is not supported.

            primary_index:
                Optional Argument.
                Creates Teradata Table(s) with Primary index column(s) when specified.
                When None, No Primary Index Teradata tables are created.
                Default Value: None
                Types: str or List of Strings (str)
                    Example:
                        primary_index = 'my_primary_index'
                        primary_index = ['my_primary_index1', 'my_primary_index2', 'my_primary_index3']

            temporary:
                Optional Argument.
                Creates Teradata SQL tables as permanent or volatile.
                When True,
                1. volatile tables are created, and
                2. schema_name is ignored.
                When False, permanent tables are created.
                Default Value: False
                Types: boolean
                
            types:
                Optional Argument.
                Specifies required data-types for requested columns to be saved in Vantage.
                Types: Python dictionary ({column_name1: type_value1, ... column_nameN: type_valueN})
                Default: None

                Note:
                    1. This argument accepts a dictionary of columns names and their required teradatasqlalchemy types
                       as key-value pairs, allowing to specify a subset of the columns of a specific type.
                       When only a subset of all columns are provided, the column types for the rest are retained.
                       When types argument is not provided, the column types are retained.
                    2. This argument does not have any effect when the table specified using table_name and schema_name
                       exists and if_exists = 'append'.

            primary_time_index_name:
                Optional Argument.
                Specifies a name for the Primary Time Index (PTI) when the table
                to be created must be a PTI table.
                Types: String

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            timecode_column:
                Optional Argument.
                Required when the DataFrame must be saved as a PTI table.
                Specifies the column in the DataFrame that reflects the form
                of the timestamp data in the time series.
                This column will be the TD_TIMECODE column in the table created.
                It should be of SQL type TIMESTAMP(n), TIMESTAMP(n) WITH TIMEZONE, or DATE,
                corresponding to Python types datetime.datetime or datetime.date.
                Types: String

                Note: When you specify this parameter, an attempt to create a PTI table
                      will be made. This argument is not required when the table to be created
                      is not a PTI table. If this argument is specified, primary_index will be ignored.

            timezero_date:
                Optional Argument.
                Used when the DataFrame must be saved as a PTI table.
                Specifies the earliest time series data that the PTI table will accept;
                a date that precedes the earliest date in the time series data.
                Value specified must be of the following format: DATE 'YYYY-MM-DD'
                Default Value: DATE '1970-01-01'.
                Types: String

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            timebucket_duration:
                Optional Argument.
                Required if columns_list is not specified or is None.
                Used when the DataFrame must be saved as a PTI table.
                Specifies a duration that serves to break up the time continuum in
                the time series data into discrete groups or buckets.
                Specified using the formal form time_unit(n), where n is a positive
                integer, and time_unit can be any of the following:
                CAL_YEARS, CAL_MONTHS, CAL_DAYS, WEEKS, DAYS, HOURS, MINUTES,
                SECONDS, MILLISECONDS, or MICROSECONDS.
                Types:  String

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            columns_list:
                Optional Argument.
                Required if timebucket_duration is not specified.
                Used when the DataFrame must be saved as a PTI table.
                Specifies a list of one or more PTI table column names.
                Types: String or list of Strings

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            sequence_column:
                Optional Argument.
                Used when the DataFrame must be saved as a PTI table.
                Specifies the column of type Integer containing the unique identifier for
                time series data readings when they are not unique in time.
                * When specified, implies SEQUENCED, meaning more than one reading from the same
                  sensor may have the same timestamp.
                  This column will be the TD_SEQNO column in the table created.
                * When not specified, implies NONSEQUENCED, meaning there is only one sensor reading
                  per timestamp.
                  This is the default.
                Types: str

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            seq_max:
                Optional Argument.
                Used when the DataFrame must be saved as a PTI table.
                Specifies the maximum number of sensor data rows that can have the
                same timestamp. Can be used when 'sequenced' is True.
                Accepted range:  1 - 2147483647.
                Default Value: 20000.
                Types: int

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            set_table:
                Optional Argument.
                Specifies a flag to determine whether to create a SET or a MULTISET table.
                When True, a SET table is created.
                When False, a MULTISET table is created.
                Default value: False
                Types: boolean

                Note: 1. Specifying set_table=True also requires specifying primary_index or timecode_column.
                      2. Creating SET table (set_table=True) may result in loss of duplicate rows.
                      3. This argument has no effect if the table already exists and if_exists='append'.

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df2 = df[(df.gpa == 4.00)]
            >>> df2.to_sql('to_sql_example', primary_index='id')
            >>> df3 = DataFrame('to_sql_example')
            >>> df3
               masters  gpa     stats programming admitted
            id
            13      no  4.0  Advanced      Novice        1
            29     yes  4.0    Novice    Beginner        0
            15     yes  4.0  Advanced    Advanced        1
            >>>
            >>> # Save as PTI table making sure it is a SET table
            >>> load_example_data("sessionize", "sessionize_table")
            >>> df4 = DataFrame('sessionize_table')
            >>> df4.to_sql("test_copyto_pti",
                           timecode_column='clicktime',
                           columns_list='event',
                           set_table=True
                          )
            >>> df5 = DataFrame('test_copyto_pti')
            >>> df5
                                    TD_TIMECODE partition_id adid productid
            event
            click    2009-07-04 09:18:17.000000         1231    1      1001
            click    2009-07-24 04:18:10.000000         1167    2      1001
            click    2009-08-08 02:18:12.000000         9231    3      1001
            click    2009-08-11 00:01:24.000000         9231    3      1001
            page_02  2009-08-22 04:20:05.000000         1039    5      1001
            page_02  2009-08-27 23:03:05.000000         1039    5      1001
            view     2009-02-09 15:17:59.000000         1263    4      1001
            view     2009-03-09 21:17:59.000000         1199    2      1001
            view     2009-03-13 17:17:59.000000         1071    4      1001
            view     2009-03-19 01:17:59.000000         1199    1      1001

        """

        return copy_to_sql(df = self, table_name = table_name, schema_name = schema_name,
                    index = False, index_label = None, temporary = temporary,
                    primary_index = primary_index, if_exists = if_exists, types = types,
                    primary_time_index_name = primary_time_index_name, timecode_column = timecode_column,
                    timebucket_duration = timebucket_duration, timezero_date = timezero_date, columns_list = columns_list,
                    sequence_column = sequence_column, seq_max = seq_max, set_table = set_table)


    def _get_assign_allowed_types(self):
        """
        DESCRIPTION:
            Get allowed types for DataFrame.assign() function.

        PARAMETERS:
            None.

        RETURNS:
            A tuple containing supported types for DataFrame.assign() operation.

        RAISES:
            None.

        EXAMPLES:
            allowed_types = self._get_assign_allowed_types()
        """
        return (type(None), int, float, str, decimal.Decimal, ColumnExpression, ClauseElement)

    def _generate_assign_metaexpr_aed_nodeid(self, drop_columns, **kwargs):
        """
        DESCRIPTION:
            Function generates the MetaExpression and AED nodeid for DataFrame.assign()
            function based on the inputs to the function.

        PARAMETERS:
            drop_columns:
                Required Argument.
                If True, drop columns that are not specified in assign.
                Default Value: False
                Types: bool

            kwargs:
                keyword, value pairs
                - keywords are the column names.
                - values can be:
                    * Column arithmetic expressions.
                    * int/float/string literals.
                    * DataFrameColumn a.k.a. ColumnExpression Functions.
                      (Visit DataFrameColumn Functions in Function reference guide for more
                      details)
                    * SQLAlchemy ClauseElements.
                      (Visit teradataml extension with SQLAlchemy in teradataml User Guide
                       and Function reference guide for more details)

        RETURNS:
            A tuple containing new MetaExpression and AED nodeid for the operation.

        RAISES:
            None.

        EXAMPLES:
            (new_meta, new_nodeid) = self._generate_assign_metaexpr_aed_nodeid(drop_columns, **kwargs)
        """
        # Apply the assign expression.
        (new_meta, result) = self._metaexpr._assign(drop_columns, **kwargs)

        # Join the expressions in result.
        assign_expression = ', '.join(list(map(lambda x: x[1], result)))
        new_nodeid = self._aed_utils._aed_assign(self._nodeid,
                                                 assign_expression,
                                                 AEDConstants.AED_ASSIGN_DROP_EXISITING_COLUMNS.value)

        # Regenerate the metaexpression with the new table name.
        new_meta = UtilFuncs._get_metaexpr_using_parent_metaexpr(new_nodeid, new_meta)
        return (new_meta, new_nodeid)

    def __assign_conditional_node_execution(self, val):
        """
        DESCRIPTION:
            Internal function for DataFrame.assign() to execute the node, if
            following conditions are satisfied:
                1. If 'kwargs' accept value(s) of SQLAlchemy ClauseElement type AND
                2. ClauseElement represents a function whoes output type depends on
                   the input argument of the function.

        PARAMETER:
            val:
                Required Argument.
                Specifies a ColumnExpression.
                Types: SQLAlchemy ClauseElement

        RETURNS:
            True, if node is executed.

        RAISES:
            None.

        EXAMPLES:
            self.__assign_conditional_node_execution(val)
        """
        # If user has requested to execute a function using SQLAlchemy, we must
        # execute the node, if it is not already.
        # We should execute it only when a specific functions are being called.
        if isinstance(val, ClauseElement):
            import sqlalchemy as sqlalc
            function_name = None
            try:
                if isinstance(val, sqlalc.sql.elements.Over):
                    # If expression is of type Over, i.e., window aggregate then we should
                    # check it's element to get the function name.
                    function_name = val.element.name.upper()
                else:
                    # Get the function name.
                    function_name = val.name.upper()
            except:
                pass

            from teradataml.dataframe.vantage_function_types import VANTAGE_FUNCTION_ARGTYPE_DEPENDENT_MAPPER
            if function_name is None or function_name in VANTAGE_FUNCTION_ARGTYPE_DEPENDENT_MAPPER:
                self.__execute_node_and_set_table_name(self._nodeid)
                return True

    def assign(self, drop_columns = False, **kwargs):
        """
        DESCRIPTION:
            Assign new columns to a teradataml DataFrame.

        PARAMETERS:
            drop_columns:
                Optional Argument.
                If True, drop columns that are not specified in assign.
                Note:
                    When DataFrame.assign() is run on DataFrame.groupby(), this argument
                    is ignored. In such cases, all columns are dropped and only new columns
                    and grouping columns are returned.
                Default Value: False
                Types: bool

            kwargs:
                keyword, value pairs
                - keywords are the column names.
                - values can be:
                    * Column arithmetic expressions.
                    * int/float/string literals.
                    * DataFrameColumn a.k.a. ColumnExpression Functions.
                      (Visit DataFrameColumn Functions in Function reference guide for more
                       details)
                    * SQLAlchemy ClauseElements.
                      (Visit teradataml extension with SQLAlchemy in teradataml User Guide
                       and Function reference guide for more details)


        RETURNS:
            teradataml DataFrame
            Columns of a new DataFrame are decided based on following factors:
            A new DataFrame is returned with:
                1. New columns in addition to all the existing columns if "drop_columns" is False.
                2. Only new columns if "drop_columns" is True.
                3. New columns in addition to group by columns, i.e., columns used for grouping,
                   if assign() is run on DataFrame.groupby().

        NOTES:
             1. The values in kwargs cannot be callable (functions).
             2. The original DataFrame is not modified.
             3. Since ``kwargs`` is a dictionary, the order of your
               arguments may not be preserved. To make things predictable,
               the columns are inserted in alphabetical order, after the existing columns
               in the DataFrame. Assigning multiple columns within the same ``assign`` is
               possible, but you cannot reference other columns created within the same
               ``assign`` call.
             4. The maximum number of columns that a DataFrame can have is 2048.
             5. With DataFrame.groupby(), only aggregate functions and literal values
               are advised to use. Other functions, such as string functions, can also be
               used, but the column used in such function must be a part of group by columns.
               See - Examples for teradataml extension with SQLAlchemy on using various
                     functions with DataFrame.assign().

        RAISES:
             1. ValueError - When a callable is passed as a value, or columns from different
                             DataFrames are passed as values in kwargs.
             2. TeradataMlException - When the return DataFrame initialization fails, or
                                      invalid argument types are passed.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> c1 = df.gpa
            >>> c2 = df.id
            >>>

            #
            # Executing assign() with Arithmetic operations on columns.
            # All below examples use columns "gpa" and "id" for
            # arithmetic operations to create a new DataFrame including the new columns.
            #
            # Let's take a look at various operations that can be performed
            # using assign() and arithmetic operations on columns.

            # Example 1: Addition of two columns "gpa" and "id".
            >>> df.assign(new_column = c1 + c2).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0        4.95
            2      yes  3.76  Beginner    Beginner        0        5.76
            3       no  3.70    Novice    Beginner        1        6.70
            4      yes  3.50  Beginner      Novice        1        7.50
            5       no  3.44    Novice      Novice        0        8.44
            6      yes  3.50  Beginner    Advanced        1        9.50
            7      yes  2.33    Novice      Novice        1        9.33
            8       no  3.60  Beginner    Advanced        1       11.60
            9       no  3.82  Advanced    Advanced        1       12.82
            10      no  3.71  Advanced    Advanced        1       13.71
            >>>

            # Example 2: Multiplication of columns "gpa" and "id".
            >>> df.assign(new_column = c1 * c2).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0        3.95
            2      yes  3.76  Beginner    Beginner        0        7.52
            3       no  3.70    Novice    Beginner        1       11.10
            4      yes  3.50  Beginner      Novice        1       14.00
            5       no  3.44    Novice      Novice        0       17.20
            6      yes  3.50  Beginner    Advanced        1       21.00
            7      yes  2.33    Novice      Novice        1       16.31
            8       no  3.60  Beginner    Advanced        1       28.80
            9       no  3.82  Advanced    Advanced        1       34.38
            10      no  3.71  Advanced    Advanced        1       37.10
            >>>

            # Example 3: Division of columns. Divide "id" by "gpa".
            >>> df.assign(new_column = c2 / c1).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0    0.253165
            2      yes  3.76  Beginner    Beginner        0    0.531915
            3       no  3.70    Novice    Beginner        1    0.810811
            4      yes  3.50  Beginner      Novice        1    1.142857
            5       no  3.44    Novice      Novice        0    1.453488
            6      yes  3.50  Beginner    Advanced        1    1.714286
            7      yes  2.33    Novice      Novice        1    3.004292
            8       no  3.60  Beginner    Advanced        1    2.222222
            9       no  3.82  Advanced    Advanced        1    2.356021
            10      no  3.71  Advanced    Advanced        1    2.695418
            >>>

            # Example 4: Subtract values in column "id" from "gpa".
            >>> df.assign(new_column = c1 - c2).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0        2.95
            2      yes  3.76  Beginner    Beginner        0        1.76
            3       no  3.70    Novice    Beginner        1        0.70
            4      yes  3.50  Beginner      Novice        1       -0.50
            5       no  3.44    Novice      Novice        0       -1.56
            6      yes  3.50  Beginner    Advanced        1       -2.50
            7      yes  2.33    Novice      Novice        1       -4.67
            8       no  3.60  Beginner    Advanced        1       -4.40
            9       no  3.82  Advanced    Advanced        1       -5.18
            10      no  3.71  Advanced    Advanced        1       -6.29

            # Example 5: Modulo division of values in column "id" and "gpa".
            >>> df.assign(new_column = c2 % c1).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0        1.00
            2      yes  3.76  Beginner    Beginner        0        2.00
            3       no  3.70    Novice    Beginner        1        3.00
            4      yes  3.50  Beginner      Novice        1        0.50
            5       no  3.44    Novice      Novice        0        1.56
            6      yes  3.50  Beginner    Advanced        1        2.50
            7      yes  2.33    Novice      Novice        1        0.01
            8       no  3.60  Beginner    Advanced        1        0.80
            9       no  3.82  Advanced    Advanced        1        1.36
            10      no  3.71  Advanced    Advanced        1        2.58
            >>>

            #
            # Executing assign() with literal values.
            #
            # Example 6: Adding an integer literal value to the values of columns "gpa" and "id".
            >>> df.assign(c3 = c1 + 1, c4 = c2 + 1).sort("id")
               masters   gpa     stats programming admitted    c3  c4
            id
            1      yes  3.95  Beginner    Beginner        0  4.95   2
            2      yes  3.76  Beginner    Beginner        0  4.76   3
            3       no  3.70    Novice    Beginner        1  4.70   4
            4      yes  3.50  Beginner      Novice        1  4.50   5
            5       no  3.44    Novice      Novice        0  4.44   6
            6      yes  3.50  Beginner    Advanced        1  4.50   7
            7      yes  2.33    Novice      Novice        1  3.33   8
            8       no  3.60  Beginner    Advanced        1  4.60   9
            9       no  3.82  Advanced    Advanced        1  4.82  10
            10      no  3.71  Advanced    Advanced        1  4.71  11
            >>>

            # Example 7: Create a new column with an integer literal value.
            >>> df.assign(c1 = 1).sort("id")
               masters   gpa     stats programming admitted c1
            id
            1      yes  3.95  Beginner    Beginner        0  1
            2      yes  3.76  Beginner    Beginner        0  1
            3       no  3.70    Novice    Beginner        1  1
            4      yes  3.50  Beginner      Novice        1  1
            5       no  3.44    Novice      Novice        0  1
            6      yes  3.50  Beginner    Advanced        1  1
            7      yes  2.33    Novice      Novice        1  1
            8       no  3.60  Beginner    Advanced        1  1
            9       no  3.82  Advanced    Advanced        1  1
            10      no  3.71  Advanced    Advanced        1  1
            >>>

            # Example 8: Create a new column with a string literal value.
            >>> df.assign(c3 = 'string').sort("id")
               masters   gpa     stats programming admitted      c3
            id
            1      yes  3.95  Beginner    Beginner        0  string
            2      yes  3.76  Beginner    Beginner        0  string
            3       no  3.70    Novice    Beginner        1  string
            4      yes  3.50  Beginner      Novice        1  string
            5       no  3.44    Novice      Novice        0  string
            6      yes  3.50  Beginner    Advanced        1  string
            7      yes  2.33    Novice      Novice        1  string
            8       no  3.60  Beginner    Advanced        1  string
            9       no  3.82  Advanced    Advanced        1  string
            10      no  3.71  Advanced    Advanced        1  string
            >>>

            # Example 9: Concatenation of strings, a string literal and value from
            #            "masters" column.
            #            '+' operator is overridden for string columns.
            >>> df.assign(concatenated = "Completed? " + df.masters).sort("id")
               masters   gpa     stats programming admitted    concatenated
            id
            1      yes  3.95  Beginner    Beginner        0  Completed? yes
            2      yes  3.76  Beginner    Beginner        0  Completed? yes
            3       no  3.70    Novice    Beginner        1   Completed? no
            4      yes  3.50  Beginner      Novice        1  Completed? yes
            5       no  3.44    Novice      Novice        0   Completed? no
            6      yes  3.50  Beginner    Advanced        1  Completed? yes
            7      yes  2.33    Novice      Novice        1  Completed? yes
            8       no  3.60  Beginner    Advanced        1   Completed? no
            9       no  3.82  Advanced    Advanced        1   Completed? no
            10      no  3.71  Advanced    Advanced        1   Completed? no
            >>>

            #
            # Significance of "drop_columns" in assign().
            # Setting drop_columns to True will only return assigned expressions.
            #
            # Example 10: Drop all column and return new assigned expressions.
            >>> df.assign(drop_columns = True,
            ...           addc = c1 + c2,
            ...           subc = c1 - c2,
            ...           mulc = c1 * c2,
            ...           divc = c1/c2).sort("addc")
                addc      divc   mulc  subc
            0   4.95  3.950000   3.95  2.95
            1   5.76  1.880000   7.52  1.76
            2   6.70  1.233333  11.10  0.70
            3   7.50  0.875000  14.00 -0.50
            4   8.44  0.688000  17.20 -1.56
            5   9.33  0.332857  16.31 -4.67
            6   9.50  0.583333  21.00 -2.50
            7  11.60  0.450000  28.80 -4.40
            8  12.82  0.424444  34.38 -5.18
            9  13.71  0.371000  37.10 -6.29
            >>>

            # Example 11: Duplicate a column with a new name.
            #             In the example here, we are duplicating:
            #               1. Column "id" to new column "c1".
            #               2. Column "gpa" to new column "c2".
            >>> df.assign(c1 = c2, c2 = c1).sort("id")
               masters   gpa     stats programming admitted  c1    c2
            id
            1      yes  3.95  Beginner    Beginner        0   1  3.95
            2      yes  3.76  Beginner    Beginner        0   2  3.76
            3       no  3.70    Novice    Beginner        1   3  3.70
            4      yes  3.50  Beginner      Novice        1   4  3.50
            5       no  3.44    Novice      Novice        0   5  3.44
            6      yes  3.50  Beginner    Advanced        1   6  3.50
            7      yes  2.33    Novice      Novice        1   7  2.33
            8       no  3.60  Beginner    Advanced        1   8  3.60
            9       no  3.82  Advanced    Advanced        1   9  3.82
            10      no  3.71  Advanced    Advanced        1  10  3.71
            >>>

            # Example 12: Renaming columns.
            #             Example 6 command can be modified a bit to rename columns, rather than
            #             duplicating it.
            #             Use "drop_column=True" in example 6 command to select all the desired columns.
            >>> df.assign(drop_columns=True, c1 = c2, c2 = c1,
            ...           masters=df.masters,
            ...           stats=df.stats,
            ...           programming=df.programming,
            ...           admitted=df.admitted).sort("c1")
              masters     stats programming  admitted  c1    c2
            0     yes  Beginner    Beginner         0   1  3.95
            1     yes  Beginner    Beginner         0   2  3.76
            2      no    Novice    Beginner         1   3  3.70
            3     yes  Beginner      Novice         1   4  3.50
            4      no    Novice      Novice         0   5  3.44
            5     yes  Beginner    Advanced         1   6  3.50
            6     yes    Novice      Novice         1   7  2.33
            7      no  Beginner    Advanced         1   8  3.60
            8      no  Advanced    Advanced         1   9  3.82
            9      no  Advanced    Advanced         1  10  3.71
            >>>

            #
            # Executing Aggregate Functions with assign() and DataFrame.groupby().
            #
            # Here, we will be using 'func' from sqlalchemy to run some aggregate functions.
            >>> from sqlalchemy import func
            >>>

            # Example 13: Calculate average "gpa" for values in the "stats" column.
            >>> df.groupby("stats").assign(res=func.ave(df.gpa.expression))
                  stats       res
            0  Beginner  3.662000
            1  Advanced  3.508750
            2    Novice  3.559091
            >>>

            # Example 14: Calculate standard deviation, kurtosis value and sum of values in
            #             the "gpa" column with values grouped by values in the "stats" column.
            #             Alternate approach for DataFrame.agg(). This allows user to name the
            #             result columns.
            >>> df.groupby("stats").assign(gpa_std_=func.ave(df.gpa.expression),
            ...                            gpa_kurtosis_=func.kurtosis(df.gpa.expression),
            ...                            gpa_sum_=func.sum(df.gpa.expression))
                  stats  gpa_kurtosis_  gpa_std_  gpa_sum_
            0  Beginner      -0.452859  3.662000     18.31
            1  Advanced       2.886226  3.508750     84.21
            2    Novice       6.377775  3.559091     39.15
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["drop_columns", drop_columns, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if len(kwargs) == 0:
            return self

        elif len(kwargs) >= TeradataConstants['TABLE_COLUMN_LIMIT'].value:
            errcode = MessageCodes.TD_MAX_COL_MESSAGE
            raise TeradataMlException(Messages.get_message(errcode), errcode)

        allowed_types = self._get_assign_allowed_types()

        node_executed = False
        for key, val in kwargs.items():

            if isinstance(val, ColumnExpression) and val.get_flag_has_multiple_dataframes():
                raise ValueError("Combining Columns from different dataframes is unsupported for "
                                 "assign operation.")

            is_allowed = lambda x: isinstance(*x) and type(x[0]) != bool
            value_type_allowed = map(is_allowed, ((val, t) for t in allowed_types))

            if callable(val):
                err = 'Unsupported callable value for key: {}'.format(key)
                raise ValueError(err)

            elif not any(list(value_type_allowed)):
                err = 'Unsupported values of type {t} for key {k}'.format(k = key, t = type(val))
                raise ValueError(err)

            if isinstance(val, ClauseElement) and not node_executed:
                # We should execute the node, if input kwargs contains a value, i.e.,
                # val of type ClauseElements and if such function needs a node in
                # executed state, i.e., underlying table/view must exist on the system.
                node_executed = self.__assign_conditional_node_execution(val)

        if self._metaexpr is None:
            msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
            raise TeradataMlException(msg, MessageCodes.TDMLDF_INFO_ERROR)

        try:
            (new_meta, new_nodeid) = self._generate_assign_metaexpr_aed_nodeid(drop_columns, **kwargs)
            return DataFrame._from_node(new_nodeid, new_meta, self._index_label)
        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
            raise TeradataMlException(msg, errcode) from err

    def get(self, key):
        """
        DESCRIPTION:
            Retrieve required columns from DataFrame using column name(s) as key.
            Returns a new teradataml DataFrame with requested columns only.

        PARAMETERS:

            key:
                Required Argument.
                Specifies column(s) to retrieve from the teradataml DataFrame.
                Types: str OR List of Strings (str)

            teradataml supports the following formats (only) for the "get" method:

            1] Single Column String: df.get("col1")
            2] Single Column List: df.get(["col1"])
            3] Multi-Column List: df.get(['col1', 'col2', 'col3'])
            4] Multi-Column List of List: df.get([["col1", "col2", "col3"]])

            Note: Multi-Column retrieval of the same column such as df.get(['col1', 'col1']) is not supported.

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df.sort('id')
               masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1
            4      yes  3.50  Beginner      Novice        1
            ...

            1] Single String Column
            >>> df.get("gpa")
                gpa
            0  3.46
            1  3.52
            2  3.68
            3  3.65
            ...

            2] Single Column List
            >>> df.get(["gpa"])
                gpa
            0  3.46
            1  3.52
            2  3.68
            3  3.65
            ...

            3] Multi-Column List
            >>> df.get(["programming", "masters", "gpa"])
              programming masters   gpa
            0    Beginner     yes  3.46
            1      Novice      no  3.52
            2    Beginner      no  3.68
            3      Novice      no  3.65
            ...

            4] Multi-Column List of List
            >>> df.get([['programming', 'masters', 'gpa']])
              programming masters   gpa
            0    Advanced     yes  4.00
            1    Advanced     yes  3.45
            2    Beginner     yes  3.50
            3    Beginner     yes  4.00
            ...

        """
        return self.select(key)

    def set_index(self, keys, drop = True, append = False):
        """
        DESCRIPTION:
            Assigns one or more existing columns as the new index to a teradataml DataFrame.

        PARAMETERS:

            keys:
                Required Argument.
                Specifies the column name or a list of column names to use as the DataFrame index.
                Types: str OR list of Strings (str)

            drop:
                Optional Argument.
                Specifies whether or not to display the column(s) being set as index as
                teradataml DataFrame columns anymore.
                When drop is True, columns are set as index and not displayed as columns.
                When drop is False, columns are set as index; but also displayed as columns.
                Note: When the drop argument is set to True, the column being set as index does not cease to
                      be a part of the underlying table upon which the teradataml DataFrame is based off.
                      A column that is dropped while being set as an index is merely not used for display
                      purposes anymore as a column of the teradataml DataFrame.
                Default Value: True
                Types: bool

            append:
                Optional Argument.
                Specifies whether or not to append requested columns to the existing index.
    `           When append is False, replaces existing index.
                When append is True, retains both existing & currently appended index.
                Default Value: False
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df.sort('id')
               masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1
            4      yes  3.50  Beginner      Novice        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            8       no  3.60  Beginner    Advanced        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1

            >>> # Set new index.
            >>> df.set_index('masters').sort('id')
                     id   gpa     stats programming admitted
            masters
            yes       1  3.95  Beginner    Beginner        0
            yes       2  3.76  Beginner    Beginner        0
            no        3  3.70    Novice    Beginner        1
            yes       4  3.50  Beginner      Novice        1
            no        5  3.44    Novice      Novice        0
            yes       6  3.50  Beginner    Advanced        1
            yes       7  2.33    Novice      Novice        1
            no        8  3.60  Beginner    Advanced        1
            no        9  3.82  Advanced    Advanced        1
            no       10  3.71  Advanced    Advanced        1

            >>> # Set multiple indexes using list of columns
            >>> df.set_index(['masters', 'id']).sort('id')
                         gpa     stats programming admitted
            id masters
            1  yes      3.95  Beginner    Beginner        0
            2  yes      3.76  Beginner    Beginner        0
            3  no       3.70    Novice    Beginner        1
            4  yes      3.50  Beginner      Novice        1
            5  no       3.44    Novice      Novice        0
            6  yes      3.50  Beginner    Advanced        1
            7  yes      2.33    Novice      Novice        1
            8  no       3.60  Beginner    Advanced        1
            9  no       3.82  Advanced    Advanced        1
            10 no       3.71  Advanced    Advanced        1

            >>> # Append to new index to the existing set of index.
            >>> df.set_index(['masters', 'id']).set_index('gpa', drop = False, append = True).sort('id')
                                stats programming admitted
            gpa  masters id
            3.95 yes     1   Beginner    Beginner        0
            3.76 yes     2   Beginner    Beginner        0
            3.70 no      3     Novice    Beginner        1
            3.50 yes     4   Beginner      Novice        1
            3.44 no      5     Novice      Novice        0
            3.50 yes     6   Beginner    Advanced        1
            2.33 yes     7     Novice      Novice        1
            3.60 no      8   Beginner    Advanced        1
            3.82 no      9   Advanced    Advanced        1
            3.71 no      10  Advanced    Advanced        1
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["keys", keys, False, (str, list), True])
        awu_matrix.append(["drop", drop, True, (bool)])
        awu_matrix.append(["append", append, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(keys, self._metaexpr)

        try:
            new_index_list = self._index_label if self._index_label is not None else []

            # Creating a list with requested index labels bases on append
            if append:
                if isinstance(keys, str):
                    new_index_list.append(keys)
                elif isinstance(keys, list):
                    new_index_list.extend(keys)
            else:
                if isinstance(keys, str):
                    new_index_list = [keys]
                elif isinstance(keys, list):
                    new_index_list = keys

            # Takes care of appending already existing index
            new_index_list = list(set(new_index_list))

            # In case requested index is same as existing index, return same DF
            if new_index_list == self._index_label:
                return self

            # Creating list of undropped columns for printing
            undropped_columns = []
            if not drop:
                if isinstance(keys, str):
                    undropped_columns = [keys]
                elif isinstance(keys, list):
                    undropped_columns = keys

            if len(undropped_columns) == 0:
                undropped_columns = None

            # Assigning self attributes to newly created dataframe.
            new_df = DataFrame._from_node(self._nodeid, self._metaexpr, new_index_list, undropped_columns)
            new_df._table_name = self._table_name
            new_df._index = self._index
            return new_df

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    @property
    def index(self):
        """
        DESCRIPTION:
            Returns the index_label for the teradataml DataFrame.

        RETURNS:
            str or List of Strings (str) representing the index_label of the DataFrame.

        RAISES:
            None

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            5       no  3.44    Novice      Novice         0
            3       no  3.70    Novice    Beginner         1
            1      yes  3.95  Beginner    Beginner         0
            20     yes  3.90  Advanced    Advanced         1
            8       no  3.60  Beginner    Advanced         1
            25      no  3.96  Advanced    Advanced         1
            18     yes  3.81  Advanced    Advanced         1
            24      no  1.87  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1

            >>> # Get the index_label
            >>> df.index
            ['id']

            >>> # Set new index_label
            >>> df = df.set_index(['id', 'masters'])
            >>> df
                         gpa     stats programming  admitted
            id masters
            5  no       3.44    Novice      Novice         0
            3  no       3.70    Novice    Beginner         1
            1  yes      3.95  Beginner    Beginner         0
            17 no       3.83  Advanced    Advanced         1
            13 no       4.00  Advanced      Novice         1
            32 yes      3.46  Advanced    Beginner         0
            11 no       3.13  Advanced    Advanced         1
            9  no       3.82  Advanced    Advanced         1
            34 yes      3.85  Advanced    Beginner         0
            24 no       1.87  Advanced      Novice         1

            >>> # Get the index_label
            >>> df.index
            ['id', 'masters']

        """
        return self._index_label

    def groupby(self, columns_expr):
        """
        DESCRIPTION:
            Apply GroupBy to one or more columns of a teradataml Dataframe
            The result will always behaves like calling groupby with as_index = False in pandas

        PARAMETERS:
            columns_expr:
                Required Argument.
                Specifies the column name(s) to group by.
                Types: str OR list of Strings (str)

        NOTES:
            1. Users can still apply teradataml DataFrame methods (filters/sort/etc) on top of the result.
            2. Consecutive operations of grouping, i.e., groupby_time(), resample() and groupby() are not permitted.
               An exception will be raised. Following are some cases where exception will be raised as
               "Invalid operation applied, check documentation for correct usage."
                    a. df.resample().groupby()
                    b. df.resample().resample()
                    c. df.resample().groupby_time()

        RETURNS:
            teradataml DataFrameGroupBy Object

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df1 = df.groupby(["masters"])
            >>> df1.min()
              masters min_id  min_gpa min_stats min_programming min_admitted
            0      no      3     1.87  Advanced        Advanced            0
            1     yes      1     1.98  Advanced        Advanced            0

        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["columns_expr", columns_expr, False, (str, list), True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(columns_expr, self._metaexpr)

        try:
            column_list=[]
            unsupported_types = ['BLOB', 'CLOB', 'PERIOD_DATE', 'PERIOD_TIME', 'PERIOD_TIMESTAMP', 'ARRAY', 'VARRAY', 'XML', 'JSON']
            type_expr=[]
            invalid_types = []
            # check for consecutive groupby operations
            if isinstance(self, DataFrameGroupBy) or isinstance(self, DataFrameGroupByTime) :
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_OPERATION), MessageCodes.UNSUPPORTED_OPERATION)

            if (isinstance(columns_expr, list)):
                column_list=columns_expr

            elif (isinstance(columns_expr, str)):
                column_list.append(columns_expr)

            # Checking each element in columns_expr to be valid column in dataframe
            for col in column_list:
                type_expr.append(self._metaexpr.t.c[col].type)

            # Convert types to string from sqlalchemy type
            columns_types = [repr(type_expr[i]).split("(")[0] for i in range(len(type_expr))]

            # Checking each element in passed columns_types to be valid a data type for groupby
            # and create a list of invalid_types
            for col_type in columns_types:
                if col_type in unsupported_types:
                    invalid_types.append(col_type)

            if len(invalid_types) > 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_types,
                                                               "ANY, except following {}".format(unsupported_types)),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            groupbyexpr = ', '.join(UtilFuncs._teradata_quote_arg(col, "\"", False) for col in column_list)
            groupbyObj = DataFrameGroupBy(self._nodeid, self._metaexpr, self._column_names_and_types, self.columns,
                                          groupbyexpr, column_list)
            return groupbyObj
        except TeradataMlException:
            raise

    def __group_time_series_data(self, timebucket_duration, timebucket_duration_arg_name = "timebucket_duration",
                                 value_expression = None, timecode_column = None,
                                 timecode_column_arg_name = "timecode_column", sequence_column = None,
                                 fill = None, fill_arg_name = "fill"):
        """
        DESCRIPTION:
            Internal function to resample/group time series data using Group By Time and a column.

        PARAMETERS:
            timebucket_duration:
                Required Argument.
                Specifies the duration of each timebucket for aggregation and is used to
                assign each potential timebucket a unique number.
                Permitted Values:
                     ===================================================================================================
                    | Time Units        | Formal Form       | Shorthand Equivalents for time_units                      |
                     ===================================================================================================
                    | Calendar Years    | CAL_YEARS(N)      | Ncy OR Ncyear OR Ncyears                                  |
                     ---------------------------------------------------------------------------------------------------
                    | Calendar Months   | CAL_MONTHS(N)     | Ncm OR Ncmonth OR Ncmonths                                |
                     ---------------------------------------------------------------------------------------------------
                    | Calendar Days     | CAL_DAYS(N)       | Ncd OR Ncday OR Ncdays                                    |
                     ---------------------------------------------------------------------------------------------------
                    | Weeks             | WEEKS(N)          | Nw  OR Nweek OR Nweeks                                    |
                     ---------------------------------------------------------------------------------------------------
                    | Days              | DAYS(N)           | Nd  OR Nday OR Ndays                                      |
                     ---------------------------------------------------------------------------------------------------
                    | Hours             | HOURS(N)          | Nh  OR Nhr OR Nhrs OR Nhour OR Nhours                     |
                     ---------------------------------------------------------------------------------------------------
                    | Minutes           | MINUTES(N)        | Nm  OR Nmins OR Nminute OR Nminutes                       |
                     ---------------------------------------------------------------------------------------------------
                    | Seconds           | SECONDS(N)        | Ns  OR Nsec OR Nsecs OR Nsecond OR Nseconds               |
                     ---------------------------------------------------------------------------------------------------
                    | Milliseconds      | MILLISECONDS(N)   | Nms OR Nmsec OR Nmsecs OR Nmillisecond OR Nmilliseconds   |
                     ---------------------------------------------------------------------------------------------------
                    | Microseconds      | MICROSECONDS(N)   | Nus OR Nusec OR Nusecs OR Nmicrosecond OR Nmicroseconds   |
                     ===================================================================================================
                    Where, N is a 16-bit positive integer with a maximum value of 32767.
                Types: str
                Example: MINUTES(23) which is equal to 23 Minutes
                         CAL_MONTHS(5) which is equal to 5 calendar months

            timebucket_duration_arg_name:
                Optional Argument.
                Specifies the name of the timebucket_duration argument used in exposed API.
                Default Values: "timebucket_duration"
                Types: str

            value_expression:
                Optional Argument.
                Specifies a column or any expression involving columns (except for scalar subqueries).
                These expressions are used for grouping purposes not related to time.
                Types: str or List of Strings
                Example: col1 or ["col1", "col2"]

            timecode_column:
                Optional Argument.
                Specifies a column expression that serves as the timecode for a non-PTI table.
                TD_TIMECODE is used implicitly for PTI tables, but can also be specified
                explicitly by the user with this parameter.
                Types: str

            timecode_column_arg_name:
                Optional Argument.
                Specifies the name of the timecode_column argument used in exposed API.
                Default Values: "timecode_column"
                Types: str

            sequence_column:
                Optional Argument.
                Specifies a column expression (with an optional table name) that is the sequence number.
                For a PTI table, it can be TD_SEQNO or any other column that acts as a sequence number.
                For a non-PTI table, sequence_column is a column that plays the role of TD_SEQNO
                (because non-PTI tables do not have TD_SEQNO).
                Types: str

            fill:
                Optional Argument.
                Specifies values for missing timebucket values.
                Below is the description for the accepted values:
                    NULLS:
                        The missing timebuckets are returned to the user with a null value for all
                        aggregate results.

                    numeric_constant:
                        Any Teradata Database supported Numeric literal. The missing timebuckets
                        are returned to the user with the specified constant value for all
                        aggregate results. If the data type specified in the fill argument is
                        incompatible with the input data type for an aggregate function,
                        an error is reported.

                    PREVIOUS/PREV:
                        The missing timebuckets are returned to the user with the aggregate results
                        populated by the value of the closest previous timebucket with a non-missing
                        value. If the immediate predecessor of a missing timebucket is also missing,
                        both buckets, and any other immediate predecessors with missing values,
                        are loaded with the first preceding non-missing value. If a missing
                        timebucket has no predecessor with a result (for example, if the
                        timebucket is the first in the series or all the preceding timebuckets in
                        the entire series are missing), the missing timebuckets are returned to the
                        user with a null value for all aggregate results. The abbreviation PREV may
                        be used instead of PREVIOUS.

                    NEXT:
                        The missing timebuckets are returned to the user with the aggregate results populated
                        by the value of the closest succeeding timebucket with a non-missing value. If the
                        immediate successor of a missing timebucket is also missing, both buckets, and any
                        other immediate successors with missing values, are loaded with the first succeeding
                        non-missing value. If a missing timebucket has no successor with a result
                        (for example, if the timebucket is the last in the series or all the succeeding
                        timebuckets in the entire series are missing), the missing timebuckets are returned
                        to the user with a null value for all aggregate results.

                Permitted values: NULLS, PREV / PREVIOUS, NEXT, and any numeric_constant
                Types: str or int or float

            fill_arg_name:
                Optional Argument.
                Specifies the name of the fill argument used in exposed API.
                Default Values: "fill"
                Types: str

        NOTES:
            Users can still apply teradataml DataFrame methods (filters/sort/etc) on top of the result.

        RETURNS:
            teradataml DataFrameGroupBy Object

        RAISES:
            TypeError, ValueError, TeradataMLException

        EXAMPLES:
            self.__group_time_series_data(timebucket_duration=timebucket_duration, value_expression=value_expression,
                                             timecode_column = timecode_column, sequence_column = sequence_column,
                                             fill = fill)
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append([timebucket_duration_arg_name, timebucket_duration, False, str, True])
        awu_matrix.append(["value_expression", value_expression, True, (str, list), True])
        awu_matrix.append([timecode_column_arg_name, timecode_column, True, str, True])
        awu_matrix.append(["sequence_column", sequence_column, True, str, True])
        awu_matrix.append([fill_arg_name, fill, True, (float, int, str), True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(value_expression, self._metaexpr)
        _Validators._validate_column_exists_in_dataframe(timecode_column, self._metaexpr)
        _Validators._validate_column_exists_in_dataframe(sequence_column, self._metaexpr)

        # Validate Permitted values for fills.
        if isinstance(fill, str):
            _Validators._validate_permitted_values(fill, ["NULLS", "PREV", "PREVIOUS", "NEXT", "any numeric_constant"],
                                                   fill_arg_name)

        # Validate the types passed to timecode column and sequence column.
        if timecode_column is not None:
            _Validators._validate_column_type(self, timecode_column, timecode_column_arg_name,
                                              PTITableConstants.VALID_TIMECODE_DATATYPES.value)
        if sequence_column is not None:
            _Validators._validate_column_type(self, sequence_column, 'sequence_column',
                                              PTITableConstants.VALID_SEQUENCE_COL_DATATYPES.value)
            if timecode_column is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT,
                                                               "sequence_column", timecode_column_arg_name),
                                          MessageCodes.DEPENDENT_ARGUMENT)

        # Validate for consecutive groupby operations, if consecutive, raise error.
        if isinstance(self, DataFrameGroupByTime) or isinstance(self, DataFrameGroupBy):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_OPERATION),
                                      MessageCodes.UNSUPPORTED_OPERATION)

        # Validate the values passed to timebucket duration
        if timebucket_duration.strip() == "*":
            # 'timebucket_duration' set to '*' is also allowed for 'delta_t' time series aggregate function.
            pass
        else:
            # If 'timebucket_duration' is set to anything other than '*', we should validate it's values.
            _Validators._validate_timebucket_duration(timebucket_duration, timebucket_duration_arg_name)

        # Check the timebucket_duration, is it in shorthand notation or formal notation
        if timebucket_duration[0].isdigit():
            # timebucket_duration value is provided in shorthand format.
            # Let's convert it to formal notation, so that column name can
            # be easily retrieved.
            # Even though we use shorthand notation in here, generated column name contains
            # formal notation.
            short_to_formal_mapper = PTITableConstants.TIMEBUCKET_DURATION_FORMAT_MAPPER.value
            timebucket_duration_formal = short_to_formal_mapper[re.sub(r'\d', '', timebucket_duration)]
            n = re.match(r'\d+', timebucket_duration).group(0)
            timebucket_duration = timebucket_duration_formal.format(str(n))

        try:
            unsupported_types = ['BLOB', 'CLOB', 'PERIOD_DATE', 'PERIOD_TIME', 'PERIOD_TIMESTAMP', 'ARRAY', 'VARRAY',
                                 'XML', 'JSON']
            type_expr = []
            invalid_types = []

            group_by_column_list = ["TIMECODE_RANGE"]
            if timebucket_duration.strip() != "*":
                group_by_column_list.append("GROUP BY TIME({})".format(timebucket_duration))
            else:
                group_by_column_list.append("GROUP BY TIME( * )")

            # If fill is a numeric constant, then convert it to a string as AED required it in string format.
            if isinstance(fill, (int, float)):
                fill = str(fill)

            if value_expression is not None:
                if isinstance(value_expression, str):
                    value_expression = [value_expression]

                # Column used in sequence_column should not appear in value_expression,
                # which is part of GROUP BY TIME column list
                if sequence_column is not None and sequence_column in value_expression:
                    # ARG_VALUE_INTERSECTION_NOT_ALLOWED
                    raise TeradataMlException(Messages.get_message(MessageCodes.ARG_VALUE_INTERSECTION_NOT_ALLOWED,
                                                                   sequence_column, "sequence_column",
                                                                   "value_expression"),
                                              MessageCodes.ARG_VALUE_INTERSECTION_NOT_ALLOWED)

                # Column used in timecode_column should not appear in value_expression,
                # which is part of GROUP BY TIME column list
                if timecode_column is not None and timecode_column in value_expression:
                    # ARG_VALUE_INTERSECTION_NOT_ALLOWED
                    raise TeradataMlException(Messages.get_message(MessageCodes.ARG_VALUE_INTERSECTION_NOT_ALLOWED,
                                                                   timecode_column, timecode_column_arg_name,
                                                                   "value_expression"),
                                              MessageCodes.ARG_VALUE_INTERSECTION_NOT_ALLOWED)

                # Checking each element in columns_expr to be valid column in dataframe
                for col in value_expression:
                    type_expr.append(self._metaexpr.t.c[col].type)
                    # Add column from value_expression to group_by_column_list
                    group_by_column_list.append(col)

                # Convert types to string from sqlalchemy type
                columns_types = [repr(type_expr[i]).split("(")[0] for i in range(len(type_expr))]

                # Checking each element in passed columns_types to be valid a data type for group by time
                # and create a list of invalid_types
                for col_type in columns_types:
                    if col_type in unsupported_types:
                        invalid_types.append(col_type)

                if len(invalid_types) > 0:
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_types,
                                                                   "ANY, except following {}".format(unsupported_types)),
                                              MessageCodes.UNSUPPORTED_DATATYPE)

                groupby_column_expr = ', '.join(UtilFuncs._teradata_quote_arg(col, "\"", False)
                                                for col in value_expression)
            else:
                groupby_column_expr = None

            groupbyObj = DataFrameGroupByTime(nodeid=self._nodeid, metaexpr=self._metaexpr,
                                              column_names_and_types=self._column_names_and_types, columns=self.columns,
                                              groupby_value_expr = groupby_column_expr,
                                              column_list=group_by_column_list, timebucket_duration=timebucket_duration,
                                              value_expression=value_expression, timecode_column=timecode_column,
                                              sequence_column=sequence_column, fill=fill)
            return groupbyObj
        except TeradataMlException:
            raise

    def groupby_time(self, timebucket_duration, value_expression = None, timecode_column = None, sequence_column = None,
                     fill = None):
        """
        DESCRIPTION:
            Apply Group By Time to one or more columns of a teradataml DataFrame.
            The result always behaves like calling group by time. Outcome of this function
            can be used to run Time Series Aggregate functions.

        PARAMETERS:
            timebucket_duration:
                Required Argument.
                Specifies the time unit duration of each timebucket for aggregation and is used to
                assign each potential timebucket a unique number.
                Permitted Values:
                     ===================================================================================================
                    | Time Units        | Formal Form       | Shorthand Equivalents for time_units                      |
                     ===================================================================================================
                    | Calendar Years    | CAL_YEARS(N)      | Ncy OR Ncyear OR Ncyears                                  |
                     ---------------------------------------------------------------------------------------------------
                    | Calendar Months   | CAL_MONTHS(N)     | Ncm OR Ncmonth OR Ncmonths                                |
                     ---------------------------------------------------------------------------------------------------
                    | Calendar Days     | CAL_DAYS(N)       | Ncd OR Ncday OR Ncdays                                    |
                     ---------------------------------------------------------------------------------------------------
                    | Weeks             | WEEKS(N)          | Nw  OR Nweek OR Nweeks                                    |
                     ---------------------------------------------------------------------------------------------------
                    | Days              | DAYS(N)           | Nd  OR Nday OR Ndays                                      |
                     ---------------------------------------------------------------------------------------------------
                    | Hours             | HOURS(N)          | Nh  OR Nhr OR Nhrs OR Nhour OR Nhours                     |
                     ---------------------------------------------------------------------------------------------------
                    | Minutes           | MINUTES(N)        | Nm  OR Nmins OR Nminute OR Nminutes                       |
                     ---------------------------------------------------------------------------------------------------
                    | Seconds           | SECONDS(N)        | Ns  OR Nsec OR Nsecs OR Nsecond OR Nseconds               |
                     ---------------------------------------------------------------------------------------------------
                    | Milliseconds      | MILLISECONDS(N)   | Nms OR Nmsec OR Nmsecs OR Nmillisecond OR Nmilliseconds   |
                     ---------------------------------------------------------------------------------------------------
                    | Microseconds      | MICROSECONDS(N)   | Nus OR Nusec OR Nusecs OR Nmicrosecond OR Nmicroseconds   |
                     ===================================================================================================
                    Where, N is a 16-bit positive integer with a maximum value of 32767.

                    Notes:
                        1. When timebucket_duration is Calendar Days, it will group the columns in
                           24 hour periods starting at 00:00:00.000000 and ending at 23:59:59.999999 on
                           the day identified by time zero.
                        2. A DAYS time unit is a 24 hour span relative to any moment in time.
                           For example,
                                If time zero (in teradataml DataFraame created on PTI tables) equal to
                                2016-10-01 12:00:00, the day buckets are:
                                    2016-10-01 12:00:00.000000 - 2016-10-02 11:59:59.999999.
                                This spans multiple calendar days, but encompasses one 24 hour period
                                representative of a day.
                        3. The time units do not store values such as the year or the month.
                           For example,
                                CAL_YEARS(2017) does not set the year to 2017. It sets the timebucket_duration
                                to intervals of 2017 years. Similarly, CAL_MONTHS(7) does not set the month to
                                July. It sets the timebucket_duration to intervals of 7 months.
                Types: str
                Example: MINUTES(23) which is equal to 23 Minutes
                         CAL_MONTHS(5) which is equal to 5 calendar months

            value_expression:
                Optional Argument.
                Specifies a column used for grouping purposes not related to time.
                Types: str or List of Strings
                Example: col1 or ["col1", "col2"]

            timecode_column:
                Optional Argument.
                Specifies a column that serves as the timecode for a non-PTI table. This is the column
                used for resampling time series data.
                For teradataml DataFrame created on PTI table:
                    TD_TIMECODE is used implicitly for PTI tables, but can also be specified explicitly
                    by the user with this parameter.
                For teradataml DataFrame created on non-PTI table:
                    One must pass column name to this argument for teradataml DataFrame created on non-PTI table,
                    otherwise an exception is raised.

            sequence_column:
                Optional Argument.
                Specifies a column that is the sequence number.
                For teradataml DataFrame created on PTI table:
                    It can be TD_SEQNO or any other column that acts as a sequence number.
                For teradataml DataFrame created on non-PTI table:
                    sequence_column is a column that plays the role of TD_SEQNO, because non-PTI
                    tables do not have TD_SEQNO.
                Types: str

            fill:
                Optional Argument.
                Specifies values for missing timebucket values.
                Permitted values: NULLS, PREV / PREVIOUS, NEXT, and any numeric_constant
                    NULLS:
                        The missing timebuckets are returned to the user with a null value for all
                        aggregate results.

                    numeric_constant:
                        Any Teradata Database supported Numeric literal. The missing timebuckets
                        are returned to the user with the specified constant value for all
                        aggregate results. If the data type specified in the fill argument is
                        incompatible with the input data type for an aggregate function,
                        an error is reported.

                    PREVIOUS/PREV:
                        The missing timebuckets are returned to the user with the aggregate results
                        populated by the value of the closest previous timebucket with a non-missing
                        value. If the immediate predecessor of a missing timebucket is also missing,
                        both buckets, and any other immediate predecessors with missing values,
                        are loaded with the first preceding non-missing value. If a missing
                        timebucket has no predecessor with a result (for example, if the
                        timebucket is the first in the series or all the preceding timebuckets in
                        the entire series are missing), the missing timebuckets are returned to the
                        user with a null value for all aggregate results. The abbreviation PREV may
                        be used instead of PREVIOUS.

                    NEXT:
                        The missing timebuckets are returned to the user with the aggregate results populated
                        by the value of the closest succeeding timebucket with a non-missing value. If the
                        immediate successor of a missing timebucket is also missing, both buckets, and any
                        other immediate successors with missing values, are loaded with the first succeeding
                        non-missing value. If a missing timebucket has no successor with a result
                        (for example, if the timebucket is the last in the series or all the succeeding
                        timebuckets in the entire series are missing), the missing timebuckets are returned
                        to the user with a null value for all aggregate results.

                Types: str or int or float

        NOTES:
            1. This API is similar to resample().
            2. Users can still apply teradataml DataFrame methods (filters/sort/etc) on top of the result.
            3. Consecutive operations of grouping, i.e., groupby_time(), resample() and groupby() are not permitted.
               An exception will be raised. Following are some cases where exception will be raised as
               "Invalid operation applied, check documentation for correct usage."
                    a. df.groupby_time().groupby()
                    b. df.groupby_time().resample()
                    c. df.groupby_time().groupby_time()

        RETURNS:
            teradataml DataFrameGroupBy Object

        RAISES:
            TypeError, ValueError, TeradataMLException

        EXAMPLES:
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_nonpti"])
            >>>

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['buoyid', 'timecode', 'temperature', 'salinity']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  temperature  salinity
            timecode
            2014-01-06 08:09:59.999999       0         99.0        55
            2014-01-06 08:10:00.000000       0         10.0        55
            2014-01-06 09:01:25.122200       1         70.0        55
            2014-01-06 09:01:25.122200       1         77.0        55
            2014-01-06 09:02:25.122200       1         71.0        55
            2014-01-06 09:03:25.122200       1         72.0        55
            2014-01-06 09:02:25.122200       1         78.0        55
            2014-01-06 08:10:00.000000       0        100.0        55
            2014-01-06 08:08:59.999999       0          NaN        55
            2014-01-06 08:00:00.000000       0         10.0        55

            #
            # Example 1: Group by timebucket of 2 calendar years, using formal notation and buoyid column on
            #            DataFrame created on non-sequenced PTI table.
            #            Fill missing values with Nulls.
            #
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="CAL_YEARS(2)",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_grpby1.bottom(number_of_values_to_column).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  bottom2temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                  10
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                  10
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                  71
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                  70
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                  80
            5  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                  81
            6  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                  43
            7  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                  43
            >>>

            #
            # Example 2: Group by timebucket of 2 minutes, using shorthand notation to specify timebucket,
            #            on DataFrame created on non-PTI table. Fill missing values with Nulls.
            #            Time column must be specified for non-PTI table.
            #
            >>> ocean_buoys_nonpti_grpby2 = ocean_buoys_nonpti.groupby_time(timebucket_duration="2m",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby2.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE",
            ...                                                                                    "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                          10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                           NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                           NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                           NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                          99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                         100.0
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                          10.0
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                          70.0
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                          77.0
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                          71.0
            >>>

            #
            # Example 3: Group by timebucket of 2 minutes, using shorthand notation to specify timebucket,
            #            on DataFrame created on non-PTI table. Fill missing values with previous values.
            #            Time column must be specified for non-PTI table.
            #
            >>> ocean_buoys_nonpti_grpby2 = ocean_buoys_nonpti.groupby_time(timebucket_duration="2mins",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="prev")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby2.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE",
            ...                                                                                    "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                            10
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                            10
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                            10
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                            10
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                            99
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                            10
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                           100
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                            77
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                            70
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                            71

            #
            # Example 4: Group by timebucket of 2 minutes, using shorthand notation to specify timebucket,
            #            on DataFrame created on non-PTI table. Fill missing values with numeric constant 12345.
            #            Time column must be specified for non-PTI table.
            #
            >>> ocean_buoys_nonpti_grpby2 = ocean_buoys_nonpti.groupby_time(timebucket_duration="2minute",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill=12345)
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby2.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE",
            ...                                                                                    "buoyid"])

                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                            10
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                         12345
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                         12345
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                         12345
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                            99
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                            10
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                           100
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                            77
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                            70
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                            71
            >>>

        """
        return self.__group_time_series_data(timebucket_duration=timebucket_duration, value_expression=value_expression,
                                             timecode_column = timecode_column, sequence_column = sequence_column,
                                             fill = fill)

    def resample(self, rule, value_expression = None, on = None, sequence_column = None,
                     fill_method = None):
        """
        DESCRIPTION:
            Resample time series data. This function allows grouping done by time on
            a datetime column of a teradataml DataFrame. Outcome of this function
            can be used to run Time Series Aggregate functions.

        PARAMETERS:
            rule:
                Required Argument.
                Specifies the time unit duration/interval of each timebucket for resampling and is used to
                assign each potential timebucket a unique number.
                Permitted Values:
                     ===================================================================================================
                    | Time Units        | Formal Form       | Shorthand Equivalents for time_units                      |
                     ===================================================================================================
                    | Calendar Years    | CAL_YEARS(N)      | Ncy OR Ncyear OR Ncyears                                  |
                     ---------------------------------------------------------------------------------------------------
                    | Calendar Months   | CAL_MONTHS(N)     | Ncm OR Ncmonth OR Ncmonths                                |
                     ---------------------------------------------------------------------------------------------------
                    | Calendar Days     | CAL_DAYS(N)       | Ncd OR Ncday OR Ncdays                                    |
                     ---------------------------------------------------------------------------------------------------
                    | Weeks             | WEEKS(N)          | Nw  OR Nweek OR Nweeks                                    |
                     ---------------------------------------------------------------------------------------------------
                    | Days              | DAYS(N)           | Nd  OR Nday OR Ndays                                      |
                     ---------------------------------------------------------------------------------------------------
                    | Hours             | HOURS(N)          | Nh  OR Nhr OR Nhrs OR Nhour OR Nhours                     |
                     ---------------------------------------------------------------------------------------------------
                    | Minutes           | MINUTES(N)        | Nm  OR Nmins OR Nminute OR Nminutes                       |
                     ---------------------------------------------------------------------------------------------------
                    | Seconds           | SECONDS(N)        | Ns  OR Nsec OR Nsecs OR Nsecond OR Nseconds               |
                     ---------------------------------------------------------------------------------------------------
                    | Milliseconds      | MILLISECONDS(N)   | Nms OR Nmsec OR Nmsecs OR Nmillisecond OR Nmilliseconds   |
                     ---------------------------------------------------------------------------------------------------
                    | Microseconds      | MICROSECONDS(N)   | Nus OR Nusec OR Nusecs OR Nmicrosecond OR Nmicroseconds   |
                     ===================================================================================================
                    Where, N is a 16-bit positive integer with a maximum value of 32767.

                    Notes:
                        1. When timebucket_duration is Calendar Days, it will group the columns in
                           24 hour periods starting at 00:00:00.000000 and ending at 23:59:59.999999 on
                           the day identified by time zero.
                        2. A DAYS time unit is a 24 hour span relative to any moment in time.
                           For example,
                                If time zero (in teradataml DataFraame created on PTI tables) equal to
                                2016-10-01 12:00:00, the day buckets are:
                                    2016-10-01 12:00:00.000000 - 2016-10-02 11:59:59.999999.
                                This spans multiple calendar days, but encompasses one 24 hour period
                                representative of a day.
                        3. The time units do not store values such as the year or the month.
                           For example,
                                CAL_YEARS(2017) does not set the year to 2017. It sets the timebucket_duration
                                to intervals of 2017 years. Similarly, CAL_MONTHS(7) does not set the month to
                                July. It sets the timebucket_duration to intervals of 7 months.

                Types: str
                Example: MINUTES(23) which is equal to 23 Minutes
                         CAL_MONTHS(5) which is equal to 5 calendar months

            value_expression:
                Optional Argument.
                Specifies a column used for grouping purposes not related to time.
                Types: str or List of Strings
                Example: col1 or ["col1", "col2"]

            on:
                Optional Argument.
                Specifies a column that serves as the timecode for a non-PTI table. This is the column
                used for resampling time series data.
                For teradataml DataFrame created on PTI table:
                    TD_TIMECODE is used implicitly for PTI tables, but can also be specified explicitly
                    by the user with this parameter.
                For teradataml DataFrame created on non-PTI table:
                    Column must be specified to this argument if DataFrame is created on non-PTI table,
                    otherwise, an exception is raised.
                Types: str

            sequence_column:
                Optional Argument.
                Specifies a column that is the sequence number.
                For teradataml DataFrame created on PTI table:
                    It can be TD_SEQNO or any other column that acts as a sequence number.
                For teradataml DataFrame created on non-PTI table:
                    sequence_column is a column that plays the role of TD_SEQNO, because non-PTI
                    tables do not have TD_SEQNO.
                Types: str

            fill_method:
                Optional Argument.
                Specifies values for missing timebucket values.
                Permitted values: NULLS, PREV / PREVIOUS, NEXT, and any numeric_constant
                    NULLS:
                        The missing timebuckets are returned to the user with a null value for all
                        aggregate results.

                    numeric_constant:
                        Any Teradata Database supported Numeric literal. The missing timebuckets
                        are returned to the user with the specified constant value for all
                        aggregate results. If the data type specified in the fill_method argument is
                        incompatible with the input data type for an aggregate function,
                        an error is reported.

                    PREVIOUS/PREV:
                        The missing timebuckets are returned to the user with the aggregate results
                        populated by the value of the closest previous timebucket with a non-missing
                        value. If the immediate predecessor of a missing timebucket is also missing,
                        both buckets, and any other immediate predecessors with missing values,
                        are loaded with the first preceding non-missing value. If a missing
                        timebucket has no predecessor with a result (for example, if the
                        timebucket is the first in the series or all the preceding timebuckets in
                        the entire series are missing), the missing timebuckets are returned to the
                        user with a null value for all aggregate results. The abbreviation PREV may
                        be used instead of PREVIOUS.

                    NEXT:
                        The missing timebuckets are returned to the user with the aggregate results populated
                        by the value of the closest succeeding timebucket with a non-missing value. If the
                        immediate successor of a missing timebucket is also missing, both buckets, and any
                        other immediate successors with missing values, are loaded with the first succeeding
                        non-missing value. If a missing timebucket has no successor with a result
                        (for example, if the timebucket is the last in the series or all the succeeding
                        timebuckets in the entire series are missing), the missing timebuckets are returned
                        to the user with a null value for all aggregate results.

                Types: str or int or float

        NOTES:
            1. This API is similar to groupby_time().
            2. Users can still apply teradataml DataFrame methods (filters/sort/etc) on top of the result.
            3. Consecutive operations of grouping, i.e., groupby_time(), resample() and groupby() are not permitted.
               An exception will be raised. Following are some cases where exception will be raised as
               "Invalid operation applied, check documentation for correct usage."
                    a. df.resample().groupby()
                    b. df.resample().resample()
                    c. df.resample().groupby_time()

        RETURNS:
            teradataml DataFrameGroupBy Object

        RAISES:
            TypeError, ValueError, TeradataMLException

        EXAMPLES:
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_nonpti"])
            >>>

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['buoyid', 'timecode', 'temperature', 'salinity']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  temperature  salinity
            timecode
            2014-01-06 08:09:59.999999       0         99.0        55
            2014-01-06 08:10:00.000000       0         10.0        55
            2014-01-06 09:01:25.122200       1         70.0        55
            2014-01-06 09:01:25.122200       1         77.0        55
            2014-01-06 09:02:25.122200       1         71.0        55
            2014-01-06 09:03:25.122200       1         72.0        55
            2014-01-06 09:02:25.122200       1         78.0        55
            2014-01-06 08:10:00.000000       0        100.0        55
            2014-01-06 08:08:59.999999       0          NaN        55
            2014-01-06 08:00:00.000000       0         10.0        55

            #
            # Example 1: Resample by timebucket of 2 calendar years, using formal notation and buoyid column on
            #            DataFrame created on non-sequenced PTI table.
            #            Fill missing values with Nulls.
            #
            >>> ocean_buoys_grpby1 = ocean_buoys.resample(rule="CAL_YEARS(2)", value_expression="buoyid", fill_method="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_grpby1.bottom(number_of_values_to_column).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  bottom2temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                  10
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                  10
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                  71
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                  70
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                  80
            5  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                  81
            6  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                  43
            7  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                  43
            >>>

            #
            # Example 2: Resample data by timebucket of 2 minutes, using shorthand notation to specify timebucket,
            #            on DataFrame created on non-PTI table. Fill missing values with Nulls.
            #            Time column must be specified for non-PTI table using 'on' argument.
            #
            >>> ocean_buoys_nonpti_grpby2 = ocean_buoys_nonpti.resample(rule="2m", value_expression="buoyid",
            ...                                                         on="timecode", fill_method="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby2.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE",
            ...                                                                                    "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                          10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                           NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                           NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                           NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                          99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                         100.0
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                          10.0
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                          70.0
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                          77.0
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                          71.0
            >>>

            #
            # Example 3: Resample time series data by timebucket of 2 minutes, using shorthand notation to specify
            #            timebucket, on teradataml DataFrame created on non-PTI table. Fill missing values with
            #            previous values. Time column must be specified for non-PTI table using 'on' argument.
            #
            >>> ocean_buoys_nonpti_grpby2 = ocean_buoys_nonpti.resample(rule="2mins", value_expression="buoyid",
            ...                                                         on="timecode", fill_method="prev")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby2.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE",
            ...                                                                                    "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                            10
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                            10
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                            10
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                            10
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                            99
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                            10
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                           100
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                            77
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                            70
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                            71

            #
            # Example 4: Resample time series data by timebucket of 2 minutes, using shorthand notation to specify
            #            timebucket, on teradataml DataFrame created on non-PTI table. Fill missing values with
            #            numeric 12345. Time column must be specified for non-PTI table using 'on' argument.
            #
            >>> ocean_buoys_nonpti_grpby2 = ocean_buoys_nonpti.resample(rule="2minute", value_expression="buoyid",
            ...                                                         on="timecode", fill=12345)
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby2.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE",
            ...                                                                                    "buoyid"])

                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                            10
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                         12345
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                         12345
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                         12345
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                            99
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                            10
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                           100
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                            77
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                            70
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                            71
            >>>

        """
        return self.__group_time_series_data(timebucket_duration=rule, timebucket_duration_arg_name="rule",
                                             value_expression=value_expression, timecode_column_arg_name="on",
                                             timecode_column = on, sequence_column = sequence_column,
                                             fill = fill_method, fill_arg_name="fill_method")

    def get_values(self, num_rows = 99999):
        """
        DESCRIPTION:
            Retrieves all values (only) present in a teradataml DataFrame.
            Values are retrieved as per a numpy.ndarray representation of a teradataml DataFrame.
            This format is equivalent to the get_values() representation of a Pandas DataFrame.

        PARAMETERS:
            num_rows:
                Optional Argument.
                Specifies the number of rows to retrieve values for from a teradataml DataFrame.
                The num_rows parameter specified needs to be an integer value.
                Default Value: 99999
                Types: int

        RETURNS:
            Numpy.ndarray representation of a teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df1 = DataFrame.from_table('admissions_train')
            >>> df1
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  Advanced    Advanced        1
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            26     yes  3.57  Advanced    Advanced        1
            5       no  3.44    Novice      Novice        0
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            # Retrieve all values from the teradataml DataFrame

            >>> vals = df1.get_values()
            >>> vals
            array([['yes', 4.0, 'Advanced', 'Advanced', 1],
                   ['yes', 3.45, 'Advanced', 'Advanced', 0],
                   ['yes', 3.5, 'Advanced', 'Beginner', 1],
                   ['yes', 4.0, 'Novice', 'Beginner', 0],
                                 . . .
                   ['no', 3.68, 'Novice', 'Beginner', 1],
                   ['yes', 3.5, 'Beginner', 'Advanced', 1],
                   ['yes', 3.79, 'Advanced', 'Novice', 0],
                   ['no', 3.0, 'Advanced', 'Novice', 0],
                   ['yes', 1.98, 'Advanced', 'Advanced', 0]], dtype=object)

            # Retrieve values for a given number of rows from the teradataml DataFrame

            >>> vals = df1.get_values(num_rows = 3)
            >>> vals
            array([['yes', 4.0, 'Advanced', 'Advanced', 1],
                   ['yes', 3.45, 'Advanced', 'Advanced', 0],
                   ['yes', 3.5, 'Advanced', 'Beginner', 1]], dtype=object)

            # Access specific values from the entire set received as per below:
            # Retrieve all values from an entire row (for example, the first row):

            >>> vals[0]
            array(['yes', 4.0, 'Advanced', 'Advanced', 1], dtype=object)

            # Alternatively, specify a range to retrieve values from  a subset of rows (For example, first 3 rows):

            >>> vals[0:3]
            array([['yes', 4.0, 'Advanced', 'Advanced', 1],
            ['yes', 3.45, 'Advanced', 'Advanced', 0],
            ['yes', 3.5, 'Advanced', 'Beginner', 1]], dtype=object)

            # Alternatively, retrieve all values from an entire column (For example, the first column):

            >>> vals[:, 0]
            array(['yes', 'yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes',
                   'yes', 'no', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no',
                   'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes',
                   'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no',
                   'yes'], dtype=object)

            # Alternatively, retrieve a single value from a given row and column (For example, 3rd row, and 2nd column):
            >>> vals[2,1]
            3.5

            Note:
            1) Row and column indexing starts from 0, so the first column = index 0, second column = index 1, and so on...

            2) When a Pandas DataFrame is saved to Teradata Vantage & retrieved back as a teradataml DataFrame, the get_values()
               method on a Pandas DataFrame and the corresponding teradataml DataFrames have the following type differences:
                   - teradataml DataFrame get_values() retrieves 'bool' type Pandas DataFrame values (True/False) as BYTEINTS (1/0)
                   - teradataml DataFrame get_values() retrieves 'Timedelta' type Pandas DataFrame values as equivalent values in seconds.

        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["num_rows", num_rows, True, (int)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Validate n is a positive int.
        _Validators._validate_positive_int(num_rows, "num_rows")

        return self.to_pandas(self._index_label, num_rows).values

    @property
    def shape(self):
        """
        Returns a tuple representing the dimensionality of the DataFrame.

        PARAMETERS:
            None

        RETURNS:
            Tuple representing the dimensionality of this DataFrame.

        Examples:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df
                          Feb   Jan   Mar   Apr  datetime
            accounts
            Orange Inc  210.0  None  None   250  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Blue Inc     90.0    50    95   101  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            >>> df.shape
            (6, 6)
            >>>

        RAISES:
            TeradataMlException (TDMLDF_INFO_ERROR)
        """
        try:
            # To know the number of rows in a DF, we need to execute the node
            # Generate/Execute AED nodes
            self.__execute_node_and_set_table_name(self._nodeid)

            # The dimension of the DF is (# of rows, # of columns)
            return df_utils._get_row_count(self._table_name), len(self._column_names_and_types)

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    @property
    def size(self):
        """
        Returns a value representing the number of elements in the DataFrame.

        PARAMETERS:
            None

        RETURNS:
            Value representing the number of elements in the DataFrame.

        Examples:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df
                          Feb   Jan   Mar   Apr  datetime
            accounts
            Orange Inc  210.0  None  None   250  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Blue Inc     90.0    50    95   101  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            >>> df.size
            36

        RAISES:
            None
        """
        dimension = self.shape
        return dimension[0] * dimension[1]

    def merge(self, right, on=None, how="inner", left_on=None, right_on=None, use_index=False,
              lsuffix=None, rsuffix=None):
        """
        DESCRIPTION:
            Merges two teradataml DataFrames together.
         
            Supported merge operations are:
                - inner: Returns only matching rows, non-matching rows are eliminated.
                - left: Returns all matching rows plus non-matching rows from the left teradataml DataFrame.
                - right: Returns all matching rows plus non-matching rows from the right teradataml DataFrame.
                - full: Returns all rows from both teradataml DataFrames, including non matching rows.

        PARAMETERS:
         
            right:
                Required Argument.
                Specifies right teradataml DataFrame on which merge is to be performed.
                Types: teradataml DataFrame
            
            on:
                Optional Argument.
                Specifies list of conditions that indicate the columns used for the merge.
                When no arguments are provided for this condition, the merge is performed using the indexes
                of the teradataml DataFrames. Both teradataml DataFrames are required to have index labels to
                perform a merge operation when no arguments are provided for this condition.
                When either teradataml DataFrame does not have a valid index label in the above case,
                an exception is thrown.
                • String comparisons, in the form of "col1 <= col2", where col1 is
                  the column of left DataFrame df1 and col2 is the column of right
                  DataFrame df2.
                  Examples:
                    1. ["a","b"] indicates df1.a = df2.a and df1.b = df2.b.
                    2. ["a = b", "c = d"] indicates df1.a = df2.b and df1.c = df2.d
                    3. ["a <= b", "c > d"] indicates df1.a <= df2.b and df1.c > df2.d.
                    4. ["a < b", "c >= d"] indicates df1.a < df2.b and df1.c >= df2.d.
                    5. ["a <> b"] indicates df1.a != df2.b. Same is the case for ["a != b"].
                • Column comparisons, in the form of df1.col1 <= df2.col2, where col1
                  is the column of left DataFrame df1 and col2 is the column of right
                  DataFrame df2.
                  Examples:
                    1. [df1.a == df2.a, df1.b == df2.b] indicates df1.a = df2.a and df1.b = df2.b.
                    2. [df1.a == df2.b, df1.c == df2.d] indicates df1.a = df2.b and df1.c = df2.d.
                    3. [df1.a <= df2.b and df1.c > df2.d] indicates df1.a <= df2.b and df1.c > df2.d.
                    4. [df1.a < df2.b and df1.c >= df2.d] indicates df1.a < df2.b and df1.c >= df2.d.
                    5. df1.a != df2.b indicates df1.a != df2.b.
                • The combination of both string comparisons and comparisons as column expressions.
                  Examples:
                    1. ["a", df1.b == df2.b] indicates df1.a = df2.a and df1.b = df2.b.
                    2. [df1.a <= df2.b, "c > d"] indicates df1.a <= df2.b and df1.c > df2.d.
                Default Value: None
                Types: str or ColumnExpression or List of strings(str) or ColumnExpressions

            how:
                Optional Argument.
                Specifies the type of merge to perform. Supports inner, left, right, full and cross merge operations.
                When how is "cross", the arguments on, left_on, right_on and use_index are ignored.
                Default Value: "inner".
                Types: str
                      
            left_on:
                Optional Argument.
                Specifies column to merge on, in the left teradataml DataFrame.
                When both the 'on' and 'left_on' parameters are unspecified, the index columns
                of the teradataml DataFrames are used to perform the merge operation.
                Default Value: None.
                Types: str or ColumnExpression or List of strings(str) or ColumnExpressions
                      
            right_on:
                Optional Argument.
                Specifies column to merge on, in the right teradataml DataFrame.
                When both the 'on' and 'right_on' parameters are unspecified, the index columns
                of the teradataml DataFrames are used to perform the merge operation.
                Default Value: None.
                Types: str or ColumnExpression or List of strings(str) or ColumnExpressions
                       
            use_index:
                Optional Argument.
                Specifies whether (or not) to use index from the teradataml DataFrames as the merge key(s).
                When False, and 'on', 'left_on', and 'right_on' are all unspecified, the index columns
                of the teradataml DataFrames are used to perform the merge operation.
                Default value: False.
                Types: bool
                         
            lsuffix:
                Optional Argument.
                Specifies suffix to be added to the left table columns.
                Default Value: None.
                Types: str
                         
                Note: A suffix is required if teradataml DataFrames being merged have columns
                      with the same name.
                      
            rsuffix:
                Optional Argument.
                Specifies suffix to be added to the right table columns.
                Default Value: None.
                Types: str
                     
                Note: A suffix is required if teradataml DataFrames being merged have columns
                      with the same name.

        RAISES:
            TeradataMlException

        RETURNS:
            teradataml DataFrame

        EXAMPLES:
            
            # Example set-up teradataml DataFrames for merge
            >>> from datetime import datetime, timedelta
            >>> dob = datetime.strptime('31101991', '%d%m%Y').date()
            
            >>> df1 = pd.DataFrame(data={'col1': [1, 2,3],
                           'col2': ['teradata','analytics','platform'],
                           'col3': [1.3, 2.3, 3.3],
                           'col5': ['a','b','c'],
                            'col 6': [dob, dob + timedelta(1), dob + timedelta(2)],
                            "'col8'":[3,4,5]})
            
            >>> df2 = pd.DataFrame(data={'col1': [1, 2, 3],
                                'col4': ['teradata', 'analytics', 'are you'],
                                'col3': [1.3, 2.3, 4.3],
                                 'col7':['a','b','d'],
                                 'col 6': [dob, dob + timedelta(1), dob + timedelta(3)],
                                 "'col8'": [3, 4, 5]})
            >>> # Persist the Pandas DataFrames in Vantage.
            >>> copy_to_sql(df1, "table1", primary_index="col1")
            >>> copy_to_sql(df2, "table2", primary_index="col1")
            >>> df1 = DataFrame("table1")
            >>> df2 = DataFrame("table2")
            >>> df1
                 'col8'       col 6       col2  col3 col5
            col1                                         
            2         4  1991-11-01  analytics   2.3    b
            1         3  1991-10-31   teradata   1.3    a
            3         5  1991-11-02   platform   3.3    c
            >>> df2
                 'col8'       col 6  col3       col4 col7
            col1                                         
            2         4  1991-11-01   2.3  analytics    b
            1         3  1991-10-31   1.3   teradata    a
            3         5  1991-11-03   4.3    are you    d            
            
            >>> # 1) Specify both types of 'on' conditions and DataFrame indexes as merge keys:
            >>> df1.merge(right = df2, how = "left", on = ["col3","col2=col4"], use_index = True, lsuffix = "t1", rsuffix = "t2")
            
              t2_col1 col5    t2_col 6 t1_col1 t2_'col8'  t1_col3       col4  t2_col3  col7       col2    t1_col 6 t1_'col8'
            0       2    b  1991-11-01       2         4      2.3  analytics      2.3     b  analytics  1991-11-01         4
            1       1    a  1991-10-31       1         3      1.3   teradata      1.3     a   teradata  1991-10-31         3
            2    None    c        None       3      None      3.3       None      NaN  None   platform  1991-11-02         5

            >>> # 2) Specify 'on' conditions as ColumnExpression and DataFrame indexes as merge keys:
            >>> df1.merge(right = df2, how = "left", on = [df1.col1, df1.col3], use_index = True, lsuffix = "t1", rsuffix = "t2")

              t1_col1  t2_col1       col2  t1_col3  t2_col3 col5    t1_col 6    t2_col 6  t1_'col8'  t2_'col8'       col4  col7
            0        2      2.0  analytics      2.3      2.3    b  1991-06-23  1991-06-23          4        4.0  analytics     b
            1        1      1.0   teradata      1.3      1.3    a  1991-06-22  1991-06-22          3        3.0   teradata     a
            2        3      NaN   platform      3.3      NaN    c  1991-06-24        None          5        NaN       None  None

            
            >>> # 3) Specify left_on, right_on conditions along with DataFrame indexes as merge keys:
            >>> df1.merge(right = df2, how = "right", left_on = "col2", right_on = "col4", use_index = True, lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3  col5    t1_col 6    t2_col 6 t1_'col8' t2_'col8'       col4 col7
            0       2       2  analytics      2.3      2.3     b  1991-11-01  1991-11-01         4         4  analytics    b
            1       1       1   teradata      1.3      1.3     a  1991-10-31  1991-10-31         3         3   teradata    a
            2    None       3       None      NaN      4.3  None        None  1991-11-03      None         5    are you    d
            
            
            >>> # 4) If teradataml DataFrames to be merged do not contain common columns, lsuffix and
                #  rsuffix are not required:
            >>> new_df1 = df1.select(['col2', 'col5'])
            >>> new_df2 = df2.select(['col4', 'col7'])
            >>> new_df1
              col5       col2
            0    b  analytics
            1    a   teradata
            2    c   platform
            >>> new_df2
              col7       col4
            0    b  analytics
            1    a   teradata
            2    d    are you
            >>> new_df1.merge(right = new_df2, how = "inner", on = "col5=col7")
              col5       col4       col2 col7
            0    b  analytics  analytics    b
            1    a   teradata   teradata    a
            
            
            >>> # 5) When no merge conditions are specified, teradataml DataFrame
                # indexes are used as merge keys.
            >>> df1.merge(right = df2, how = "full", lsuffix = "t1", rsuffix = "t2")
              t2_col1 col5    t2_col 6 t1_col1 t2_'col8'  t1_col3       col4  t2_col3 col7       col2    t1_col 6 t1_'col8'
            0       2    b  1991-11-01       2         4      2.3  analytics      2.3    b  analytics  1991-11-01         4
            1       1    a  1991-10-31       1         3      1.3   teradata      1.3    a   teradata  1991-10-31         3
            2       3    c  1991-11-03       3         5      3.3    are you      4.3    d   platform  1991-11-02         5
            
         """
        tdp = preparer(td_dialect)

        # Argument validations
        awu_matrix = []
        awu_matrix.append(["right", right, False, (DataFrame)])
        awu_matrix.append(["on", on, True, (str, ColumnExpression, list)])
        awu_matrix.append(["how", how, True, (str), False, TeradataConstants.TERADATA_JOINS.value])
        awu_matrix.append(["left_on", left_on, True, (str, ColumnExpression, list)])
        awu_matrix.append(["right_on", right_on, True, (str, ColumnExpression, list)])
        awu_matrix.append(["use_index", use_index, True, (bool)])
        awu_matrix.append(["lsuffix", lsuffix, True, (str), True])
        awu_matrix.append(["rsuffix", rsuffix, True, (str), True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if (right_on is not None and left_on is None) or (right_on is None and left_on is not None):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.MUST_PASS_ARGUMENT, "left_on", "right_on"),
                MessageCodes.MUST_PASS_ARGUMENT)

        if isinstance(on,list):
            join_conditions = on
        elif isinstance(on, (str, ColumnExpression)):
            join_conditions = [on]
        else:
            join_conditions = []


        if isinstance(left_on, list) and isinstance(right_on, list) and len(left_on) != len(right_on):
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                  MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        elif isinstance(left_on, list) and isinstance(right_on, (str, ColumnExpression)) and len(left_on) != 1:
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                  MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        elif isinstance(right_on, list) and isinstance(left_on, (str, ColumnExpression)) and len(right_on) != 1:
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        if left_on is not None and not isinstance(left_on, list):
            if isinstance(left_on, str):
                left_on = [left_on]
            else:
                left_on = [left_on.compile()]

        if right_on is not None and not isinstance(right_on, list):
            if isinstance(right_on, str):
                right_on = [right_on]
            else:
                right_on = [right_on.compile()]

        if isinstance(left_on, list):
            for index in range(len(left_on)):
                if isinstance(left_on[index], ColumnExpression):
                    left_on[index] = left_on[index].compile()

        if isinstance(right_on, list):
            for index in range(len(right_on)):
                if isinstance(right_on[index], ColumnExpression):
                    right_on[index] = right_on[index].compile()


        if left_on is not None and right_on is not None:
            for left_column, right_column in zip(left_on, right_on):
                join_conditions.append("{} = {}".format(tdp.quote(left_column), tdp.quote(right_column)))

        # If user did not pass any arguments which form join conditions,
        # Merge is performed using index columns of TeradataML DataFrames
        if on is None and left_on is None and right_on is None and not use_index:
            if self._index_label is None or right._index_label is None:
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.TDMLDF_INDEXES_ARE_NONE), MessageCodes.TDMLDF_INDEXES_ARE_NONE)
            else:
                use_index = True

        if use_index:
            if self._index_label is None or right._index_label is None:
                    raise TeradataMlException(
                    Messages.get_message(MessageCodes.TDMLDF_INDEXES_ARE_NONE), MessageCodes.TDMLDF_INDEXES_ARE_NONE)

            left_index_labels = self._index_label
            right_index_labels = right._index_label
            if not isinstance(self._index_label, list):
                left_index_labels = [left_index_labels]
            if not isinstance(right._index_label, list):
                right_index_labels = [right_index_labels]

            for left_index_label, right_index_label in zip(left_index_labels, right_index_labels):
                join_conditions.append("{} = {}".format(tdp.quote(left_index_label), tdp.quote(right_index_label)))


        return self.join(other=right, on=join_conditions, how=how, lsuffix=lsuffix, rsuffix=rsuffix)

    def squeeze(self, axis=None):
        """
        DESCRIPTION:
            Squeeze one-dimensional axis objects into scalars.
            teradataml DataFrames with a single element are squeezed to a scalar.
            teradataml DataFrames with a single column are squeezed to a Series.
            Otherwise the object is unchanged.

            Note: Currently only '1' and 'None' are supported for axis.
                  For now with axis = 0, the teradataml DataFrame is returned.

        PARAMETERS:
            axis:
                Optional Argument.
                A specific axis to squeeze. By default, all axes with
                length equals one are squeezed.
                Permitted Values: 0 or 'index', 1 or 'columns', None
                Default: None

        RETURNS:
            teradataml DataFrame, teradataml Series, or scalar,
            the projection after squeezing 'axis' or all the axes.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming admitted
            id
            22     yes  3.46    Novice    Beginner        0
            36      no  3.00  Advanced      Novice        0
            15     yes  4.00  Advanced    Advanced        1
            38     yes  2.65  Advanced    Beginner        1
            5       no  3.44    Novice      Novice        0
            17      no  3.83  Advanced    Advanced        1
            34     yes  3.85  Advanced    Beginner        0
            13      no  4.00  Advanced      Novice        1
            26     yes  3.57  Advanced    Advanced        1
            19     yes  1.98  Advanced    Advanced        0

            >>> gpa = df.select(["gpa"])
            >>> gpa.squeeze()
            0    4.00
            1    2.33
            2    3.46
            3    3.83
            4    4.00
            5    2.65
            6    3.57
            7    3.44
            8    3.85
            9    3.95
            Name: gpa, dtype: float64
            >>> gpa.squeeze(axis = 1)
            0    3.46
            1    3.00
            2    4.00
            3    2.65
            4    3.44
            5    3.83
            6    3.85
            7    4.00
            8    3.57
            9    1.98
            Name: gpa, dtype: float64
            >>> gpa.squeeze(axis = 0)
                gpa
            0  3.46
            1  3.00
            2  4.00
            3  2.65
            4  3.44
            5  3.83
            6  3.85
            7  4.00
            8  3.57
            9  1.98

            >>> df = DataFrame.from_query('select gpa, stats from admissions_train where gpa=2.33')
            >>> s = df.squeeze()
            >>> s
                gpa   stats
            0  2.33  Novice

            >>> single_gpa = DataFrame.from_query('select gpa from admissions_train where gpa=2.33')
            >>> single_gpa
                gpa
            0  2.33
            >>> single_gpa.squeeze()
            2.33
            >>> single_gpa.squeeze(axis = 1)
            0    2.33
            Name: gpa, dtype: float64
            >>> single_gpa.squeeze(axis = 0)
                gpa
            0  2.33
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["axis", axis, True, (int, str), False, [0, 1, 'index', 'columns']])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Let's begin
        num_row, num_col = self.shape

        # Check if the number of elements in DF = 1
        if (num_row, num_col) == (1,1) and axis is None:
            # To get the single row/column value in the DF, we need to execute the node
            # Generate/Execute AED nodes
            self.__execute_node_and_set_table_name(self._nodeid)
            return df_utils._get_scalar_value(self._table_name)

        if axis is None:
            if num_col == 1:
                axis = 1
            elif num_row == 1:
                axis = 0
            else:
                return self
        else:
            if isinstance(axis, str):
                # Set the integer value to use further for based on the string value
                if axis == "index":
                    axis = 0
                else:
                    axis = 1

            if (axis == 0 and num_row != 1) or \
               (axis == 1 and num_col != 1):
                return self

        if axis == 1:
            return Series._from_dataframe(self, axis = 1)
        else:
            # TODO : Research and add capabilities to handle rowexpression based return objects
            # For now, returning the DataFrame as is
            return self

    def sort_index(self, axis=0, ascending=True, kind='quicksort'):
        """
        DESCRIPTION:
            Get sorted object by labels (along an axis) in either ascending or descending order for a teradataml DataFrame.
                
        PARAMETERS:
            axis:
                Optional Argument.
                Specifies the value to direct sorting on index or columns. 
                Values can be either 0 ('rows') OR 1 ('columns'), value as 0 will sort on index (if no index is present then parent DataFrame will be returned)
                and value as 1 will sort on columns names (if no index is present then parent DataFrame will be returned with sorted columns) for the DataFrame. 
                Default value: 0
                Types: int
                
            ascending:
                Optional Argument.
                Specifies a flag to sort columns in either ascending (True) or descending (False).
                Default value: True
                Types: bool
            
            kind:
                Optional Argument.
                Specifies a value for desired algorithm to be used. 
                Permitted values: 'quicksort', 'mergesort' or 'heapsort'
                Default value: 'quicksort'
                Types: str

        RETURNS:
            teradataml DataFrame
        
        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","scale_housing_test")
            >>> df = DataFrame.from_table('scale_housing_test')
            >>> df
                      id    price  lotsize  bedrooms  bathrms  stories
            types                                                     
            classic   14  36000.0   2880.0       3.0      1.0      1.0
            bungalow  11  90000.0   7200.0       3.0      2.0      1.0
            classic   15  37000.0   3600.0       2.0      1.0      1.0
            classic   13  27000.0   1700.0       3.0      1.0      2.0
            classic   12  30500.0   3000.0       2.0      1.0      1.0
            
            >>> df.sort_index()
                      id    price  lotsize  bedrooms  bathrms  stories
            types                                                     
            bungalow  11  90000.0   7200.0       3.0      2.0      1.0
            classic   13  27000.0   1700.0       3.0      1.0      2.0
            classic   12  30500.0   3000.0       2.0      1.0      1.0
            classic   14  36000.0   2880.0       3.0      1.0      1.0
            classic   15  37000.0   3600.0       2.0      1.0      1.0
            
            >>> df.sort_index(0)
                      id    price  lotsize  bedrooms  bathrms  stories
            types                                                     
            bungalow  11  90000.0   7200.0       3.0      2.0      1.0
            classic   13  27000.0   1700.0       3.0      1.0      2.0
            classic   12  30500.0   3000.0       2.0      1.0      1.0
            classic   14  36000.0   2880.0       3.0      1.0      1.0
            classic   15  37000.0   3600.0       2.0      1.0      1.0
            
            >>> df.sort_index(1, False) # here 'False' means DESCENDING for respective axis
                      stories    price  lotsize  id  bedrooms  bathrms
            types                                                     
            classic       1.0  36000.0   2880.0  14       3.0      1.0
            bungalow      1.0  90000.0   7200.0  11       3.0      2.0
            classic       1.0  37000.0   3600.0  15       2.0      1.0
            classic       2.0  27000.0   1700.0  13       3.0      1.0
            classic       1.0  30500.0   3000.0  12       2.0      1.0
            
            >>> df.sort_index(1, True, 'mergesort')
                      bathrms  bedrooms  id  lotsize    price  stories
            types                                                     
            classic       1.0       3.0  14   2880.0  36000.0      1.0
            bungalow      2.0       3.0  11   7200.0  90000.0      1.0
            classic       1.0       2.0  15   3600.0  37000.0      1.0
            classic       1.0       3.0  13   1700.0  27000.0      2.0
            classic       1.0       2.0  12   3000.0  30500.0      1.0

        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["axis", axis, True, (int, str), False, [0, 1, 'columns', 'rows']])
        awu_matrix.append(["ascending", ascending, True, (bool)])
        awu_matrix.append(["kind", kind, True, (str), False, ['quicksort', 'mergesort', 'heapsort']])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        try:
            if axis in (0, 'rows'):
                # For NoPI objects
                if self._index_label is None:
                    return self
                else:
                    return self.sort(self._index_label, ascending)
            else:
                colnames_list, coltypes_list = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)
                colnames_list = self.__get_sorted_list(colnames_list, ascending=ascending, kind=kind)
                return self.select(colnames_list)
        except TeradataMlException:
            raise

    def concat(self, other, join='OUTER', allow_duplicates=True, sort=False, ignore_index=False):
        """
        DESCRIPTION:
            Concatenates two teradataml DataFrames along the index axis.

        PARAMETERS:
            other:
                Required Argument.
                Specifies the other teradataml DataFrame with which the concatenation is to be performed.
                Types: teradataml DataFrame

            join:
                Optional Argument.
                Specifies how to handle indexes on columns axis.
                Supported values are:
                • 'OUTER': It instructs the function to project all columns from both the DataFrames.
                           Columns not present in either DataFrame will have a SQL NULL value.
                • 'INNER': It instructs the function to project only the columns common to both DataFrames.
                Default value: 'OUTER'
                Permitted values: 'INNER', 'OUTER'
                Types: str

            allow_duplicates:
                Optional Argument.
                Specifies if the result of concatenation can have duplicate rows.
                Default value: True
                Types: bool

            sort:
                Optional Argument.
                Specifies a flag to sort the columns axis if it is not already aligned when the join argument is set to 'outer'.
                Default value: False
                Types: bool
                
            ignore_index:
                Optional argument.
                Specifies whether to ignore the index columns in resulting DataFrame or not.
                If True, then index columns will be ignored in the concat operation.
                Default value: False
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradataml import load_example_data
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            >>> # Default options
            >>> df = DataFrame('admissions_train')
            >>> df1 = df[df.gpa == 4].select(['id', 'stats', 'masters', 'gpa'])
            >>> df1
                   stats masters  gpa
            id
            13  Advanced      no  4.0
            29    Novice     yes  4.0
            15  Advanced     yes  4.0
            >>> df2 = df[df.gpa < 2].select(['id', 'stats', 'programming', 'admitted'])
            >>> df2
                   stats programming admitted
            id
            24  Advanced      Novice        1
            19  Advanced    Advanced        0
            >>>
            >>> cdf = df1.concat(df2)
            >>> cdf
                   stats masters  gpa programming admitted
            id
            19  Advanced    None  NaN    Advanced        0
            24  Advanced    None  NaN      Novice        1
            13  Advanced      no  4.0        None     None
            29    Novice     yes  4.0        None     None
            15  Advanced     yes  4.0        None     None
            >>>
            >>> # join = 'inner'
            >>> cdf = df1.concat(df2, join='inner')
            >>> cdf
                   stats
            id
            19  Advanced
            24  Advanced
            13  Advanced
            29    Novice
            15  Advanced
            >>>
            >>> # allow_duplicates = True (default)
            >>> cdf = df1.concat(df2)
            >>> cdf
                   stats masters  gpa programming admitted
            id
            19  Advanced    None  NaN    Advanced        0
            24  Advanced    None  NaN      Novice        1
            13  Advanced      no  4.0        None     None
            29    Novice     yes  4.0        None     None
            15  Advanced     yes  4.0        None     None
            >>> cdf = cdf.concat(df2)
            >>> cdf
                   stats masters  gpa programming admitted
            id
            19  Advanced    None  NaN    Advanced        0
            13  Advanced      no  4.0        None     None
            24  Advanced    None  NaN      Novice        1
            24  Advanced    None  NaN      Novice        1
            19  Advanced    None  NaN    Advanced        0
            29    Novice     yes  4.0        None     None
            15  Advanced     yes  4.0        None     None
            >>>
            >>> # allow_duplicates = False
            >>> cdf = cdf.concat(df2, allow_duplicates=False)
            >>> cdf
                   stats masters  gpa programming admitted
            id
            19  Advanced    None  NaN    Advanced        0
            29    Novice     yes  4.0        None     None
            24  Advanced    None  NaN      Novice        1
            15  Advanced     yes  4.0        None     None
            13  Advanced      no  4.0        None     None
            >>>
            >>> # sort = True
            >>> cdf = df1.concat(df2, sort=True)
            >>> cdf
               admitted  gpa masters programming     stats
            id
            19        0  NaN    None    Advanced  Advanced
            24        1  NaN    None      Novice  Advanced
            13     None  4.0      no        None  Advanced
            29     None  4.0     yes        None    Novice
            15     None  4.0     yes        None  Advanced
            >>> 
            >>> # ignore_index = True
            >>> cdf = df1.concat(df2, ignore_index=True)
            >>> cdf
                  stats masters  gpa programming  admitted
            0  Advanced     yes  4.0        None       NaN
            1  Advanced    None  NaN    Advanced       0.0
            2    Novice     yes  4.0        None       NaN
            3  Advanced    None  NaN      Novice       1.0
            4  Advanced      no  4.0        None       NaN

        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["other", other, False, (DataFrame)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return concat([self, other], join, allow_duplicates, sort, ignore_index)

    def __validate_sum_of_list_for_sample_api(self, samples, arg_name):
        """
        Function to verify whether the given samples is
        having float elements and sum of list is greater than 1.

        PARAMETERS:
            samples:
                Required Argument.
                Specifies the list to validate.

            arg_name:
                Required Argument.
                Specifies the name of parameter to be validated.

        RETURNS:
            True, if the sum of elements of samples is less than 1.

        RAISES:
            TeradataMLException

        EXAMPLES:
            then_list = [0.5, 0.2, 0.1]
            __validate_sum_of_list_for_sample_api(then_list, "case_when_then")
        """

        # Raise exception if all elements in list are float and sum of list is 
        # greater than 1.
        if isinstance(samples, float) and samples > 1:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_ARG_VALUE, str(samples), arg_name,
                         "greater than 0 and less than or equal to 1"),
                         MessageCodes.INVALID_ARG_VALUE)
        if isinstance(samples, list) and all(isinstance(item, float) for item in samples) \
           and sum(samples) > 1:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_ARG_VALUE, str(samples), arg_name,
                         "a list having sum of all elements greater than 0 and less than or equal to 1" ),
                         MessageCodes.INVALID_ARG_VALUE)

        return True

    def __validate_len_of_list_for_sample_api(self, samples, arg_name):
        """
        Function to verify whether the given samples is
        having length greater than 16.

        PARAMETERS:
            samples:
                Required Argument.
                Specifies the list to validate.

            arg_name:
                Required Argument.
                Specifies the name of parameter to be validated.

        RETURNS:
            True, if the length of samples is less than 16.

        RAISES:
            TeradataMLException

        EXAMPLES:
            then_list = [0.5, 0.2, 0.1]
            __validate_len_of_list_for_sample_api(then_list, "case_when_then")
        """

        # Raise exception if the length of list is greater than 16.
        if len(samples) > 16:
           raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_ARG_VALUE, str(samples), arg_name,
                         "a list having less than or equal to 16 samples"),
                         MessageCodes.INVALID_ARG_VALUE)

        return True

    def __validate_number_of_rows_for_sample_api(self, samples, arg_name):
        """
        Function to verify whether the argument 'samples' is
        negative by itself or it has any negative numbers if
        the 'samples' is a list and to check if 'samples' specified
        as fractions has 0.0.

        PARAMETERS:
            samples:
                Required Argument.
                Specifies the parameter to validate.

            arg_name:
                Required Argument.
                Specifies the name of parameter to be validated.

        RETURNS:
            True, if samples itself is positive or all the elements in it
            are positive if 'samples' is a list and 'samples' is not 0.0 
            by itself or does not contain 0.0 if it is a list.

        RAISES:
            TeradataMLException

        EXAMPLES:
            then_list = [-0.5, 0.2, -0.1]
            __validate_number_of_rows_for_sample_api(then_list, "case_when_then")
        """

        # Raise exception if number of rows given are negative.
        if isinstance(samples, (int, float)) and samples < 0 or isinstance(samples, list) \
                     and any(item < 0 for item in samples):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_ARG_VALUE, str(samples), arg_name,
                         "greater than 0" ),
                         MessageCodes.INVALID_ARG_VALUE)

        # Raise exception if fractions specified as 0.
        if isinstance(samples,  float) and samples == 0 or (isinstance(samples, list) \
                     and all(isinstance(item, float) for item in samples) 
                     and any(item == 0 for item in samples)):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_ARG_VALUE, str(samples), arg_name,
                         "greater than 0" ),
                         MessageCodes.INVALID_ARG_VALUE)


        return True

    def sample(self, n = None, frac = None, replace = False, randomize = False, case_when_then = None, case_else = None):
        """
        DESCRIPTION:
            Allows to sample few rows from dataframe directly or based on conditions.
            Creates a new column 'sampleid' which has a unique id for each sample
            sampled, it helps to uniquely identify each sample.

        PARAMETERS:
            n:
                Required Argument, if neither of 'frac' and 'case_when_then' are specified.
                Specifies a set of positive integer constants that specifies the number of 
                rows to be sampled from the teradataml DataFrame.
                Example:
                    n = 10 or n = [10] or n = [10, 20, 30, 40]
                Default Value: None
                Types: int or list of ints.
                Note:
                    1. You should use only one of the following arguments: 'n', 'frac' and 'case_when_then'.
                    2. No more than 16 samples can be requested per count description.

            frac:
                Required Argument, if neither of 'n' and 'case_when_then' are specified.
                Specifies any set of unsigned floating point constant numbers in the half
                opened interval (0,1] that means greater than 0 and less than or equal to 1.
                It specifies the percentage of rows to be sampled from the teradataml DataFrame.
                Example:
                    frac = 0.4 or frac = [0.4] or frac = [0.2, 0.5]
                Default Value: None
                Types: float or list of floats.
                Note:
                    1. You should use only one of the following arguments: 'n', 'frac' and 'case_when_then'.
                    2. No more than 16 samples can be requested per count description.
                    3. Sum of elements in list should not be greater than 1 as total percentage cannot be
                       more than 100% and should not be less than or equal to 0.

            replace:
                Optional Argument.
                Specifies if sampling should be done with replacement or not.
                Default Value: False
                Types: bool

            randomize:
                Optional Argument.
                Specifies if sampling should be done across AMPs in Teradata or per AMP.
                Default Value: False
                Types: bool

            case_when_then :
                Required Argument, if neither of 'frac' and 'n' are specified.
                Specifies condition and number of samples to be sampled as key value pairs.
                Keys should be of type ColumnExpressions.
                Values should be either of type int, float, list of ints or list of floats.
                The following usage of key is not allowed:
                    case_when_then = {"gpa" > 2 : 2}
                The following operators are supported:
                      comparison: ==, !=, <, <=, >, >=
                      boolean: & (and), | (or), ~ (not), ^ (xor)
                Example :
                      case_when_then = {df.gpa > 2 : 2}
                      case_when_then = {df.gpa > 2 & df.stats == 'Novice' : [0.2, 0.3],
                                       df.programming == 'Advanced' : [10,20,30]}
                Default Value: None
                Types: dictionary
                Note:
                    1. You should use only one of the following arguments: 'n', 'frac' and 'case_when_then'.
                    2. No more than 16 samples can be requested per fraction description or count description.
                    3. If any value in dictionary is specified as list of floats then
                       sum of elements in list should not be greater than 1 as total percentage cannot be
                       more than 100% and should not be less than or equal to 0.

            case_else :
                Optional Argument.
                Specifies number of samples to be sampled from rows where none of the conditions in
                'case_when_then' are met.
                Example :
                    case_else = 10
                    case_else = [10,20]
                    case_else = [0.5]
                    case_else = [0.2,0.4]
                Default Value: None
                Types: int or float or list of ints or list of floats
                Note:
                    1. This argument can only be used with 'case_when_then'. 
                       If used otherwise, below error will raised.
                           'case_else' can only be used when 'case_when_then' is specified.
                    2. No more than 16 samples can be requested per fraction description 
                       or count description.
                    3. If case_else is list of floats then sum of elements in list should not be 
                       greater than 1 as total percentage cannot be more than 100% and should not 
                       be less than or equal to 0.

        RETURNS:
            teradataml DataFrame

        RAISES:
            1. ValueError - When columns of different dataframes are given in ColumnExpression.
                             or
                            When columns are given in string format and not ColumnExpression.
            2. TeradataMlException - If types of input parameters are mismatched.
            3. TypeError

        Examples:
            >>> from teradataml import *
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")

            # Print dataframe.
            >>> df
                  masters   gpa     stats programming admitted
               id
               13      no  4.00  Advanced      Novice        1
               26     yes  3.57  Advanced    Advanced        1
               5       no  3.44    Novice      Novice        0
               19     yes  1.98  Advanced    Advanced        0
               15     yes  4.00  Advanced    Advanced        1
               40     yes  3.95    Novice    Beginner        0
               7      yes  2.33    Novice      Novice        1
               22     yes  3.46    Novice    Beginner        0
               36      no  3.00  Advanced      Novice        0
               38     yes  2.65  Advanced    Beginner        1

            # Sample with only n argument.
            # Randomly samples 2 rows from the teradataml DataFrame.
            # As there is only 1 sample 'sampleid' is 1.
            >>> df.sample(n = 2)
                  masters   gpa     stats programming admitted SampleId
               id
               18     yes  3.81  Advanced    Advanced        1        1
               19     yes  1.98  Advanced    Advanced        0        1

            # Sample with multiple sample values for n.
            # Creates 2 samples with 2 and 1 rows each respectively.
            # There are 2 values(1,2) for 'sampleid' each for one sample.
            >>> df.sample(n = [2, 1])
                  masters   gpa     stats programming admitted SampleId
               id
               1      yes  3.95  Beginner    Beginner        0        1
               10      no  3.71  Advanced    Advanced        1        1
               11      no  3.13  Advanced    Advanced        1        2

            # Sample with only frac parameter.
            # Randomly samples 20% of total rows present in teradataml DataFrame.
            >>> df.sample(frac = 0.2)
                  masters   gpa     stats programming admitted SampleId
               id
               18     yes  3.81  Advanced    Advanced        1        1
               15     yes  4.00  Advanced    Advanced        1        1
               14     yes  3.45  Advanced    Advanced        0        1
               35      no  3.68    Novice    Beginner        1        1
               27     yes  3.96  Advanced    Advanced        0        1
               25      no  3.96  Advanced    Advanced        1        1
               10      no  3.71  Advanced    Advanced        1        1
               9       no  3.82  Advanced    Advanced        1        1

            # Sample with multiple sample values for frac.
            # Creates 2 samples each with 4% and 2% of total rows in teradataml DataFrame.
            >>> df.sample(frac = [0.04, 0.02])
                  masters   gpa     stats programming admitted SampleId
               id
               29     yes  4.00    Novice    Beginner        0        1
               19     yes  1.98  Advanced    Advanced        0        2
               11      no  3.13  Advanced    Advanced        1        1

            # Sample with n and replace and randomization.
            # Creates 2 samples with 2 and 1 rows respectively with possible redundant
            # sampling as replace is True and also selects rows from different AMPS as
            # randomize is True.
            >>> df.sample(n = [2, 1], replace = True, randomize = True)
                  masters   gpa     stats programming admitted SampleId
               id
               12      no  3.65    Novice      Novice        1        1
               39     yes  3.75  Advanced    Beginner        0        1
               20     yes  3.90  Advanced    Advanced        1        2

            # Sample with frac and replace and randomization.
            # Creates 2 samples with 4% and 2% of total rows in teradataml DataFrame
            # respectively with possible redundant sampling and also selects rows from different AMPS.
            >>> df.sample(frac = [0.04, 0.02], replace = True, randomize = True)
                  masters   gpa     stats programming admitted SampleId
               id
               7      yes  2.33    Novice      Novice        1        2
               30     yes  3.79  Advanced      Novice        0        1
               33      no  3.55    Novice      Novice        1        1

            # Sample with case_when_then.
            # Creates 2 samples with 1, 2 rows respectively from rows which satisfy df.gpa < 2
            # and 2.5% of rows from rows which satisfy df.stats == 'Advanced'.
            >>> df.sample(case_when_then={df.gpa < 2 : [1, 2], df.stats == 'Advanced' : 0.025})
                  masters   gpa     stats programming admitted SampleId
               id
               19     yes  1.98  Advanced    Advanced        0        1
               24      no  1.87  Advanced      Novice        1        1
               11      no  3.13  Advanced    Advanced        1        3

            # Sample with case_when_then and replace, randomize.
            # Creates 2 samples with 1, 2 rows respectively from rows which satisfy df.gpa < 2
            # and 2.5% of rows from rows which satisfy df.stats == 'Advanced' and selects rows
            # from different AMPs with replacement.
            >>> df.sample(replace = True, randomize = True, case_when_then={df.gpa < 2 : [1, 2],
                                                                           df.stats == 'Advanced' : 0.025})
                  masters   gpa     stats programming admitted SampleId
               id
               24      no  1.87  Advanced      Novice        1        1
               24      no  1.87  Advanced      Novice        1        2
               24      no  1.87  Advanced      Novice        1        2
               24      no  1.87  Advanced      Novice        1        2
               24      no  1.87  Advanced      Novice        1        2
               24      no  1.87  Advanced      Novice        1        1
               31     yes  3.50  Advanced    Beginner        1        3

            # Sample with case_when_then and case_else.
            # Creates 7 samples 2 with 1, 3 rows from rows which satisfy df.gpa > 2.
            # 1 sample with 5 rows from rows which satisify df.programming == 'Novice'.
            # 1 sample with 5 rows from rows which satisify df.masters == 'no'.
            # 1 sample with 1 row from rows which does not meet all above conditions.
            >>> df.sample(case_when_then = {df.gpa > 2 : [1, 3], df.stats == 'Novice' : [1, 2],
                                           df.programming == 'Novice' : 5, df.masters == 'no': 5}, case_else = 1)
                  masters   gpa     stats programming admitted SampleId
               id
               24      no  1.87  Advanced      Novice        1        5
               2      yes  3.76  Beginner    Beginner        0        1
               12      no  3.65    Novice      Novice        1        2
               38     yes  2.65  Advanced    Beginner        1        2
               36      no  3.00  Advanced      Novice        0        2
               19     yes  1.98  Advanced    Advanced        0        7

            # Sample with case_when_then and case_else
            # Creates 4 samples 2 with 1, 3 rows from rows which satisfy df.gpa > 2.
            # 2 samples with 2.5%, 5% of rows from all the rows which does not
            # meet condition df.gpa < 2.
            >>> df.sample(case_when_then = {df.gpa < 2 : [1, 3]}, case_else = [0.025, 0.05])
                  masters   gpa     stats programming admitted SampleId
               id
               9       no  3.82  Advanced    Advanced        1        4
               24      no  1.87  Advanced      Novice        1        1
               26     yes  3.57  Advanced    Advanced        1        4
               13      no  4.00  Advanced      Novice        1        3
               19     yes  1.98  Advanced    Advanced        0        1

            # Sample with case_when_then, case_else, replace, randomize
            # Creates 4 samples 2 with 1, 3 rows from rows which satisfy df.gpa > 2 and
            # 2 samples with 2.5%, 5% of rows from all the rows which does not
            # meet condition df.gpa < 2  with possible redundant replacement
            # and also selects rows from different AMPs
            >>> df.sample(case_when_then = {df.gpa < 2 : [1, 3]}, replace = True,
                        randomize = True, case_else = [0.025, 0.05])
                  masters   gpa     stats programming admitted SampleId
               id
               19     yes  1.98  Advanced    Advanced        0        1
               19     yes  1.98  Advanced    Advanced        0        2
               19     yes  1.98  Advanced    Advanced        0        2
               19     yes  1.98  Advanced    Advanced        0        2
               19     yes  1.98  Advanced    Advanced        0        2
               40     yes  3.95    Novice    Beginner        0        3
               3       no  3.70    Novice    Beginner        1        4
               19     yes  1.98  Advanced    Advanced        0        2
               19     yes  1.98  Advanced    Advanced        0        2
               19     yes  1.98  Advanced    Advanced        0        1
        """
        try:
            if n is not None and frac is not None:
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                           "n", "frac"),
                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)
            if n is not None and case_when_then is not None:
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                           "n", "case_when_then"),
                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)
            if frac is not None and case_when_then is not None:
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                           "frac", "case_when_then"),
                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)
            if case_when_then is None and case_else is not None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT,
                                                           "case_else", "case_when_then"),
                          MessageCodes.DEPENDENT_ARGUMENT)
            if n is None and frac is None and case_when_then is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT, 
                                                           "n or frac", "case_when_then"), 
                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

            # Argument validations
            awu_matrix = []
            awu_matrix.append(["n", n, True, (int, list)])
            awu_matrix.append(["frac", frac, True, (float, list)])
            awu_matrix.append(["replace", replace, True, (bool)])
            awu_matrix.append(["randomize", randomize, True, (bool)])
            awu_matrix.append(["case_when_then", case_when_then, True, (dict)])
            awu_matrix.append(["case_else", case_else, True, (int, float, list)])

            # Validate argument types
            _Validators._validate_function_arguments(awu_matrix)

            if self._metaexpr is None:
                msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
                raise TeradataMlException(msg, MessageCodes.TDMLDF_INFO_ERROR)

            list_of_fracs = []
            case_else_var = []
            if n is not None:
                # Processing by number of samples
                n = [n] if isinstance(n, int) else n
                # Let's perform validations for following:
                # Teradata Advanced SQL Engine Sample does not allows samples more than 16.
                # Check for the same for 'n'.
                self.__validate_len_of_list_for_sample_api(n, "n")

                # Number of rows specified to sample cannot be negative.
                # Check for the same for 'n'.
                self.__validate_number_of_rows_for_sample_api(n, "n")
                case_when_then = {}
                list_of_fracs = n

            elif frac is not None:
                # Processing for sampling by percentages.
                frac = [frac] if isinstance(frac, float) else frac
                # Validations for samples.
                self.__validate_len_of_list_for_sample_api(frac, "frac")

                # Teradata Advanced SQL Engine Sample does not allow sum of samples specified as
                # percentages to be greater than 1(because it exceeds 100%) or equals to 0.
                # Check for same for 'frac'.
                self.__validate_sum_of_list_for_sample_api(frac, "frac")
                self.__validate_number_of_rows_for_sample_api(frac, "frac")
                case_when_then = {}
                list_of_fracs  = frac

            else:
                # Creating OrderDict for 'case_when_then' so that order of keys doesn't change after
                # modifying while we are traversing dictionary.
                case_when_then = OrderedDict(case_when_then)
                if len(case_when_then) > 16:
                    raise TeradataMlException(
                          Messages.get_message(MessageCodes.TDML_SAMPLE_INVALID_NUMBER_OF_SAMPLES, "case_when_then"), 
                          MessageCodes.TDML_SAMPLE_INVALID_NUMBER_OF_SAMPLES)

                transformed_case_when_then = OrderedDict()
                for when_condition, then_sample_number in case_when_then.items():
                    # Validate conditions in case_when_then dictionary.
                    if not isinstance(when_condition, ColumnExpression):
                        raise ValueError("Condition in case_when_then should not be in "
                                         "string format for sample operation.")

                    # Make sure that ColumnExpression is not constituted from multiple DataFrames.
                    if when_condition.get_flag_has_multiple_dataframes():
                        raise ValueError("Combining Columns from different dataframes is "
                                         "unsupported for sample operation.")

                    # Validating values in the dict.
                    if isinstance(then_sample_number, int) or (isinstance(then_sample_number, list) \
                       and isinstance(then_sample_number[0], int)):
                        _Validators._validate_function_arguments([["Values in case_when_then", then_sample_number,
                                                     True, (int, list)]])
                    else:
                        _Validators._validate_function_arguments([["Values in case_when_then", then_sample_number,
                                                     True, ((float, list))]])

                    if isinstance(then_sample_number, list):
                        self.__validate_len_of_list_for_sample_api(then_sample_number, "case_when_then")

                    if not isinstance(then_sample_number, int):
                        self.__validate_sum_of_list_for_sample_api(then_sample_number, "case_when_then")

                    self.__validate_number_of_rows_for_sample_api(then_sample_number, "case_when_then")

                    clause_exp = when_condition.compile()
                    transformed_case_when_then[clause_exp] = case_when_then[when_condition]

                case_when_then = dict(transformed_case_when_then)

                # Processing case_else argument if given.
                if case_else is not None:
                    if isinstance(case_else, (int, float)):
                        case_else = [case_else]

                    case_else_awu_matrix = []
                    if isinstance(case_else[0], int):
                        case_else_awu_matrix.append(['Number of rows or fractions in case_else', 
                                                      case_else, True, (int, list)])
                    else:
                        case_else_awu_matrix.append(['Number of rows or fractions in case_else', 
                                                      case_else, True, (float, list)])

                    # Validating argument values for 'case_else'.
                    _Validators._validate_function_arguments(case_else_awu_matrix)

                    self.__validate_len_of_list_for_sample_api(case_else, "case_else")
                    self.__validate_sum_of_list_for_sample_api(case_else, "case_else")
                    self.__validate_number_of_rows_for_sample_api(case_else, "case_else")
                    case_else_var = case_else

            # Sample id column
            sample_column = "sampleid"
            selected_columns = self.columns
            if sample_column in selected_columns:
                selected_columns.remove(sample_column)
            selected_columns.append("{} as \"{}\"".format(sample_column, sample_column))
            df_columns_types = df_utils._get_required_columns_types_from_metaexpr(self._metaexpr)

            new_metaexpr_columns_types = OrderedDict()
            for column in self.columns:
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types, column, 
                                                    column, df_columns_types)
    
            # As we are creating new column name, adding it to new metadata dict
            new_metaexpr_columns_types[sample_column] = INTEGER()
            sample_node_id = self._aed_utils._aed_sample(self._nodeid, ",".join(selected_columns),
                                             list_of_fracs, replace, randomize, case_when_then, case_else_var)
            column_info = ((col_name, col_type) for col_name, col_type in 
                                                new_metaexpr_columns_types.items())
            # Get new metaexpr for sample_node_id
            new_metaexpr = UtilFuncs._get_metaexpr_using_columns(sample_node_id, column_info)
            return DataFrame._from_node(sample_node_id, new_metaexpr, self._index_label)

        except TeradataMlException:
            raise

        except ValueError:
            raise

        except TypeError:
            raise

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode) from err

    def show_query(self, full_query = False):
        """
        DESCRIPTION:
            Function returns underlying SQL for the teradataml DataFrame. It is the same 
            SQL that is used to view the data for a teradataml DataFrame.

        PARAMETERS:
            full_query:
                Optional Argument.
                Specifies if the complete query for the dataframe should be returned.
                When this parameter is set to True, query for the dataframe is returned
                with respect to the base dataframe's table (from_table() or from_query()) or from the
                output tables of analytical functions (if there are any in the workflow).
                This query may or may not be directly used to retrieve data for the dataframe upon
                which the function is called.
                When this parameter is not used, string returned is the query already used
                or will be used to retrieve data for the teradataml DataFrame.
                Default Value: False
                Types: bool

        RETURNS:
            String representing the underlying SQL query for the teradataml DataFrame.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> load_example_data("NaiveBayes", "nb_iris_input_train")
            >>> df = DataFrame.from_table("admissions_train")

            # Example 1: Show query on base (from_table) dataframe, with default option
            >>> df.show_query()
            'select * from "admissions_train"'

            # Example 2: Show query on base (from_query) dataframe, with default option
            >>> df_from_query = DataFrame.from_query("select masters, gpa from admissions_train")
            >>> df_from_query.show_query()
            'select masters, gpa from admissions_train'

            # Example 3: Show query on base (from_table) dataframe, with full_query option
            #            This will return same query as with default option because workflow
            #            only has one dataframe.
            >>> df.show_query(full_query = True)
            'select * from "admissions_train"'

            # Example 4: Show query on base (from_query) dataframe, with full_query option
            #            This will return same query as with default option because workflow
            #            only has one dataframe.
            >>> df_from_query = DataFrame.from_query("select masters, gpa from admissions_train")
            >>> df_from_query.show_query(full_query = True)
            'select masters, gpa from admissions_train'

            # Example 5: Show query used in a workflow demonstrating default and full_query options.

            # Workflow Step-1: Assign operation on base dataframe
            >>> df1 = df.assign(temp_column=admissions_train_df.gpa + admissions_train_df.admitted)

            # Workflow Step-2: Selecting columns from assign's result
            >>> df2 = df1.select(["masters", "gpa", "programming", "admitted"])

            # Workflow Step-3: Filtering on top of select's result
            >>> df3 = df2[df2.admitted > 0]

            # Workflow Step-4: Sampling 90% rows from filter's result
            >>> df4 = df3.sample(frac=0.9)

            # Show query with full_query option on df4. 
            # This will give full query upto base dataframe(df)
            >>> df4.show_query(full_query = True)
            'select masters,gpa,stats,programming,admitted,sampleid as "sampleid" from (
             select * from (select masters,gpa,stats,programming,admitted from (select id AS 
             id, masters AS masters, gpa AS gpa, stats AS stats, programming AS programming, 
             admitted AS admitted, gpa + admitted AS temp_column from "admissions_train") as
             temp_table) as temp_table where admitted > 0) as temp_table SAMPLE 0.9'

            # Show query with default option on df4. This will give same query as give in above case.
            >>> df4.show_query()
            'select masters,gpa,stats,programming,admitted,sampleid as "sampleid" from (select * 
             from (select masters,gpa,stats,programming,admitted from (select id AS id, masters 
             AS masters, gpa AS gpa, stats AS stats, programming AS programming, admitted AS admitted, 
             gpa + admitted AS temp_column from "admissions_train") as temp_table) as temp_table 
             where admitted > 0) as temp_table SAMPLE 0.9'

            # Executing intermediate dataframe df3
            >>> df2
              masters   gpa programming  admitted
            0      no  4.00      Novice         1
            1     yes  3.57    Advanced         1
            2      no  3.44      Novice         0
            3     yes  1.98    Advanced         0
            4     yes  4.00    Advanced         1
            5     yes  3.95    Beginner         0
            6     yes  2.33      Novice         1
            7     yes  3.46    Beginner         0
            8      no  3.00      Novice         0
            9     yes  2.65    Beginner         1

            # Show query with default option on df4. This will give query with respect 
            # to view/table created by the latest executed dataframe in the workflow (df2 in this scenario).
            # This is the query teradataml internally uses to retrieve data for dataframe df4, if executed
            # at this point.
            >>> df4.show_query()
            'select masters,gpa,stats,programming,admitted,sampleid as "sampleid" from (select * from
            "ALICE"."ml__select__1585722211621282" where admitted > 0) as temp_table SAMPLE 0.9'

            # Show query with full_query option on df4. This will still give the same full query upto base dataframe(df)
            >>> df4.show_query(full_query = True)
            'select masters,gpa,stats,programming,admitted,sampleid as "sampleid" from (select *
             from (select masters,gpa,stats,programming,admitted from (select id AS id, masters
             AS masters, gpa AS gpa, stats AS stats, programming AS programming, admitted AS admitted,
             gpa + admitted AS temp_column from "admissions_train") as temp_table) as temp_table
             where admitted > 0) as temp_table SAMPLE 0.9'

        """

        try:
            # Argument validations
            awu_matrix = []
            awu_matrix.append(["full_query", full_query, False, (bool)])
            # Validate argument types
            _Validators._validate_function_arguments(awu_matrix)

            node_id = self._nodeid

            if isinstance(self, (DataFrameGroupBy, DataFrameGroupByTime)):
                # If dataframe is either of type groupby or groupbytime 
                # then get it's parent dataframe nodeid and return queries 
                # for the same
                node_id = self._aed_utils._aed_get_parent_nodeids(self._nodeid)[0]

            queries = self._aed_utils._aed_show_query(node_id, query_with_reference_to_top=full_query)

            return queries[0][0]

        except TeradataMlException:
            raise

        except TypeError:
            raise

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode) from err

    def map_row(self,
                user_function,
                exec_mode='IN-DB',
                chunk_size=1000,
                num_rows=1000,
                **kwargs):
        """
        DESCRIPTION:
            Function to apply a user defined function to each row in the
            teradataml DataFrame, leveraging Vantage's Script Table Operator.

        PARAMETERS:
            user_function:
                Required Argument.
                Specifies the user defined function to apply to each row in
                the teradataml DataFrame.
                Types: function or functools.partial

                Notes:
                    * This can be either a lambda function, a regular python
                      function, or an object of functools.partial.
                    * The first argument (positional) to the user defined
                      function must be a row in a pandas DataFrame corresponding
                      to the teradataml DataFrame to which it is to be applied.
                    * A non-lambda function can be passed only when the user
                      defined function does not accept any arguments other than
                      the mandatory input - the input row.
                      A user can also use functools.partial and lambda functions
                      for the same, which are especially handy when:
                          * there is a need to pass positional and/or keyword
                            arguments (lambda).
                          * there is a need to pass keyword arguments only
                            (functool.partial).
                    * The return type of the user defined function must be one
                      of the following:
                          * numpy ndarray
                              * For a one-dimensional array, it is expected that
                                it has as many values as the number of expected
                                output columns.
                              * For a two-dimensional array, it is expected that
                                every array contained in the outer array has as
                                many values as the number of expected output
                                columns.
                          * pandas Series
                                This represents a row in the output, and the
                                number of values in it must be the same as the
                                number of expected output columns.
                          * pandas DataFrame
                                It is expected that a pandas DataFrame returned
                                by the "user_function" has the same number of
                                columns as the number of expected output columns.
                    * The return objects will be printed to the standard output
                      as required by Script using the 'quotechar' and 'delimiter'
                      values.
                    * The user function can also print the required output to
                      the standard output in the delimited (and possibly quoted)
                      format instead of returning an object of supported type.

            exec_mode:
                Optional Argument.
                Specifies the mode of execution for the user defined function.
                Permitted values:
                    * IN-DB: Execute the function on data in the teradataml
                             DataFrame in Vantage.
                    * LOCAL: Execute the function locally on sample data (at
                             most "num_rows" rows) from the teradataml
                             DataFrame.
                    * SANDBOX: Execute the function locally within a sandbox
                               environment on sample data (at most "num_rows"
                               rows) from the teradataml DataFrame.
                Default value: 'IN-DB'
                Types: str

            chunk_size:
                Optional Argument.
                Specifies the number of rows to be read in a chunk in each
                iteration using an iterator to apply the user defined function
                to each row in the chunk.
                Varying the value passed to this argument affects the
                performance and the memory utilization.
                Default value: 1000
                Types: int

            num_rows:
                Optional Argument.
                Specifies the maximum number of sample rows to use from the
                teradataml DataFrame to apply the user defined function to when
                "exec_mode" is 'LOCAL' or 'SANDBOX'.
                Default value: 1000
                Types: int

            returns:
                Optional Argument.
                Specifies the output column definition corresponding to the
                output of "user_function".
                When not specified, the function assumes that the names and
                types of the output columns are same as that of the input.
                Types: Dictionary specifying column name to
                       teradatasqlalchemy type mapping.

            delimiter:
                Optional Argument.
                Specifies a delimiter to use when reading columns from a row and
                writing result columns.
                Default value: '\t'
                Types: str with one character
                Notes:
                    * This argument cannot be same as "quotechar" argument.
                    * This argument cannot be a newline character i.e., '\n'.

            quotechar:
                Optional Argument.
                Specifies a character that forces all input and output of the
                user function to be quoted using this specified character.
                Using this argument enables the Advanced SQL Engine to
                distinguish between NULL fields and empty strings.
                A string with length zero is quoted, while NULL fields are not.
                If this character is found in the data, it will be escaped by a
                second quote character.
                Types: str with one character
                Notes:
                    * This argument cannot be same as "delimiter" argument.
                    * This argument cannot be a newline character i.e., '\n'.

            auth:
                Optional Argument.
                Specifies an authorization to use when running the
                "user_function".
                Types: str

            charset:
                Optional Argument.
                Specifies the character encoding for data.
                Permitted values: 'utf-16', 'latin'
                Types: str

            data_order_column:
                Optional Argument.
                Specifies the Order By columns for the teradataml DataFrame.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                This argument is used in both cases:
                "is_local_order = True" and "is_local_order = False".
                Types: str OR list of Strings (str)
                Note:
                    "is_local_order" must be set to 'True' when
                    "data_order_column" is used with "data_hash_column".

            is_local_order:
                Optional Argument.
                Specifies a boolean value to determine whether the input data is
                to be ordered locally or not.
                "data_order_column" with "is_local_order" set to 'False'
                specifies the order in which the values in a group, or
                partition, are sorted.
                When this argument is set to 'True', qualified rows on each AMP
                are ordered in preparation to be input to a table function.
                This argument is ignored, if "data_order_column" is None.
                Default value: False
                Types: bool
                Notes:
                    * "is_local_order" cannot be specified along with
                      "data_partition_column".
                    * When "is_local_order" is set to True, "data_order_column"
                      should be specified, and the columns specified in
                      "data_order_column" are used for local ordering.

            nulls_first:
                Optional Argument.
                Specifies a boolean value to determine whether NULLS are listed
                first or last during ordering.
                This argument is ignored, if "data_order_column" is None.
                NULLS are listed first when this argument is set to 'True', and
                last when set to 'False'.
                Default value: True
                Types: bool

            sort_ascending:
                Optional Argument.
                Specifies a boolean value to determine if the result set is to
                be sorted on the "data_order_column" column in ascending or
                descending order.
                The sorting is ascending when this argument is set to 'True',
                and descending when set to 'False'.
                This argument is ignored, if "data_order_column" is None.
                Default Value: True
                Types: bool

        RETURNS:
            1. teradataml DataFrame if exec_mode is "IN-DB".
            2. Pandas DataFrame if exec_mode is "LOCAL".

        RAISES:
             TypeError, TeradataMlException.

        EXAMPLES:
            >>> # This example uses the 'admissions_train' dataset, to increase
            >>> # the 'gpa' by a give percentage.
            >>> # Load the example data.
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> print(df)
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0

            >>> # Example 1:
            >>> # Create the user defined function to increase the 'gpa' by the
            >>> # percentage provided. Note that the input to and the output
            >>> # from the function is a pandas Series object.
            >>> def increase_gpa(row, p=20):
            ...     row['gpa'] = row['gpa'] + row['gpa'] * p/100
            ...     return row
            ...
            >>>
            >>> # Apply the user defined function to the DataFrame.
            >>> # Note that since the output of the user defined function
            >>> # expects the same columns with the same types, we can skip
            >>> # passing the 'returns' argument.
            >>> increase_gpa_20 = df.map_row(increase_gpa)
            >>>
            >>> # Print the result.
            >>> print(increase_gpa_20)
               masters    gpa     stats programming  admitted
            id
            22     yes  4.152    Novice    Beginner         0
            36      no  3.600  Advanced      Novice         0
            15     yes  4.800  Advanced    Advanced         1
            38     yes  3.180  Advanced    Beginner         1
            5       no  4.128    Novice      Novice         0
            17      no  4.596  Advanced    Advanced         1
            34     yes  4.620  Advanced    Beginner         0
            13      no  4.800  Advanced      Novice         1
            26     yes  4.284  Advanced    Advanced         1
            19     yes  2.376  Advanced    Advanced         0

            >>> # Example 2:
            >>> # Use the same user defined function with a lambda notation to
            >>> # pass the percentage, 'p = 40'.
            >>> increase_gpa_40 = df.map_row(lambda row: increase_gpa(row,
            ...                                                       p = 40))
            >>>
            >>> print(increase_gpa_40)
               masters    gpa     stats programming  admitted
            id
            22     yes  4.844    Novice    Beginner         0
            36      no  4.200  Advanced      Novice         0
            15     yes  5.600  Advanced    Advanced         1
            38     yes  3.710  Advanced    Beginner         1
            5       no  4.816    Novice      Novice         0
            17      no  5.362  Advanced    Advanced         1
            34     yes  5.390  Advanced    Beginner         0
            13      no  5.600  Advanced      Novice         1
            26     yes  4.998  Advanced    Advanced         1
            19     yes  2.772  Advanced    Advanced         0

            >>> # Example 3:
            >>> # Use the same user defined function with functools.partial to
            >>> # pass the percentage, 'p = 50'.
            >>> from functools import partial
            >>> increase_gpa_50 = df.map_row(partial(increase_gpa, p = 50))
            >>>
            >>> print(increase_gpa_50)
               masters    gpa     stats programming  admitted
            id
            13      no  6.000  Advanced      Novice         1
            26     yes  5.355  Advanced    Advanced         1
            5       no  5.160    Novice      Novice         0
            19     yes  2.970  Advanced    Advanced         0
            15     yes  6.000  Advanced    Advanced         1
            40     yes  5.925    Novice    Beginner         0
            7      yes  3.495    Novice      Novice         1
            22     yes  5.190    Novice    Beginner         0
            36      no  4.500  Advanced      Novice         0
            38     yes  3.975  Advanced    Beginner         1

            >>> # Example 4:
            >>> # Use a lambda function to increase the 'gpa' by 50 percent, and
            >>> # return numpy ndarray.
            >>> from numpy import asarray
            >>> inc_gpa_lambda = lambda row, p=20: asarray([row['id'],
            ...                                row['masters'],
            ...                                row['gpa'] + row['gpa'] * p/100,
            ...                                row['stats'],
            ...                                row['programming'],
            ...                                row['admitted']])
            >>> increase_gpa_100 = df.map_row(lambda row: inc_gpa_lambda(row,
            ...                                                          p=100))
            >>>
            >>> print(increase_gpa_100)
               masters   gpa     stats programming  admitted
            id
            13      no  8.00  Advanced      Novice         1
            26     yes  7.14  Advanced    Advanced         1
            5       no  6.88    Novice      Novice         0
            19     yes  3.96  Advanced    Advanced         0
            15     yes  8.00  Advanced    Advanced         1
            40     yes  7.90    Novice    Beginner         0
            7      yes  4.66    Novice      Novice         1
            22     yes  6.92    Novice    Beginner         0
            36      no  6.00  Advanced      Novice         0
            38     yes  5.30  Advanced    Beginner         1
        """
        # Input validation.
        # With 'apply', 'returns' and 'data' are optional, and 'exec-mode'
        # may have different values.
        arg_info_matrix = []
        arg_info_matrix.append(["data", self, False, (DataFrame)])
        arg_info_matrix.append(["exec_mode", exec_mode, True, (str), True,
                                TableOperatorConstants.EXEC_MODE.value])
        arg_info_matrix.append(["chunk_size", chunk_size, True, (int)])
        arg_info_matrix.append(["num_rows", num_rows, True, (int)])

        returns = kwargs.pop('returns', OrderedDict(zip(self.columns,
                                                        [col.type for col in
                                                         self._metaexpr.c])))
        # Add the "returns" for validation.
        arg_info_matrix.append(["returns", returns, False, (dict)])

        # The following arguments are specific to Script, and will be validated
        # by Script itself.
        delimiter = kwargs.pop('delimiter', '\t')
        quotechar = kwargs.pop('quotechar', None)
        data_order_column = kwargs.pop('data_order_column', None)
        is_local_order = kwargs.pop('is_local_order', False)
        nulls_first = kwargs.pop('nulls_first', True)
        sort_ascending = kwargs.pop('sort_ascending', True)
        auth = kwargs.pop('auth', None)
        charset = kwargs.pop('charset', None)

        # Check for other extra/unknown arguments.
        unknown_args = list(kwargs.keys())
        if len(unknown_args) > 0:
            raise TypeError(Messages.get_message(MessageCodes.UNKNOWN_ARGUMENT,
                                                 "map_row", unknown_args[0]))

        tbl_op_util = _TableOperatorUtils(arg_info_matrix, self, "map_row",
                                          user_function, exec_mode,
                                          chunk_size=chunk_size,
                                          data_partition_column=None,
                                          data_hash_column=None,
                                          data_order_column=data_order_column,
                                          is_local_order=is_local_order,
                                          nulls_first=nulls_first,
                                          sort_ascending=sort_ascending,
                                          returns=returns, delimiter=delimiter,
                                          quotechar=quotechar, auth=auth,
                                          charset=charset, num_rows=num_rows)

        return tbl_op_util.execute()

    def map_partition(self,
                      user_function,
                      exec_mode='IN-DB',
                      chunk_size=1000,
                      num_rows=1000,
                      data_partition_column=None,
                      data_hash_column=None,
                      **kwargs):
        """
        DESCRIPTION:
            Function to apply a user defined function to a group or partition of rows
            in the teradataml DataFrame, leveraging Vantage's Script Table Operator.

        PARAMETERS:
            user_function:
                Required Argument.
                Specifies the user defined function to apply to each group or partition of
                rows in the teradataml DataFrame.
                Types: function or functools.partial

                Notes:
                    * This can be either a lambda function, a regular python
                      function, or an object of functools.partial.
                    * The first argument (positional) to the user defined
                      function must be an iterator on the partition of rows
                      from the teradataml DataFrame represented as a pandas
                      DataFrame to which it is to be applied.
                    * A non-lambda function can be passed only when the user
                      defined function does not accept any arguments other than
                      the mandatory input - the iterator on the partition of
                      rows.
                      A user can also use functools.partial and lambda functions
                      for the same, which are especially handy when:
                          * there is a need to pass positional and/or keyword
                            arguments (lambda).
                          * there is a need to pass keyword arguments only
                            (functool.partial).
                    * The return type of the user defined function must be one
                      of the following:
                          * numpy ndarray
                              * For a one-dimensional array, it is expected that
                                it has as many values as the number of expected
                                output columns.
                              * For a two-dimensional array, it is expected that
                                every array contained in the outer array has as
                                many values as the number of expected output
                                columns.
                          * pandas Series
                                This represents a row in the output, and the
                                number of values in it must be the same as the
                                number of expected output columns.
                          * pandas DataFrame
                                It is expected that a pandas DataFrame returned
                                by the "user_function" has the same number of
                                columns as the number of expected output columns.
                    * The return objects will be printed to the standard output
                      as required by Script using the 'quotechar' and 'delimiter'
                      values.
                    * The user function can also print the required output to
                      the standard output in the delimited (and possibly quoted)
                      format instead of returning an object of supported type.

            exec_mode:
                Optional Argument.
                Specifies the mode of execution for the user defined function.
                Permitted values:
                    * IN-DB: Execute the function on data in the teradataml
                             DataFrame in Vantage.
                    * LOCAL: Execute the function locally on sample data (at
                             most "num_rows" rows) from the teradataml
                             DataFrame.
                    * SANDBOX: Execute the function locally within a sandbox
                               environment on sample data (at most "num_rows"
                               rows) from the teradataml DataFrame.
                Default value: 'IN-DB'
                Types: str

            chunk_size:
                Optional Argument.
                Specifies the number of rows to be read in a chunk in each
                iteration using the iterator that will be passed to the user
                defined function.
                Varying the value passed to this argument affects the
                performance and the memory utilization.
                Default value: 1000
                Types: int

            num_rows:
                Optional Argument.
                Specifies the maximum number of sample rows to use from the
                teradataml DataFrame to apply the user defined function to when
                "exec_mode" is 'LOCAL' or 'SANDBOX'.
                Default value: 1000
                Types: int

            data_partition_column:
                Optional Argument.
                Specifies the Partition By columns for the teradataml DataFrame.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)
                Note:
                    * "data_partition_column" cannot be specified along with
                      "data_hash_column".
                    * "data_partition_column" cannot be specified along with
                      "is_local_order = True".

            data_hash_column:
                Optional Argument.
                Specifies the column to be used for hashing.
                The rows in the teradataml DataFrame are redistributed to AMPs
                based on the hash value of the column specified.
                The "user_function" then runs once on each AMP.
                If there is no "data_partition_column", then the entire result
                set, delivered by the function, constitutes a single group or
                partition.
                Types: str
                Note:
                    * "data_hash_column" cannot be specified along with
                      "data_partition_column".
                    * "is_local_order" must be set to 'True' when
                      "data_order_column" is used with "data_hash_column".

            returns:
                Optional Argument.
                Specifies the output column definition corresponding to the
                output of "user_function".
                When not specified, the function assumes that the names and
                types of the output columns are same as that of the input.
                Types: Dictionary specifying column name to
                       teradatasqlalchemy type mapping.

            delimiter:
                Optional Argument.
                Specifies a delimiter to use when reading columns from a row and
                writing result columns.
                Default value: '\t'
                Types: str with one character
                Notes:
                    * This argument cannot be same as "quotechar" argument.
                    * This argument cannot be a newline character i.e., '\n'.

            quotechar:
                Optional Argument.
                Specifies a character that forces all input and output of the
                user function to be quoted using this specified character.
                Using this argument enables the Advanced SQL Engine to
                distinguish between NULL fields and empty strings. A string with
                length zero is quoted, while NULL fields are not.
                If this character is found in the data, it will be escaped by a
                second quote character.
                Types: str with one character
                Notes:
                    * This argument cannot be same as "delimiter" argument.
                    * This argument cannot be a newline character i.e., '\n'.

            auth:
                Optional Argument.
                Specifies an authorization to use when running the
                "user_function".
                Types: str

            charset:
                Optional Argument.
                Specifies the character encoding for data.
                Permitted values: 'utf-16', 'latin'
                Types: str

            data_order_column:
                Optional Argument.
                Specifies the Order By columns for the teradataml DataFrame.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                This argument is used in both cases:
                "is_local_order = True" and "is_local_order = False".
                Types: str OR list of Strings (str)
                Note:
                    "is_local_order" must be set to 'True' when
                    "data_order_column" is used with "data_hash_column".

            is_local_order:
                Optional Argument.
                Specifies a boolean value to determine whether the input data
                is to be ordered locally or not.
                "data_order_column" with "is_local_order" set to 'False'
                specifies the order in which the values in a group, or
                partition, are sorted.
                When this argument is set to 'True', qualified rows on each AMP
                are ordered in preparation to be input to a table function.
                This argument is ignored, if "data_order_column" is None.
                Default value: False
                Types: bool
                Notes:
                    * "is_local_order" cannot be specified along with
                      "data_partition_column".
                    * When "is_local_order" is set to True, "data_order_column"
                      should be specified, and the columns specified in
                      "data_order_column" are used for local ordering.

            nulls_first:
                Optional Argument.
                Specifies a boolean value to determine whether NULLS are listed
                first or last during ordering.
                This argument is ignored, if "data_order_column" is None.
                NULLS are listed first when this argument is set to 'True', and
                last when set to 'False'.
                Default value: True
                Types: bool

            sort_ascending:
                Optional Argument.
                Specifies a boolean value to determine if the result set is to
                be sorted on the "data_order_column" column in ascending or
                descending order.
                The sorting is ascending when this argument is set to 'True',
                and descending when set to 'False'.
                This argument is ignored, if "data_order_column" is None.
                Default Value: True
                Types: bool

        RETURNS:
            1. teradataml DataFrame if exec_mode is "IN-DB".
            2. Pandas DataFrame if exec_mode is "LOCAL".

        RAISES:
             TypeError, TeradataMlException.

        EXAMPLES:
            >>> # This example uses the 'admissions_train' dataset, calculates
            >>> # the average 'gpa' per partition based on the value in
            >>> # 'admitted' column.
            >>> # Load the example data.
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> print(df)
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0

            >>> # Example 1:
            >>> # Create the user defined function to calculate the average
            >>> # 'gpa', by reading data in chunks.
            >>> # Note that the function accepts a TextFileReader object to
            >>> # iterate on data in chunks.
            >>> # The return type of the function is a numpy ndarray.
            >>>
            >>> from numpy import asarray
            >>> def grouped_gpa_avg(rows):
            ...     admitted = None
            ...     row_count = 0
            ...     gpa = 0
            ...     for chunk in rows:
            ...         for _, row in chunk.iterrows():
            ...             row_count += 1
            ...             gpa += row['gpa']
            ...             if admitted is None:
            ...                 admitted = row['admitted']
            ...     if row_count > 0:
            ...         return asarray([admitted, gpa/row_count])
            ...
            >>>
            >>> # Apply the user defined function to the DataFrame.
            >>> from teradatasqlalchemy.types import INTEGER, FLOAT
            >>> returns = OrderedDict([('admitted', INTEGER()),
            ...                        ('avg_gpa', FLOAT())])
            >>> avg_gpa_1 = df.map_partition(grouped_gpa_avg,
            ...                              returns = returns,
            ...                              data_partition_column = 'admitted')
            >>>
            >>> # Print the result.
            >>> print(avg_gpa_1)
               admitted   avg_gpa
            0         1  3.533462
            1         0  3.557143

            >>> # Example 2:
            >>> # Create the user defined function to calculate the average
            >>> # 'gpa', by reading data at once into a pandas DataFrame.
            >>> # Note that the function accepts a TextFileReader object to
            >>> # iterate on data in chunks.
            >>> # The return type of the function is a pandas Series.
            >>> def grouped_gpa_avg_2(rows):
            ...     pdf = rows.read()
            ...     if pdf.shape[0] > 0:
            ...         return pdf[['admitted', 'gpa']].mean()
            ...
            >>> avg_gpa_2 = df.map_partition(grouped_gpa_avg_2,
            ...                              returns = returns,
            ...                              data_partition_column = 'admitted')
            >>>
            >>> print(avg_gpa_2)
               admitted   avg_gpa
            0         0  3.557143
            1         1  3.533462

            >>> # Example 3:
            >>> # The following example demonstrates using a lambda function to
            >>> # achieve the same result.
            >>> # Note that the the function is written to accept an iterator
            >>> # (TextFileReader object), and return the result which is of
            >>> # type pandas Series.
            >>> avg_gpa_3 = df.map_partition(lambda rows: grouped_gpa_avg(rows),
            ...                              returns = returns,
            ...                              data_partition_column = 'admitted')
            >>>
            >>> print(avg_gpa_3)
               admitted   avg_gpa
            0         0  3.557143
            1         1  3.533462

            >>> # Example 4:
            >>> # The following example demonstrates using a function that
            >>> # returns the input data.
            >>> # Note that the the function is written to accept an iterator
            >>> # (TextFileReader object), and returns the result which is of
            >>> # type pandas DataFrame.
            >>> def echo(rows):
            ...     pdf = rows.read()
            ...     if pdf is not None:
            ...         return pdf
            ...
            >>> echo_out = df.map_partition(echo,
            ...                             data_partition_column = 'admitted')
            >>> print(echo_out)
               masters   gpa     stats programming  admitted
            id
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            19     yes  1.98  Advanced    Advanced         0
            15     yes  4.00  Advanced    Advanced         1
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            40     yes  3.95    Novice    Beginner         0
        """
        # Input validation.
        # With 'apply', 'returns' and 'data' are optional, and 'exec-mode' may
        # have different values.
        arg_info_matrix = []
        arg_info_matrix.append(["data", self, False, (DataFrame)])
        arg_info_matrix.append(["exec_mode", exec_mode, True, (str), True,
                                TableOperatorConstants.EXEC_MODE.value])
        arg_info_matrix.append(["chunk_size", chunk_size, True, (int)])
        arg_info_matrix.append(["num_rows", num_rows, True, (int)])

        returns = kwargs.pop('returns', OrderedDict(zip(self.columns,
                                                        [col.type for col in
                                                         self._metaexpr.c])))
        # Add the "returns" for validation.
        arg_info_matrix.append(["returns", returns, False, (dict)])

        # Exactly one of 'data_partition_column' or 'data_hash_column' must be
        # provided.
        if (data_hash_column is not None and
            data_partition_column is not None) or \
                (data_hash_column is None and
                 data_partition_column is None):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                     "data_hash_column", "data_partition_column"
                                     ),
                MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

        # The following arguments are specific to Script, and will be validated
        # by Script itself.
        delimiter = kwargs.pop('delimiter', '\t')
        quotechar = kwargs.pop('quotechar', None)
        data_order_column = kwargs.pop('data_order_column', None)
        is_local_order = kwargs.pop('is_local_order', False)
        nulls_first = kwargs.pop('nulls_first', True)
        sort_ascending = kwargs.pop('sort_ascending', True)
        auth = kwargs.pop('auth', None)
        charset = kwargs.pop('charset', None)

        # Check for other extra/unknown arguments.
        unknown_args = list(kwargs.keys())
        if len(unknown_args) > 0:
            raise TypeError(Messages.get_message(MessageCodes.UNKNOWN_ARGUMENT,
                                                 "map_partition", unknown_args[0]))

        tbl_op_util = _TableOperatorUtils(arg_info_matrix, self, "map_partition",
                                          user_function, exec_mode,
                                          chunk_size=chunk_size,
                                          data_partition_column=data_partition_column,
                                          data_hash_column=data_hash_column,
                                          data_order_column=data_order_column,
                                          is_local_order=is_local_order,
                                          nulls_first=nulls_first,
                                          sort_ascending=sort_ascending,
                                          returns=returns, delimiter=delimiter,
                                          quotechar=quotechar, auth=auth,
                                          charset=charset, num_rows=num_rows)

        return tbl_op_util.execute()


class DataFrameGroupBy(DataFrame):
    """
    This class integrate GroupBy clause with AED.
    Updates AED node for DataFrame groupby object.

    """
    def __init__(self, nodeid, metaexpr, column_names_and_types, columns, groupbyexpr, column_list):
        """
        init() method for DataFrameGroupBy.

        PARAMETERS:
            nodeid:
                Required Argument.
                Specifies the input teradataml DataFrame nodeid.
                Types: str

            metaexpr:
                Required Argument.
                Specifies the input teradataml DataFrame metaexpr.
                Types: _MetaExpression

            column_names_and_types:
                Required Argument.
                Specifies the input teradataml DataFrame column_names_and_types.
                Types: List of tuple of column names and types

            columns:
                Required Argument.
                Specifies the input teradataml DataFrame columns.
                Types: List of Strings

            groupbyexpr:
                Required Argument.
                Specifies Group By Expression to be passed to AED API.
                Types: str

            column_list:
                Required Argument.
                Specifies list of columns provided by user to be part group by clause.
                Types: str or List of Strings

        RETURNS:
            teradataml DataFrameGroupBy instance
        """
        super(DataFrameGroupBy, self).__init__()
        self._nodeid = self._aed_utils._aed_groupby(nodeid, groupbyexpr)
        self._metaexpr = metaexpr
        self._column_names_and_types = column_names_and_types
        self._columns = columns
        self.groupby_column_list = column_list

    def _get_assign_allowed_types(self):
        """
        DESCRIPTION:
            Get allowed types for DataFrameGroupBy.assign() function.

        PARAMETERS:
            None.

        RETURNS:
            A tuple containing supported types for DataFrame.assign() operation.

        RAISES:
            None.

        EXAMPLES:
            allowed_types = self._get_assign_allowed_types()
        """
        from sqlalchemy.sql.functions import Function
        return (type(None), int, float, str, decimal.Decimal, Function)

    def _generate_assign_metaexpr_aed_nodeid(self, drop_columns, **kwargs):
        """
        DESCRIPTION:
            Function generates the MetaExpression and AED nodeid for DataFrameGroupBy.assign()
            function based on the inputs to the function.

        PARAMETERS:
            drop_columns:
                Optional Argument.
                This argument is ignored and all columns are dropped and only new columns
                and grouping columns are returned. This is unused argument.
                Types: bool

            kwargs:
                keyword, value pairs
                - keywords are the column names.
                - values can be:
                    * Column arithmetic expressions.
                    * int/float/string literals.
                    * DataFrameColumn a.k.a. ColumnExpression Functions.
                      (Visit DataFrameColumn Functions in Function reference guide for more
                      details)
                    * SQLAlchemy ClauseElements.
                      (Visit teradataml extension with SQLAlchemy in teradataml User Guide
                       and Function reference guide for more details)

        RETURNS:
            A tuple containing new MetaExpression and AED nodeid for the operation.

        RAISES:
            None.

        EXAMPLES:
            (new_meta, new_nodeid) = self._generate_assign_metaexpr_aed_nodeid(drop_columns, **kwargs)
        """
        # By default, we will drop old columns for DataFrameGroupBy.
        # Apply the assign expression.
        (new_meta, result) = self._metaexpr._assign(True, **kwargs)

        # Join the expressions in result.
        assign_expression = ', '.join(list(map(lambda x: x[1], result)))

        # Construct new MetaExpression with grouped columns in the list.
        new_column_names = []
        new_column_types = []
        for col in self.groupby_column_list:
            new_column_names.append(col)
            new_column_types.append(self[col].type)

        for col in new_meta.c:
            new_column_names.append(col.name)
            new_column_types.append(col.type)

        # No need to add group by columns to 'assign_expression'. AED will take care
        # of it while producing a query.
        new_nodeid = self._aed_utils._aed_aggregate(self._nodeid, assign_expression, "agg")

        new_meta = UtilFuncs._get_metaexpr_using_columns(new_nodeid,
                                                         zip(new_column_names,
                                                             new_column_types))

        return (new_meta, new_nodeid)


class DataFrameGroupByTime(DataFrame):
    """
    This class integrate Group By Time clause with AED.
    Updates AED node for DataFrame GROUP BY TIME object.

    """
    def __init__(self, nodeid, metaexpr, column_names_and_types, columns, groupby_value_expr, column_list, timebucket_duration,
                 value_expression = None, timecode_column = None, sequence_column = None, fill = None):
        """
        init() method for DataFrameGroupByTime.

        PARAMETERS:
            nodeid:
                Required Argument.
                Specifies the input teradataml DataFrame nodeid.
                Types: str

            metaexpr:
                Required Argument.
                Specifies the input teradataml DataFrame metaexpr.
                Types: _MetaExpression

            column_names_and_types:
                Required Argument.
                Specifies the input teradataml DataFrame column_names_and_types.
                Types: List of tuple of column names and types

            columns:
                Required Argument.
                Specifies the input teradataml DataFrame columns.
                Types: List of Strings

            groupby_value_expr:
                Required Argument.
                Specifies Group By Expression to be passed to AED API.
                Types: str

            column_list:
                Required Argument.
                Specifies list of columns provided by user to be part of GROUP BY TIME clause.
                Types: str or List of Strings

            timebucket_duration:
                Required Argument.
                Specifies the duration of each timebucket for aggregation and is used to
                assign each potential timebucket a unique number.
                Types: Str
                Example: MINUTES(23) which is equal to 23 Minutes
                         CAL_MONTHS(5) which is equal to 5 calendar months

            value_expression:
                Required Argument.
                Specifies a column or any expression involving columns (except for scalar subqueries).
                These expressions are used for grouping purposes not related to time.
                Types: str or List of Strings
                Example: col1 or ["col1", "col2"]

            timecode_column:
                Required Argument.
                Specifies a column expression that serves as the timecode for a non-PTI table.
                TD_TIMECODE is used implicitly for PTI tables, but can also be specified
                explicitly by the user with this parameter.
                Types: str

            sequence_column:
                Required Argument.
                Specifies a column expression (with an optional table name) that is the sequence number.
                For a PTI table, it can be TD_SEQNO or any other column that acts as a sequence number.
                For a non-PTI table, sequence_column is a column that plays the role of TD_SEQNO (because non-PTI tables
                do not have TD_SEQNO).
                Types: str

            fill:
                Required Argument.
                Specifies values for missing timebucket values.
                Types: str or int or float

        RETURNS:
            teradataml DataFrameGroupByTime instance

        """
        super(DataFrameGroupByTime, self).__init__()

        # Processing for GROUP BY TIME clasue.
        if groupby_value_expr is None:
            groupby_value_expr = ""

        if timecode_column is None:
            timecode_column = ""

        if sequence_column is None:
            sequence_column = ""

        if fill is None:
            fill = ""

        self._nodeid = self._aed_utils._aed_groupby_time(nodeid = nodeid, timebucket_duration = timebucket_duration,
                                                         value_expression = groupby_value_expr,
                                                         using_timecode = timecode_column, seqno_col = sequence_column,
                                                         fill = fill)

        # MetaExpression is same as that of parent.
        self._metaexpr = metaexpr
        # Columns are same as that of parent columns
        self._columns = columns
        # List of columns is GROUP BY TIME clause.
        self.groupby_column_list = column_list
        # Retrieve metadata information
        #   1. '_column_names_and_types',
        #   2. '_td_column_names_and_types' and
        #   3. '_td_column_names_and_sqlalchemy_types'
        self._get_metadata_from_metaexpr(self._metaexpr)

        # Saving attributes used while constructing Group By Time clause
        self._timebucket_duration = timebucket_duration
        self._value_expression = []
        if value_expression is not None:
            self._value_expression = value_expression
        self._timecode_column = timecode_column
        self._sequence_column = sequence_column
        self._fill = fill

    def bottom(self, number_of_values_to_column, with_ties=False):
        """
        DESCRIPTION:
            Returns the smallest number of values in the columns for each group, with or without ties.

            Note:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            number_of_values_to_column:
                Required Argument.
                Specifies a dictionary that accepts number of values to be selected for each column.
                Number of values is a key in the dictionary. Key should be any positive integer.
                Whereas value in the dictionary can be a column name or list of column names.
                Sometimes, value can also include a special character '*', instead of column name.
                This should be used only when one wants to return same number of values for all columns.
                Types: Dictionary
                Examples:
                    # Let's assume, a teradataml DataFrame has following columns:
                    #   col1, col2, col3, ..., colN

                    # For bottom() to return 2 values for column "col1":
                    number_of_values_to_column = {2: "col1"}

                    # For bottom() to return 2 values for column "col1" and 5 values for "col3":
                    number_of_values_to_column = {2: "col1", 5: "col3"}

                    # For bottom() to return 2 values for column "col1", "col2" and "col3":
                    number_of_values_to_column = {2: ["col1", "col2", "col3"]}

                    # Use cases for using '*' default value.
                    # For bottom() to return 2 values for all columns. In case, we need to return 2 values
                    # for each column in the DataFrame, then one can use '*'.
                    number_of_values_to_column = {2: "*"}

                    # For bottom() to return 2 values for column "col1" and "col3"
                    # and 5 values for rest of the columns:
                    number_of_values_to_column = {2: ["col1", "col3"], 5: "*"}

                    # We can use default value column character ('*') in list as well
                    # For bottom() to return 2 values for column "col1" and "col3"
                    # and 5 values for "col4" and rest of the columns:
                    number_of_values_to_column = {2: ["col1", "col3"], 5: ["col4", "*"]}

            with_ties:
                Optional Argument.
                Specifies a flag to decide whether to run bottom function with ties or not.
                BOTTOM WITH TIES implies that the rows returned include the specified number of rows in
                the ordered set for each timebucket. It includes any rows where the sort key value
                is the same as the sort key value in the last row that satisfies the specified number
                or percentage of rows. If this clause is omitted and ties are found, the earliest
                value in terms of timecode is returned.
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TypeError - If incorrect type of values passed to input argument.
            ValueError - If invalid value passed to the the argument.
            TeradataMLException
                1. If required argument 'number_of_values_to_column' is missing or None is passed.
                2. TDMLDF_AGGREGATE_FAILED - If bottom() operation fails to
                    generate the column-wise smallest number of values for the columns.

        EXAMPLES :
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])
            >>>

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> # DataFrame on sequenced PTI table
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq.head()
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            0       2014-01-06 08:00:00.000000        26        55         10.0  2016-02-26
            0       2014-01-06 08:08:59.999999        18        55          NaN  2015-06-18
            1       2014-01-06 09:02:25.122200        24        55         78.0  2015-12-24
            1       2014-01-06 09:01:25.122200        23        55         77.0  2015-11-23
            1       2014-01-06 09:02:25.122200        12        55         71.0  2014-12-12
            1       2014-01-06 09:03:25.122200        13        55         72.0  2015-01-13
            1       2014-01-06 09:01:25.122200        11        55         70.0  2014-11-11
            0       2014-01-06 08:10:00.000000        19        55         10.0  2015-07-19
            0       2014-01-06 08:09:59.999999        17        55         99.0  2015-05-17
            0       2014-01-06 08:10:00.000000        27        55        100.0  2016-03-27

            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['buoyid', 'timecode', 'temperature', 'salinity']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  temperature  salinity
            timecode
            2014-01-06 08:09:59.999999       0         99.0        55
            2014-01-06 08:10:00.000000       0         10.0        55
            2014-01-06 09:01:25.122200       1         70.0        55
            2014-01-06 09:01:25.122200       1         77.0        55
            2014-01-06 09:02:25.122200       1         71.0        55
            2014-01-06 09:03:25.122200       1         72.0        55
            2014-01-06 09:02:25.122200       1         78.0        55
            2014-01-06 08:10:00.000000       0        100.0        55
            2014-01-06 08:08:59.999999       0          NaN        55
            2014-01-06 08:00:00.000000       0         10.0        55

            ### Examples for bottom without ties ###
            #
            # Example 1: Executing bottom function on DataFrame created on non-sequenced PTI table.
            #
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="MINUTES(2)",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_grpby1.bottom(number_of_values_to_column).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                     530161       0                10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                     530162       0                 NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                     530163       0                 NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                     530164       0                 NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                     530165       0                99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166       0               100.0
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166       0                10.0
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     530191       1                70.0
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     530191       1                77.0
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                     530192       1                71.0

            #
            # Example 2: Executing bottom to select 2 values for all the columns in ocean_buoys_seq DataFrame
            #            on sequenced PTI table.
            #
            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="MINUTES(2)",
            ...                                                       value_expression="buoyid", fill="NULLS")
            >>> number_of_values_to_column = {2: "*"}
            >>> ocean_buoys_seq_grpby1.bottom(number_of_values_to_column).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom2TD_SEQNO  bottom2salinity  bottom2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                     530161       0             26.0             55.0                10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                     530162       0              NaN              NaN                 NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                     530163       0              NaN              NaN                 NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                     530164       0              NaN              NaN                 NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                     530165       0             17.0             55.0                99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166       0             19.0             55.0                10.0
            6  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     530191       1             11.0             55.0                70.0
            7  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                     530192       1             12.0             55.0                71.0
            8  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                     530221      44              4.0             55.0                43.0
            9  ('2014-01-06 10:02:00.000000+00:00', '2014-01-...                     530222      44              9.0             55.0                53.0

            #
            # Example 3: Executing bottom function on DataFrame created on NON-PTI table.
            #
            >>> ocean_buoys_nonpti_grpby1 = ocean_buoys_nonpti.groupby_time(timebucket_duration="MINUTES(2)",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby1.bottom(number_of_values_to_column).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                 NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                 NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                 NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0               100.0
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                10.0
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                70.0
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                77.0
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                71.0

            ### Examples for bottom with ties ###
            #
            # Example 4: Executing bottom with ties function on DataFrame created on non-sequenced PTI table.
            #
            >>> ocean_buoys_grpby2 = ocean_buoys.groupby_time(timebucket_duration="MINUTES(2)",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_grpby2.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                     530161       0                          10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                     530162       0                           NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                     530163       0                           NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                     530164       0                           NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                     530165       0                          99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166       0                         100.0
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166       0                          10.0
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     530191       1                          77.0
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     530191       1                          70.0
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                     530192       1                          71.0

            #
            # Example 5: Executing bottom with ties to select 2 values for temperature and 3 for rest of the columns in
            #            ocean_buoys DataFrame.
            #
            >>> ocean_buoys_grpby3 = ocean_buoys.groupby_time(timebucket_duration="MINUTES(2)", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature", 3:"*"}
            >>> ocean_buoys_grpby3.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  bottom_with_ties3buoyid  bottom_with_ties3salinity  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                     530161                      0.0                       55.0                          10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                     530162                      NaN                        NaN                           NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                     530163                      NaN                        NaN                           NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                     530164                      NaN                        NaN                           NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                     530165                      0.0                       55.0                          99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166                      0.0                       55.0                          10.0
            6  ('2014-01-06 08:12:00.000000+00:00', '2014-01-...                     530167                      NaN                        NaN                           NaN
            7  ('2014-01-06 08:14:00.000000+00:00', '2014-01-...                     530168                      NaN                        NaN                           NaN
            8  ('2014-01-06 08:16:00.000000+00:00', '2014-01-...                     530169                      NaN                        NaN                           NaN
            9  ('2014-01-06 08:18:00.000000+00:00', '2014-01-...                     530170                      NaN                        NaN                           NaN
            >>>

            #
            # Example 6: Executing bottom with ties function on DataFrame created on NON-PTI table.
            #
            >>> ocean_buoys_nonpti_grpby2 = ocean_buoys_nonpti.groupby_time(timebucket_duration="MINUTES(2)",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby2.bottom(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  bottom_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                          10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                           NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                           NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                           NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                          99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                          10.0
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                         100.0
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                          77.0
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                          70.0
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                          71.0
            >>>
            >>>
        """
        # Set the operation
        operation = "bottom"
        if with_ties:
            operation = "bottom with ties"

        # Argument validations
        awu_matrix = []
        awu_matrix.append(["number_of_values_to_column", number_of_values_to_column, False, (dict)])
        awu_matrix.append(["with_ties", with_ties, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        _Validators._validate_missing_required_arguments(awu_matrix)

        # Check if number_of_values_to_column dict is empty or not.
        if not number_of_values_to_column:
            raise ValueError(Messages.get_message(MessageCodes.ARG_EMPTY, "number_of_values_to_column"))

        return self.__process_time_series_aggregate_with_multi_input_arguments(number_of_values_to_column, operation)

    def delta_t(self, start_condition, end_condition):
        """
        DESCRIPTION:
            Calculates the time difference, or DELTA_T, between a starting and an ending event.
            The calculation is performed against a time-ordered time series data set.

            Note:
                1. This is the only Time Series Aggregate function that works with timebucket_duration as "*"
                   in groupby_time(), i.e., unbounded time.
                2. When using groupby_time() with unbounded time, the following rules apply to
                   the system virtual columns:
                    a. $TD_GROUP_BY_TIME: Always has a value of 1, since there is only one timebucket.
                    b. $TD_TIMECODE_RANGE: Composed of the first and last timecode values read for the group.
                Note that the data being evaluated in the filtering conditions (for example, the minimum and
                maximum temperature observation) must belong to the timecode value present in the same row
                of data. This is the expected behavior. However, this assumption can be violated when
                joining multiple tables together. It is possible to construct a query where the result of a
                join causes specific data points (for example, a temperature reading) to be present in a
                data row with a timecode that is not indicative of when that data point occurred.
                In such a scenario, it is highly likely that the results are not as expected, or are misleading.
                Vantage does not detect these types of queries, so one must make sure to preserve the
                correlation between data points and timecodes.

        PARAMETERS:
            start_condition:
                Required Argument.
                Specifies any supported filtering condition that defines the start of the time period for which
                you are searching.
                Types: str or ColumnExpression

            end_condition:
                Required Argument.
                Specifies any supported filtering condition that defines the end of the time period for which
                you are searching.
                Types:  str or ColumnExpression

        RETURNS:
            teradataml DataFrame

            Note:
                1. Function returns a column of PERIOD(TIMESTAMP WITH TIME ZONE) type (Vantage Data type)
                   composed of the start and end timecode, i.e., timecode column used for aggregation
                   of each start-end pair.
                2. One result is returned per complete start-end pair found within the
                   GROUP BY TIME window. The start-end pair process is as follows:
                    a. If the current source data meets the start condition, the current
                       timecode is saved as the start time.
                    b. If the current source data meets the end condition, and a saved start
                       timecode already exists, the start timecode is saved with the end timecode
                       encountered as a result pair.
                3. The processing algorithm implies that multiple results may be found in each group.
                4. If no start-end pair is encountered, no result row is returned.
                5. Any result of delta_t which has a delta less than 1 microsecond (including a delta of 0,
                   in the case of a result which comes from a single point in time) is automatically
                   rounded to 1 microsecond.
                   This is strictly enforced to match Period data type semantics in Vantage which dictate that a
                   starting and ending bound of a Period type may not be equivalent. The smallest granularity
                   supported in Vantage is the microsecond, so these results are rounded accordingly.

        RAISES:
            TypeError - If incorrect type of values passed to input argument.
            ValueError - If invalid value passed to the the argument.
            TeradataMLException - In case illegal conditions are passed

        EXAMPLES :
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti", "package_tracking_pti", "package_tracking"])
            >>>

            #
            # Example 1: Finding Time Elapsed between Shipping and Receiving an Item.
            #            Input data used for this example contains information about parcels
            #            sent by a delivery service.
            #

            #
            # Case 1: Using DataFrame on PTI Table and showcasing usage of unbounded time in grouping.
            #
            >>> # Create DataFrame on PTI table
            ... package_tracking_pti = DataFrame("package_tracking_pti")
            >>> package_tracking_pti.columns
            ['TD_TIMECODE', 'parcelnumber', 'status']
            >>> package_tracking_pti
                                         TD_TIMECODE                          status
            parcelnumber
            55            2016-10-15 10:00:00.000000       in transit to destination
            75            2016-10-15 16:30:00.000000          in transit to customer
            75            2016-10-15 08:00:00.000000         picked up from customer
            55            2016-10-15 09:10:00.000000    arrived at receiving station
            60            2016-10-15 10:45:00.000000    arrived at receiving station
            75            2016-10-15 17:00:00.000000           delivered to customer
            59            2016-10-15 08:05:00.000000         picked up from customer
            79            2016-10-15 08:05:00.000000         picked up from customer
            60            2016-10-15 09:20:00.000000         picked up from customer
            75            2016-10-15 16:10:00.000000  arrived at destination station
            >>>
            >>> # Execute groupby_time() using unbounded time for timebucket_duration.
            ... gbt = package_tracking_pti.groupby_time("*", "parcelnumber")
            >>> # Execute delta_t, with start and end conditions specified as String.
            ... start_condition = "status LIKE 'picked%up%customer'"
            >>> end_condition = "status LIKE 'delivered%customer'"
            >>> gbt.delta_t(start_condition, end_condition)
                                                  TIMECODE_RANGE  parcelnumber                                delta_t_td_timecode
            0  ('2012-01-01 00:00:00.000000+00:00', '9999-12-...            75  ('2016-10-15 08:00:00.000000-00:00', '2016-10-...
            1  ('2012-01-01 00:00:00.000000+00:00', '9999-12-...            55  ('2016-10-15 08:00:00.000000-00:00', '2016-10-...
            >>>

            #
            # Case 2: Using DataFrame on Non-PTI Table and showcasing usage of unbounded time in grouping.
            #
            >>> # Create DataFrame on Non-PTI table
            ... package_tracking = DataFrame("package_tracking")
            >>> package_tracking.columns
            ['parcelnumber', 'clock_time', 'status']
            >>> package_tracking
                                          clock_time                          status
            parcelnumber
            79            2016-10-15 08:05:00.000000         picked up from customer
            75            2016-10-15 09:10:00.000000    arrived at receiving station
            75            2016-10-15 10:00:00.000000       in transit to destination
            75            2016-10-15 16:10:00.000000  arrived at destination station
            75            2016-10-15 17:00:00.000000           delivered to customer
            80            2016-10-15 09:20:00.000000         picked up from customer
            59            2016-10-15 08:05:00.000000         picked up from customer
            75            2016-10-15 16:30:00.000000          in transit to customer
            75            2016-10-15 08:00:00.000000         picked up from customer
            60            2016-10-15 10:45:00.000000    arrived at receiving station
            >>>
            >>> # Execute groupby_time() using unbounded time for timebucket_duration.
            ... gbt = package_tracking.groupby_time("*", "parcelnumber", "clock_time")
            >>> # Execute delta_t, with start and end conditions specified as String.
            ... start_condition = "status LIKE 'picked%up%customer'"
            >>> end_condition = "status LIKE 'delivered%customer'"
            >>> gbt.delta_t(start_condition, end_condition)
                                                  TIMECODE_RANGE  parcelnumber                                delta_t_td_timecode
            0  ('1970-01-01 00:00:00.000000+00:00', '9999-12-...            75  ('2016-10-15 08:00:00.000000-00:00', '2016-10-...
            1  ('1970-01-01 00:00:00.000000+00:00', '9999-12-...            55  ('2016-10-15 08:00:00.000000-00:00', '2016-10-...
            >>>


            #
            # Example 2: Searching the Minimum and Maximum Observed Temperatures
            #            This example measures the time between minimum and maximum observed temperatures every
            #            30 minutes between 8:00 AM and 10:30 AM on each buoy.
            #

            #
            # Case 1: DataFrame on Non-sequenced PTI Table - specifying start condition and end condition as string
            #
            >>> # Create DataFrame
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> # Filter the data and grab all rows between  timestamp '2014-01-06 08:00:00' and '2014-01-06 10:30:00'
            ... ocean_buoys_dt = ocean_buoys[(ocean_buoys.TD_TIMECODE >= '2014-01-06 08:00:00') & (ocean_buoys.TD_TIMECODE < '2014-01-06 10:30:00')]
            >>>
            >>> # Let's get the minimum and maximum temperature within time range of 30 minutes
            ... df_min_max_temp1 = ocean_buoys_dt.groupby_time("MINUTES(30)", "buoyid", "TD_TIMECODE").agg({"temperature": ["min", "max"]})
            >>> # Join the dataframe with original 'ocean_buoys'
            ... df2_join1 = ocean_buoys.join(df_min_max_temp1, on="buoyid", how="inner", lsuffix="t1", rsuffix="t2")
            >>> gbt3 = df2_join1.groupby_time("DAYS(1)", "t1_buoyid", timecode_column="TD_TIMECODE")
            >>>
            >>> # Let's set the start and end conditions
            ... start_condition = "temperature = min_temperature"
            >>> end_condition = "temperature = max_temperature"
            >>> gbt3.delta_t(start_condition, end_condition)
                                                  TIMECODE_RANGE  GROUP BY TIME(DAYS(1))  t1_buoyid                                delta_t_td_timecode
            0  ('2014-01-06 00:00:00.000000+00:00', '2014-01-...                   16077         44  ('2014-01-06 10:00:26.122200-00:00', '2014-01-...
            1  ('2014-01-06 00:00:00.000000+00:00', '2014-01-...                   16077          1  ('2014-01-06 09:01:25.122200-00:00', '2014-01-...
            2  ('2014-01-06 00:00:00.000000+00:00', '2014-01-...                   16077          0  ('2014-01-06 08:00:00.000000-00:00', '2014-01-...
            >>>

            #
            # Case 2: Same example as that of above, just DataFrame on Sequenced PTI Table and
            #         specifying start condition and end condition as ColumnExpression.
            #
            >>> # Create DataFrame
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq.head()
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            0       2014-01-06 08:00:00.000000        26        55         10.0  2016-02-26
            0       2014-01-06 08:08:59.999999        18        55          NaN  2015-06-18
            1       2014-01-06 09:02:25.122200        24        55         78.0  2015-12-24
            1       2014-01-06 09:01:25.122200        23        55         77.0  2015-11-23
            1       2014-01-06 09:02:25.122200        12        55         71.0  2014-12-12
            1       2014-01-06 09:03:25.122200        13        55         72.0  2015-01-13
            1       2014-01-06 09:01:25.122200        11        55         70.0  2014-11-11
            0       2014-01-06 08:10:00.000000        19        55         10.0  2015-07-19
            0       2014-01-06 08:09:59.999999        17        55         99.0  2015-05-17
            0       2014-01-06 08:10:00.000000        27        55        100.0  2016-03-27
            >>> # Filter the data and grab all rows between  timestamp '2014-01-06 08:00:00' and '2014-01-06 10:30:00'
            ... ocean_buoys_seq_dt = ocean_buoys_seq[(ocean_buoys_seq.TD_TIMECODE >= '2014-01-06 08:00:00') & (ocean_buoys_seq.TD_TIMECODE < '2014-01-06 10:30:00')]
            >>>
            >>> # Let's get the minimum and maximum temperature within time range of 30 minutes
            ... df_min_max_temp2 = ocean_buoys_seq_dt.groupby_time("MINUTES(30)", "buoyid", "TD_TIMECODE").agg({"temperature": ["min", "max"]})
            >>> # Join the dataframe with original 'ocean_buoys'
            ... df2_join2 = ocean_buoys_seq.join(df_min_max_temp2, on="buoyid", how="inner", lsuffix="t1", rsuffix="t2")
            >>> gbt4 = df2_join2.groupby_time("DAYS(1)", "t1_buoyid", timecode_column="TD_TIMECODE")
            >>>
            >>> # Let's set the start and end conditions
            >>> start_condition = gbt4.temperature == gbt4.min_temperature
            >>> end_condition = gbt4.temperature == gbt4.max_temperature
            >>> gbt4.delta_t(start_condition, end_condition)
                                                  TIMECODE_RANGE  GROUP BY TIME(DAYS(1))  t1_buoyid                                delta_t_td_timecode
            0  ('2014-01-06 00:00:00.000000+00:00', '2014-01-...                   16077         44  ('2014-01-06 10:00:26.122200-00:00', '2014-01-...
            1  ('2014-01-06 00:00:00.000000+00:00', '2014-01-...                   16077          1  ('2014-01-06 09:01:25.122200-00:00', '2014-01-...
            2  ('2014-01-06 00:00:00.000000+00:00', '2014-01-...                   16077          0  ('2014-01-06 08:00:00.000000-00:00', '2014-01-...
            >>>
            
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["start_condition", start_condition, False, (str, ColumnExpression)])
        awu_matrix.append(["end_condition", end_condition, False, (str, ColumnExpression)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Note: Validation of start_condition and end_condition is not done here, as conditions can be anything
        #       (any SQL Expression going in where clause as str or any SQLColumnExpression). In case any issue
        #       with these arguments being incorrect, error will be raised from Vantage side.
        # Check for empty string, if arguments are of type String.
        if isinstance(start_condition, str):
            _Validators._validate_input_columns_not_empty(start_condition, "start_condition")

        if isinstance(end_condition, str):
            _Validators._validate_input_columns_not_empty(end_condition, "end_condition")

        # Set the operation
        operation = "delta_t"

        kwargs = {
            "start_condition": start_condition.compile() if isinstance(start_condition, ColumnExpression) else start_condition,
            "end_condition": end_condition.compile() if isinstance(end_condition, ColumnExpression) else end_condition
        }
        return self._get_dataframe_aggregate(operation=operation, **kwargs)

    def first(self, columns = None):
        """
        DESCRIPTION:
            Returns the oldest value, determined by the timecode, for each group. FIRST is a single-threaded function.
            In the event of a tie, such as simultaneous timecode values for a particular group, all tied results
            are returned. If a sequence number is present with the data, it can break a tie, assuming it is unique
            across identical timecode values.

            Note:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            columns:
                Optional Argument.
                Specifies a column name or list of column names on which first() operation
                must be run. By default oldest value is returned for all the compatible columns
                in a teradataml DataFrame.
                Types: str OR list of Strings (str)

        RETURNS:
            teradataml DataFrame object with first() operation performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If first() operation fails to
                return oldest value of columns in the teradataml DataFrame.

                Possible error message:
                Unable to perform 'first()' on the teradataml DataFrame.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the first() operation
                doesn't support all the columns in the teradataml DataFrame.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'first' operation.

        EXAMPLES :
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])
            >>>

            #
            # Example 1: Executing first function on DataFrame created on non-sequenced PTI table.
            #
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cd",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.first().sort(["TIMECODE_RANGE", "buoyid"])
            /mnt/c/Users/pp186043/GitHub_Repos/pyTeradata/teradataml/common/utils.py:398: VantageRuntimeWarning: [Teradata][teradataml](TDML_2086) Following warning raised from Vantage with warning code: 4001
            [Teradata Database] [Warning 4001] Time Series Auxiliary Cache Warning: Multiple results found for one or more Time Series aggregate functions in this query, but only one result was returned. To get all results, resubmit this query with these aggregates isolated.
              VantageRuntimeWarning)
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  buoyid  first_salinity  first_temperature
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       0              55                 10
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       1              55                 70
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       2              55                 80
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369      44              55                 43
            >>>

            #
            # Example 2: In Example 1, a VantageRuntimeWarning is raised as:
            #           "[Teradata Database] [Warning 4001] Time Series Auxiliary Cache Warning: Multiple results
            #            found for one or more Time Series aggregate functions in this query, but only one result
            #            was returned. To get all results, resubmit this query with these aggregates isolated."
            #
            #            This warning recommends to execute first() independently on each column, so that we will get
            #            all the results.
            #            To run first() on one single column we can pass column name as input. Let's run first()
            #            on 'temperature' column.
            #
            >>> ocean_buoys_grpby1.first('temperature')
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  buoyid  first_temperature
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       2                 80
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       0                 10
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369      44                 43
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       1                 77
            4  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       1                 70
            >>>

            #
            # Example 3: Executing first function on ocean_buoys_seq DataFrame created on sequenced PTI table.
            #            Table has few columns incompatible for first() operation 'dates' and 'TD_TIMECODE',
            #            while executing this first() incompatible columns are ignored.
            #
            >>> # DataFrame on sequenced PTI table
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq.head()
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            0       2014-01-06 08:00:00.000000        26        55         10.0  2016-02-26
            0       2014-01-06 08:08:59.999999        18        55          NaN  2015-06-18
            1       2014-01-06 09:02:25.122200        24        55         78.0  2015-12-24
            1       2014-01-06 09:01:25.122200        23        55         77.0  2015-11-23
            1       2014-01-06 09:02:25.122200        12        55         71.0  2014-12-12
            1       2014-01-06 09:03:25.122200        13        55         72.0  2015-01-13
            1       2014-01-06 09:01:25.122200        11        55         70.0  2014-11-11
            0       2014-01-06 08:10:00.000000        19        55         10.0  2015-07-19
            0       2014-01-06 08:09:59.999999        17        55         99.0  2015-05-17
            0       2014-01-06 08:10:00.000000        27        55        100.0  2016-03-27

            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="2cd",
            ...                                                       value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_seq_grpby1.first().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  buoyid  first_TD_SEQNO  first_salinity  first_temperature
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       0              26              55                 10
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       1              11              55                 70
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       2              14              55                 80
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369      22               1              25                 23
            4  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369      44               4              55                 43
            >>>

            #
            # Example 4: Executing first function on DataFrame created on NON-PTI table.
            #
            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['buoyid', 'timecode', 'temperature', 'salinity']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  temperature  salinity
            timecode
            2014-01-06 08:09:59.999999       0         99.0        55
            2014-01-06 08:10:00.000000       0         10.0        55
            2014-01-06 09:01:25.122200       1         70.0        55
            2014-01-06 09:01:25.122200       1         77.0        55
            2014-01-06 09:02:25.122200       1         71.0        55
            2014-01-06 09:03:25.122200       1         72.0        55
            2014-01-06 09:02:25.122200       1         78.0        55
            2014-01-06 08:10:00.000000       0        100.0        55
            2014-01-06 08:08:59.999999       0          NaN        55
            2014-01-06 08:00:00.000000       0         10.0        55

            >>> ocean_buoys_nonpti_grpby1 = ocean_buoys_nonpti.groupby_time(timebucket_duration="2cd",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> ocean_buoys_nonpti_grpby1.first().sort(["TIMECODE_RANGE", "buoyid"])
            /mnt/c/Users/pp186043/GitHub_Repos/pyTeradata/teradataml/common/utils.py:398: VantageRuntimeWarning: [Teradata][teradataml](TDML_2086) Following warning raised from Vantage with warning code: 4001
            [Teradata Database] [Warning 4001] Time Series Auxiliary Cache Warning: Multiple results found for one or more Time Series aggregate functions in this query, but only one result was returned. To get all results, resubmit this query with these aggregates isolated.
              VantageRuntimeWarning)
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  buoyid  first_salinity  first_temperature
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       0              55                 10
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       1              55                 70
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       2              55                 80
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039      44              55                 43
            >>>

            #
            # Example 5: Execute first() on a few select columns 'temperature' and 'salinity'.
            #
            >>> ocean_buoys_seq_grpby1.first(["temperature", "salinity"]).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  buoyid  first_temperature  first_salinity
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       0                 10              55
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       1                 70              55
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       2                 80              55
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369      22                 23              25
            4  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369      44                 43              55
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["columns", columns, True, (str, list), True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(columns, self._metaexpr)

        return self._get_dataframe_aggregate(operation = 'first', columns=columns)

    def last(self, columns=None):
        """
        DESCRIPTION:
            Returns the newest value, determined by the timecode, for each group. LAST is a single-threaded function.
            In the event of a tie, such as simultaneous timecode values for a particular group, all tied results
            are returned. If a sequence number is present with the data, it can break a tie, assuming it is unique
            across identical timecode values.

            Note:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            columns:
                Optional Argument.
                Specifies a column name or list of column names on which last() operation
                must be run. By default newest value is returned for all the compatible columns
                in a teradataml DataFrame.
                Types: str OR list of Strings (str)

        RETURNS:
            teradataml DataFrame object with last() operation performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If last() operation fails to
                return newest value of columns in the teradataml DataFrame.

                Possible error message:
                Unable to perform 'last()' on the teradataml DataFrame.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the last() operation
                doesn't support all the columns in the teradataml DataFrame.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'last' operation.

        EXAMPLES :
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])
            >>>

            #
            # Example 1: Executing last function on DataFrame created on non-sequenced PTI table.
            #
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.last().sort(["TIMECODE_RANGE", "buoyid"])
            /mnt/c/Users/pp186043/GitHub_Repos/pyTeradata/teradataml/common/utils.py:398: VantageRuntimeWarning: [Teradata][teradataml](TDML_2086) Following warning raised from Vantage with warning code: 4001
            [Teradata Database] [Warning 4001] Time Series Auxiliary Cache Warning: Multiple results found for one or more Time Series aggregate functions in this query, but only one result was returned. To get all results, resubmit this query with these aggregates isolated.
              VantageRuntimeWarning)
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  last_salinity  last_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0             55               100
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1             55                72
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2             55                82
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44             55                43
            >>>

            #
            # Example 2: In Example 1, a VantageRuntimeWarning is raised as:
            #           "[Teradata Database] [Warning 4001] Time Series Auxiliary Cache Warning: Multiple results
            #            found for one or more Time Series aggregate functions in this query, but only one result
            #            was returned. To get all results, resubmit this query with these aggregates isolated."
            #
            #            This warning recommends to execute last() independently on each column, so that we will get
            #            all the results.
            #            To run last() on one single column we can pass column name as input. Let's run last()
            #            on 'temperature' column.
            #
            >>> ocean_buoys_grpby1.last("temperature")
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  last_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                82
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0               100
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0                10
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                43
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                79
            5  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                72
            >>>

            #
            # Example 3: Executing last function on ocean_buoys_seq DataFrame created on sequenced PTI table.
            #            Table has few columns incompatible for last() operation 'dates' and 'TD_TIMECODE',
            #            while executing this last() incompatible columns are ignored.
            #
            >>> # DataFrame on sequenced PTI table
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq.head()
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            0       2014-01-06 08:00:00.000000        26        55         10.0  2016-02-26
            0       2014-01-06 08:08:59.999999        18        55          NaN  2015-06-18
            1       2014-01-06 09:02:25.122200        24        55         78.0  2015-12-24
            1       2014-01-06 09:01:25.122200        23        55         77.0  2015-11-23
            1       2014-01-06 09:02:25.122200        12        55         71.0  2014-12-12
            1       2014-01-06 09:03:25.122200        13        55         72.0  2015-01-13
            1       2014-01-06 09:01:25.122200        11        55         70.0  2014-11-11
            0       2014-01-06 08:10:00.000000        19        55         10.0  2015-07-19
            0       2014-01-06 08:09:59.999999        17        55         99.0  2015-05-17
            0       2014-01-06 08:10:00.000000        27        55        100.0  2016-03-27

            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="2cy",
            ...                                                       value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_seq_grpby1.last().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  last_TD_SEQNO  last_salinity  last_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0             27             55               100
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1             25             55                79
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2             16             55                82
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      22              1             25                23
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44              2             55                43
            >>>

            #
            # Example 4: Executing last function on DataFrame created on NON-PTI table.
            #
            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['buoyid', 'timecode', 'temperature', 'salinity']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  temperature  salinity
            timecode
            2014-01-06 08:09:59.999999       0         99.0        55
            2014-01-06 08:10:00.000000       0         10.0        55
            2014-01-06 09:01:25.122200       1         70.0        55
            2014-01-06 09:01:25.122200       1         77.0        55
            2014-01-06 09:02:25.122200       1         71.0        55
            2014-01-06 09:03:25.122200       1         72.0        55
            2014-01-06 09:02:25.122200       1         78.0        55
            2014-01-06 08:10:00.000000       0        100.0        55
            2014-01-06 08:08:59.999999       0          NaN        55
            2014-01-06 08:00:00.000000       0         10.0        55

            >>> ocean_buoys_nonpti_grpby1 = ocean_buoys_nonpti.groupby_time(timebucket_duration="2cy",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> ocean_buoys_nonpti_grpby1.last().sort(["TIMECODE_RANGE", "buoyid"])
            /mnt/c/Users/pp186043/GitHub_Repos/pyTeradata/teradataml/common/utils.py:398: VantageRuntimeWarning: [Teradata][teradataml](TDML_2086) Following warning raised from Vantage with warning code: 4001
            [Teradata Database] [Warning 4001] Time Series Auxiliary Cache Warning: Multiple results found for one or more Time Series aggregate functions in this query, but only one result was returned. To get all results, resubmit this query with these aggregates isolated.
              VantageRuntimeWarning)
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  buoyid  last_salinity  last_temperature
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       0             55               100
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       1             55                79
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       2             55                82
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039      44             55                43
            >>>

            #
            # Example 5: Executing last() on selected columns 'temperature' and 'salinity'
            #
            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time("2cy", 'buoyid')
            >>> ocean_buoys_seq_grpby1.last(['temperature', 'salinity'])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  last_temperature  last_salinity
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2                82             55
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44                43             55
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      22                23             25
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1                79             55
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0               100             55
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["columns", columns, True, (str, list), True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Checking each element in passed columns to be valid column in dataframe
        _Validators._validate_column_exists_in_dataframe(columns, self._metaexpr)

        return self._get_dataframe_aggregate(operation = 'last', columns=columns)

    def mad(self, constant_multiplier_columns=None):
        """
        DESCRIPTION:
            Median Absolute Deviation (MAD) returns the median of the set of values defined as
            the absolute value of the difference between each value and the median of all values
            in each group.
            This is a single-threaded function.

            Formula for computing MAD is as follows:
                MAD = b * Mi(|Xi - Mj(Xj)|)

                Where,
                    b       = Some numeric constant. Default value is 1.4826.
                    Mj(Xj)  = Median of the original set of values.
                    Xi      = The original set of values.
                    Mi      = Median of absolute value of the difference between
                              each value in Xi and the Median calculated in Mj(Xj).

            Note:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            constant_multiplier_columns:
                Optional Argument.
                Specifies a dictionary that accepts numeric values to be used as constant multiplier
                (b in the above formula) as key in the dictionary. Key should be any numeric value
                greater than or equal to 0. Whereas value in the dictionary can be a column name or
                list of column names. Sometimes, value can also include a special character '*',
                instead of column name. This should be used only when one wants to use same constant
                multiplier for all columns.
                Note:
                    For all numeric columns in teradataml DataFrame, that are not specified in this argument,
                    default value of constant_multiplier is used, which is 1.4826.
                Types: Dictionary
                Examples:
                    # Let's assume, a teradataml DataFrame has following columns:
                    #   col1, col2, col3, ..., colN

                    # Use 2 as constant multiplier for column "col1" and default for rest.
                    constant_multiplier_columns = {2: "col1"}

                    # Use 2.485 as constant multiplier for column "col1", 5 for "col3" and default for rest.
                    constant_multiplier_columns = {2.485: "col1", 5: "col3"}

                    # Use 2.485 as constant multiplier for column "col1", "col2" and "col3" and default for rest.
                    constant_multiplier_columns = {2.485: ["col1", "col2", "col3"]}

                    #
                    # Use cases for using '*' default value.
                    #
                    # Use 2.485 as constant multiplier for all columns. In this case, we do not need
                    # to specify all the columns, we can just use '*'.
                    constant_multiplier_columns = {2.485: "*"}

                    # Use 2.485 as constant multiplier for column "col1" and "col3"
                    # and 1.5 for rest of the columns:
                    constant_multiplier_columns = {2.485: ["col1", "col3"], 1.5: "*"}

                    # We can use default value column character ('*') in list as well
                    # Use 2.485 as constant multiplier for column "col1" and "col3"
                    # and 1.5 for "col4" and rest of the columns:
                    constant_multiplier_columns = {2.485: ["col1", "col3"], 1.5: ["col4", "*"]}

        RETURNS:
            teradataml DataFrame

        RAISES:
            TypeError - If incorrect type of values passed to input argument.
            ValueError - If invalid value passed to the the argument.
            TeradataMLException
                1. TDMLDF_AGGREGATE_FAILED - If mad() operation fails to
                    generate the column-wise median absolute deviation in the columns.

        EXAMPLES :
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])
            >>>

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> # DataFrame on sequenced PTI table
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq.head()
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            0       2014-01-06 08:00:00.000000        26        55         10.0  2016-02-26
            0       2014-01-06 08:08:59.999999        18        55          NaN  2015-06-18
            1       2014-01-06 09:02:25.122200        24        55         78.0  2015-12-24
            1       2014-01-06 09:01:25.122200        23        55         77.0  2015-11-23
            1       2014-01-06 09:02:25.122200        12        55         71.0  2014-12-12
            1       2014-01-06 09:03:25.122200        13        55         72.0  2015-01-13
            1       2014-01-06 09:01:25.122200        11        55         70.0  2014-11-11
            0       2014-01-06 08:10:00.000000        19        55         10.0  2015-07-19
            0       2014-01-06 08:09:59.999999        17        55         99.0  2015-05-17
            0       2014-01-06 08:10:00.000000        27        55        100.0  2016-03-27

            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['buoyid', 'timecode', 'temperature', 'salinity']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  temperature  salinity
            timecode
            2014-01-06 08:09:59.999999       0         99.0        55
            2014-01-06 08:10:00.000000       0         10.0        55
            2014-01-06 09:01:25.122200       1         70.0        55
            2014-01-06 09:01:25.122200       1         77.0        55
            2014-01-06 09:02:25.122200       1         71.0        55
            2014-01-06 09:03:25.122200       1         72.0        55
            2014-01-06 09:02:25.122200       1         78.0        55
            2014-01-06 08:10:00.000000       0        100.0        55
            2014-01-06 08:08:59.999999       0          NaN        55
            2014-01-06 08:00:00.000000       0         10.0        55

            #
            # Example 1: Calculate Median Absolute Deviation for all columns over 1 calendar day of
            #            timebucket duration. Use default constant multiplier.
            #            No need to pass any arguments.
            #
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="1cd",value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.mad()
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(1))  buoyid  mad_salinity  mad_temperature
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         737      44           0.0           0.0000
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         737       0           0.0          65.9757
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         737       2           0.0           1.4826
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         737       1           0.0           5.1891
            >>>

            #
            # Example 2: Calculate MAD values using 2 as constant multiplier for all the columns
            #            in ocean_buoys_seq DataFrame on sequenced PTI table.
            #
            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="CAL_DAYS(2)", value_expression="buoyid", fill="NULLS")
            >>> constant_multiplier_columns = {2: "*"}
            >>> ocean_buoys_seq_grpby1.mad(constant_multiplier_columns).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  buoyid  mad2TD_SEQNO  mad2salinity  mad2temperature
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       0           4.0           0.0             89.0
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       1          12.0           0.0              7.0
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369       2           2.0           0.0              2.0
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369      22           0.0           0.0              0.0
            4  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369      44           6.0           0.0              0.0
            >>>

            #
            # Example 3: Calculate MAD values for all the column in teradataml DataFrame created on NON-PTI table.
            #            Use default constant multiplier while calculating MAD value for all columns except
            #            column 'temperature', where 2.485 is used as constant multiplier.
            #
            >>> ocean_buoys_nonpti_grpby1 = ocean_buoys_nonpti.groupby_time(timebucket_duration="2cdays",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> constant_multiplier_columns = {2.485: "temperature"}
            >>> ocean_buoys_nonpti_grpby1.mad(constant_multiplier_columns).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  buoyid  mad2.485temperature  mad_salinity
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       0             110.5825           0.0
            1  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       1               8.6975           0.0
            2  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039       2               2.4850           0.0
            3  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                        8039      44               0.0000           0.0
            >>>

            #
            # Example 4: Calculate MAD values for all the column in teradataml DataFrame created on NON-PTI table.
            #            Use 3 as constant multiplier while calculating MAD value for all columns (buoyid and
            #            salinity), except column 'temperature', where 2 is used as constant multiplier.
            #
            >>> ocean_buoys_grpby3 = ocean_buoys.groupby_time(timebucket_duration="2cday", fill="NULLS")
            >>> constant_multiplier_columns = {2: "temperature", 3:"*"}
            >>> ocean_buoys_grpby3.mad(constant_multiplier_columns).sort(["TIMECODE_RANGE"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_DAYS(2))  mad3buoyid  mad3salinity  mad2temperature
            0  ('2014-01-06 00:00:00.000000-00:00', '2014-01-...                         369         6.0           0.0             27.0
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["constant_multiplier_columns", constant_multiplier_columns, True, (dict)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if constant_multiplier_columns is None:
            constant_multiplier_columns = {}

        return self.__process_time_series_aggregate_with_multi_input_arguments(constant_multiplier_columns, 'mad')

    def mode(self):
        """
        DESCRIPTION:
            Returns the column-wise mode of all values in each group. In the event of a tie between two or more
            values from column, a row per result is returned. mode() is a single-threaded function.

            Note:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            None.

        RETURNS:
            teradataml DataFrame object with mode() operation performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If mode() operation fails to
                return mode value of columns in the teradataml DataFrame.

                Possible error message:
                Unable to perform 'mode()' on the teradataml DataFrame.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the mode() operation
                doesn't support all the columns in the teradataml DataFrame.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'mode' operation.

        EXAMPLES :
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])
            >>>

            #
            # Example 1: Executing mode function on DataFrame created on non-sequenced PTI table.
            #
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="10m",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.mode().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(10))  buoyid  mode_temperature  mode_salinity
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                      106033       0                99             55
            1  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                      106033       0                10             55
            2  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                      106034       0               100             55
            3  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                      106034       0                10             55
            4  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                      106039       1                79             55
            5  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                      106039       1                70             55
            6  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                      106039       1                72             55
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                      106039       1                78             55
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                      106039       1                71             55
            9  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                      106039       1                77             55

            #
            # Example 2: Executing mode function on ocean_buoys_seq DataFrame created on sequenced PTI table.
            #            Table has few columns incompatible for mode() operation 'dates' and 'TD_TIMECODE',
            #            while executing this mode() incompatible columns are ignored.
            #
            >>> # DataFrame on sequenced PTI table
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq.head()
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            0       2014-01-06 08:00:00.000000        26        55         10.0  2016-02-26
            0       2014-01-06 08:08:59.999999        18        55          NaN  2015-06-18
            1       2014-01-06 09:02:25.122200        24        55         78.0  2015-12-24
            1       2014-01-06 09:01:25.122200        23        55         77.0  2015-11-23
            1       2014-01-06 09:02:25.122200        12        55         71.0  2014-12-12
            1       2014-01-06 09:03:25.122200        13        55         72.0  2015-01-13
            1       2014-01-06 09:01:25.122200        11        55         70.0  2014-11-11
            0       2014-01-06 08:10:00.000000        19        55         10.0  2015-07-19
            0       2014-01-06 08:09:59.999999        17        55         99.0  2015-05-17
            0       2014-01-06 08:10:00.000000        27        55        100.0  2016-03-27

            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="MINUTES(10)",
            ...                                                       value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_seq_grpby1.mode().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(10))  buoyid  mode_TD_SEQNO  mode_salinity  mode_temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                      106033       0             17             55                10
            1  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                      106034       0             19             55                10
            2  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                      106039       1             11             55                70
            3  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                      106045      44              7             55                43
            4  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                      106045      44             21             55                43
            5  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                      106045      44             20             55                43
            6  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                      106045      44              4             55                43
            7  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                      106045      44              9             55                43
            8  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                      106045      44              8             55                43
            9  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                      106045      44              5             55                43

            #
            # Example 3: Executing mode function on DataFrame created on NON-PTI table.
            #
            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['buoyid', 'timecode', 'temperature', 'salinity']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  temperature  salinity
            timecode
            2014-01-06 08:09:59.999999       0         99.0        55
            2014-01-06 08:10:00.000000       0         10.0        55
            2014-01-06 09:01:25.122200       1         70.0        55
            2014-01-06 09:01:25.122200       1         77.0        55
            2014-01-06 09:02:25.122200       1         71.0        55
            2014-01-06 09:03:25.122200       1         72.0        55
            2014-01-06 09:02:25.122200       1         78.0        55
            2014-01-06 08:10:00.000000       0        100.0        55
            2014-01-06 08:08:59.999999       0          NaN        55
            2014-01-06 08:00:00.000000       0         10.0        55

            >>> ocean_buoys_nonpti_grpby1 = ocean_buoys_nonpti.groupby_time(timebucket_duration="10minutes",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> ocean_buoys_nonpti_grpby1.mode().sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(10))  buoyid  mode_temperature  mode_salinity
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                     2314993       0                99             55
            1  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                     2314993       0                10             55
            2  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     2314994       0                10             55
            3  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     2314994       0               100             55
            4  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     2314999       1                70             55
            5  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     2314999       1                71             55
            6  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     2314999       1                72             55
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     2314999       1                77             55
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     2314999       1                78             55
            9  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     2314999       1                79             55

        """
        return self._get_dataframe_aggregate(operation='mode')

    def percentile(self, percentile, distinct=False, interpolation="LINEAR"):
        """
        DESCRIPTION:
            Function returns the value which represents the desired percentile from each group.
            The result value is determined by the desired index (di) in an ordered list of values.
            The following equation is for the di:
                di = (number of values in group - 1) * percentile/100
            When di is a whole number, that value is the returned result.
            The di can also be between two data points, i and j, where i<j. In that case, the result
            is interpolated according to the value specified in interpolation argument.
            Note:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            percentile:
                Required Argument.
                Specifies the desired percentile value to calculate.
                It should be between 0 and 1, both inclusive.
                Types: int or float

            distinct:
                Optional Argument.
                Specifies whether to exclude duplicate values while calculating
                the percentile value.
                Default Values: False
                Types: bool

            interpolation:
                Optional Argument.
                Specifies the interpolation type to use to interpolate the result value when the
                desired result lies between two data points.
                The desired result lies between two data points, i and j, where i<j. In this case,
                the result is interpolated according to the permitted values.
                Permitted Values: "LINEAR", "LOW", "HIGH", "NEAREST", "MIDPOINT"
                    * LINEAR: Linear interpolation.
                        The result value is computed using the following equation:
                            result = i + (j - i) * (di/100)MOD 1
                        Specify by passing "LINEAR" as string to this parameter.
                    * LOW: Low value interpolation.
                        The result value is equal to i.
                        Specify by passing "LOW" as string to this parameter.
                    * HIGH: High value interpolation.
                        The result value is equal to j.
                        Specify by passing "HIGH" as string to this parameter.
                    * NEAREST: Nearest value interpolation.
                        The result value is i if (di/100 )MOD 1 <= .5; otherwise, it is j.
                        Specify by passing "NEAREST" as string to this parameter.
                    * MIDPOINT: Midpoint interpolation.
                         The result value is equal to (i+j)/2.
                         Specify by passing "MIDPOINT" as string to this parameter.
                Default Values: "LINEAR"
                Types: str

        RETURNS:
            teradataml DataFrame.

        RAISES:
            TypeError - If incorrect type of values passed to input argument.
            ValueError - If invalid value passed to the the argument.
            TeradataMLException - TDMLDF_AGGREGATE_FAILED - If percentile() operation fails to
                                  generate the column-wise percentile values in the columns.

        EXAMPLES:
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])
            >>>

            #
            # Example 1: Executing percentile() function on DataFrame created on non-sequenced PTI table.
            #            Calculate the 25th percentile value for all numeric columns using default
            #            values, i.e., consider all rows (duplicate rows as well) and linear
            #            interpolation while computing the percentile value.
            #
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['TD_TIMECODE', 'buoyid', 'salinity', 'temperature']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  salinity  temperature
            buoyid
            0       2014-01-06 08:10:00.000000        55        100.0
            0       2014-01-06 08:08:59.999999        55          NaN
            1       2014-01-06 09:01:25.122200        55         77.0
            1       2014-01-06 09:03:25.122200        55         79.0
            1       2014-01-06 09:01:25.122200        55         70.0
            1       2014-01-06 09:02:25.122200        55         71.0
            1       2014-01-06 09:03:25.122200        55         72.0
            0       2014-01-06 08:09:59.999999        55         99.0
            0       2014-01-06 08:00:00.000000        55         10.0
            0       2014-01-06 08:10:00.000000        55         10.0
            >>>
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="10m", value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.percentile(0.25).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(10))  buoyid  percentile_salinity  percentile_temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                      106033       0                 55.0                   32.25
            1  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                      106034       0                 55.0                   32.50
            2  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                      106039       1                 55.0                   71.25
            3  ('2014-01-06 10:00:00.000000+00:00', '2014-01-...                      106045      44                 55.0                   43.00
            4  ('2014-01-06 10:10:00.000000+00:00', '2014-01-...                      106046      44                 55.0                   43.00
            5  ('2014-01-06 10:20:00.000000+00:00', '2014-01-...                      106047      44                  NaN                     NaN
            6  ('2014-01-06 10:30:00.000000+00:00', '2014-01-...                      106048      44                 55.0                   43.00
            7  ('2014-01-06 10:40:00.000000+00:00', '2014-01-...                      106049      44                  NaN                     NaN
            8  ('2014-01-06 10:50:00.000000+00:00', '2014-01-...                      106050      44                 55.0                   43.00
            9  ('2014-01-06 21:00:00.000000+00:00', '2014-01-...                      106111       2                 55.0                   80.50
            >>>

            #
            # Example 2: Executing percentile() function on ocean_buoys_seq DataFrame created on
            #            sequenced PTI table.
            #            Calculate the 50th percentile value for all numeric columns.
            #            To calculate percentile consider all rows (duplicate rows as well) and
            #            use "MIDPOINT" interpolation while computing the percentile value.
            #
            >>> # DataFrame on sequenced PTI table
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq.head()
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            0       2014-01-06 08:00:00.000000        26        55         10.0  2016-02-26
            0       2014-01-06 08:08:59.999999        18        55          NaN  2015-06-18
            1       2014-01-06 09:02:25.122200        24        55         78.0  2015-12-24
            1       2014-01-06 09:01:25.122200        23        55         77.0  2015-11-23
            1       2014-01-06 09:02:25.122200        12        55         71.0  2014-12-12
            1       2014-01-06 09:03:25.122200        13        55         72.0  2015-01-13
            1       2014-01-06 09:01:25.122200        11        55         70.0  2014-11-11
            0       2014-01-06 08:10:00.000000        19        55         10.0  2015-07-19
            0       2014-01-06 08:09:59.999999        17        55         99.0  2015-05-17
            0       2014-01-06 08:10:00.000000        27        55        100.0  2016-03-27
            >>>
            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="1cy", value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_seq_grpby1.percentile(0.5, interpolation="MIDPOINT").sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(1))  buoyid  percentile_TD_SEQNO  percentile_salinity  percentile_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                            3       0                 22.5                 55.0                    54.5
            1  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                            3       1                 18.0                 55.0                    74.5
            2  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                            3       2                 15.5                 55.0                    81.5
            3  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                            3      22                  1.0                 25.0                    23.0
            4  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                            3      44                  7.5                 55.0                    48.0
            >>>

            #
            # Example 3: Executing percentile() function for all numeric columns in
            #            teradataml DataFrame created on NON-PTI table.
            #            Calculate the 75th percentile value, exclude duplicate rows and
            #            "LOW" as interpolation.
            #
            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['timecode', 'buoyid', 'salinity', 'temperature']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  salinity  temperature
            timecode
            2014-01-06 08:09:59.999999       0        55         99.0
            2014-01-06 08:10:00.000000       0        55        100.0
            2014-01-06 09:01:25.122200       1        55         70.0
            2014-01-06 09:01:25.122200       1        55         77.0
            2014-01-06 09:02:25.122200       1        55         71.0
            2014-01-06 09:03:25.122200       1        55         72.0
            2014-01-06 09:02:25.122200       1        55         78.0
            2014-01-06 08:10:00.000000       0        55         10.0
            2014-01-06 08:08:59.999999       0        55          NaN
            2014-01-06 08:00:00.000000       0        55         10.0
            >>>
            >>> ocean_buoys_nonpti_grpby1 = ocean_buoys_nonpti.groupby_time(timebucket_duration="1cy", value_expression="buoyid", timecode_column="timecode", fill="NULLS")
            >>> ocean_buoys_nonpti_grpby1.percentile(0.75, distinct=True, interpolation="low").sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(1))  buoyid  percentile_salinity  percentile_temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                           45       0                 55.0                    99.0
            1  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                           45       1                 55.0                    77.0
            2  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                           45       2                 55.0                    81.0
            3  ('2014-01-01 00:00:00.000000-00:00', '2015-01-...                           45      44                 55.0                    55.0
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["percentile", percentile, False, (int, float)])
        awu_matrix.append(["distinct", distinct, True, (bool)])
        awu_matrix.append(["interpolation", interpolation, True, (str), True,
                           ["LINEAR", "LOW", "HIGH", "NEAREST", "MIDPOINT"]])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        _Validators._validate_missing_required_arguments(awu_matrix)

        if distinct is None:
            distinct = False

        if interpolation is None:
            interpolation = "LINEAR"

        if percentile < 0 or percentile > 1:
            raise ValueError(Messages.get_message(MessageCodes.TDMLDF_LBOUND_UBOUND).format("percentile",
                                                                                            "or equal to 0", "1"))

        return self._get_dataframe_aggregate(operation='percentile', percentile=percentile,
                                             distinct=distinct, interpolation=interpolation)

    def top(self, number_of_values_to_column, with_ties=False):
        """
        DESCRIPTION:
            Returns the largest number of values in the columns for each group, with or without ties.
            TOP is a single-threaded function.

            Note:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.

        PARAMETERS:
            number_of_values_to_column:
                Required Argument.
                Specifies a dictionary that accepts number of values to be selected for each column.
                Number of values is a key in the dictionary. Key should be any positive integer.
                Whereas value in the dictionary can be a column name or list of column names.
                Sometimes, value can also include a special character '*', instead of column name.
                This should be used only when one wants to return same number of values for all columns.
                Types: Dictionary
                Examples:
                    # Let's assume, a teradataml DataFrame has following columns:
                    #   col1, col2, col3, ..., colN

                    # For top() to return 2 values for column "col1":
                    number_of_values_to_column = {2: "col1"}

                    # For top() to return 2 values for column "col1" and 5 values for "col3":
                    number_of_values_to_column = {2: "col1", 5: "col3"}

                    # For top() to return 2 values for column "col1", "col2" and "col3":
                    number_of_values_to_column = {2: ["col1", "col2", "col3"]}

                    # Use cases for using '*' default value.
                    # For top() to return 2 values for all columns. In case, we need to return 2 values
                    # for each column in the DataFrame, then one can use '*'.
                    number_of_values_to_column = {2: "*"}

                    # For top() to return 2 values for column "col1" and "col3"
                    # and 5 values for rest of the columns:
                    number_of_values_to_column = {2: ["col1", "col3"], 5: "*"}

                    # We can use default value column character ('*') in list as well
                    # For top() to return 2 values for column "col1" and "col3"
                    # and 5 values for "col4" and rest of the columns:
                    number_of_values_to_column = {2: ["col1", "col3"], 5: ["col4", "*"]}

            with_ties:
                Optional Argument.
                Specifies a flag to decide whether to run top function with ties or not.
                TOP WITH TIES implies that the rows returned include the specified number of rows in
                the ordered set for each timebucket. It includes any rows where the sort key value
                is the same as the sort key value in the last row that satisfies the specified number
                or percentage of rows. If this clause is omitted and ties are found, the earliest
                value in terms of timecode is returned.
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TypeError - If incorrect type of values passed to input argument.
            ValueError - If invalid value passed to the the argument.
            TeradataMLException
                1. If required argument 'number_of_values_to_column' is missing or None is passed.
                2. TDMLDF_AGGREGATE_FAILED - If top() operation fails to
                    generate the column-wise largest number of values in the columns.

        EXAMPLES :
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])
            >>>

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys.columns
            ['buoyid', 'TD_TIMECODE', 'temperature', 'salinity']
            >>> ocean_buoys.head()
                                   TD_TIMECODE  temperature  salinity
            buoyid
            0       2014-01-06 08:10:00.000000        100.0        55
            0       2014-01-06 08:08:59.999999          NaN        55
            1       2014-01-06 09:01:25.122200         77.0        55
            1       2014-01-06 09:03:25.122200         79.0        55
            1       2014-01-06 09:01:25.122200         70.0        55
            1       2014-01-06 09:02:25.122200         71.0        55
            1       2014-01-06 09:03:25.122200         72.0        55
            0       2014-01-06 08:09:59.999999         99.0        55
            0       2014-01-06 08:00:00.000000         10.0        55
            0       2014-01-06 08:10:00.000000         10.0        55

            >>> # DataFrame on sequenced PTI table
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_seq.columns
            ['TD_TIMECODE', 'TD_SEQNO', 'buoyid', 'salinity', 'temperature', 'dates']
            >>> ocean_buoys_seq.head()
                                   TD_TIMECODE  TD_SEQNO  salinity  temperature       dates
            buoyid
            0       2014-01-06 08:00:00.000000        26        55         10.0  2016-02-26
            0       2014-01-06 08:08:59.999999        18        55          NaN  2015-06-18
            1       2014-01-06 09:02:25.122200        24        55         78.0  2015-12-24
            1       2014-01-06 09:01:25.122200        23        55         77.0  2015-11-23
            1       2014-01-06 09:02:25.122200        12        55         71.0  2014-12-12
            1       2014-01-06 09:03:25.122200        13        55         72.0  2015-01-13
            1       2014-01-06 09:01:25.122200        11        55         70.0  2014-11-11
            0       2014-01-06 08:10:00.000000        19        55         10.0  2015-07-19
            0       2014-01-06 08:09:59.999999        17        55         99.0  2015-05-17
            0       2014-01-06 08:10:00.000000        27        55        100.0  2016-03-27

            >>> # DataFrame on NON-PTI table
            ... ocean_buoys_nonpti = DataFrame("ocean_buoys_nonpti")
            >>> # Check DataFrame columns and let's peek at the data
            ... ocean_buoys_nonpti.columns
            ['buoyid', 'timecode', 'temperature', 'salinity']
            >>> ocean_buoys_nonpti.head()
                                        buoyid  temperature  salinity
            timecode
            2014-01-06 08:09:59.999999       0         99.0        55
            2014-01-06 08:10:00.000000       0         10.0        55
            2014-01-06 09:01:25.122200       1         70.0        55
            2014-01-06 09:01:25.122200       1         77.0        55
            2014-01-06 09:02:25.122200       1         71.0        55
            2014-01-06 09:03:25.122200       1         72.0        55
            2014-01-06 09:02:25.122200       1         78.0        55
            2014-01-06 08:10:00.000000       0        100.0        55
            2014-01-06 08:08:59.999999       0          NaN        55
            2014-01-06 08:00:00.000000       0         10.0        55

            ### Examples for top without ties ###
            #
            # Example 1: Executing top function on DataFrame created on non-sequenced PTI table.
            #
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cy",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_grpby1.top(number_of_values_to_column).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  top2temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0              100
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0               99
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1               78
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1               79
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2               82
            5  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2               81
            6  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44               55
            7  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44               56
            >>>

            #
            # Example 2: Executing top to select 2 values for all the columns in ocean_buoys_seq DataFrame
            #            on sequenced PTI table.
            #
            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="CAL_YEARS(2)",
            ...                                                       value_expression="buoyid", fill="NULLS")
            >>> number_of_values_to_column = {2: "*"}
            >>> ocean_buoys_seq_grpby1.top(number_of_values_to_column).sort(["TIMECODE_RANGE", "buoyid"])
                                                    TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  top2TD_SEQNO  top2salinity  top2temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       0            26            55               99
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       1            24            55               78
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2       2            15            55               81
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      22             1            25               23
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                            2      44            21            55               55

            #
            # Example 3: Executing top function on DataFrame created on NON-PTI table.
            #
            >>> ocean_buoys_nonpti_grpby1 = ocean_buoys_nonpti.groupby_time(timebucket_duration="2cyear",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby1.top(number_of_values_to_column).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(CAL_YEARS(2))  buoyid  top2temperature
            0  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                           23       0               99
            1  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                           23       0              100
            2  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                           23       1               79
            3  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                           23       1               78
            4  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                           23       2               81
            5  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                           23       2               82
            6  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                           23      44               56
            7  ('2014-01-01 00:00:00.000000-00:00', '2016-01-...                           23      44               55


            ### Examples for top with ties ###
            #
            # Example 4: Executing top with ties function on DataFrame created on non-sequenced PTI table.
            #
            >>> ocean_buoys_grpby2 = ocean_buoys.groupby_time(timebucket_duration="2m",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_grpby2.top(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE", "buoyid"])
                                                    TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  top_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                     530161       0                       10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                     530162       0                        NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                     530163       0                        NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                     530164       0                        NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                     530165       0                       99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166       0                      100.0
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166       0                       10.0
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     530191       1                       70.0
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                     530191       1                       77.0
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                     530192       1                       78.0

            #
            # Example 5: Executing top with ties to select 2 values for temperature and 3 for rest of the columns in
            #            ocean_buoys DataFrame.
            #
            >>> ocean_buoys_grpby3 = ocean_buoys.groupby_time(timebucket_duration="MINUTES(2)", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature", 3:"*"}
            >>> ocean_buoys_grpby3.top(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  top_with_ties3buoyid  top_with_ties3salinity  top_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                     530161                   0.0                    55.0                       10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                     530162                   NaN                     NaN                        NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                     530163                   NaN                     NaN                        NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                     530164                   NaN                     NaN                        NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                     530165                   0.0                    55.0                       99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                     530166                   0.0                    55.0                       10.0
            6  ('2014-01-06 08:12:00.000000+00:00', '2014-01-...                     530167                   NaN                     NaN                        NaN
            7  ('2014-01-06 08:14:00.000000+00:00', '2014-01-...                     530168                   NaN                     NaN                        NaN
            8  ('2014-01-06 08:16:00.000000+00:00', '2014-01-...                     530169                   NaN                     NaN                        NaN
            9  ('2014-01-06 08:18:00.000000+00:00', '2014-01-...                     530170                   NaN                     NaN                        NaN
            >>>

            #
            # Example 6: Executing top with ties function on DataFrame created on NON-PTI table.
            #
            >>> ocean_buoys_nonpti_grpby2 = ocean_buoys_nonpti.groupby_time(timebucket_duration="2mins",
            ...                                                             value_expression="buoyid",
            ...                                                             timecode_column="timecode", fill="NULLS")
            >>> number_of_values_to_column = {2: "temperature"}
            >>> ocean_buoys_nonpti_grpby2.top(number_of_values_to_column, with_ties=True).sort(["TIMECODE_RANGE", "buoyid"])
                                                  TIMECODE_RANGE  GROUP BY TIME(MINUTES(2))  buoyid  top_with_ties2temperature
            0  ('2014-01-06 08:00:00.000000+00:00', '2014-01-...                   11574961       0                       10.0
            1  ('2014-01-06 08:02:00.000000+00:00', '2014-01-...                   11574962       0                        NaN
            2  ('2014-01-06 08:04:00.000000+00:00', '2014-01-...                   11574963       0                        NaN
            3  ('2014-01-06 08:06:00.000000+00:00', '2014-01-...                   11574964       0                        NaN
            4  ('2014-01-06 08:08:00.000000+00:00', '2014-01-...                   11574965       0                       99.0
            5  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                      100.0
            6  ('2014-01-06 08:10:00.000000+00:00', '2014-01-...                   11574966       0                       10.0
            7  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                       70.0
            8  ('2014-01-06 09:00:00.000000+00:00', '2014-01-...                   11574991       1                       77.0
            9  ('2014-01-06 09:02:00.000000+00:00', '2014-01-...                   11574992       1                       79.0
            >>>
            >>>
        """
        # Set the operation
        operation = "top"
        if with_ties:
            operation = "top with ties"

        # Argument validations
        awu_matrix = []
        awu_matrix.append(["number_of_values_to_column", number_of_values_to_column, False, (dict)])
        awu_matrix.append(["with_ties", with_ties, True, (bool)])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        _Validators._validate_missing_required_arguments(awu_matrix)

        # Check if number_of_values_to_column dict is empty or not.
        if not number_of_values_to_column:
            raise ValueError(Messages.get_message(MessageCodes.ARG_EMPTY, "number_of_values_to_column"))

        return self.__process_time_series_aggregate_with_multi_input_arguments(number_of_values_to_column, operation)

    def __process_time_series_aggregate_with_multi_input_arguments(self, number_of_values_to_column, operation):
        """
        Internal function to process bottom(), mad() and top() time series aggregate functions.

        PARAMETERS:
            number_of_values_to_column:
                Required Argument.
                Specifies a dictionary that accepts number of values to be selected for each column.
                Number of values is a key in the dictionary. Key should be any positive integer.
                Whereas value in the dictionary can be a column name or list of column names.
                Sometimes, value can also include a special character '*', instead of column name.
                This should be used only when one wants to return same number of values for all columns.
                Types: Dictionary
                Examples:
                    # Let's assume, a teradataml DataFrame has following columns:
                    #   col1, col2, col3, ..., colN

                    # For top() to return 2 values for column "col1":
                    number_of_values_to_column = {2: "col1"}

                    # For top() to return 2 values for column "col1" and 5 values for "col3":
                    number_of_values_to_column = {2: "col1", 5: "col3"}

                    # For top() to return 2 values for column "col1", "col2" and "col3":
                    number_of_values_to_column = {2: ["col1", "col2", "col3"]}

                    # Use cases for using '*' default value.
                    # For top() to return 2 values for all columns. In case, we need to return 2 values
                    # for each column in the DataFrame, then one can use '*'.
                    number_of_values_to_column = {2: "*"}

                    # For top() to return 2 values for column "col1" and "col3"
                    # and 5 values for rest of the columns:
                    number_of_values_to_column = {2: ["col1", "col3"], 5: "*"}

                    # We can use default value column character ('*') in list as well
                    # For top() to return 2 values for column "col1" and "col3"
                    # and 5 values for "col4" and rest of the columns:
                    number_of_values_to_column = {2: ["col1", "col3"], 5: ["col4", "*"]}

            with_ties:
                Required Argument.
                Specifies a flag to decide whether to run top function with ties or not.
                TOP WITH TIES implies that the rows returned include the specified number of rows in
                the ordered set for each timebucket. It includes any rows where the sort key value
                is the same as the sort key value in the last row that satisfies the specified number
                or percentage of rows. If this clause is omitted and ties are found, the earliest
                value in terms of timecode is returned.
                Types: bool

            operation:
                Required Argument.
                Specifies the bottom or top function to be run.
                Types: str

        RETURNS:
            teradataml DataFrame

        RAISES:
            TypeError - If incorrect type of values passed to input argument.
            ValueError - If invalid value passed to the the argument.
            TeradataMLException
                1. If required argument 'number_of_values_to_column' is missing or None is passed.
                2. TDMLDF_AGGREGATE_FAILED - If top() operation fails to
                    generate the column-wise smallest(bottom)/largest(top) number of values in the columns.

        EXAMPLES :
            self.__process_time_series_aggregate_with_multi_input_arguments(number_of_values_to_column, with_ties, operation)
        """
        default_constant_for_columns = []
        argument_name = "number_of_values_to_column"
        key_types = (int)
        if operation == 'mad':
            argument_name = "constant_multiplier_columns"
            key_types = (int, float)

        # Columns explicitly asked by user to process.
        columns_processed = []

        # Default value, if any, provided by used using { 5: '*' }. Here it means, 5 is num val and that will
        # be appicable for all columns. Sometimes user can specify 'x' number of values for a specific column and
        # 'y' number of values for all other columns.
        # Example:
        #    { x: ['col1'], y: '*' } - x and y are positive integers.
        # Following are couple of variables to play with this.
        default_num_val = None
        apply_default_num_val_to_rest = False

        # Dictionary to hold column:num_value pair for further processing.
        colname_to_numvalues = {}

        # Validations for key and value in number_of_values_to_column dictionary.
        # And processing the  input argument as well.
        for num_val in number_of_values_to_column:
            # Validate each key in 'argument_name' is a of correct type.
            _Validators._validate_function_arguments([["{} keys".format(argument_name), num_val, False, key_types]])

            if operation == 'mad':
                if num_val < 0:
                    raise ValueError(Messages.get_message(
                        MessageCodes.INVALID_ARG_VALUE).format(num_val, "key: {} in {}".format(num_val, argument_name),
                                                               'greater than or equal to 0'))
            else:
                # Validate each key, i.e., requested number of values in number_of_values_to_column dictionary
                # is a positive integer.
                _Validators._validate_positive_int(num_val, "key: {} in {}".format(num_val, argument_name))

            # If number values provided is applicable just single column, which is provided as string,
            # then let's convert it to a list.
            if isinstance(number_of_values_to_column[num_val], str):
                number_of_values_to_column[num_val] = [number_of_values_to_column[num_val]]

            # Process each column in the list to provide number of values 'num_val'
            for column in number_of_values_to_column[num_val]:
                if apply_default_num_val_to_rest and column.strip() == "*":
                    # Raise error for duplicate entry for applying num val to multiple columns.
                    raise ValueError(Messages.get_message(
                        MessageCodes.INVALID_ARG_VALUE).format("several \"*\"", argument_name,
                                                               'used only once'))

                # Check whether user has asked for any default value.
                if column.strip() == "*":
                    apply_default_num_val_to_rest = True
                    default_num_val = num_val
                    continue

                colname_to_numvalues[column] = num_val
                columns_processed.append(column)

        self.__validate_time_series_aggr_columns(operation=operation, columns=columns_processed)

        # Now that we have already processed all the columns explicitly mentioned by the user.
        # Let's apply default value to remaining columns, if user has specified the same.
        if apply_default_num_val_to_rest:
            remaining_columns = list(set(self.columns) - set(columns_processed))
            unsupported_types = _Dtypes._get_unsupported_data_types_for_aggregate_operations(operation)
            for column in remaining_columns:
                if not isinstance(self._td_column_names_and_sqlalchemy_types[column.lower()], tuple(unsupported_types)):
                    # We should not involve columns used in value expression of GROUP BY TIME clause as well.
                    if column not in self._value_expression:
                        colname_to_numvalues[column] = default_num_val
        else:
            # Processing columns for default value 1.4826 with MAD function.
            # Here we shall process columns, that are not explicitly specified by user either by name or '*'.
            if operation == 'mad':
                # We shall process, if and only if, user has not used '*' while passing value to
                # 'constant_multiplier_columns' argument.
                remaining_columns = list(set(self.columns) - set(columns_processed))
                unsupported_types = _Dtypes._get_unsupported_data_types_for_aggregate_operations(operation)
                for column in remaining_columns:
                    if not isinstance(self._td_column_names_and_sqlalchemy_types[column.lower()], tuple(unsupported_types)):
                        # We should not involve columns used in value expression of GROUP BY TIME clause as well.
                        if column not in self._value_expression:
                            default_constant_for_columns.append(column)

        return self._get_dataframe_aggregate(operation=operation, colname_to_numvalues=colname_to_numvalues,
                                             default_constant_for_columns=default_constant_for_columns)

    def __validate_time_series_aggr_columns(self, operation, columns):
        """
        Function to validate columns involved in time series aggregate. Columns are validated for:
            1. Column exists or not in the input teradataml DataFrame.
            2. Column has supported types for aggregate operation or not.

        PARAMETERS:
            operation:
                Required Argument.
                Aggregate operation being performed.
                Types: str

            columns:
                Required Argument.
                Column name or list of column names to be validated.
                Types: str or List of Strings

        RAISES:
            ValueError - If column does not exist in the teradataml DataFrame.
            TeradataMlException - If column has unsupported type for the aggregate operation.

        RETURNS:
            None.

        EXAMPLES:
            columns_processed = ["col1", "col2", "col3"]
            self.__validate_time_series_aggr_columns(operation="bottom", columns=columns_processed)
        """
        # Validate each column name, i.e., values in the number_of_values_to_column dictionary, is a
        # valid column in teradataml DataFrame
        _Validators._validate_column_exists_in_dataframe(columns, self._metaexpr)

        # Check if the user provided columns has unsupported datatype for aggregate operation or not.
        _Validators._validate_aggr_operation_unsupported_datatype(operation, columns,
                                                                  self._td_column_names_and_sqlalchemy_types)

class MetaData():
    """
    This class contains the column names and types for a dataframe.
    This class is used for printing DataFrame.dtypes

    """

    def __init__(self, column_names_and_types):
        """
        Constructor for TerdataML MetaData.

        PARAMETERS:
            column_names_and_types - List containing column names and Python types.

        EXAMPLES:
            meta = MetaData([('col1', 'int'),('col2', 'str')])

        RAISES:

        """
        self._column_names_and_types = column_names_and_types

    def __repr__(self):
        """
        This is the __repr__ function for MetaData.
        Returns a string containing column names and Python types.

        PARAMETERS:

        EXAMPLES:
            meta = MetaData([('col1', 'int'),('col2', 'str')])
            print(meta)

        RAISES:

        """
        if self._column_names_and_types is not None:
            return df_utils._get_pprint_dtypes(self._column_names_and_types)
        else:
            return ""
