# -*- coding: utf-8 -*-
"""

Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: Mark.Sandan@teradata.com
Secondary Owner:

"""
#  This module deals with creating SQLEngine expressions
#  for tables and columns as well as sql for displaying 
#  the DataFrame. The objects in this module are internal 
#  and implement the interfaces in sql_interfaces.py

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.options.configure import configure
from teradataml.options.display import display
from teradataml.utils.dtypes import _Dtypes
from teradataml.utils.validators import _Validators
from teradataml.dataframe.vantage_function_types import _get_function_expression_type
from teradatasqlalchemy.types import _TDType
from .sql_interfaces import TableExpression, ColumnExpression
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy import (Table, Column, literal, MetaData, func, or_, and_, literal_column, null)
from sqlalchemy.sql.expression import text, case as case_when
import functools
import sqlalchemy as sqlalc

import re

from teradatasqlalchemy.dialect import dialect as td_dialect, compiler as td_compiler
from teradatasqlalchemy import (INTEGER, SMALLINT, BIGINT, BYTEINT, DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy import (DATE, TIME, TIMESTAMP)
from teradatasqlalchemy import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)
from teradatasqlalchemy import (INTERVAL_DAY, INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE,
                                INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR, INTERVAL_HOUR_TO_MINUTE,
                                INTERVAL_HOUR_TO_SECOND, INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND,
                                INTERVAL_MONTH, INTERVAL_SECOND, INTERVAL_YEAR,
                                INTERVAL_YEAR_TO_MONTH)
from teradatasqlalchemy import (PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP)
import decimal
import datetime as dt

def _resolve_value_to_type(value, **kw):
    """
    DESCRIPTION:
        Internal function for coercing python literals to sqlalchemy_terdata types
        or retrieving the derived type of ColumnExpression

    PARAMETERS:
        value: a python literal type or ColumnExpression instance
        **kw: optional parameters
            len_: a length for the str type

    RETURNS:
        result: sqlalchemy TypeEngine derived type or ColumnExpression derived type

    Note:
        - Currently the supported literal types are str/float/int/decimal
          since these are being rendered already by teradatasqlalchemy

        - Mainly used in assign when passing literal values to be literal columns
    """
    length = kw.get('len_', configure.default_varchar_size)

    type_map = {
        str: VARCHAR(length, charset = 'UNICODE'),
        bytes: VARBYTE(length),
        int: INTEGER(),
        float: FLOAT(),
        bool: BYTEINT(),
        decimal.Decimal: DECIMAL(38,37),
        dt.date: DATE(),
        dt.datetime: TIMESTAMP(),
        dt.time: TIME()
    }

    result = type_map.get(type(value))

    if isinstance(value, ColumnExpression):
        result = value.type
    return result

def _handle_sql_error(f):
    """
    DESCRIPTION:
        This decorator wraps python special methods that generate SQL for error handling.
        Any error messages or error codes involving sql generating methods
        can be considered here.

    PARAMETERS:
        A function or method that generates sql

    EXAMPLES:
        @_handle_sql_error
        def __and__(self, other)
    """
    @functools.wraps(f)
    def binary(*args, **kw):

        self_ = None
        other_ = None

        if len(args) == 2:
            self_, other_ = args

        # Used to determine whether multiple dataframes are given in _SQLColumnExpression.
        multiple_dataframes = False

        try:
            if self_ is not None and other_ is not None and\
                isinstance(self_, ColumnExpression) and\
                isinstance(other_, ColumnExpression) and\
                self_.table is not None and other_.table is not None:

                # If table names or schema names are different or has_multiple_dataframes flag
                # is True for any of the two _SQLColumnExpressions.
                if self_.table.name != other_.table.name or\
                    self_.table.schema != other_.table.schema or\
                    self_.get_flag_has_multiple_dataframes() == True or\
                    other_.get_flag_has_multiple_dataframes() == True:

                    multiple_dataframes = True

            # If _SQLColumnExpressions have NULL tables (ie at later levels of a multi level
            # expression).
            elif isinstance(self_, ColumnExpression) and\
                isinstance(other_, ColumnExpression) and\
                self_.table is None and other_.table is None:

                multiple_dataframes = self_.get_flag_has_multiple_dataframes() | \
                                      other_.get_flag_has_multiple_dataframes()

            res = f(*args, **kw)
            # Assign True or False to resultant _SQLColumnExpression based on previous two
            # _SQLColumnExpressions.
            res.set_flag_has_multiple_dataframes(multiple_dataframes)
            res.original_column_expr = [self_, other_]

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode) from err

        return res

    return binary


class _MetaExpression(object):
    """
    The _MetaExpression contains the TableExpression and provides the DataFrame with metadata
    from the underlying Table as well as methods for translating and generating SQL.

    The main responsibility of this class is to translate sql expressions internally in DataFrame.
    Other responsibilities are delegated to the underlying TableExpression.

    This class is internal.
    """

    def __init__(self, table, **kw):
        """
        PARAMETERS:
            table: the table to use for TableExpression

            kw: kwargs for implementation specific TableExpressions/ColumnExpressions
              - dialect: an implementation of a SQLAlchemy Dialect
        """

        self._dialect = kw.get('dialect', td_dialect())
        self.__t = _SQLTableExpression(table, **kw)

    def __getattr__(self, key):
        """
        DESCRIPTION:
            Retrieve an attribute from _MetaExpression or the underlying TableExpression

        PARAMETERS:
            key: attribute name

        RAISES:
            AttributeError if attribute can't be found
        """

        res = getattr(self.__t, key, None)
        if res is None:
            raise AttributeError('Unable to find attribute: %s' % key)

        return res

    @property
    def _n_rows(self):
        return self.__t._n_rows

    @_n_rows.setter
    def _n_rows(self, value):
        """Use n number of rows for print() instead of display.max_rows for this metaexpr. If 0, display.max_rows is used"""
        if not isinstance(value, int) or value <= 0:
            raise ValueError('n_rows must be a positive int.')

        self.__t._n_rows = value

    def __repr__(self):
      return repr(self.__t)

class _PandasTableExpression(TableExpression):

    def _assign(self, drop_columns, **kw):
        """
        DESCRIPTION:
            Internal method for DataFrame.assign
            Generates the new select list column expressions and
            provides an updated _SQLTableExpression for the new _MetaExpression

        PARAMETERS:
            drop_columns (optional):  bool If True, drop columns that are not specified in assign. The default is False.
            kw: keyword, value pairs
                    - keywords are the column names.
                    - values can be column arithmetic expressions and int/float/string literals.

        RAISES:
            ValueError when a value that is callable is given in kwargs


        See Also
        --------
            DataFrame.assign


        Returns
        -------
        result : -Updated _SQLTableExpression
                 -list of compiled column expressions

        Note: This method assumes that the values in each key of kw
              are valid types (supported python literals or ColumnExpressions)
        """
        compiler = td_compiler(td_dialect(), None)
        current = {c.name for c in self.c}

        assigned_expressions = []

        existing = [(c.name, c) for c in self.c]
        new = [(label, expression) for label, expression in kw.items() if label not in current]
        new = sorted(new, key = lambda x: x[0])

        for alias, expression in existing + new:
            if drop_columns and alias not in kw:
                continue

            else:
                expression = kw.get(alias, expression)
                if isinstance(expression, ClauseElement):
                    expression = _SQLColumnExpression(expression)

                type_ = _resolve_value_to_type(expression)

                if not isinstance(expression, ColumnExpression):
                    # wrap literals. See DataFrame.assign for valid literal values
                    if expression == None:
                        expression = _SQLColumnExpression(null())
                    else:
                        expression = _SQLColumnExpression(literal(expression, type_ = type_))

                aliased_expression = compiler.visit_label(expression.expression.label(alias),
                                                        within_columns_clause=True,
                                                        include_table = False,
                                                        literal_binds = True)
                assigned_expressions += [(alias, aliased_expression, type_)]

        if len(assigned_expressions) >= TeradataConstants['TABLE_COLUMN_LIMIT'].value:
            raise ValueError('Maximum column limit reached')

        cols = (Column(name, type_) for name, expression, type_ in assigned_expressions)
        t = Table(self.name, MetaData(), *cols)

        return (_SQLTableExpression(t), assigned_expressions)


    def _filter(self, axis, op, index_labels, **kw):
        """
        DESCRIPTION:
            Subset rows or columns of dataframe according to labels in the specified index.

        PARAMETERS:
            axis: int
                1 for columns to filter
                0 for rows to filter

            op: string
                A string representing the way to index.
                This parameter is used along with axis to get the correct expression.

            index_labels: list or iterable of string
                contains column names/labels of the DataFrame

            **kw: keyword arguments
                items: None or a list of strings
                like: None or a string representing a substring
                regex: None or a string representing a regex pattern

                optional keywords:
                match_args: string of characters to use for REGEXP_SUBSTR

        RETURNS:
            tuple of two elements:
                Either a tuple of (list of str, 'select') if axis == 1
                Or a tuple of (list of ColumnExpressions, 'where') if axis == 0

        Note:
            Implementation outline:

            axis == 1 (column based filter)

                items - [colname for colname in colnames if colname in items]
                like - [colname for colname in colnames if like in colname]
                regex - [colname for colname in colnames if re.search(regex, colname) is not None]

            axis == 0 (row value based filter on index)

                items - WHERE index IN ( . . . )
                like -  same as regex except the string (kw['like']) is a substring pattern
                regex - WHERE REGEXP_SUBSTR(index, regex, 1, 1, 'c')


        EXAMPLES:

            # self is a reference to DataFrame's _metaexpr.
            # This method is usually called from the DataFrame.
            # Suppose the DataFrame has columns ['a', 'b', 'c'] in its index:

            # select columns given in items list
            self._filter(1, 'items', ['a', 'b', 'c'], items = ['a', 'b'])

            # select columns matching like pattern (index_labels is ignored)
            self._filter(1, 'like', ['a', 'b', 'c'], like = 'substr')

            # select columns matching regex pattern (index_labels is ignored)
            self._filter(1, 'regex', ['a', 'b', 'c'], regex = '[0|1]')

            # select rows where index column(s) are in items list
            self._filter(0, 'items', ['a', 'b', 'c'], items = [('a', 'b', 'c')])

            # select rows where index column(s) match the like substring
            self._filter(0, 'like', ['a', 'b', 'c'], like = 'substr')

            # select rows where index column(s) match the regex pattern
            self._filter(0, 'regex', ['a', 'b', 'c'], regex = '[0|1]')
        """

        impls = dict({

            ('like', 1):  lambda col: kw['like'] in col.name,

            ('regex', 1): lambda col: re.search(kw['regex'], col.name) is not None,

            ('items', 0): lambda colexp, lst: colexp.in_(lst),

            ('like', 0):  lambda colexp: func.regexp_substr(colexp, kw['like'], 1, 1,
                                                            kw.get('match_arg', 'c')) != None,

            ('regex', 0): lambda colexp: func.regexp_substr(colexp, kw['regex'], 1, 1,
                                                            kw.get('match_arg', 'c')) != None
        }
        )

        filtered_expressions = []
        filter_ = impls.get((op, axis))
        is_char_like = lambda x: isinstance(x, CHAR) or\
                                 isinstance(x, VARCHAR) or\
                                 isinstance(x, CLOB)
        if axis == 1:

            # apply filtering to columns and then select()
            if op == 'items':
                for col in kw['items']:
                    filtered_expressions += [col]

            else:
                for col in self.c:
                    if filter_(col):
                        filtered_expressions += [col.name]

        else:
            # filter based on index values
            # apply filtering to get appropriate ColumnExpression then __getitem__()

            if op == 'items':

                if len(index_labels) == 1:

                    # single index case
                    for c in self.c:
                        if c.name in index_labels:

                            expression = c.expression
                            filtered_expressions += [filter_(expression, kw['items'])]

                else:

                    # multi index case
                    items_by_position = zip(*kw['items'])

                    # traverse in the order given by index_label
                    for index_col, item in zip(index_labels, items_by_position):
                        for c in self.c:
                            if c.name == index_col:
                                expression = c.expression
                                filtered_expressions += [filter_(expression, item)]

            else:

                var_size = kw.get('varchar_size', configure.default_varchar_size)
                for c in self.c:
                    if c.name in index_labels:

                        expression = c.expression
                        if not is_char_like(expression.type):
                            # need to cast to char-like operand for REGEXP_SUBSTR
                            expression = expression.cast(type_ = VARCHAR(var_size))

                        filtered_expressions += [filter_(expression)]

            if axis == 0:

                if op == 'items' and len(index_labels) > 1:

                    # multi index item case is a conjunction
                    filtered_expressions = _SQLColumnExpression(and_(*filtered_expressions))

                else:
                    filtered_expressions = _SQLColumnExpression(or_(*filtered_expressions))

        return filtered_expressions


class _SQLTableExpression(_PandasTableExpression):
    """
        This class implements TableExpression and is contained
        in the _MetaExpressions class

        It handles:
            - SQL generation for the table or all it's columns
            - DataFrame metadata access using a sqlalchemy.Table

      This class is internal.
    """
    def __init__(self, table, **kw):

        """
        DESCRIPTION:
            Initialize the _SQLTableExpression

        PARAMETERS:
            table : A sqlalchemy.Table
            kw**: a dict of optional parameters
                - column_order: a collection of string column names
                                in the table to be ordered in the c attribute
        """

        self.t = table
        if 'column_order' in kw:
            # Use DataFrame.columns to order the columns in the metaexpression
            columns = []
            for c in kw['column_order']:
                name = c.strip()
                col = table.c.get(name, table.c.get(name.lower(), table.c.get(name.upper())))

                if col is None:
                    raise ValueError('Reflected column names do not match those in DataFrame.columns')

                columns.append(_SQLColumnExpression(col))

            self.c = columns

        else:
            self.c = [_SQLColumnExpression(c) for c in table.c]

        self._n_rows = 0


    @property
    def c(self):
        """
        Returns the underlying collection of _SQLColumnExpressions
        """
        return self.__c

    @c.setter
    def c(self, collection):
        """
        Set the underlying map of _SQLColumnExpressions

        PARAMETERS:
            collection: a dict of _SQLColumnExpressions

        """
        is_sql_colexpression = lambda x: type(x) == _SQLColumnExpression
        valid_collection = isinstance(collection, list) and\
                         len(collection) > 0 and\
                         all(map(is_sql_colexpression, collection))

        if (not valid_collection):
            raise ValueError("collection must be a non empty list of _SQLColumnExpression instances. Got {}".format(collection))


        self.__c = collection

    @property
    def name(self):
        """
        Returns the name of the underlying SQLAlchemy Table
        """
        return self.t.name

    @property
    def t(self):
        """
        Returns the underlying SQLAlchemy Table
        """
        return self.__t

    @t.setter
    def t(self, table):
        """
        Set the underlying SQLAlchemy Table

        PARAMETERS:
            table : A sqlalchemy.Table
        """
        if (not isinstance(table, Table)):
            raise ValueError("table must be a sqlalchemy.Table")

        self.__t = table

    def __repr__(self):
        """
        Returns a SELECT TOP string representing the underlying table.
        For representation purposes:
            - the columns are cast into VARCHAR
            - certain numeric columns are first rounded
            - character-like columns are unmodfied
            - byte-like columns are called with from_bytes to show them as ASCII


        Notes:
            - The top integer is taken from teradataml.options
            - The rounding value for numeric types is taken from teradataml.options
            - from_bytes is called on byte-like columns to represent them as ASCII encodings
              See from_bytes for more info on different encodings supported:
              Teradata® Database SQL Functions, Operators, Expressions, and Predicates, Release 16.20

        """
        # TODO: refactor this to be in the ColumnExpression instances
        single_quote = literal_column("''''")
        from_bytes = lambda c: ('b' + single_quote + func.from_bytes(c, display.byte_encoding) + single_quote).label(c.name)
        display_decimal = lambda c: func.round(c, display.precision).cast(type_ = DECIMAL(38, display.precision)).label(c.name)
        display_number = lambda c: func.round(c, display.precision).label(c.name)

        compiler = td_compiler(td_dialect(), None)
        var_size = configure.default_varchar_size
        cast_expr = lambda c: c.cast(type_ = VARCHAR(var_size)).label(c.name)

        max_rows = display.max_rows
        if self._n_rows > 0:
            max_rows = self._n_rows

        res = 'select top {} '.format(max_rows)
        expressions = []

        for c in self.c:

            if isinstance(c.type, (CHAR, VARCHAR, CLOB, FLOAT, INTEGER, SMALLINT, BIGINT, BYTEINT)):
                expression = c.expression.label(c.name)

            elif isinstance(c.type, (BYTE, VARBYTE, BLOB)):
                expression = from_bytes(c.expression)

            elif isinstance(c.type, DECIMAL):
                expression = cast_expr(display_decimal(c.expression))

            elif isinstance(c.type, NUMBER):
                expression = cast_expr(display_number(c.expression))

            else:
                expression = cast_expr(c.expression)

            expressions.append(compiler.visit_label(expression,
                                                within_columns_clause=True,
                                                include_table = False,
                                                literal_binds = True))

        return res + ', '.join(expressions)

class _LogicalColumnExpression(ColumnExpression):

    """
        The _LogicalColumnExpression implements the logical special methods
        for _SQLColumnExpression.
    """

    def __coerce_to_text(self, other):
        """
        Internal function to coerce to text, using SQLAlchemy text(), a string literal passed as an argument.

        PARAMETERS:
            other: A python literal or another ColumnExpression.

        RETURNS:
            Python literal coerced to text if the input is a string literal, else the input argument itself.
        """
        if isinstance(other, str):
            return text(other)
        return other

    @_handle_sql_error
    def __and__(self, other):
        """
        Compute the logical and between two column expressions using &

        PARAMETERS:
            other : A python literal or another ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[(c1 > 0) & (c2 > 0)]
            df[(c1 > 0) & (c2 > 0) & (c1 > c2)]

        """
        other = self.__coerce_to_text(other)
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression & expr)
        return res

    @_handle_sql_error
    def __rand__(self, other):
        """
        Reverse and
        See __and__
        """
        return self & other

    @_handle_sql_error
    def __or__(self, other):

        """
        Compute the logical or between two column expressions using |


        PARAMETERS:
            other : literal or ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[(c1 > 0) | (c2 > 0)]
            df[(c1 > 0) | (c2 > 0) | (c1 > c2)]
        """
        other = self.__coerce_to_text(other)
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression | expr)
        return res

    @_handle_sql_error
    def __ror__(self, other):
        """
        Reverse or
        See __or__
        """
        return self | other

    @_handle_sql_error
    def __invert__(self):

        """
        Compute the logical not between two column expressions using ~


        PARAMETERS:
            self

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        See Also
        --------

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[~(c1 > 0)]
            df[~((c1 > 0) | (c2 > 0))]
        """
        return _SQLColumnExpression(~self.expression)

    @_handle_sql_error
    def __gt__(self, other):
        """
        Compare the column expression using >

        PARAMETERS:
            other : A python literal or another ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1 > 0]
            df[(c1 > 0) & (c2 > c1)]

        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression > expr)
        return res

    @_handle_sql_error
    def __lt__(self, other):

        """
        Compare the column expression using <

        PARAMETERS:
            other : A python literal or another ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1 < 0]
            df[(c1 < 0) & (c2 < c1)]

        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression < expr)
        return res

    @_handle_sql_error
    def __ge__(self, other):
        """
        Compare the column expression using >=

        PARAMETERS:
            other : A python literal or another ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1 >= 0]
            df[(c1 >= 0) & (c2 >= c1)]

        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression >= expr)
        return res

    @_handle_sql_error
    def __le__(self, other):
        """
        Compare the column expression using <=

        PARAMETERS:
            other : A python literal or another ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1 <= 0]
            df[(c1 <= 0) & (c2 <= c1)]

        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression <= expr)
        return res

    @_handle_sql_error
    def __xor__(self, other):
        """
        Compute the logical or between two column expressions using ^

        PARAMETERS:
            other : A python literal or another ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[(c1 > 0) ^ (c2 > c1)]

        """
        other = self.__coerce_to_text(other)
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression((self.expression | expr) & ~(self.expression & expr))
        return res

    @_handle_sql_error
    def __rxor__(self, other):
        """
        Reverse xor
        See __xor__
        """
        return self ^ other

    @_handle_sql_error
    def __eq__(self, other):
        """
        Compute equality using ==

        PARAMETERS:
            other : A python literal or another ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1 == 0]
            df[(c1 == 0) & (c2 == c1)]

        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression == expr)
        return res

    @_handle_sql_error
    def __ne__(self, other):
        """
        Compute inequality using !=

        PARAMETERS:
            other : A python literal or another ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1 != 0]
            df[(c1 != 0) & (c2 != c1)]

        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression != expr)
        return res


class _ArithmeticColumnExpression(ColumnExpression):

    """
        The _ArithmeticColumnExpression implements the arithmetic special methods
        for _SQLColumnExpression.
    """

    @_handle_sql_error
    def __add__(self, other):

        """
        Compute the sum between two column expressions using +
        This is also the concatenation operator for string-like columns

        PARAMETERS:
            other : literal or ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(x = 1 + c2)
            df.assign(x = c2 + c1)
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression + expr)
        return res

    @_handle_sql_error
    def __radd__(self, other):

        """
        Compute the rhs sum between two column expressions using +

        PARAMETERS:
            other : literal or ColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(x = 1 + c2)
            df.assign(x = c2 + c1)
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(expr + self.expression)
        return res

    @_handle_sql_error
    def __sub__(self, other):
        """
        Compute the difference between two column expressions using -

        PARAMETERS:
            other : literal or ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame('df')
            c1 = df.c1
            c2 = df.c2
            df.assign(c1_minus_c2 = c1 - c2)
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression - expr)
        return res

    @_handle_sql_error
    def __rsub__(self, other):
        """
            Compute the difference between two column expressions using -
            See __sub__.
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(expr - self.expression)
        return res

    @_handle_sql_error
    def __mul__(self, other):
        """
        Compute the product between two column expressions using *

        PARAMETERS:
            other : literal or ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame('df')
            c1 = df.c1
            c2 = df.c2
            df.assign(c1_x_c2 = c1 * c2)
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression * expr)
        return res

    @_handle_sql_error
    def __rmul__(self, other):

        """
            Compute the product between two column expressions using *
            See __truediv__
        """
        return self * other

    @_handle_sql_error
    def __truediv__(self, other):
        """
        Compute the division between two column expressions using /

        PARAMETERS:
            other : literal or ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(c1 /c2)
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression / expr)
        return res

    @_handle_sql_error
    def __rtruediv__(self, other):

        """
            Compute the division between two column expressions using /
            See __truediv__
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(expr / self.expression)
        return res

    @_handle_sql_error
    def __floordiv__(self, other):
        """
        Compute the floor division between two column expressions using //

        PARAMETERS:
            other : literal or ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(floord = c1 // c2)
        """

        raise NotImplementedError()

    @_handle_sql_error
    def __rfloordiv__(self, other):

        """
            Compute the floor division between two column expressions using //
            See __floordiv__
        """
        raise NotImplementedError()

    @_handle_sql_error
    def __mod__(self, other):
        """
        Compute the MOD between two column expressions using %

        PARAMETERS:
            other : literal or ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame('df')
            c1 = df.c1
            c2 = df.c2
            df.assign(c1modc2 = c1 % c2)
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression % expr)
        return res

    @_handle_sql_error
    def __rmod__(self, other):
        """
            Compute the MOD between two column expressions using %
            Note: string types already override the __mod__ . We cannot override it
                  if the string type is the left operand.

            See __mod__
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other

        if type(expr) is str:
            raise ValueError('MOD with string literals as the left operand is unsupported')

        res = _SQLColumnExpression(expr % self.expression)
        return res

    @_handle_sql_error
    def __neg__(self):
        """
        Compute the unary negation of the column expressions using -

        PARAMETERS:
            other : literal or ColumnExpression

        RETURNS:
            res : _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            df = DataFrame(...)

            c1 = df.c1
            a = df[c1 >= 0]

            c1 = -df.c1
            b = df[c1 <= 0]

            a == b
        """

        res = _SQLColumnExpression(-self.expression)
        return res


# Accessor classes
class _StringMethods(object):
    """
    A class for implementing string methods for string-like ColumnExpressions
    This accessor class should only be used from the str property of a ColumnExpression

    This class is internal.
    """
    def __init__(self, c):
        """
            PARAMETERS:
                c: A ColumnExpression instance

        """
        self.c = c

    def lower(self):
        """
        This function maps character values to lowercase.

        REFERENCE:
            SQL Functions, Operators, Expressions, and Predicates
            Chapter 26 String Operators and Functions

        RETURNS:
            A str Series with values lowercased

        EXAMPLES:
            >>> tdf = DataFrame('iris')
            >>> tdf
               SepalLength  SepalWidth  PetalLength  PetalWidth             Name
            0        5.500       2.400        3.800        1.10  Iris-versicolor
            1        4.900       2.400        3.300        1.00  Iris-versicolor
            2        7.700       2.600        6.900        2.30   Iris-virginica
            3        5.700       2.800        4.500        1.30  Iris-versicolor
            4        7.700       3.000        6.100        2.30   Iris-virginica
            5        6.300       2.500        4.900        1.50  Iris-versicolor
            6        5.700       3.000        4.200        1.20  Iris-versicolor
            7        6.900       3.200        5.700        2.30   Iris-virginica
            8        5.000       3.500        1.300        0.30      Iris-setosa
            9        1.012       1.202        3.232        4.23             None

            >>> tdf.assign(drop_columns = True, lower = tdf.Name.str.lower())
                       lower
            0   iris-virginica
            1   iris-virginica
            2  iris-versicolor
            3  iris-versicolor
            4  iris-versicolor
            5   iris-virginica
            6   iris-virginica
            7  iris-versicolor
            8  iris-versicolor
            9      iris-setosa

            >>> tdf[tdf.Name.str.lower() == 'iris-virginica']
             SepalLength  SepalWidth  PetalLength  PetalWidth            Name
            0          6.9         3.1          5.4         2.1  Iris-virginica
            1          6.4         3.1          5.5         1.8  Iris-virginica
            2          5.8         2.8          5.1         2.4  Iris-virginica
            3          6.9         3.2          5.7         2.3  Iris-virginica
            4          7.7         3.0          6.1         2.3  Iris-virginica
            5          6.5         3.0          5.5         1.8  Iris-virginica
            6          6.3         2.8          5.1         1.5  Iris-virginica
            7          7.9         3.8          6.4         2.0  Iris-virginica
            8          7.7         2.6          6.9         2.3  Iris-virginica
            9          7.7         2.8          6.7         2.0  Iris-virginica

        """
        res = _SQLColumnExpression(
                func.lower(
                  self.c.expression,
                  type_ = self.c.type
                )
               )
        return res

    def contains(self, pattern, case = True, na = None, **kw):
        """
        Test if the regexp pattern matches strings in the Series.

        PARAMETERS:
            pattern: str. A regex pattern
            case: bool. True if case-sensitive matching, else False for case-insensitive matching
            na: bool, str, or numeric python literal. None by default.
                Specifies an optional fill value for NULL values in the column

            **kw: optional parameters to pass to regexp_substr
                - match_arg : a string of characters to use for the match_arg parameter for REGEXP_SUBSTR
                          See the Reference for more information about the match_arg parameter.
                Note: specifying match_arg overrides the case parameter

        REFERENCE:
            SQL Functions, Operators, Expressions, and Predicates
            Chapter 24: Regular Expression Functions

        RETURNS:
            A numeric Series of values where:
                - Nulls are replaced by the fill parameter
                - A 1 if the value matches the pattern or else 0
            The type of the series is upcasted to support the fill value, if specified.

        EXAMPLES:
            >>> tdf = DataFrame('iris')
            >>> species = tdf['Name']
            >>> tdf.assign(drop_columns = True,
                         Name = species,
                         has_setosa = species.str.contains('setosa'))

                         Name has_setosa
            0      Iris-setosa          1
            1  Iris-versicolor          0
            2      Iris-setosa          1
            3  Iris-versicolor          0
            4      Iris-setosa          1
            5  Iris-versicolor          0
            6  Iris-versicolor          0
            7   Iris-virginica          0
            8      Iris-setosa          1
            9             None       None

            # case-sensitive by default
            >>> tdf.assign(drop_columns = True,
                         Name = species,
                         has_iris = species.str.contains('iris'))

                        Name   has_iris
            0  Iris-versicolor          0
            1  Iris-versicolor          0
            2   Iris-virginica          0
            3  Iris-versicolor          0
            4   Iris-virginica          0
            5  Iris-versicolor          0
            6  Iris-versicolor          0
            7   Iris-virginica          0
            8      Iris-setosa          0
            9             None       None

            >>> tdf.assign(drop_columns = True,
                         Name = species,
                         has_iris = species.str.contains('iris', case = False))

                        Name   has_iris
            0  Iris-versicolor          1
            1  Iris-versicolor          1
            2   Iris-virginica          1
            3  Iris-versicolor          1
            4   Iris-virginica          1
            5  Iris-versicolor          1
            6  Iris-versicolor          1
            7   Iris-virginica          1
            8      Iris-setosa          1
            9             None       None

            # specify a literal for null values
            >>> tdf.assign(drop_columns = True,
                         Name = species,
                         has_iris = species.str.contains('iris', case = False, na = 'no value'))

                        Name   has_iris
            0  Iris-versicolor          1
            1  Iris-versicolor          1
            2   Iris-virginica          1
            3  Iris-versicolor          1
            4   Iris-virginica          1
            5  Iris-versicolor          1
            6  Iris-versicolor          1
            7   Iris-virginica          1
            8      Iris-setosa          1
            9             None   no value

          # filter where Name has 'setosa'
          >>> tdf[species.str.contains('setosa') == True].select('Name')
                      Name 
          0    Iris-setosa 
          1    Iris-setosa 
          2    Iris-setosa 
          3    Iris-setosa 
          4    Iris-setosa 
          5    Iris-setosa 
          6    Iris-setosa 
          7    Iris-setosa 
          8    Iris-setosa 
          9    Iris-setosa 

          # filter where Name does not have 'setosa'
          >>> tdf[species.str.contains('setosa') == False].select('Name')
                          Name 
          0    Iris-versicolor 
          1    Iris-versicolor 
          2    Iris-versicolor 
          3    Iris-versicolor 
          4    Iris-versicolor 
          5     Iris-virginica 
          6     Iris-virginica 
          7     Iris-virginica 
          8    Iris-versicolor 
          9     Iris-virginica 

          # you can use numeric literals for True (1) and False (0)
          >>> tdf[species.str.contains('setosa') == 1].select('Name')
                      Name 
          0    Iris-setosa 
          1    Iris-setosa 
          2    Iris-setosa 
          3    Iris-setosa 
          4    Iris-setosa 
          5    Iris-setosa 
          6    Iris-setosa 
          7    Iris-setosa 
          8    Iris-setosa 
          9    Iris-setosa 

          >>> tdf[species.str.contains('setosa') == 0].select('Name')
                          Name 
          0    Iris-versicolor 
          1    Iris-versicolor 
          2    Iris-versicolor 
          3    Iris-versicolor 
          4    Iris-versicolor 
          5     Iris-virginica 
          6     Iris-virginica 
          7     Iris-virginica 
          8    Iris-versicolor 
          9     Iris-virginica 

        """
        if not isinstance(pattern, str):
            raise TypeError('str.contains requires the pattern parameter to be a string.')

        if not isinstance(case, bool):
            raise TypeError('str.contains requires the case parameter to be True or False.')

        match_arg = kw.get('match_arg', 'c' if case else 'i')
        regexp_substr = func.regexp_substr(
                           self.c.expression,
                           pattern, 1, 1,
                           match_arg)

        expr = case_when([(regexp_substr == None, 0)], else_ = 1)
        expr = case_when([(self.c.expression == None, na)], else_ = expr)

        if na is not None:

            # na should be numeric or string-like or bool
            if not isinstance(na, (str, float, int, decimal.Decimal, bool)):
                raise TypeError('str.contains requires the na parameter to be a numeric, string, or bool literal.')

            # the resulting type is the type of the na (if not None), otherwise BYTEINT
            type_ = _resolve_value_to_type(na, len_ = len(na) if isinstance(na, str) else None)
            expr.type = type_

        return _SQLColumnExpression(expr)

    def strip(self):
        """
        Remove leading and trailing whitespace.

        REFERENCE:
            SQL Functions, Operators, Expressions, and Predicates
            Chapter 26 String Operators and Functions

        RETURNS:
            A str Series with leading and trailing whitespace removed

        EXAMPLES:
            >>> tdf = DataFrame('iris')
            >>> species = tdf['Name']

            # create a column with some whitespace
            >>> wdf = df.assign(drop_columns = True,
                              species = species,
                              w_spaces = '\n ' + species + '\v\f \t')

                     species                 w_spaces
            0  Iris-versicolor  \n Iris-versicolor

            \t
            1  Iris-versicolor  \n Iris-versicolor

            \t
            2   Iris-virginica   \n Iris-virginica

            \t
            3  Iris-versicolor  \n Iris-versicolor

            \t
            4   Iris-virginica   \n Iris-virginica

            \t
            5  Iris-versicolor  \n Iris-versicolor

            \t
            6  Iris-versicolor  \n Iris-versicolor

            \t
            7   Iris-virginica   \n Iris-virginica

            \t
            8      Iris-setosa      \n Iris-setosa

            \t
            9             None                     None


            >>> wdf.assign(drop_columns = True,
                         wo_wspaces = wdf.w_spaces.str.strip())

                  wo_wspaces
            0  Iris-versicolor
            1  Iris-versicolor
            2   Iris-virginica
            3  Iris-versicolor
            4   Iris-virginica
            5  Iris-versicolor
            6  Iris-versicolor
            7   Iris-virginica
            8      Iris-setosa
            9             None

        """
        whitespace = '\n \t\r\v\f'
        res = func.rtrim(
                func.ltrim(
                    self.c.expression,
                    whitespace
                ),
                whitespace, type_ = self.c.type
              )

        return _SQLColumnExpression(res)

class _SeriesColumnExpression(ColumnExpression):

    """
        The _SeriesColumnExpression implements the pandas.Series methods
        for _SQLColumnExpression.
    """

    @property # TODO: consider making this a cached property
    def str(self):
        """
        The string accessor.
        Upon validation, returns a reference to a _StringMethods instance
        """
        if not isinstance(self.type, (CHAR, VARCHAR, CLOB)):
            raise AttributeError('The str accessor is only valid for string-like columns (CHAR, VARCHAR, or CLOB).')

        elif isinstance(getattr(self, '_SeriesColumnExpression__str', None), _StringMethods):
            return self.__str

        # otherwise, initialize the accessor
        self.str = _StringMethods(self)
        return self.__str

    @str.setter
    def str(self, accessor):
        """
        """
        if isinstance(accessor, _StringMethods):
            self.__str = accessor

        # otherwise, just ignore

    def gt(self, other):
      """
      PARAMETERS:
          other : ColumnExpression or literal

      RETURNS:
          _SQLColumnExpression

      EXAMPLES:
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.gt(0)]
          df[c1.gt(0) & c2.gt(c1)]
      """
      return self > other

    def ge(self, other):
      """
      PARAMETERS:
          other : ColumnExpression or literal

      RETURNS:
          _SQLColumnExpression

      EXAMPLES:
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.ge(0)]
          df[c1.ge(0) & c2.ge(c1)]
      """
      return self >= other

    def lt(self, other):
      """
      PARAMETERS:
          other : ColumnExpression or literal

      RETURNS:
          _SQLColumnExpression

      EXAMPLES:
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.lt(0)]
          df[c1.lt(0) & c2.lt(c1)]
      """
      return self < other

    def le(self, other):
      """
      PARAMETERS:
          other : ColumnExpression or literal

      RETURNS:
          _SQLColumnExpression

      EXAMPLES:
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.le(0)]
          df[c1.le(0) & c2.le(c1)]
      """
      return self <= other

    def eq(self, other):
        """
        PARAMETERS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1.eq(0)]
            df[c1.eq(0) & c2.eq(c1)]
        """
        return self == other

    def ne(self, other):
        """
        PARAMETERS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1.ne(0)]
            df[c1.ne(0) & c2.ne(c1)]
        """
        return self != other

    def add(self, other):
        """
        PARAMETERS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(add = c1 + c2)
        """
        return self + other

    def sub(self, other):
        """
        PARAMETERS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(sub = c1.sub(c2))
        """
        return self - other

    def mul(self, other):
        """
        PARAMETERS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(mul = c1.mul(c2))
        """
        return self * other

    def div(self, other):
        """
        PARAMETERS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(div = c1.div(c2))
        """
        return self.truediv(other)

    def truediv(self, other):
        """
        PARAMETERS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(div = c1.truediv(c2))
        """
        return self / other

    def floordiv(self, other):
        """
        PARAMETRS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df.assign(c1_floordiv_c2 = c1.floordiv(c2))
        """
        return self // other

    def mod(self, other):
        """
        PARAMETERS:
            other : ColumnExpression or literal

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c2 = df.c2
            df[c1.mod(2)]
            df[c1.mod(c2) == 0 & c2.mod(c1) == 0]
        """
        return self % other

    def isna(self):
        """
        Test for NA values

        RETURNS:
            A boolean Series of numeric values:
              - 1 if value is NA (None)
              - 0 if values is not NA

        EXAMPLES:
            df = DataFrame('')
            c1 = df.c1

            df[c1.isna() == 1]
            df[c1.isna() == 0]

            # alternatively, True and False can be used
            df[c1.isna() == True]
            df[c1.isna() == False]
        """
        res = _SQLColumnExpression(
                case_when(
                           [(self.expression != None, 0)],
                           else_ = 1
                )
            )

        return res

    def isnull(self):
        """
        Alias for isna()
        """
        return self.isna()

    def notna(self):
        """
        Test for non NA values
        The boolean complement of isna()

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1

            df[c1.notna() == 1]
            df[c1.notna() == 0]

            # alternatively, True and False can be used
            df[c1.notna() == True]
            df[c1.notna() == False]
        """

        res = _SQLColumnExpression(
                case_when(
                           [(self.expression != None, 1)],
                           else_ = 0
                )
              )

        return res

    def notnull(self):
        """
        Alias for notna()
        """
        return self.notna()

    def _unique(self):
        """
        Private method to return _SQLColumnExpression with DISTINCT applied on it.

        NOTE : This operation is valid only when the resultant _MetaExpression has
               just this one _SQLColumnExpression. All other operations will fail with
               a database error given the nature of the DISTINCT keyword.

               For example:
               >>> df = DataFrame("admissions_train") # a multi-column table
               >>> # Filter operations will fail
               >>> df = df[df.gpa._unique() > 2.00]
               >>> # Assign operations resulting in multiple columns
               >>> df.assign(x = df.gpa._unique())

               The following however is fine since it return only the one column
               with DISTINCT applied to it

               >>> df.assign(drop_columns = True, x = df.gpa._unique())

        PARAMETERS:
            None

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c1.unique()
        """
        res = _SQLColumnExpression(
                    self.expression.distinct()
              )

        return res

    def isin(self, values=None):
        """
        Function to check for the presence of values in a column.

        PARAMETERS:
            values:
                Required Argument.
                Specifies the list of values to check for their presence in the column.
                in the provided set of values.
                Types: list

        RETURNS:
            _SQLColumnExpression

        RAISES:
            TypeError - If invalid type of values are passed to argument 'values'.
            ValueError - If None is passed to argument 'values'.

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            17      no  3.83  Advanced    Advanced         1
            13      no  4.00  Advanced      Novice         1
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            34     yes  3.85  Advanced    Beginner         0
            40     yes  3.95    Novice    Beginner         0
            >>>

            # Example 1: Filter results where gpa values are in any of these following values:
            #            4.0, 3.0, 2.0, 1.0, 3.5, 2.5, 1.5
            >>> df[df.gpa.isin([4.0, 3.0, 2.0, 1.0, 3.5, 2.5, 1.5])]
               masters  gpa     stats programming  admitted
            id
            31     yes  3.5  Advanced    Beginner         1
            6      yes  3.5  Beginner    Advanced         1
            13      no  4.0  Advanced      Novice         1
            4      yes  3.5  Beginner      Novice         1
            29     yes  4.0    Novice    Beginner         0
            15     yes  4.0  Advanced    Advanced         1
            36      no  3.0  Advanced      Novice         0
            >>>

            # Example 2: Filter results where stats values are neither 'Novice' nor 'Advanced'
            >>> df[~df.stats.isin(['Novice', 'Advanced'])]
               masters   gpa     stats programming  admitted
            id
            1      yes  3.95  Beginner    Beginner         0
            2      yes  3.76  Beginner    Beginner         0
            8       no  3.60  Beginner    Advanced         1
            4      yes  3.50  Beginner      Novice         1
            6      yes  3.50  Beginner    Advanced         1
            >>>
        """
        # If 'values' is None or not specified, raise an Exception
        if values is None:
            raise ValueError(Messages.get_message(MessageCodes.MISSING_ARGS, 'values'))

        if not isinstance(values, list):
            raise TypeError(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, 'values', 'list'))

        return _SQLColumnExpression(self.expression.in_(values))


class _AggregateColumnExpresion(ColumnExpression):
    """
    A class for implementing aggregate methods for ColumnExpressions.
    This class contains several methods that can work as regular aggregates as well as
    time series aggregates.
    This class is internal.
    """

    original_expressions = []

    def __validate_operation(self, name, as_time_series_aggregate=False, describe_op=False,
                                   **kwargs):
        """
        DESCRIPTION:
            Internal function used by aggregates to validate whether column supports
            the aggregate operation or not.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the name of the aggregate function/operation.
                Types: str

            as_time_series_aggregate:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation is time
                series aggregate or regular aggregate.
                Default Values: False (Regular Aggregate)
                Types: bool

            describe_op:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation being
                run is for describe operation or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
            None.

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            self.__validate_operation(func_obj.name, describe_op=describe_op, **kwargs)
        """
        if not describe_op:
            unsupported_types = _Dtypes._get_unsupported_data_types_for_aggregate_operations(name,
                                                                                             as_time_series_aggregate)
        else:
            unsupported_types = _Dtypes._get_unsupported_data_types_for_describe_operations(name)
        if type(self.type) in unsupported_types:
            raise RuntimeError(
                "Unsupported operation '{}' on column '{}' of type '{}'".format(name, self.name, str(self.type)))

    def __generate_function_call_object(self, func_obj, distinct=False, skipna=False, describe_op=False, **kwargs):
        """
        DESCRIPTION:
            Internal function used by aggregates to generate actual function call using
            sqlalchemy FunctionGenerator.

        PARAMETERS:
            func_obj:
                Required Argument.
                Specifies the sqlalchemy FunctionGenerator object to be used generate
                actual function call.
                Types: sqlalchemy FunctionGenerator

            distinct:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation should consider
                duplicate rows or not.
                Default Values: False
                Types: bool

            skipna:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation should skip
                null values or not.
                Default Values: False
                Types: bool

            describe_op:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation being
                run is for describe operation or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
            _SQLColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            self.__generate_function_call_object(func.count, distinct=distinct, skipna=skipna, **kwargs)
        """
        expr = self
        if skipna:
            expr = self.notna()

        # Create a Function Generator object for a function call.
        if distinct:
            func_obj = func_obj(expr.expression.distinct())
        else:
            func_obj = func_obj(expr.expression)

        return self.__process_function_call_object(func_obj, describe_op, **kwargs)

    def __process_function_call_object(self, func_obj, describe_op=False, **kwargs):
        """
        DESCRIPTION:
            Internal function used by aggregates to process actual function call generated
            using sqlalchemy FunctionGenerator.
            This functions:
                1. Validates whether aggregate operation for the column is supported or not.
                2. Creates a new _SQLColumnExpression.
                3. Identifies the output column type for the aggregate function.

        PARAMETERS:
            func_obj:
                Required Argument.
                Specifies the sqlalchemy FunctionGenerator object to be used generate
                actual function call.
                Types: sqlalchemy FunctionGenerator

            describe_op:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation being
                run is for describe operation or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
            _SQLColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            self.__process_function_call_object(func_obj, describe_op, **kwargs)
        """
        # Perform validations for the function to check if operation is valid or not.
        self.__validate_operation(func_obj.name, describe_op=describe_op, **kwargs)

        # Add self to original expression lists.
        self.original_expressions.append(self)

        # Set _SQLColumnExpression type
        new_expression_type = _get_function_expression_type(func_obj, self.expression, **kwargs)
        columnExpression = _SQLColumnExpression(func_obj)
        columnExpression.type = new_expression_type
        if describe_op:
            columnExpression = columnExpression.cast(NUMBER())
        return columnExpression

    def count(self, distinct=False, skipna=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the number of values in a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            skipna:
                Optional Argument.
                Specifies a flag that decides whether to skip null values or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.count, distinct=distinct, skipna=skipna, **kwargs)

    def kurtosis(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function returns kurtosis value for a column.
            Kurtosis is the fourth moment of the distribution of the standardized
            (z) values. It is a measure of the outlier (rare, extreme observation)
            character of the distribution as compared with the normal, Gaussian
            distribution.
                * The normal distribution has a kurtosis of 0.
                * Positive kurtosis indicates that the distribution is more
                  outlier-prone than the normal distribution.
                * Negative kurtosis indicates that the distribution is less
                  outlier-prone than the normal distribution.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.kurtosis, distinct=distinct, **kwargs)

    def first(self, **kwargs):
        """
        DESCRIPTION:
            Function returns oldest value, determined by the timecode, for each group
            in a column.
            Note:
                This can only be used as Time Series Aggregate function.

        PARAMETERS:
            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.first)

    def last(self, **kwargs):
        """
        DESCRIPTION:
            Function returns newest value, determined by the timecode, for each group
            in a column.
            Note:
                This can only be used as Time Series Aggregate function.

        PARAMETERS:
            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.last)

    def mad(self, constant_multiplier=None, **kwargs):
        """
        DESCRIPTION:
            Function returns the median of the set of values defined as the
            absolute value of the difference between each value and the median
            of all values in each group.

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
                3. This can only be used as Time Series Aggregate function.

        PARAMETERS:
            constant_multiplier:
                Optional Argument.
                Specifies a numeric values to be used as constant multiplier
                (b in the above formula). It should be any numeric value
                greater than or equal to 0.
                Note:
                    When this argument is not used, Vantage uses 1.4826 as
                    constant multiplier.
                Default Values: None
                Types: int or float

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        if constant_multiplier:
            func_obj = func.mad(constant_multiplier, self.expression)
        else:
            func_obj = func.mad(self.expression)
        return self.__process_function_call_object(func_obj)

    def max(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the maximum value for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.max, distinct=distinct, **kwargs)

    def mean(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the average value for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        # TODO:: Validate if below lines of code is needed or not.
        if self.type in [INTEGER, DECIMAL]:
            return _SQLColumnExpression(self).cast(FLOAT).mean()

        return self.__generate_function_call_object(func.avg, distinct=distinct, **kwargs)

    def median(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the median value for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.median, distinct=distinct, **kwargs)

    def min(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the minimum value for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.min, distinct=distinct, **kwargs)

    def mode(self, **kwargs):
        """
        DESCRIPTION:
            Function to get the mode value for a column.
            Note:
                This can only be used as Time Series Aggregate function.

        PARAMETERS:
            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.mode)

    def percentile(self, percentile, distinct=False, interpolation="LINEAR",
                   as_time_series_aggregate=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the percentile values for a column.

        PARAMETERS:
            percentile:
                Required Argument.
                Specifies the desired percentile value to calculate.
                It should be between 0 and 1, both inclusive.
                Types: float

            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
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

            as_time_series_aggregate:
                Optional Argument.
                Specifies a flag that decides whether percentiles are being calculated
                as regular aggregate or time series aggregate. When it is set to False, it'll
                be executed as regular aggregate, if set to True; then it is used as time series
                aggregate.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["percentile", percentile, False, (int, float)])
        awu_matrix.append(["distinct", distinct, True, (bool)])
        awu_matrix.append(["interpolation", interpolation, True, (str), True,
                           ["LINEAR", "LOW", "HIGH", "NEAREST", "MIDPOINT"]])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if percentile < 0 or percentile > 1:
            raise ValueError(Messages.get_message(MessageCodes.TDMLDF_LBOUND_UBOUND).format("percentile",
                                                                                            "or equal to 0", "1"))
        if not as_time_series_aggregate:
            # Regular Aggregate
            # SQL Equivalent: """percentile_cont({}) within group order by {}"""
            func_percentile = func.percentile_cont(percentile)

            # Check if it is describe operation or not.
            describe_op=False
            if "describe_op" in kwargs.keys():
                describe_op = kwargs["describe_op"]

            # Validate the operation.
            self.__validate_operation(func_percentile.name, **kwargs)

            # Add within group clause to the percentile operation.
            if describe_op:
                # Cast order by column to Number.
                cast_expression = self.cast(NUMBER())
                column_expression = _SQLColumnExpression(func_percentile.within_group(cast_expression.expression))
                column_expression = column_expression.cast(NUMBER())
            else:
                column_expression = _SQLColumnExpression(func_percentile.within_group(self.expression))
                column_expression.type = _get_function_expression_type(func_percentile, self.expression, **kwargs)
            return column_expression
        else:
            # Time Series Aggregate
            # SQL Equivalent: """percentile([DISTINCT] column, percentile [interpolation])"""
            if distinct:
                func_percentile = func.percentile(self.expression.distinct(), percentile * 100, text(interpolation))
            else:
                func_percentile = func.percentile(self.expression, percentile * 100, text(interpolation))
            return self.__process_function_call_object(func_percentile)

    def rank(self, distinct=False, **kwargs):
        """TODO - PLACEHOLDER"""
        raise NotImplementedError("Yet to be implemented")
        # return self.__generate_function_call_object(func.rank, distinct=distinct, **kwargs)

    def skew(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the skewness of the distribution for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.skew, distinct=distinct, **kwargs)

    def sum(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the sum of values in a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        return self.__generate_function_call_object(func.sum, distinct=distinct, **kwargs)

    def std(self, distinct=False, population=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the sample or population standard deviation for values in a column.
            The standard deviation is the second moment of a distribution.
                * For a sample, it is a measure of dispersion from the mean of that sample.
                * For a population, it is a measure of dispersion from the mean of that population.
            The computation is more conservative for the population standard deviation
            to minimize the effect of outliers on the computed value.
            Note:
                1. When there are fewer than two non-null data points in the sample used
                   for the computation, then std returns None.
                2. Null values are not included in the result computation.
                3. If data represents only a sample of the entire population for the
                   column, Teradata recommends to calculate sample standard deviation,
                   otherwise calculate population standard deviation.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            population:
                Optional Argument.
                Specifies whether to calculate standard deviation on entire population or not.
                Set this argument to True only when the data points represent the complete
                population. If your data represents only a sample of the entire population for the
                column, then set this variable to False, which will compute the sample standard
                deviation. As the sample size increases, even though the values for sample
                standard deviation and population standard deviation approach the same number,
                you should always use the more conservative sample standard deviation calculation,
                unless you are absolutely certain that your data constitutes the entire population
                for the column.
                Default Value: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        if population:
            return self.__generate_function_call_object(func.stddev_pop, distinct=distinct, **kwargs)
        else:
            return self.__generate_function_call_object(func.stddev_samp, distinct=distinct, **kwargs)

    def unique(self, **kwargs):
        """
        DESCRIPTION:
            Function to get the number of unique values in a column.

        PARAMETERS:
            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        # Check if it is describe operation or not.
        describe_op = False
        if "describe_op" in kwargs.keys():
            describe_op = kwargs["describe_op"]

        if describe_op:
            # If a describe operation function name is used as "unique" to retrieve unsupported types.
            self.__validate_operation(name="unique", describe_op=describe_op)
        return self.count(True)

    def var(self, distinct=False, population=False, **kwargs):
        """
        DESCRIPTION:
            Returns sample or population variance for values in a column.
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
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
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

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            TODO
        """
        if population:
            return self.__generate_function_call_object(func.var_pop, distinct=distinct, **kwargs)
        else:
            return self.__generate_function_call_object(func.var_samp, distinct=distinct, **kwargs)

class _SQLColumnExpression(_LogicalColumnExpression,
                           _ArithmeticColumnExpression,
                           _SeriesColumnExpression,
                           _AggregateColumnExpresion):
    """
    _SQLColumnExpression is used to build Series/Column manipulations into SQL.
    It represents a column from a Table or an expression involving some operation
    between columns and other literals.

    These objects are created from _SQLTableExpression or from operations
    involving other _SQLColumnExpressions.

    They behave like sqlalchemy.Column objects when accessed from the SQLTableExpression.
    Thus you can access certain common attributes (decorated with property) specified by
    the ColumnExpression interface. Otherwise, the attributes refer to expressions.
    In this case, None is returned if an attribute is not found in the expression.

    This class is internal.
    """

    def __init__(self, expression, **kw):
        """
        Initialize the ColumnExpression

        PARAMETERS:
            expression : Required Argument.
                         A sqlalchemy.ClauseElement instance.

        """
        self.expression = expression
        self.type = expression.type
        # Initial ColumnExpression has only one dataframe and hence
        # __has_multiple_dataframes = False.
        # eg: df1.col1, df2.col2
        self.__has_multiple_dataframes = False

    @property
    def expression(self):
        """
        A reference to the underlying column expression.
        """
        return self.__expression

    @expression.setter
    def expression(self, expression):
        """
        Sets a reference to the underlying column expression.
        """
        if (not isinstance(expression, ClauseElement)):
            raise ValueError('_SQLColumnExpression requires a sqlalchemy.ClauseElement expression')
        self.__expression = expression

    def get_flag_has_multiple_dataframes(self):
        """
        Returns whether the underlying column expression uses multiple dataframes or not.
        If column expression has only one dataframe, this function returns False; otherwise True.
        """
        return self.__has_multiple_dataframes

    def set_flag_has_multiple_dataframes(self, has_multiple_dataframes):
        """
        Sets __has_multiple_dataframes True or False based on the argument has_multiple_dataframes.
        """
        if (not isinstance(has_multiple_dataframes, bool)):
            raise ValueError('_SQLColumnExpression requires a boolean type argument '
                         'has_multiple_dataframes')
        self.__has_multiple_dataframes = has_multiple_dataframes

    @property
    def original_column_expr(self):
        """
        Returns a list of original ColumnExpression.
        """
        return self.original_expressions

    @original_column_expr.setter
    def original_column_expr(self, expression):
        """
        Sets the original_column_expr property to a list of ColumnExpressions.
        """
        if not isinstance(expression, list):
            raise ValueError('_SQLColumnExpression requires a list type argument '
                         'expression')
        self.original_expressions = expression

    @property
    def type(self):
        """
        Returns the underlying sqlalchemy type of the current expression.
        """
        if self._type is not None:
            return self._type
        else:
            return self.expression.type

    @type.setter
    def type(self, value):
        """
        Setter for type property of _SQLColumnExpression.
        Allows to set the column expression type.
        """
        if value is None:
            self._type = self.expression.type
        else:
            self._type = value

        if not isinstance(self._type, _TDType):
            # If value is either SQLAlchemy NullType or any of SQLAlchemy type, then retrieve the
            # type for function expression from SQLAlchemy expression and input arguments.
            # sqlalc.sql.type_api.TypeEngine is grand parent class to all SQLAlchemy data types.
            # Hence checking if self._type is instance of that class.
            if isinstance(self._type, sqlalc.sql.sqltypes.NullType) or \
                    isinstance(self._type, sqlalc.sql.type_api.TypeEngine):
                if isinstance(self.expression, sqlalc.sql.elements.Over) \
                        or isinstance(self.expression, sqlalc.sql.functions.Function):
                    from teradataml.dataframe.vantage_function_types import \
                        _retrieve_function_expression_type
                    self._type = _retrieve_function_expression_type(self.expression)

    @property
    def name(self):
        """
        Returns the underlying name attribute of self.expression or None
        if the expression has no name. Note that the name may also refer to
        an alias or label() in sqlalchemy
        """
        return getattr(self.expression, 'name', None)

    @property
    def table(self):
        """
        Returns the underlying table attribute of the sqlalchemy.Column
        """
        return getattr(self.expression, 'table', None)

    def compile(self, *args, **kw):
        """
        Calls the compile method of the underlying sqlalchemy.Column
        """
        if len(kw) == 0:
            kw = dict({'dialect': td_dialect(),
                'compile_kwargs':
                    {
                        'include_table': False,
                        'literal_binds': True
                    }
                })

        return str(self.expression.compile(*args, **kw))

    def compile_label(self, label):
        """
        DESCRIPTION:
            Compiles expression with label, by calling underlying sqlalchemy methods.
        PARAMETES:
            label:
                Required Argument.
                Specifies the label to be used to alias the compiled expression.
                Types: str
        RAISES:
            None.
        RETURNS:
            string - compiled expression.
        EXAMPLES:
            self.compile_label("col1")
        """
        compiler = td_compiler(td_dialect(), None)
        aliased_expression = compiler.visit_label(self.expression.label(label),
                                                  within_columns_clause=True,
                                                  include_table=False,
                                                  literal_binds=True)
        return aliased_expression

    def cast(self, type_ = None):
        """
        DESCRIPTION:
            Apply the CAST SQL function to the column with the type specified.

            NOTE: This method can currently be used only with 'filter' and
                  'assign' methods of teradataml DataFrame.

        PARAMETERS:
            type_:
                Required Argument.
                Specifies a teradatasqlalchemy type or an object of a teradatasqlalchemy type
                that the column needs to be cast to.
                Default value: None
                Types: teradatasqlalchemy type or object of teradatasqlalchemy type

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            19     yes  1.98  Advanced    Advanced         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            38     yes  2.65  Advanced    Beginner         1
            >>> df.dtypes
            id               int
            masters          str
            gpa            float
            stats            str
            programming      str
            admitted         int

            >>> # Let's try creating a new DataFrame casting 'id' column (of type INTEGER) to VARCHAR(5),
            >>> # an object of a teradatasqlalchemy type.
            >>> from teradatasqlalchemy import VARCHAR
            >>> new_df = df.assign(char_id = df.id.cast(type_=VARCHAR(5)))
            >>> new_df
               masters   gpa     stats programming  admitted char_id
            id
            5       no  3.44    Novice      Novice         0       5
            34     yes  3.85  Advanced    Beginner         0      34
            13      no  4.00  Advanced      Novice         1      13
            40     yes  3.95    Novice    Beginner         0      40
            22     yes  3.46    Novice    Beginner         0      22
            19     yes  1.98  Advanced    Advanced         0      19
            36      no  3.00  Advanced      Novice         0      36
            15     yes  4.00  Advanced    Advanced         1      15
            7      yes  2.33    Novice      Novice         1       7
            17      no  3.83  Advanced    Advanced         1      17
            >>> new_df.dtypes
            id               int
            masters          str
            gpa            float
            stats            str
            programming      str
            admitted         int
            char_id          str

            >>> # Now let's try creating a new DataFrame casting 'id' column (of type INTEGER) to VARCHAR,
            >>> # a teradatasqlalchemy type.
            >>> new_df_2 = df.assign(char_id = df.id.cast(type_=VARCHAR))
            >>> new_df_2
               masters   gpa     stats programming  admitted char_id
            id
            5       no  3.44    Novice      Novice         0       5
            34     yes  3.85  Advanced    Beginner         0      34
            13      no  4.00  Advanced      Novice         1      13
            40     yes  3.95    Novice    Beginner         0      40
            22     yes  3.46    Novice    Beginner         0      22
            19     yes  1.98  Advanced    Advanced         0      19
            36      no  3.00  Advanced      Novice         0      36
            15     yes  4.00  Advanced    Advanced         1      15
            7      yes  2.33    Novice      Novice         1       7
            17      no  3.83  Advanced    Advanced         1      17
            >>> new_df_2.dtypes
            id               int
            masters          str
            gpa            float
            stats            str
            programming      str
            admitted         int
            char_id          str

            >>> # Let's try filtering some data with a match on a column cast to another type,
            >>> # an object of a teradatasqlalchemy type.
            >>> df[df.id.cast(VARCHAR(5)) == '1']
               masters   gpa     stats programming  admitted
            id
            1      yes  3.95  Beginner    Beginner         0

            >>> # Now let's try the same, this time using a teradatasqlalchemy type.
            >>> df[df.id.cast(VARCHAR) == '1']
               masters   gpa     stats programming  admitted
            id
            1      yes  3.95  Beginner    Beginner         0

        RETURNS:
            _SQLColumnExpression

        RAISES:
            TeradataMlException
        """
        valid_types = [BIGINT, BLOB, BYTE, BYTEINT, CHAR, CLOB, DATE, DECIMAL, FLOAT, INTEGER, INTERVAL_DAY,
                       INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE, INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR,
                       INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND, INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND,
                       INTERVAL_MONTH, INTERVAL_SECOND, INTERVAL_YEAR, INTERVAL_YEAR_TO_MONTH, NUMBER, PERIOD_DATE,
                       PERIOD_TIME, PERIOD_TIMESTAMP, SMALLINT, TIME, TIMESTAMP, VARBYTE, VARCHAR]

        # If type_ is None or not specified, raise an Exception
        if type_ is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS, 'type_'),
                                      MessageCodes.MISSING_ARGS)

        # Check that the type_ is a valid teradatasqlalchemy type
        if type_ not in valid_types and type(type_) not in valid_types:
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, 'type_',
                                                           'a valid teradatasqlalchemy type'),
                                      MessageCodes.UNSUPPORTED_DATATYPE)

        expression = func.cast(self.expression, type_=type_).label(self.name)
        return _SQLColumnExpression(expression)

    def __hash__(self):
        return hash(self.expression)

    def __dir__(self):
        # currently str is the only accessor
        # if we end up adding more, consider making this 
        # list an instance attribute (i.e self._accessors) of the class
        accessors = ['str']
        attrs = {x for x in dir(type(self)) if not x.startswith('_') and x not in accessors}

        if isinstance(self.type, (CLOB, CHAR, VARCHAR)):
            return attrs | set(['str']) # str accessor is only visible for string-like columns

        return attrs
