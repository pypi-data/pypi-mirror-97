# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: mounika.kotha@teradata.com
Secondary Owner:

This is a common class to include common functionality required
by other classes which can be reused according to the need.

Add all the common functions in this class  like creating tempoarray table names, getting
the datatypes etc.
"""

import uuid
from math import floor
import time
import re
import sqlalchemy
from pathlib import Path
from numpy import number
from sqlalchemy import Table, Column
from teradataml.context import context as tdmlctx
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.sqlbundle import SQLBundle
from teradataml.common import td_coltype_code_to_tdtype
from teradataml.common.constants import PythonTypes
from teradataml.common.constants import TeradataTypes
from teradataml.dataframe.sql import _MetaExpression
from teradataml.common.garbagecollector import GarbageCollector
from teradataml.common.constants import TeradataConstants, PTITableConstants, \
    TableOperatorConstants
from teradataml.common.warnings import VantageRuntimeWarning
from teradataml.options.configure import configure
from teradatasqlalchemy.types import (INTEGER, SMALLINT, BIGINT, BYTEINT,
                                      DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy.types import (DATE, TIME, TIMESTAMP)
from teradatasqlalchemy.types import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy.types import (CHAR, VARCHAR, CLOB)

from functools import wraps
import warnings
from teradataml.utils.validators import _Validators


def package_deprecation(version, replacement=None, type="class"):
    """
    Define a deprecation decorator.

    PARAMETERS:
        replacement:
            Optional Argument.
            `replacement` should refer to the new API to be used instead.

        type:
            Optional Argument.
             Specifies the type of entity being deprecated.
             For example,
                class or function

    EXAMPLES:
        @package_deprecation('16.20.x.y')
        def old_func(): ...
        @package_deprecation('16.20.x.y', 'teradataml.analytics.mle')
        def old_func(): ..."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            msg = "\nThe \"{}\" {} has moved to a new package in version {}."
            if replacement:
                msg += "\nImport from the teradataml package, or directly from the {} module." + \
                       "\nSee the teradataml {} User Guide for more information."
            warnings.warn(msg.format('.'.join([func.__module__, func.__name__]), type, version,
                                     replacement + '.' + func.__name__, version),
                          category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wraps(func)(wrapper)

    return decorator


class UtilFuncs():
    def _get_numeric_datatypes(self):
        """
        Returns the numeric data types used in Teradata Vantage
        **From : https://www.info.teradata.com/HTMLPubs/DB_TTU_16_00/
        index.html#page/General_Reference/B035-1091-160K/psa1472241434371.html

        PARAMETERS:
            None

        RAISES:
            None

        RETURNS:
            List of numeric data types used in Teradata Vantage
        """
        return [BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER]

    def _get_timedate_datatypes(self):
        """
        Returns a list of TimeDate data types.

        PARAMETERS:
            None

        RAISES:
            None

        RETURNS:
            List of TimeDate data types used in Teradata Vantage
        """
        return [TIMESTAMP, DATE, TIME]

    def _get_character_datatypes(self):
        """
        Returns a list of Character data types.

        PARAMETERS:
            None

        RAISES:
            None

        RETURNS:
            List of Character data types used in Teradata Vantage
        """
        return [CHAR, VARCHAR, CLOB]

    def _get_byte_datatypes(self):
        """
        Returns a list of byte like data types.

        PARAMETERS:
            None

        RAISES:
            None

        RETURNS:
            List of Byte data types used in Teradata Vantage
        """
        return [BYTE, VARBYTE, BLOB]

    def _get_categorical_datatypes(self):
        """
        Returns a list of containing Character and TimeDate data types.

        PARAMETERS:
            None

        RAISES:
            None

        RETURNS:
            List of Character and TimeDate data types used in Teradata Vantage
        """
        return list.__add__(self._get_character_datatypes(), self._get_timedate_datatypes())

    def _get_all_datatypes(self):
        """
        Returns a list of Character, Numeric and TimeDate data types.

        PARAMETERS:
            None

        RAISES:
            None

        RETURNS:
            List of Character, Numeric and TimeDate data types used in Teradata Vantage
        """
        return list.__add__(self._get_categorical_datatypes(), self._get_numeric_datatypes())

    def _get_db_name_from_dataframe(self, df):
        """
        DESCRIPTION:
            Function to get database name from teradataml DataFrame.

        PARAMETERS:
            df:
                Required Argument.
                Specifies the input teradataml DataFrame.
                Types: teradataml DataFrame

        RETURNS:
            Database name.

        RAISES:
            None.

        EXAMPLES:
            UtilFuncs()._get_db_name_from_dataframe(df)
        """
        if df._table_name is None:
            from teradataml.dataframe.dataframe_utils import DataFrameUtils
            df._table_name = DataFrameUtils()._execute_node_return_db_object_name(df._nodeid,
                                                                                  df._metaexpr)
        db_name = self._extract_db_name(df._table_name)
        if db_name is None or db_name == "":
            # Extract db_name from SQLAlchemy Engine URL.
            if 'DATABASE' in tdmlctx.get_context().url.query:
                db_name = tdmlctx.get_context().url.query['DATABASE']
            else:
                db_name = tdmlctx._get_current_databasename()
        else:
            db_name = db_name.replace("\"", "")

        return db_name

    @staticmethod
    def _get_valid_aggregate_operations():
        """
        Returns the list of valid aggregate operations on Teradata Vantage

        PARAMETERS:
            None

        RAISES:
            None

        RETURNS:
            List of valid aggregate operations possible on Teradata Vantage
        """
        return ['count', 'kurtosis', 'max', 'mean', 'median', 'min', 'percentile', 'skew', 'std',
                'sum', 'unique', 'var']

    @staticmethod
    def _get_valid_time_series_aggregate_operations():
        """
        Returns the list of valid aggregate operations on Teradata Vantage

        PARAMETERS:
            None

        RAISES:
            None

        RETURNS:
            List of valid aggregate operations possible on Teradata Vantage
        """
        return ['bottom', 'bottom with ties', 'delta_t', 'first', 'last', 'mad', 'mode', 'top',
                'top with ties']

    @staticmethod
    def _generate_temp_table_name(databasename=None, user=None, prefix=None,
                                  use_default_database=False, gc_on_quit=True, quote=True,
                                  table_type=TeradataConstants.TERADATA_VIEW):
        """
        DESCRIPTION:
            Function to return the random string for temporary table names.

        PARAMETERS:
            databasename:
                Optional Argument.
                Specifies the database name to use while generating the script.
                Types: str

            user:
                Optional Argument.
                Specifies the current username or database name on which user logged on to Teradata Vantage.
                Types: str

            prefix:
                Optional Argument.
                Specifies the prefix of the module from which table/view name is requested.
                Types: str

            use_default_database:
                Optional Argument.
                Specifies whether to create a table or view in the default database when
                "databasename" is not provided.
                Default value: False
                Types: str

            gc_on_quit:
                Optional Argument.
                Specifies whether to garbage collect the table/view with the generated name
                at the end of the session.
                When 'True', the objects created with the generated name will be garbage
                collected at the end of the session.
                Default value: True
                Types: bool

            quote:
                Optional Argument.
                Specifies whether to quote the database name and table/view name.
                When 'True', quotes are added around the database name and the table/view name.
                Default value: True
                Types: bool

            table_type:
                Optional Argument.
                Specifies the type of objects - table or view.
                Default value: TeradataConstants.TERADATA_VIEW
                Types: TeradataConstant

        RETURNS:
            Temporary table name.

        RAISES:

        EXAMPLES:
            new_table_name = UtilFuncs._generate_temp_table_name(user='tdqg', prefix="from_pandas")
            new_table_name = UtilFuncs._generate_temp_table_name(user='tdqg', prefix="from_pandas",
                                                                 table_type = TeradataConstants.TERADATA_VIEW)
            new_table_name = UtilFuncs._generate_temp_table_name(user='tdqg', prefix="from_pandas",
                                                                 table_type = TeradataConstants.TERADATA_TABLE)

        Output:
            tdml_temp_table__1517501990393350 (or)
            tdqg.tdml_temp_table__1517501990393350 (or)
            tdml_temp_table__from_pandas_1517501990393350 (or)
            tdqg.tdml_temp_table__from_pandas_1517501990393350
        """
        # Number of seconds since  Jan 1, 1970 00:00:00
        timestamp = time.time()
        tabname = "ml_"
        random_string = "{}{}".format(floor(timestamp / 1000000),
                                      floor(timestamp % 1000000 * 1000000 +
                                            int(str(uuid.uuid4().fields[-1])[:10])))
        if prefix is not None:
            tabname = "{}_{}".format(tabname, prefix)

        tabname = "{}_{}".format(tabname, random_string)
        gc_tabname = tabname

        if use_default_database and databasename is None:
            tabname = "{}.{}".format(tdmlctx._get_context_temp_databasename(), tabname)
            gc_tabname = "\"{}\".\"{}\"".format(tdmlctx._get_context_temp_databasename(),
                                                gc_tabname)

        if user is not None:
            tabname = "{}.{}".format(user, tabname)
            gc_tabname = "\"{}\".\"{}\"".format(user, gc_tabname)

        if databasename is not None:
            tabname = "{}.{}".format(databasename, tabname)
            gc_tabname = "\"{}\".\"{}\"".format(databasename, gc_tabname)

        # Enable garbage collection for the temporary view & table created while transformations.
        if gc_on_quit:
            GarbageCollector._add_to_garbagecollector(gc_tabname, table_type)
        if quote:
            return UtilFuncs._quote_table_names(tabname)
        else:
            return tabname

    @staticmethod
    def _generate_temp_script_name(database_name=None, prefix=None, use_default_database=True,
                                   gc_on_quit=True, quote=True,
                                   script_type=TeradataConstants.TERADATA_SCRIPT):
        """
        DESCRIPTION:
            Function to return the random string for temporary script names.

        PARAMETERS:
            database_name:
                Optional Argument:
                Specifies the database name on which user logged on to Teradata Vantage.
                Types: str

            prefix:
                Optional Argument.
                Specifies the prefix of the module or function from which script name is requested.
                Types: str

            use_default_database:
                Optional Argument.
                Specifies whether the script will be installed in the default/connected database.
                When 'True', the current/default database name will be used for generating the name.
                Default value: True
                Types: bool

            gc_on_quit:
                Optional Argument.
                Specifies whether to garbage collect the object with the generated name
                at the end of the session.
                When 'True', the objects created with the generated name will be garbage
                collected at the end of the session.
                Default value: True
                Types: bool

            quote:
                Optional Argument.
                Specifies whether to quote the database name and script name.
                When 'True', quotes are added around the database name and the script name.
                Default value: True
                Types: bool

            script_type:
                Optional Argument.
                Specifies the type of script.
                Default value: TeradataConstants.TERADATA_SCRIPT
                Types: TeradataConstant

        RETURNS:
            Temporary script name.

        RAISES:
            None.

        EXAMPLES:
            new_script_name = UtilFuncs._generate_temp_script_name(use_default_database=True,
                                                                  script_type = TeradataConstants.TERADATA_SCRIPT)
        """
        # NOTE:
        # 1. There can be other types of scripts going forward which may require their own type (like for Apply).
        #    Hence, we have a 'script_type' argument which currently has only one possible value.
        # 2. Currently map_row and map_partition use only default database, but going forward this can be changed
        #    to use other databases for installation of script, using 'database_name'.

        timestamp = time.time()
        script_name = "ml_"

        random_string = "{}{}".format(floor(timestamp / 1000000),
                                      floor(timestamp % 1000000 * 1000000 +
                                            int(str(uuid.uuid4().fields[-1])[:10])))

        if prefix is not None:
            script_name = "{}_{}".format(script_name, prefix)

        script_name = "{}_{}".format(script_name, random_string)
        gc_tabname = script_name

        dbname_to_use = tdmlctx._get_current_databasename()
        if not use_default_database and database_name is not None:
            dbname_to_use = database_name

        script_name = "{}.{}".format(dbname_to_use, script_name)
        gc_tabname = "\"{}\".\"{}\"".format(dbname_to_use, gc_tabname)

        # Enable garbage collection for the temporary script created.
        if gc_on_quit:
            GarbageCollector._add_to_garbagecollector(gc_tabname, script_type)

        return UtilFuncs._quote_table_names(script_name) if quote else script_name

    @staticmethod
    def _serialize_and_encode(obj):
        """
        DESCRIPTION:
            Internal utility to serialize any Python object (including functions)
            using dill and encode using base64.

        PARAMETERS:
            obj:
                Specifies the Python object to serialize and encode.
                Types: object

        RAISES:
            None.

        RETURNS:
            An encoded byte string representing the serialized object 'obj'.

        EXAMPLES:
            >>> # Serializing and encoding a literal value
            >>> literal = UtilFuncs._serialize_and_encode('literal value')
            >>> # Serializing and encoding a function
            >>> def udf(a, b): return a + b
            >>> func = UtilFuncs._serialize_and_encode(udf)
        """
        from dill import dumps as dill_dumps
        from base64 import b64encode as base64_b64encode

        return base64_b64encode(dill_dumps(obj, recurse=True))

    @staticmethod
    def _quote_table_names(table_name):
        """
        Quotes table names or view names.
        If the table name is in the format schema.table_name, it will quote the
        schema name and table name.

        Example:
            mytab -> "mytab"
            schema.mytable -> "schema"."mytab"
            myview -> "myview"

        PARAMETERS:
            table_name - The name of table or view. The name can include the schema (e.g. schema.table_name)

        RETURNS:
            returns the quoted table name.

        RAISES:

        EXAMPLES:
            table_name = UtilFuncs._quote_table_names(table_name)

        """
        table_name_list = table_name.split(".")
        for i in range(0, len(table_name_list)):
            if not (table_name_list[i].startswith("\"") and table_name_list[i].endswith("\"")):
                table_name_list[i] = UtilFuncs._teradata_quote_arg(table_name_list[i], "\"", False)

        return ".".join(table_name_list)

    @staticmethod
    def _execute_ddl_statement(ddl_statement):
        """
        Executes a DDL statment and commits transaction
        This is an internal function.

        PARAMETERS:
            ddl_statement - Teradata DDL statement.

        RETURNS:

        RAISES:
            Database error if an error occurred while executing the DDL statement.

        EXAMPLES:
            UtilFuncs._execute_ddl_statement('create table mytab (col1 int, col2 varchar(20))')

        """
        # Let's execute our DDL statement with escape function '{fn teradata_fake_result_sets}'
        # offered by teradatasql driver. This function will allow us catch any warnings thrown
        # from the Vantage. Hence, executing the DDL statement with this escape function.
        ddl_statement = "{fn teradata_fake_result_sets} " + ddl_statement

        if tdmlctx.td_connection is not None:
            cursor = None
            try:
                conn = tdmlctx.td_connection.connection
                cursor = conn.cursor()
                cursor.execute(ddl_statement)

                # Fetch the result set just to check whether we have received any warnings or not.
                warnRes = cursor.fetchone()
                # Check for warning code and warning message
                # warnRes[5] contains the Warning Code
                # warnRes[6] contains the actual Warning Message
                if warnRes[5] != 0 and warnRes[6] != "":
                    # Raise warning raised from Vantage as is.
                    warnings.simplefilter("always")
                    msg_ = Messages.get_message(MessageCodes.VANTAGE_WARNING)
                    warnings.warn(msg_.format(warnRes[5], warnRes[6]), VantageRuntimeWarning)

                conn.commit()
            except:
                # logger.debug("Got exception while executing ({0})".format(teradataSQL))
                raise
            finally:
                if cursor:
                    cursor.close()
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE),
                                      MessageCodes.CONNECTION_FAILURE)

    @staticmethod
    def _execute_query(query, fetchWarnings=False, expect_none_result=False):
        """
        Retrieves result set data from query.

        PARAMETERS:
            query:
                Required Argument.
                Specifies the SQL query to execute.
                Types: str

            fetchWarnings:
                Optional Argument.
                Specifies a flag that decides whether to raise warnings thrown from Vanatge or not.
                Default Values: False
                Types: bool

            expect_none_result:
               Optional Argument.
               When set to True, warnings will not be fetched and only result set is fetched.
               Returns None if no result set is received from the backend.
               When fetchWarnings is set to True this option is ignored.
               Default Values: False
               Types: bool

        RETURNS:
            Returns only result set from query if 'fetchWarnings' is False. If set to True, then
            return result set and columns for the result set.

        RAISES:
            Database error if an error occurred while executing query.

        EXAMPLES:
            result = UtilFuncs._execute_query('select col1, col2 from mytab')
            result = UtilFuncs._execute_query('help column mytab.*')

            result = UtilFuncs._execute_query('help column mytab.*')

            # Execute the stored procedure using fetchWarnings.
            UtilFuncs._execute_query("call SYSUIF.INSTALL_FILE('myfile',
                                                             'filename.py',
                                                             'cb!/Documents/filename.py')",
                                                              True, False)

            # Execute the stored procedure without fetchWarnings but still needs resultsets.
            UtilFuncs._execute_query("call SYSUIF.list_base_environments()", False, True)

        """

        if fetchWarnings:
            # Let's execute our DDL statement with escape function '{fn teradata_fake_result_sets}'
            # offered by teradatasql driver. This function will allow us catch any warnings thrown
            # from the Vantage. Hence, executing the DDL statement with this escape function.
            query = "{fn teradata_fake_result_sets} " + query

        if tdmlctx.td_connection is not None:
            cursor = None
            try:
                conn = tdmlctx.td_connection.connection
                cursor = conn.cursor()
                cursor.execute(query)

                if fetchWarnings:
                    # Fetch the result set just to check whether we have received any warnings or not.
                    warnRes = cursor.fetchone()
                    # Check for warning code and warning message
                    # warnRes[5] contains the Warning Code
                    # warnRes[6] contains the actual Warning Message
                    if warnRes[5] != 0 and warnRes[6] != "":
                        # Raise warning raised from Vantage as is.
                        warnings.simplefilter("always")
                        msg_ = Messages.get_message(MessageCodes.VANTAGE_WARNING)
                        warnings.warn(msg_.format(warnRes[5], warnRes[6]), VantageRuntimeWarning)

                    cursor.nextset()

                    return cursor.fetchall(), [col_desc[0] for col_desc in cursor.description]

                # This check may be removed if DBS side stored procedure are fixed to return empty
                # result sets with columns in cursor.description
                elif expect_none_result:
                    cursor.nextset()
                    # Some of the stored procedure returns None if result set has no rows.
                    # cannot use fetchall call in such cases. If SPs are fixed to support result sets with zero
                    # rows then below call may be removed in future.
                    if cursor.rowcount <= 0:
                        return None
                    return cursor.fetchall(), [col_desc[0] for col_desc in cursor.description]

                else:
                    return cursor.fetchall()
            except:
                raise
            finally:
                if cursor:
                    cursor.close()
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE),
                                      MessageCodes.CONNECTION_FAILURE)

    @staticmethod
    def _create_view(view_name, query):
        """
        Create a view from the given query.

        PARAMETERS:
            view_name - View name
            query - SQL query

        RAISES

        RETURNS:
            True if success.

        EXAMPLES:
            UtilFuncs._create_view(view_name, "select * from table_name")
        """
        crt_view = SQLBundle._build_create_view(view_name, query)
        try:
            UtilFuncs._execute_ddl_statement(crt_view)
            return True
        except:
            raise

    @staticmethod
    def _create_table(table_name, query):
        """
        Create a table from the given query.

        PARAMETERS:
            table_name - Fully qualified quoted table name.
            query - SQL query

        RAISES

        RETURNS:
            True if success, false if fails

        EXAMPLES:
            UtilFuncs._create_table('"dbname"."table_name"', "select * from table_name")
        """
        crt_table = SQLBundle._build_create_table_with_data(table_name, query)
        UtilFuncs._execute_ddl_statement(crt_table)
        return True

    @staticmethod
    def _get_non_null_counts(col_names, table_name):
        """
        Returns a list of non-null count for each column in col_names from table table_name.

        PARAMETERS:
            col_names - list of column names for table table_name.
            table_name - table name.

        RETURNS:
            returns a list of non-null counts for each column.

        RAISES:

        EXAMPLES:
            UtilFuncs._get_non_null_counts(col_names, 'mytab')

        """
        count_col_names = ["count(\"{0}\")".format(name) for name in col_names]
        select_count = "select {0} from {1}".format(", ".join(count_col_names), table_name)
        result = UtilFuncs._execute_query(select_count)
        return [str(i) for i in result[0]]

    @staticmethod
    def _get_volatile_table(query, with_data=False):
        """
        Creates a volatile table as query.
        If with_data is True, creates the volatile table with data.
        Else, creates the volatile table without data.

        PARAMETERS:
            query - The query used to create the volatile table.
            with_data(optional) - True, creates table with data.
                                  False, creates table without data. Default is False

        RETURNS:
            returns the temporary name of the volatile table.

        RAISES:
            Database error if an error occurred while creating the volatile table.

        EXAMPLES:
            UtilFuncs._get_volatile_table('select col1, col2, from mytab')
            UtilFuncs._get_volatile_table('select col1, col2, from mytab', with_data=True)

        """
        vtab_name = UtilFuncs._generate_temp_table_name()
        if with_data:
            create_vtab_ddl = SQLBundle._build_create_volatile_table_with_data(vtab_name, query)
        else:
            create_vtab_ddl = SQLBundle._build_create_volatile_table_without_data(vtab_name, query)
        UtilFuncs._execute_ddl_statement(create_vtab_ddl)
        return vtab_name

    @staticmethod
    def _drop_table(table_name, check_table_exist=True):
        """
        Drops a table.

        PARAMETERS:
            table_name - The table to drop.
            check_table_exist - Checks if the table exist before dropping the table.

        RETURNS:
            True - if the table is dropped.

        RAISES:
            Database error if an error occurred while dropping the table.

        EXAMPLES:
            UtilFuncs._drop_table('mytab')
            UtilFuncs._drop_table('mytab', check_table_exist = False)
            UtilFuncs._drop_table('mydb.mytab', check_table_exist = False)
            UtilFuncs._drop_table("mydb"."mytab", check_table_exist = True)

        """
        drop_tab = SQLBundle._build_drop_table(table_name)
        if check_table_exist is True:
            helptable = UtilFuncs._get_help_tablename(table_name)
            if helptable:
                UtilFuncs._execute_ddl_statement(drop_tab)
                return True
        else:
            UtilFuncs._execute_ddl_statement(drop_tab)
            return True

        return False

    @staticmethod
    def _drop_view(view_name, check_view_exist=True):
        """
        Drops a view.

        PARAMETERS:
            view_name - The view to drop.
            check_view_exist - Checks if the view exist before dropping the view.

        RETURNS:
            True - if the view is dropped.

        RAISES:
            Database error if an error occurred while dropping the view.

        EXAMPLES:
            UtilFuncs._drop_view('myview')
            UtilFuncs._drop_view('myview', check_view_exist = False)
            UtilFuncs._drop_view('mydb.myview', check_view_exist = False)
            UtilFuncs._drop_view("mydb"."myview", check_view_exist = True)
        """
        drop_view = SQLBundle._build_drop_view(view_name)
        if check_view_exist is True:
            viewdetails = UtilFuncs._get_help_viewname(view_name)
            if viewdetails:
                UtilFuncs._execute_ddl_statement(drop_view)
                return True
        else:
            UtilFuncs._execute_ddl_statement(drop_view)
            return True

        return False

    @staticmethod
    def _delete_script(script_name, check_script_exist=True):
        """
        DESCRIPTION:
            Function to remove a user-installed file/script.

        PARAMETERS:
            script_name:
                Required Argument.
                Specifies the name of the script to remove.
                Types: str

            check_script_exist:
                Required Argument.
                Specifies whether to check if the script exists or not before removing it.
                When 'True', the presence of the script will be check for.
                Default value: True
                Types: bool

        RETURNS:
            True - if the script is removed.

        RAISES:
            Database error if an error occurred while dropping the view.

        EXAMPLES:
            UtilFuncs._delete_script('myview')
            UtilFuncs._delete_script('myview', check_script_exist = False)
            UtilFuncs._delete_script('mydb.myview', check_script_exist = False)
            UtilFuncs._delete_script("mydb"."myview", check_script_exist = True)
        """
        dbname = UtilFuncs._teradata_unquote_arg(UtilFuncs._extract_db_name(script_name),
                                                 quote='"')
        script_alias = UtilFuncs._teradata_unquote_arg(UtilFuncs._extract_table_name(script_name),
                                                       quote='"')
        current_db = tdmlctx._get_current_databasename()

        script_exists = False
        if check_script_exist:
            query = "select count(*) from dbc.tablesV " \
                    "where databasename = '{}' and tablename = '{}' " \
                    "and tablekind = 'Z'".format(dbname, script_alias)

            script_exists = True if UtilFuncs._execute_query(query)[0][0] == 1 else False

        if script_exists or not check_script_exist:
            try:
                # If the database is not the current/default database, we need to
                # set that as the session database to be able to remove the file.
                if dbname.lower() != current_db.lower():
                    tdmlctx.get_context().execute('database {}'.format(dbname))

                # Remove the file.
                remove_file(script_alias, force_remove=True, suppress_output=True)
                return True
            except:
                raise
            finally:
                # Reset the database if it was set to something else.
                if dbname.lower() != current_db.lower():
                    tdmlctx.get_context().execute('database {}'.format(current_db))

    @staticmethod
    def _get_help_vtablenames():
        """
        Function to get list of volatile tables.

        RETURNS:
            List of volatile tablenames.

        EXAMPLES:
            UtilFuncs._get_help_vtablenames()
        """
        vtables = UtilFuncs._execute_query(SQLBundle._build_help_volatile_table())
        if vtables:
            return list(map(str.strip, filter(None, vtables[0])))
        return []

    @staticmethod
    def _get_help_viewname(view_name):
        """
        Function to get help of the view.

        PARAMETERS:
            view_name - The name of the view.

        RETURNS:
            The help information of the view specified by view_name.

        EXAMPLES:
            UtilFuncs._get_help_viewname(myview)
        """
        return UtilFuncs._execute_query(SQLBundle._build_help_view(view_name))

    @staticmethod
    def _get_help_tablename(table_name):
        """
        Function to get help of the table.

        PARAMETERS:
            table_name - The name of the table.

        RETURNS:
            The help information of the table specified by table_name.

        EXAMPLES:
            UtilFuncs._get_help_tablename(mytable)
        """
        return UtilFuncs._execute_query(SQLBundle._build_help_table(table_name))

    @staticmethod
    def _get_select_table(table_name):
        """
        Function to get a table if exists.

        PARAMETERS:
            table_name - Table name to check if exists in the database.

        RETURNS:
            Table name in a list.

        EXAMPLES:
            UtilFuncs._get_select_table('mytab')

        """
        table = UtilFuncs._execute_query(SQLBundle._build_select_table_name(table_name))
        if table:
            return table[0]
        return []

    @staticmethod
    def _describe_column(metadata, to_type=None):
        """
        This is an internal function to retrieve
        column names and column types for the table or view.

        PARAMETERS:
            metadata:
                The result set from the HELP COLUMN command.

        RETURNS:
            A list of tuples (column_names, column_types).

        RAISES:
            Database errors if a problem occurs while trying to retrieve the column information.

        EXAMPLES:
            column_names_and_types = UtilFuncs._describe_column()

        """
        column_names_and_types = []
        for row in metadata:
            # logger.debug("Retrieving Teradata type for {0}".format(row[31]))
            # row[31] corresponds to 'Column Dictionary Name' column in the result of 'HELP COLUMN' SQL commands result.
            column_name = row[31]
            # We also need to check if the column is a TD_TIMEBUCKET column, in which case we can ignore it.
            # We do so by checking the column name, and row[48] which corresponds to the 'Time Series Column Type'
            # column in the 'HELP COLUMN' command to make sure it is indeed the TD_TIMEBUCKET column in the PTI table,
            # and not just a column with the same name in a PTI/non-PTI table.
            # TD_TIMEBUCKET column is ignored since it is not functionally available to any user.
            if column_name == PTITableConstants.TD_TIMEBUCKET.value and \
                    len(row) > 48 and row[48] is not None and \
                    row[48].strip() == PTITableConstants.TSCOLTYPE_TIMEBUCKET.value:
                continue
            if to_type == "TD":
                # row[18] corresponds to the 'UDT Name' in the 'HELP COLUMN' SQL commands result.
                # row[1] corresponds to the 'Type' in the 'HELP COLUMN' commands result.
                column_names_and_types.append((column_name,
                                               UtilFuncs._help_col_to_td_type(row[1].strip(),
                                                                              row[18],
                                                                              row[44])))
            else:
                column_names_and_types.append((column_name,
                                               UtilFuncs._help_col_to_python_type(row[1].strip(),
                                                                                  row[44])))

        return column_names_and_types

    @staticmethod
    def _get_pandas_converters(col_types):
        """
        DESCRIPTION:
            Internal util function to get a dictionary of Python type names of columns
            in a teradataml DataFrame mapped to lambda functions to process the
            data to convert it to the type, which can be readily used with pandas'
            read_csv() function's 'converters' argument.

            Note: This utility provides converter functions only for values of type
                  int, float, and decimal.Decimal.
                  For types that don't expect empty strings in input
                  i.e. for 'datetime.datetime', 'datetime.date' and 'datetime.time',
                  the converter function returns None for empty string input.

        PARAMETERS:
            col_types:
                Required Argument.
                The list of Python types names corresponding to the columns in the input data.
                Types: list

        RAISES:
            None

        RETURNS:
            dict

        EXAMPLES:
            >>> pandas_converters = UtilFuncs._get_pandas_converters(["int", "str"])
        """
        pandas_converters = dict()
        for i, type_ in enumerate(col_types):
            # Add a functions that converts the string values to float or int when
            # the value is not empty string, else return None.
            if type_ in (PythonTypes.PY_FLOAT_TYPE.value,
                         PythonTypes.PY_DECIMAL_TYPE.value):
                pandas_converters[i] = lambda x: float(x) \
                    if isinstance(x, (bytes, number, int, float)) \
                    else float("".join(x.split())) if len(x.strip()) > 0 else None

            elif type_ == PythonTypes.PY_INT_TYPE.value:
                pandas_converters[i] = lambda x: int(x) \
                    if isinstance(x, (bytes, number, int, float)) \
                    else int(float("".join(x.split()))) if len(x.strip()) > 0 else None

            elif type_ in (PythonTypes.PY_DATETIME_TYPE.value,
                           PythonTypes.PY_DATE_TYPE.value,
                           PythonTypes.PY_TIME_TYPE.value):
                # For types that do not expect empty strings, add function to
                # set them to None when value received is empty string.
                pandas_converters[i] = lambda x: x if len(x.strip()) > 0 else None

            else:
                # For 'str' and 'bytes' types, add function that returns value as is.
                pandas_converters[i] = lambda x: x

        return pandas_converters

    @staticmethod
    def _teradata_type_to_python_type(td_type):
        """
        Translate the Teradata type from metaexpr to Python types.
        PARAMETERS:
            td_type - The Teradata type from metaexpr.

        RETURNS:
            The Python type for the given td_type.

        RAISES:

        EXAMPLES:
            # o is an instance of INTEGER
            pytype = UtilFuncs._teradata_type_to_python_type(o)

        """

        # loggerlogger.debug("_help_col_to_python_type td_type = {0} ".format(td_type))
        if type(td_type) in TeradataTypes.TD_INTEGER_TYPES.value:
            return PythonTypes.PY_INT_TYPE.value
        elif type(td_type) in TeradataTypes.TD_FLOAT_TYPES.value:
            return PythonTypes.PY_FLOAT_TYPE.value
        elif type(td_type) in TeradataTypes.TD_DECIMAL_TYPES.value:
            return PythonTypes.PY_DECIMAL_TYPE.value
        elif type(td_type) in TeradataTypes.TD_BYTE_TYPES.value:
            return PythonTypes.PY_BYTES_TYPE.value
        elif type(td_type) in TeradataTypes.TD_DATETIME_TYPES.value:
            return PythonTypes.PY_DATETIME_TYPE.value
        elif type(td_type) in TeradataTypes.TD_TIME_TYPES.value:
            return PythonTypes.PY_TIME_TYPE.value
        elif type(td_type) in TeradataTypes.TD_DATE_TYPES.value:
            return PythonTypes.PY_DATE_TYPE.value

        return PythonTypes.PY_STRING_TYPE.value

    @staticmethod
    def _help_col_to_python_type(col_type, storage_format):
        """
        Translate the 1 or 2 character TD type codes from HELP COLUMN to Python types.
        PARAMETERS:
            col_type - The 1 or 2 character type code from HELP COLUMN command.
            storage_format - The storage format from HELP COLUMN command.

        RETURNS:
            The Python type for the given col_type.

        RAISES:

        EXAMPLES:
            pytype = UtilFuncs._help_col_to_python_type('CV', None)
            pytype = UtilFuncs._help_col_to_python_type('DT', 'CSV')

        """
        if col_type in TeradataTypes.TD_INTEGER_CODES.value:
            return PythonTypes.PY_INT_TYPE.value
        elif col_type in TeradataTypes.TD_FLOAT_CODES.value:
            return PythonTypes.PY_FLOAT_TYPE.value
        elif col_type in TeradataTypes.TD_DECIMAL_CODES.value:
            return PythonTypes.PY_DECIMAL_TYPE.value
        elif col_type in TeradataTypes.TD_BYTE_CODES.value:
            return PythonTypes.PY_BYTES_TYPE.value
        elif col_type in TeradataTypes.TD_DATETIME_CODES.value:
            return PythonTypes.PY_DATETIME_TYPE.value
        elif col_type in TeradataTypes.TD_TIME_CODES.value:
            return PythonTypes.PY_TIME_TYPE.value
        elif col_type in TeradataTypes.TD_DATE_CODES.value:
            return PythonTypes.PY_DATE_TYPE.value
        elif col_type == "DT":
            sfmt = storage_format.strip()
            if sfmt == "CSV":
                return PythonTypes.PY_STRING_TYPE.value
            elif sfmt == "AVRO":
                return PythonTypes.PY_BYTES_TYPE.value

        return PythonTypes.PY_STRING_TYPE.value

    @staticmethod
    def _help_col_to_td_type(col_type, udt_name, storage_format):
        """
        Translate the 2 character TD type codes from HELP COLUMN to Teradata types.
        PARAMETERS:
            col_type - The 2 character type code from HELP COLUMN command.
            udt_name - The UDT name from the HELP COLUMN command.
            storage_format - The storage format from HELP COLUMN command.

        RETURNS:
            The Teradata type for the given colType.

        RAISES:

        EXAMPLES:
            tdtype = UtilFuncs._help_col_to_td_type('CV', None, None)

        """
        # logger.debug("helpColumnToTeradataTypeName colType = {0} udtName = {1}
        # storageFormat {2}".format(colType, udtName, storageFormat))
        if col_type in td_coltype_code_to_tdtype.HELP_COL_TYPE_TO_TDTYPE:
            return td_coltype_code_to_tdtype.HELP_COL_TYPE_TO_TDTYPE[col_type]

        if col_type == "DT":
            return "DATASET STORAGE FORMAT {0}".format(storage_format.strip())

        if col_type in ["UD", "US", "UT", "A1", "AN"]:
            if udt_name:
                return udt_name

        return col_type

    @staticmethod
    def _in_schema(schema_name, table_name):
        """
        Takes a schema name and a table name and creates a database object name in
        the format "schema"."table_name".

        PARAMETERS:
            schema_name - The schema where the table resides in.
            table_name - The table name or view name in Teradata Vantage referenced by this DataFrame.

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame(in_schema("myschema", "mytab")
            df = DataFrame(in_schema("myschema", "myview")

        RAISES:

        """
        return "{0}.{1}".format(UtilFuncs._teradata_quote_arg(schema_name, "\"", False),
                                UtilFuncs._teradata_quote_arg(table_name, "\"", False))

    @staticmethod
    def _extract_db_name(full_qualified_name):
        """
        Takes in fully qualified name of the table/view (db.table), and returns
        a database name from the same.

        PARAMETERS:
            full_qualified_name - Name of the table/view

        EXAMPLES:
            UtilFuncs._extract_db_name("db1.tablename")

        RETURNS:
            Database name from the provided name.

        """
        names = full_qualified_name.split(".")
        if len(names) == 2:
            return names[0]
        else:
            return None

    @staticmethod
    def _extract_table_name(full_qualified_name):
        """
        Takes in fully qualified name of the table/view (db.table), and returns
        a table/view name from the same.

        PARAMETERS:
            full_qualified_name - Name of the table/view

        EXAMPLES:
            UtilFuncs._extract_db_name("db1.tablename")

        RETURNS:
            Table/View name from the provided name.

        """
        names = full_qualified_name.split(".")
        if len(names) == 2:
            return names[1]
        else:
            return names[0]

    @staticmethod
    def _teradata_quote_arg(args, quote="'", call_from_wrapper=True):
        """
        Function to quote argument value.
        PARAMETERS:
            args : Argument to be quoted.
            quote : Type of quote to be used for quoting. Default is
                    single quote (').
        RETURNS:
            Argument with quotes as a string.

        EXAMPLES:
            When a call is being made from wrapper:
                UtilFuncs._teradata_quote_arg(family, "'")
            When a call is being made from non-wrapper function.
                UtilFuncs._teradata_quote_arg(family, "'", False)
        """
        if call_from_wrapper and not configure.column_casesensitive_handler:
            quote = ""
            return args

        # Returning same string if it already quoted. Applicable only for strings.
        if isinstance(args, str) and args.startswith(quote) and args.endswith(quote):
            return args
        if args is None:
            return None
        if isinstance(args, list):
            return ["{0}{1}{0}".format(quote, arg) for arg in args]

        return "{0}{1}{0}".format(quote, args)

    @staticmethod
    def _teradata_unquote_arg(quoted_string, quote="'"):
        """
        Function to unquote argument value.
        PARAMETERS:
            quoted_string : String to be unquoted.
            quote         : Type of quote to be used for unquoting. Default is
                            single quote (').
        RETURNS:
            None if 'quoted_string' is not a string,
            else Argument without quotes as a string.

        EXAMPLES:
            UtilFuncs._teradata_unquote_arg(family, "'")
        """

        if not isinstance(quoted_string, str):
            return None

        # Returning same string if it already unquoted.
        if not quoted_string.startswith(quote) and not quoted_string.endswith(quote):
            return quoted_string

        return quoted_string[1:-1]

    @staticmethod
    def _teradata_collapse_arglist(args_list, quote="'"):
        """
        Given a list as an argument this will single quote all the
        list elements and combine them into a single string separated by
        commas.

        PARAMETERS:
            args_list: List containing string/s to be quoted.
            quote: Type of quote to be used for quoting. Default is single quote (').

        RETURNS:
            Single string separated by commas.

        EXAMPLES:
            UtilFuncs._teradata_collapse_arglist(family, "'")

        """
        expr = r"([\"'][\d.\d\w]+\s*[\"'][,]*\s*)+([\"']\s*[\d.\d\w]+[\"']$)"

        # # return None if list is empty
        # if not args_list and not isinstance(args_list, bool):
        #     return args_list

        # if args_list is a list quote all values of the list
        if isinstance(args_list, list):
            '''
            EXAMPLE:
                arg = ['admitted', 'masters', 'gpa', 'stats', 'programming']
                UtilFuncs._teradata_collapse_arglist(arg, "\"")
            RETURNS:
                '"admitted","masters","gpa","stats","programming"'

            '''
            return ",".join("{0}{1}{0}".format(quote, arg) for arg in args_list)
        elif (isinstance(args_list, str)) and (bool(re.match(expr, args_list)) is True):
            '''
            Quotes the arguments which is string of strings with the provided quote variable
            value.
            The expr should be strings separeted by commas. The string values can be digits or
            alphabets.
            For example:
                args_list = '"masters","gpa","stats"'
                quote = "'"
                The args_list is quoted as below based on the quote argument provided:
                    strQuotes = '"masters"','"gpa"','"stats"'
            RETURNS:
                quoted string

            The quoted value is added to list in the functions with other arguments as:
                funcOtherArgs = ["'2.0'", "'POISSON'", "'IDENTITY'", "'0.05'", "'10'", "'False'", "'True'",
                '\'"masters"\',\'"gpa"\',\'"stats"\',\'"programming"\',\'"admitted"\'',
                '\'"masters"\',\'"stats"\',\'"programming"\'']

            '''
            str_val = re.sub(r"\s+", "", args_list)
            args_list = str_val.split(",")
            return ",".join("{0}{1}{0}".format(quote, arg) for arg in args_list)
        # if argVector is any value of int/str/bool type, quote the value
        else:
            return UtilFuncs._teradata_quote_arg(args_list, quote, False)

    @staticmethod
    def _get_metaexpr_using_columns(nodeid, column_info, with_engine=False):
        """
        This internal function takes in input node ID and column information in zipped lists format
        to return metaexpr with or without engine.

        PARAMETERS:
            nodeid - AED DAG node id for which a metaexpr is to be generated.
            column_info - This contains zipped lists of column names and corresponding column types.
            with_engine - A bool parameter, deciding whether to generate metaexpr with engine or not.
                        Default is False.

        RAISES:

        RETURNS:
            metaexpr for the provided node ID and with column inforamtion.

        EXAMPLES:
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "NaiveBayesMap")
            stdout_column_info = zip(stdout_column_names, stdout_column_types)
            UtilFuncs._get_metaexpr_using_columns(node_id_list[0], stdout_column_info)
        """
        if with_engine:
            eng = tdmlctx.get_context()
            meta = sqlalchemy.MetaData(eng)
        else:
            meta = sqlalchemy.MetaData()

        # Get the output table name for node_id from AED
        aed_utils = AedUtils()
        table_name = aed_utils._aed_get_tablename(nodeid)
        db_schema = UtilFuncs._extract_db_name(table_name)
        db_table_name = UtilFuncs._extract_table_name(table_name)

        # Remove quotes because sqlalchemy.Table() does not like the quotes.
        if db_schema is not None:
            db_schema = db_schema[1:-1]
        db_table_name = db_table_name[1:-1]

        # Constructing new Metadata (_metaexpr) without DB; _MetaExpression
        ouptut_table = Table(db_table_name, meta,
                             *(Column(col_name, col_type) for col_name, col_type in column_info),
                             schema=db_schema)
        return _MetaExpression(ouptut_table)

    @staticmethod
    def _get_metaexpr_using_parent_metaexpr(nodeid, metaexpr):
        """
        This internal function takes in input node ID and metaexpr (parents)
        to return metaexpr with or without engine.

        PARAMETERS:
            nodeid:
                Required Argument.
                Specifies AED DAG node id for which a metaexpr is to be generated.

            metaexpr:
                Required Argument.
                _MetaExpression() of a DataFrame objects which is to be used to extract and
                create a new _MetaExpression.

        RAISES:
            None.

        RETURNS:
            metaexpr for the provided node ID and with metaexpr inforamtion.

        EXAMPLES:
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "NaiveBayesMap")
            UtilFuncs._get_metaexpr_using_parent_metaexpr(node_id_list[0], parent_metaexpr)
        """
        meta_cols = metaexpr.t.c
        meta_columns = [c.name for c in meta_cols]
        col_names = []
        col_types = []

        # When column list to retrieve is not provided, return meta-data for all columns.
        for col_name in meta_columns:
            col_names.append(meta_cols[col_name].name)
            col_types.append(meta_cols[col_name].type)

        return UtilFuncs._get_metaexpr_using_columns(nodeid, zip(col_names, col_types))

    @staticmethod
    def _create_table_using_columns(table_name, columns_datatypes, pti_clause=None):
        """
        Create a table with columns.

        PARAMETERS:
            table_name - Fully qualified quoted table name.
            columns_datatypes - Column names and dattypes for the table
            pti_clause - Specifies the string for the primary time index.

        RAISES

        RETURNS:
            True if success, false if fails

        EXAMPLES:
            UtilFuncs._create_table_using_columns('"dbname"."table_name"', 
                            "col1 varchar(10), col2 integer, col3 timestamp")
        """
        crt_table = SQLBundle._build_create_table_using_columns(table_name, columns_datatypes)

        if pti_clause is not None:
            crt_table = "{} PRIMARY TIME INDEX {}".format(crt_table, pti_clause)

        try:
            UtilFuncs._execute_ddl_statement(crt_table)
            return True
        except Exception:
            raise

    @staticmethod
    def _get_engine_name(engine):
        """
        Function to return the name of the engine mapped to the
        argument 'engine' in function mapped dictionary.

        PARAMETERS:
            engine:
                Required Argument.
                Specifies the type of the engine.

        RETURNS:
            Name of the engine.

        RAISES:
            TeradataMLException

        EXAMPLES:
            UtilFuncs._get_engine_name("ENGINE_SQL")

        """
        _Validators._validate_engine(engine)
        supported_engines = TeradataConstants.SUPPORTED_ENGINES.value
        return supported_engines[engine]['name']

    @staticmethod
    def _get_function_mappings_from_config_file(alias_config_file):
        """
        Function to return the function mappings given the location of configuration file in
        argument 'alias_config_file'.

        PARAMETERS:
            alias_config_file:
                Required Argument.
                Specifies the location of configuration file to be read.

        RETURNS:
            Function mappings as a dictionary of function_names to alias_names.

        RAISES:
            TeradataMLException

        EXAMPLES:
            UtilFuncs._get_function_mappings_from_config_file("config_file_location")

        """
        repeated_function_names = []
        function_mappings = {}
        invalid_function_mappings = []
        invalid_function_mappings_line_nos = []
        # Reading configuration files
        with open(alias_config_file, 'r') as fread:
            for line_no, line in enumerate(fread.readlines()):
                line = line.strip()

                # Ignoring empty lines in the config files.
                if line == "":
                    continue

                # If the separator ":" is not present.
                if ':' not in line:
                    invalid_function_mappings.append(line)
                    invalid_function_mappings_line_nos.append(str(line_no + 1))
                else:
                    func_name, alias_name = line.split(":")
                    func_name = func_name.strip()
                    alias_name = alias_name.strip()

                    # First line of 'alias_config_file' has header "functionName:aliasName".
                    if line_no == 0 and func_name == "functionName" and alias_name == "aliasName":
                        continue

                    if func_name == "" or alias_name == "":
                        invalid_function_mappings.append(line)
                        invalid_function_mappings_line_nos.append(str(line_no + 1))
                        continue

                    if func_name.lower() in function_mappings:
                        repeated_function_names.append(func_name.lower())

                    # Loading function maps with lower values for key.
                    function_mappings[func_name.lower()] = alias_name

        # Presence of Invalid function mappings in the 'alias_config_file'.
        if len(invalid_function_mappings) > 0:
            err_ = Messages.get_message(MessageCodes.CONFIG_ALIAS_INVALID_FUNC_MAPPING)
            err_ = err_.format("', '".join(invalid_function_mappings),
                               ", ".join(invalid_function_mappings_line_nos),
                               alias_config_file)
            raise TeradataMlException(err_, MessageCodes.CONFIG_ALIAS_INVALID_FUNC_MAPPING)

        # Raising teradataml exception if there are any duplicates in function names.
        if len(repeated_function_names) > 0:
            raise TeradataMlException(Messages.get_message(
                MessageCodes.CONFIG_ALIAS_DUPLICATES).format(alias_config_file,
                                                             ", ".join(repeated_function_names)),
                                      MessageCodes.CONFIG_ALIAS_DUPLICATES)

        return function_mappings

    @staticmethod
    def _check_alias_config_file_exists(vantage_version, alias_config_file):
        """
        Function to validate whether alias_config_file exists for the current vantage version.

        PARAMETERS:
            vantage_version:
                Required Argument.
                Specifies the current vantage version.

            alias_config_file:
                Required Argument.
                Specifies the location of configuration file to be read.

        RETURNS:
            True, if the file 'alias_config_file' is present in the
            teradataml/config directory for the current vantage version.

        RAISES:
            TeradataMLException

        EXAMPLES:
            UtilFuncs._check_alias_config_file_exists("vantage1.0", "config_file_location")

        """
        # Raise exception if alias config file is not defined.
        if not Path(alias_config_file).exists():
            raise TeradataMlException(Messages.get_message(
                MessageCodes.CONFIG_ALIAS_CONFIG_FILE_NOT_FOUND).format(alias_config_file,
                                                                        vantage_version),
                                      MessageCodes.CONFIG_ALIAS_CONFIG_FILE_NOT_FOUND)
        return True

    @staticmethod
    def _as_list(obj):
        """
        Function to convert an object to list, i.e., just enclose the value passed to the
        function in a list and return the same, if it is not of list type.
        PARAMETERS:
            obj:
                Required Argument.
                Specifies the object to be enclosed in a list.
                Types: Any type except list.
        RETURNS:
            list
        RAISES:
            None.
        EXAMPLES:
            obj = UtilFuncs._as_list("vantage1.0")
        """
        return obj if isinstance(obj, list) else [obj]
    
from teradataml.common.aed_utils import AedUtils
from teradataml.dbutils.filemgr import remove_file
