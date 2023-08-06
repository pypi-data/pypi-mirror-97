import re
import sqlalchemy as sqlalc
from teradatasqlalchemy import (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy import (TIMESTAMP, DATE, TIME)
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)
from teradatasqlalchemy import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy import (INTERVAL_YEAR, INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH, INTERVAL_DAY,
                                INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE, INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR,
                                INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND, INTERVAL_MINUTE,
                                INTERVAL_MINUTE_TO_SECOND, INTERVAL_SECOND)
        
def __get_function_argument_type(func_name, func_str, column_position, expression):
    """
    Internal function to get specific argument type from a function call string.

    PARAMTERS:
        func_name:
            Required Argument.
            Specifies the name of the function.
            Types: str

        func_str:
            Required Argument.
            Specifies the SQLAlchemy function string.
            Types: str

        column_position:
            Required Argument.
            Specifies the function argument position who's type needs to be returned.
            Types: int

    RETURNS:
        teradatasqlalchemy Type

    RAISES:
        None

    EXAMPLES:
        __get_function_argument_type(func_name, func_str, column_position)
    """
    pattern = re.compile(func_name, re.IGNORECASE)
    fqcn = pattern.sub("", func_str, 1).replace("(", "").replace(")", "").split(",")[column_position - 1].strip()
    if ":{}_".format(func_name) in fqcn.upper():
        # We are here that means, the argument passed is likely a literal.
        # Check whether the passed argument is int or float, then return the type accordingly.
        from teradatasqlalchemy.dialect import dialect as td_dialect
        kw = dict({'dialect': td_dialect(),
                   'compile_kwargs':
                       {
                           'include_table': False,
                           'literal_binds': True
                       }
                   })
        func_str = str(expression.compile(**kw))
        fqcn = pattern.sub("", func_str, 1).replace("(", "").replace(")", "").split(",")[column_position - 1]
        try:
            int(fqcn.replace("'", ""))
            # For an integer passed by user we will assume return type as BIGINT
            return BIGINT()
        except:
            try:
                float(fqcn.replace("'", ""))
                return FLOAT()
            except:
                # If not int or float return type will be assumed as VARCHAR()
                return VARCHAR()
    else:
        # We are here that means column was passed to the argument.
        # We will extract the column name and retrieve its type.

        # Before we retrieve the column name, argument passed may contain a DISTINCT, ASC, DESC
        # keywords, we must remove those first. These keywords will appear at the start or at the end.
        # Hence we will strip such keywords first.
        fqcn = fqcn.strip("DISTINCT").strip("ASC").strip("DESC").strip()

        # Proceed with column name and type extraction.
        arr = fqcn.split(".")
        schema = None
        if len(arr) > 1 and len(arr) < 4:
            # Let's look for the table expression is used or constant.
            # If two dots or one dot is used, then we will assume a table name.
            if len(arr) == 3:
                # We got three values that means we are considering db.tbl.col format
                schema = arr[0].strip("\"")
                tbl = arr[1].strip("\"")
                col = arr[2].strip("\"")
            elif len(arr) == 2:
                # We got three values that means we are considering tbl.col format
                tbl = arr[0].strip("\"")
                col = arr[1].strip("\"")
            try:
                from sqlalchemy import MetaData, Table
                from teradataml.context.context import get_context
                table = Table(tbl, MetaData(get_context()), schema=schema, autoload=True, autoload_with=get_context())
                return table.c.__getattr__(col).type
            except:
                # We are here, that means we were not able to retrieve the column type
                # Let's return NullType
                return sqlalc.sql.sqltypes.NullType
        else:
            # Unable to get the correct type of the argument passed, let's just return NullType.
            return sqlalc.sql.sqltypes.NullType


# Lambda function to get type of teradatasqlalchemy type instances.
__map_types = lambda x: map(type, x) if isinstance(x, list) else type(x)
# Lambda function to check type of a teradatasqlalchemy type instance is same as that of other type(s) or not.
__check_type = lambda x, y: type(x) in __map_types(y) if isinstance(y, list) else type(x) == __map_types(y)

# Function specific to determine the type of 'power' function.
def __get_power_type(function_name, func_str, expression):
    """
    'power' function needs special handling as output type depends on both the inputs of the function.
    """
    # If either of the input arguments is a FLOAT type, the result data type is FLOAT.
    # Otherwise, the result data type is NUMBER.
    inp1_col_type = __get_function_argument_type(function_name, func_str, 1, expression)
    inp2_col_type = __get_function_argument_type(function_name, func_str, 2, expression)
    if __check_type(FLOAT(), [inp1_col_type, inp2_col_type]):
        return FLOAT()
    else:
        return NUMBER()

# Function specific to determine the type of 'mod' function.
def __get_mod_type(function_name, func_str, expression):
    """
    'mod' function needs special handling as output type depends on both the inputs of the function.
    """
    # If either of the input arguments is a FLOAT/NUMBER/DECIMAL type, the result data type is FLOAT.
    # If both of the inputs are of INT type, then result is INTEGER, else FLOAT.
    inp1_col_type = __get_function_argument_type(function_name, func_str, 1, expression)
    inp2_col_type = __get_function_argument_type(function_name, func_str, 2, expression)
    if __check_type(FLOAT(), [inp1_col_type, inp2_col_type]) or \
            __check_type(DECIMAL(), [inp1_col_type, inp2_col_type]) or \
            __check_type(NUMBER(), [inp1_col_type, inp2_col_type]):
        return FLOAT()
    else:
        return INTEGER()
    
    
# Function specific to determine the type of 'subbitstr' function.
def __get_subbitstr_type(x):
    """
    'subbitstr' function needs special handling to determine the output type.
    """
    type_mapper = {
        type(BYTEINT()): VARBYTE(1),
        type(SMALLINT()): VARBYTE(2),
        type(INTEGER()): VARBYTE(4),
        type(BIGINT()): VARBYTE(8),
        type(VARBYTE()): x
    }
    return type_mapper.get(type(x))


# Function specific to determine the type of 'to_byte' function.
def __get_to_byte_type(x):
    """
    'to_byte' function needs special handling to determine the output type.
    """
    type_mapper = {
        type(BYTEINT()): BYTE(1),
        type(SMALLINT()): BYTE(2),
        type(INTEGER()): BYTE(4),
        type(BIGINT()): BYTE(8)
    }
    return type_mapper.get(type(x))

# Mapper for functions returning fixed type.
VANTAGE_FUNCTION_TYPE_MAPPER = {
    # Aggregate Functions
    # Function documentation says output type is FLOAT, but in some cases we have seen
    # function working on Date type column as well. There is a JIRA ELE-2626 open to track
    # this. This commented lines codes are kept until ELE-2626 is resolved.
    # 'AVG': FLOAT(),
    # 'AVERAGE': FLOAT(),
    'COUNT': INTEGER(),
    'GROUPING': INTEGER(),
    'REGR_COUNT': INTEGER(),
    # 'KURTOSIS': FLOAT(),
    # 'MAX': Arg dependent
    # 'MAXIMUM': Arg dependent
    # 'MIN': Arg dependent
    # 'MINIMUM': Arg dependent
    # Function documentation says output type is FLOAT, but in some cases we have seen
    # function working on Date type column as well. There is a JIRA ELE-2626 open to track
    # this. This commented lines codes are kept until ELE-2626 is resolved.
    # 'SKEW': FLOAT(),
    # 'SUM': Arg dependent
    # 'STDDEV_POP': FLOAT(),
    # 'STDDEV_SAMP': FLOAT(),
    # 'VAR_POP': FLOAT(),
    # 'VAR_SAMP': FLOAT(),

    # Arithmetic Functions
    # -- 'ABS': Arg dependent
    'DEGREES': FLOAT(),
    'EXP': FLOAT(),
    'CASE_N': INTEGER(),
    'LN': FLOAT(),
    'LOG': FLOAT(),
    # -- 'MOD': Arg dependent,
    # -- 'POWER': Arg dependent
    'RADIANS': FLOAT(),
    'RANDOM': INTEGER(),
    'SIGN': NUMBER(),
    'SQRT': FLOAT(),
    'WIDTH_BUCKET': INTEGER(),

    # Trigonometric Functions
    'COS': FLOAT(),
    'ACOS': FLOAT(),
    'SIN': FLOAT(),
    'ASIN': FLOAT(),
    'TAN': FLOAT(),
    'ATAN': FLOAT(),
    'ATAN2': FLOAT(),

    # Hyperbolic Functions
    'COSH': FLOAT(),
    'ACOSH': FLOAT(),
    'SINH': FLOAT(),
    'ASINH': FLOAT(),
    'TANH': FLOAT(),
    'ATANH': FLOAT(),

    # Attribute Functions
    'FORMAT': CHAR(),
    'TITLE': CHAR(),
    'TYPE': CHAR(),

    # Bit/Byte Manipulation Functions
    'COUNTSET': INTEGER(),
    'GETBIT': BYTEINT(),

    # Built-in Functions
    'CURRENT_DATE': DATE(),
    'CURDATE': DATE(),
    'CURRENT_TIME': TIME(),
    'CURTIME': TIME(),
    'CURRENT_TIMESTAMP': TIMESTAMP(),

    # Hash Related Functions
    'HASHAMP': INTEGER(),
    'HASHBAKAMP': INTEGER(),
    'HASHBUCKET': INTEGER(),
    'HASHROW': BYTE(4),

    # Ordered Analytical/Window Aggregate Functions
    'CUME_DIST': FLOAT(),
    'DENSE_RANK': INTEGER(),
    'PERCENT_RANK': FLOAT(),
    'PERCENTILE_CONT': FLOAT(),
    'PERCENTILE_DISC': FLOAT(),
    'QUANTILE': INTEGER(),
    'RANK': INTEGER(),
    'ROW_NUMBER': INTEGER(),

    # Regular Expression Functions
    'REGEXP_SIMILAR': INTEGER(),

    # String Functions
    'ASCII': NUMBER(),
    'CHAR2HEXINT': CHAR(),
    'CHR': CHAR(1),
    'INDEX': INTEGER(),
    'INSTR': NUMBER(),
    'LENGTH': NUMBER(),
    'LOCATE': INTEGER(),
    'NVP': VARCHAR(),
    'POSITION': INTEGER(),
    'SOUNDEX': VARCHAR(),
    'STRING_CS': INTEGER(),
}

# Few datattype lists useful for our lambda functions to get the output types.
__bitbyte_input_types = [BYTEINT(), SMALLINT(), INTEGER(), BIGINT(), VARBYTE()]
__numeric_types = [BYTEINT(), SMALLINT(), INTEGER(), BIGINT(), DECIMAL(), FLOAT(), NUMBER()]
__categorical_types = [CHAR(), VARCHAR(), CLOB()]
__float_types = [DECIMAL(), FLOAT(), NUMBER()]
__interval_types = [INTERVAL_YEAR(), INTERVAL_YEAR_TO_MONTH(), INTERVAL_MONTH(), INTERVAL_DAY(),
                    INTERVAL_DAY_TO_HOUR(), INTERVAL_DAY_TO_MINUTE(), INTERVAL_DAY_TO_SECOND(), INTERVAL_HOUR(),
                    INTERVAL_HOUR_TO_MINUTE(), INTERVAL_HOUR_TO_SECOND(), INTERVAL_MINUTE(),
                    INTERVAL_MINUTE_TO_SECOND(), INTERVAL_SECOND()]

# Few lamda functions for type validations.
__if_numeric_type = lambda x: __check_type(x, __numeric_types)
__if_categorical_type = lambda x: __check_type(x, __categorical_types)
__if_bitbyte_type = lambda x: __check_type(x, __bitbyte_input_types)
__if_char_type = lambda x: __check_type(x, [CHAR(), VARCHAR()])
__if_byte_type = lambda x: __check_type(x, [BYTE(), VARBYTE()])
__if_float_type = lambda x: __check_type(x, __float_types)
__if_interval_type = lambda x: __check_type(x, __interval_types)

# Mapper for functions returning type based on their argument type.
VANTAGE_FUNCTION_ARGTYPE_DEPENDENT_MAPPER = {
    # Aggregate Functions
    'AVE': lambda x: FLOAT() if __if_numeric_type(x) else x,
    'AVERAGE': lambda x: FLOAT() if __if_numeric_type(x) else x,
    'AVG': lambda x: FLOAT() if __if_numeric_type(x) else x,
    'CORR': lambda x: x if __if_interval_type(x) else FLOAT(),
    'COVAR_POP': lambda x: x if __if_interval_type(x) else (DATE() if __check_type(x, DATE()) else FLOAT()),
    'COVAR_SAMP': lambda x: x if __if_interval_type(x) else (DATE() if __check_type(x, DATE()) else FLOAT()),
    'KURTOSIS': lambda x: FLOAT() if __if_numeric_type(x) else x,
    'MAX': lambda x: x,
    'MAXIMUM': lambda x: x,
    'MIN': lambda x: x,
    'MINIMUM': lambda x: x,
    'REGR_AVGX': lambda x: x if __if_interval_type(x) else (DATE() if __check_type(x, DATE()) else FLOAT()),
    'REGR_AVGY': lambda x: x if __if_interval_type(x) else (DATE() if __check_type(x, DATE()) else FLOAT()),
    'REGR_INTERCEPT': lambda x: x if __if_interval_type(x) else FLOAT(),
    'REGR_R2': lambda x: x if __if_interval_type(x) else FLOAT(),
    'REGR_SLOPE': lambda x: x if __if_interval_type(x) else FLOAT(),
    'REGR_SXX': lambda x: x if __if_interval_type(x) else FLOAT(),
    'REGR_SXY': lambda x: x if __if_interval_type(x) else FLOAT(),
    'REGR_SYY': lambda x: x if __if_interval_type(x) else FLOAT(),
    'SKEW': lambda x: FLOAT() if __if_numeric_type(x) else x,
    'STDDEV_SAMP': lambda x: FLOAT() if __if_numeric_type(x) else x,
    'STDDEV_POP': lambda x: FLOAT() if __if_numeric_type(x) else x,
    'SUM': lambda x: INTEGER() if __check_type(x, [BYTEINT(), SMALLINT()]) else (FLOAT() if __if_categorical_type(x) else x),
    'VAR_POP': lambda x: FLOAT() if __if_numeric_type(x) else x,
    'VAR_SAMP': lambda x: FLOAT() if __if_numeric_type(x) else x,

    # Arithmetic Functions
    'ABS': lambda x: x if __if_numeric_type(x) else (FLOAT() if __if_categorical_type(x) else x),
    'CEIL': lambda x: x,
    'CEILING': lambda x: x,
    'FLOOR': lambda x: x,
    'MOD': __get_mod_type,
    'NULLIFZERO': lambda x: x if __if_numeric_type(x) else (FLOAT() if __if_categorical_type(x) else x),
    'POWER': __get_power_type,
    'ROUND': lambda x: x,
    'TRUNC': lambda x: x,
    'ZEROIFNULL': lambda x: x if __if_numeric_type(x) else (FLOAT() if __if_categorical_type(x) else None),

    # BitByte Functions
    'BITAND': lambda x: x if __if_bitbyte_type(x) else (NUMBER(38, 0) if __check_type(x, [DECIMAL(), NUMBER()]) else None),
    'BITNOT': lambda x: x if __if_bitbyte_type(x) else None,
    'BITOR': lambda x: x if __if_bitbyte_type(x) else None,
    'BITXOR': lambda x: x if __if_bitbyte_type(x) else None,
    'ROTATELEFT': lambda x: x if __if_bitbyte_type(x) else None,
    'ROTATERIGHT': lambda x: x if __if_bitbyte_type(x) else None,
    'SETBIT': lambda x: x if __if_bitbyte_type(x) else None,
    'SHIFTLEFT': lambda x: x if __if_bitbyte_type(x) else None,
    'SHIFTRIGHT': lambda x: x if __if_bitbyte_type(x) else None,
    'SUBBITSTR': __get_subbitstr_type,
    'TO_BYTE':  __get_to_byte_type,

    # Ordered Analytical/Window Aggregate Functions
    'CSUM': lambda x: x,
    'FIRST_VALUE': lambda x: x,
    'LAST_VALUE': lambda x: x,
    'LAG': lambda x: x,
    'LEAD': lambda x: x,
    'MAVG': lambda x: x,
    'MDIFF': lambda x: INTEGER() if __check_type(x, DATE()) else x,
    'MEDIAN': lambda x: x,
    'MLINREG': lambda x: x,
    'MSUM': lambda x: x,

    # Regular Expression
    'REGEXP_INSTR': lambda x: INTEGER() if __if_categorical_type(x) else None,
    'REGEXP_REPLACE': lambda x: VARCHAR() if __if_char_type(x) else (CLOB() if __check_type(x, CLOB()) else None),
    'REGEXP_SUBSTR': lambda x: VARCHAR() if __if_char_type(x) else (CLOB() if __check_type(x, CLOB()) else None),

    # String Functions
    'CONCAT': lambda x: CLOB() if __check_type(x, CLOB()) else VARCHAR(),
    'EDITDISTANCE': lambda x: BIGINT() if __check_type(x, CLOB()) else INTEGER(),
    'INITCAP': lambda x: x,
    'LEFT': lambda x: VARCHAR() if __check_type(x, CHAR()) else x,
    'LOWER': lambda x: x,
    'LPAD': lambda x: VARCHAR() if __if_char_type(x) else x,
    'LTRIM': lambda x: VARCHAR() if __if_char_type(x) else x,
    'NGRAM': lambda x: INTEGER() if __if_char_type(x) else (BIGINT() if __check_type(x, CLOB()) else None),
    'OREPLACE': lambda x: VARCHAR() if __if_char_type(x) else (CLOB() if __check_type(x, CLOB()) else None),
    'OTRANSLATE': lambda x: VARCHAR() if __if_char_type(x) else (CLOB() if __check_type(x, CLOB()) else None),
    'REVERSE': lambda x: VARCHAR() if __if_char_type(x) else x,
    'RIGHT': lambda x: VARCHAR() if __check_type(x, CHAR()) else x,
    'RPAD': lambda x: VARCHAR() if __if_char_type(x) else x,
    'RTRIM': lambda x: VARCHAR() if __if_char_type(x) else x,
    'SUBSTRING': lambda x: BLOB() if __check_type(x, BLOB()) else (VARBYTE() if __if_byte_type else (CLOB() if __check_type(x, CLOB()) else VARCHAR())),
    'SUBSTR': lambda x: BLOB() if __check_type(x, BLOB()) else (VARBYTE() if __if_byte_type else (CLOB() if __check_type(x, CLOB()) else VARCHAR())),
    'TRIM': lambda x: VARBYTE() if __if_byte_type(x) else VARCHAR(),
    'UCASE': lambda x: x,
    'UPPER': lambda x: x,

    # Time Series Aggregates
    'FIRST': lambda x: x,
    'LAST': lambda x: x,
    'MAD': lambda x: FLOAT() if not __check_type(x, [DECIMAL(), NUMBER()]) else x,
    'MODE': lambda x: x,
    'PERCENTILE': lambda x: FLOAT() if not __check_type(x, [DECIMAL(), NUMBER()]) else x
}

def _retrieve_function_expression_type(expression):
    """
    Returns the underlying default teradatasqlalchemy type for functions.
    """
    if isinstance(expression, sqlalc.sql.elements.Over):
        # If expression is of type Over, i.e., window aggregate then we should
        # check it's element to get the function name.
        function_name = expression.element.name.upper()
        func_str = expression.element.__str__()
    else:
        # Get the function name.
        function_name = expression.name.upper()
        func_str = expression.__str__()
    try:
        return VANTAGE_FUNCTION_TYPE_MAPPER[function_name]
    except KeyError:
        # We are here that means there is no direct mapping available for the
        # function name to output column type.
        # We must derive the column type from it's arguments or just type should be
        # default type 'sqlalc.sql.sqltypes.NullType' set by SQLAlchemy

        #
        # Let's process argument Dependent functions.
        #
        try:
            if function_name in ['MOD', 'POWER']:
                return VANTAGE_FUNCTION_ARGTYPE_DEPENDENT_MAPPER[function_name](function_name, func_str, expression)
            else:
                # Extract the first column and it's type.
                # Most of the functions output column type depends upon the type of the first column.
                argument_type = __get_function_argument_type(function_name, func_str, 1, expression)
                outtype = VANTAGE_FUNCTION_ARGTYPE_DEPENDENT_MAPPER[function_name](argument_type)
                if outtype is not None:
                    return outtype
                else:
                    return expression.type
        except KeyError:
            return expression.type

        # Unsupported Functions:
        #   1. Arithmetic Functions:
        #       - RANGE_N
        #   2. String Functions:
        #       - CSV
        #       - CSVLD
        #       - STROK
        #       - STROK_SPLIT_TO_TABLE
        #       - TRANSLATE
        #       - TRANSLATE_CHK
        #       - 'VARGRAPHIC' returns VARGRAPHIC type. teradatasqlalchemy does not have support for that.
        #   3. Regular Expression functions:
        #       - REGEXP_SPLIT_TO_TABLE


def _get_function_expression_type(function_expression, calling_expression, as_time_series_aggregate=False, **kwargs):
    """
    Returns the underlying default teradatasqlalchemy type for functions. This is used to get the
    type for a function executed on a _SQLColumnExpression.
    """
    # TODO:: Update below code for window aggregates
    # Get the function name.
    function_name = function_expression.name.upper()

    try:
        if as_time_series_aggregate and function_name == "MEDIAN":
            return FLOAT()
        # Get the function expression output type from VANTAGE_FUNCTION_TYPE_MAPPER
        return VANTAGE_FUNCTION_TYPE_MAPPER[function_name]
    except KeyError:
        # We are here that means there is no direct mapping available for the
        # function name to output column type.
        # We must derive the column type from it's arguments or just type should be
        # default type 'sqlalc.sql.sqltypes.NullType' set by SQLAlchemy

        #
        # Let's process argument Dependent functions.
        #
        try:
            if function_name == 'POWER':
                # TODO - Add support for power function.
                return None
                # return VANTAGE_FUNCTION_ARGTYPE_DEPENDENT_MAPPER[function_name](function_name, func_str, expression)
            else:
                # Extract the first column and it's type.
                # Most of the functions output column type depends upon the type of the first column.
                argument_type = calling_expression.type
                # argument_type = __get_function_argument_type(function_name, func_str, 1, expression)
                outtype = VANTAGE_FUNCTION_ARGTYPE_DEPENDENT_MAPPER[function_name](argument_type)
                if outtype is not None:
                    return outtype
                else:
                    return function_expression.type
        except KeyError:
            return function_expression.type

        # Unsupported Functions:
        #   1. Arithmetic Functions:
        #       - RANGE_N
        #   2. String Functions:
        #       - CSV
        #       - CSVLD
        #       - STROK
        #       - STROK_SPLIT_TO_TABLE
        #       - TRANSLATE
        #       - TRANSLATE_CHK
        #       - 'VARGRAPHIC' returns VARGRAPHIC type. teradatasqlalchemy does not have support for that.
        #   3. Regular Expression functions:
        #       - REGEXP_SPLIT_TO_TABLE