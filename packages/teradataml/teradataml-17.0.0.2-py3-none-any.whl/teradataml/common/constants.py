# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: ellen.nolan@teradata.com
Secondary Owner:

teradataml.common.constants
----------
A class for holding all constants
"""
import re
import sqlalchemy
from enum import Enum
from teradatasqlalchemy.types import (INTEGER, SMALLINT, BIGINT, BYTEINT, DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy.types import (DATE, TIME, TIMESTAMP)
from teradatasqlalchemy.types import (BYTE, VARBYTE, BLOB)


class SQLConstants(Enum):
    SQL_BASE_QUERY = 1
    SQL_SAMPLE_QUERY = 2
    SQL_SAMPLE_WITH_WHERE_QUERY = 3
    SQL_CREATE_VOLATILE_TABLE_FROM_QUERY_WITH_DATA = 4
    SQL_CREATE_VOLATILE_TABLE_FROM_QUERY_WITHOUT_DATA = 5
    SQL_CREATE_VOLATILE_TABLE_USING_COLUMNS = 6
    SQL_CREATE_TABLE_FROM_QUERY_WITH_DATA = 7
    SQL_HELP_COLUMNS = 8
    SQL_DROP_TABLE = 9
    SQL_DROP_VIEW = 10
    SQL_NROWS_FROM_QUERY = 11
    SQL_TOP_NROWS_FROM_TABLEORVIEW = 12
    SQL_INSERT_INTO_TABLE_VALUES = 13
    SQL_SELECT_COLUMNNAMES_FROM = 14
    SQL_SELECT_DATABASE = 15
    SQL_HELP_VOLATILE_TABLE = 16
    SQL_SELECT_TABLE_NAME = 17
    SQL_CREATE_VIEW = 18
    SQL_SELECT_USER = 19
    SQL_HELP_VIEW = 20
    SQL_HELP_TABLE = 21
    SQL_HELP_INDEX = 22
    SQL_INSERT_ALL_FROM_TABLE = 23
    SQL_SELECT_DATABASENAME = 24
    SQL_AND_TABLE_KIND = 25
    SQL_AND_TABLE_NAME = 26
    SQL_AND_TABLE_NAME_LIKE = 27
    SQL_CREATE_TABLE_USING_COLUMNS = 28
    SQL_DELETE_ALL_ROWS = 29
    SQL_DELETE_SPECIFIC_ROW = 30
    SQL_EXEC_STORED_PROCEDURE = 31


class TeradataConstants(Enum):
    TERADATA_VIEW = 1
    TERADATA_TABLE = 2
    TERADATA_SCRIPT = 3
    TERADATA_LOCAL_SCRIPT = 4
    CONTAINER = 5
    TABLE_COLUMN_LIMIT = 2048
    TERADATA_JOINS = ["inner", "left", "right", "full", "cross"]
    TERADATA_JOIN_OPERATORS = ['>=', '<=', '<>', '!=', '>', '<', '=']
    # Order of operators
    # shouldn't be changed. This is the order in which join condition is tested - first, operators
    # with two characters and then the operators with single character.
    SUPPORTED_ENGINES = {"ENGINE_ML" : {"name" : "mle", "file" : "mlengine_alias_definitions"},
                         "ENGINE_SQL" : {"name" : "sqle", "file" : "sqlengine_alias_definitions"}}
    SUPPORTED_VANTAGE_VERSIONS = {"vantage1.0": "v1.0", "vantage1.1": "v1.1",
                                  "vantage1.3": "v1.3", "vantage2.0": "v1.1"}

class AEDConstants(Enum):
    AED_NODE_NOT_EXECUTED = 0
    AED_NODE_EXECUTED     = 1
    AED_DB_OBJECT_NAME_BUFFER_SIZE = 128
    AED_NODE_TYPE_BUFFER_SIZE = 32
    AED_ASSIGN_DROP_EXISITING_COLUMNS = "Y"
    AED_ASSIGN_DO_NOT_DROP_EXISITING_COLUMNS = "N"
    AED_QUERY_NODE_TYPE_ML_QUERY_SINGLE_OUTPUT = "ml_query_single_output"
    AED_QUERY_NODE_TYPE_ML_QUERY_MULTI_OUTPUT = "ml_query_multi_output"
    AED_QUERY_NODE_TYPE_REFERENCE = "reference"


class SourceType(Enum):
    TABLE = "TABLE"
    QUERY = "QUERY"


class PythonTypes(Enum):
    PY_NULL_TYPE = "nulltype"
    PY_INT_TYPE = "int"
    PY_FLOAT_TYPE = "float"
    PY_STRING_TYPE = "str"
    PY_DECIMAL_TYPE = "decimal.Decimal"
    PY_DATETIME_TYPE = "datetime.datetime"
    PY_TIME_TYPE = "datetime.time"
    PY_DATE_TYPE = "datetime.date"
    PY_BYTES_TYPE = "bytes"


class TeradataTypes(Enum):
    TD_INTEGER_TYPES = [INTEGER, BYTEINT, SMALLINT, BIGINT, sqlalchemy.sql.sqltypes.Integer]
    TD_INTEGER_CODES = ["I", "I1", "I2", "I8"]
    TD_FLOAT_TYPES = [FLOAT, sqlalchemy.sql.sqltypes.Numeric]
    TD_FLOAT_CODES = ["F"]
    TD_DECIMAL_TYPES = [DECIMAL, NUMBER]
    TD_DECIMAL_CODES = ["D", "N"]
    TD_BYTE_TYPES = [BYTE, VARBYTE, BLOB]
    TD_BYTE_CODES = ["BF", "BV", "BO"]
    TD_DATETIME_TYPES = [TIMESTAMP, sqlalchemy.sql.sqltypes.DateTime]
    TD_DATETIME_CODES = ["TS", "SZ"]
    TD_TIME_TYPES = [TIME, sqlalchemy.sql.sqltypes.Time]
    TD_TIME_CODES = ["AT", "TZ"]
    TD_DATE_TYPES = [DATE, sqlalchemy.sql.sqltypes.Date]
    TD_DATE_CODES = ["DA"]
    TD_NULL_TYPE = "NULLTYPE"


class TeradataTableKindConstants(Enum):
    VOLATILE = "volatile"
    TABLE = "table"
    VIEW = "view"
    TEMP = "temp"
    ALL  = "all"
    ML_PATTERN = "ml_%"
    VOLATILE_TABLE_NAME = 'Table Name'
    REGULAR_TABLE_NAME = 'TableName'


class SQLPattern(Enum):
    SQLMR = re.compile(r"SELECT \* FROM .*\((\s*.*)*\) as .*", re.IGNORECASE)
    DRIVER_FUNC_SQLMR = re.compile(r".*OUT\s+TABLE.*", re.IGNORECASE)
    SQLMR_REFERENCE_NODE = re.compile("reference:.*:.*", re.IGNORECASE)


class FunctionArgumentMapperConstants(Enum):
    # Mapper related
    SQL_TO_TDML = "sql_to_tdml"
    TDML_TO_SQL = "tdml_to_sql"
    ALTERNATE_TO = "alternate_to"
    TDML_NAME = "tdml_name"
    TDML_TYPE = "tdml_type"
    USED_IN_SEQUENCE_INPUT_BY = "used_in_sequence_by"
    USED_IN_FORMULA = "used_in_formula"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    ARGUMENTS = "arguments"
    DEPENDENT_ATTR = "dependent"
    INDEPENDENT_ATTR = "independent"
    TDML_FORMULA_NAME = "formula"
    DEFAULT_OUTPUT = "__default_output__"
    DEFAULT_OUTPUT_TDML_NAME_SINGLE = "result"
    DEFAULT_OUTPUT_TDML_NAME_MULTIPLE = "output"

    # JSON related
    ALLOWS_LISTS = "allowsLists"
    DATATYPE = "datatype"
    BOOL_TYPE = "BOOLEAN"
    INT_TYPE = ["INTEGER", "LONG"]
    FLOAT_TYPE = ["DOUBLE", "DOUBLE PRECISION", "FLOAT"]
    INPUT_TABLES = "input_tables"
    OUTPUT_TABLES = "output_tables"
    ARGUMENT_CLAUSES = "argument_clauses"
    R_NAME = "rName"
    NAME = "name"
    FUNCTION_TDML_NAME = "function_tdml_name"
    R_FOMULA_USAGE = "rFormulaUsage"
    R_ORDER_NUM = "rOrderNum"
    TDML_SEQUENCE_COLUMN_NAME = "sequence_column"


class ModelCatalogingConstants(Enum):
    MODEL_CATALOG_DB = "TD_ModelCataloging"
    MODEL_ENGINE_ML = "ML Engine"
    MODEL_ENGINE_ADVSQL = "Advanced SQL Engine"

    MODEL_TDML = "teradataml"

    # Stored Procedure Names
    SAVE_MODEL = "SYSLIB.SaveModel"
    DELETE_MODEL = "SYSLIB.DeleteModel"
    PUBLISH_MODEL = "SYSLIB.PublishModel"

    # ModelCataloging Direct Views
    MODELS = "ModelsV"
    MODELS_DETAILS = "ModelDetailsV"
    MODELS_OBJECTS = "ModelObjectsV"
    MODELS_ATTRS = "ModelAttributesV"
    MODELS_PERF = "ModelPerformanceV"
    MODELS_LOC = "ModelLocationV"

    # ModelCataloging Derived Views
    MODELSX = "ModelsVX"
    MODELS_DETAILSX = "ModelDetailsVX"
    MODELS_INPUTSX = "ModelTrainingDataVX"

    # Columns names used for Filter
    MODEL_NAME = "Name"
    MODEL_ID = "ModelId"
    CREATED_BY = "CreatedBy"
    MODEL_ACCESS = "ModelAccess"
    MODEL_DERIVED_NAME = "ModelName"
    MODEL_DERIVED_ALGORITHM = "ModelAlgorithm"
    MODEL_DERIVED_PREDICTION_TYPE = "ModelPredictionType"
    MODEL_DERIVED_BUILD_TIME = "ModelBuildTime"
    MODEL_DERIVED_TARGET_COLUMN = "ModelTargetColumn"
    MODEL_DERIVED_GENENG = "ModelGeneratingEngine"
    MODEL_DERIVED_GENCLIENT = "ModelGeneratingClient"
    MODEL_ATTR_CLIENT_NAME = "ClientSpecificAttributeName"
    MODEL_ATTR_NAME = "AttributeName"
    MODEL_ATTR_VALUE = "AttributeValue"
    MODEL_ATTR_VALUEC = "AttributeValueC"
    MODEL_CLIENT_CLASS_KEY = "__class_name__"
    MODEL_INPUT_NROWS = "NRows"
    MODEL_INPUT_NCOLS = "NCols"

    MODEL_OBJ_NAME = "TableReferenceName"
    MODEL_OBJ_CLIENT_NAME = "ClientSpecificTableReferenceName"
    MODEL_OBJ_TABLE_NAME = "TableName"

    MODEL_INPUT_NAME = "InputName"
    MODEL_INPUT_CLIENT_NAME = "ClientSpecificInputName"
    MODEL_INPUT_TABLE_NAME = "TableName"

    MODEL_LIST_LIST = ['ModelName','ModelAlgorithm','ModelGeneratingEngine',
                       'ModelGeneratingClient','CreatedBy','CreatedDate']

    # Valid and default status and access
    MODEL_VALID_STATUS = ['ACTIVE', 'RETIRED', 'CANDIDATE', 'PRODUCTION', 'IN-DEVELOPMENT']
    DEFAULT_SAVE_STATUS = 'In-Development'
    DEFAULT_SAVE_ACCESS = 'Private'
    PUBLIC_ACCESS = 'Public'

    # Expected Prediction Types
    PREDICTION_TYPE_CLASSIFICATION = 'CLASSIFICATION'
    PREDICTION_TYPE_REGRESSION = 'REGRESSION'
    PREDICTION_TYPE_CLUSTERING = 'CLUSTERING'
    PREDICTION_TYPE_OTHER = 'OTHER'


class CopyToConstants(Enum):
    DBAPI_BATCHSIZE                      = 16383


class PTITableConstants(Enum):
    PATTERN_TIMEZERO_DATE = r"^DATE\s+'(.*)'$"
    TD_SEQNO = 'TD_SEQNO'
    TD_TIMECODE = 'TD_TIMECODE'
    TD_TIMEBUCKET = 'TD_TIMEBUCKET'
    TSCOLTYPE_TIMEBUCKET = 'TB'
    TSCOLTYPE_TIMECODE = 'TC'
    VALID_TIMEBUCKET_DURATIONS_FORMAL = ['CAL_YEARS', 'CAL_MONTHS', 'CAL_DAYS', 'WEEKS', 'DAYS', 'HOURS', 'MINUTES',
                                         'SECONDS', 'MILLISECONDS', 'MICROSECONDS']
    VALID_TIMEBUCKET_DURATIONS_SHORTHAND = ['cy', 'cyear', 'cyears',
                                            'cm', 'cmonth', 'cmonths',
                                            'cd', 'cday', 'cdays',
                                            'w', 'week', 'weeks',
                                            'd', 'day', 'days',
                                            'h', 'hr', 'hrs', 'hour', 'hours',
                                            'm', 'mins', 'minute', 'minutes',
                                            's', 'sec', 'secs', 'second', 'seconds',
                                            'ms', 'msec', 'msecs', 'millisecond', 'milliseconds',
                                            'us', 'usec', 'usecs', 'microsecond', 'microseconds']
    PATTERN_TIMEBUCKET_DURATION_SHORT = "^([0-9]+){}$"
    PATTERN_TIMEBUCKET_DURATION_FORMAL = r"^{}\(([0-9]+)\)$"
    VALID_TIMECODE_DATATYPES = [TIMESTAMP, DATE]
    VALID_SEQUENCE_COL_DATATYPES = [INTEGER]
    TIMEBUCKET_DURATION_FORMAT_MAPPER = {'cy': 'CAL_YEARS({})',
                                         'cyear': 'CAL_YEARS({})',
                                         'cyears': 'CAL_YEARS({})',
                                         'cm': 'CAL_MONTHS({})',
                                         'cmonth': 'CAL_MONTHS({})',
                                         'cmonths': 'CAL_MONTHS({})',
                                         'cd': 'CAL_DAYS({})',
                                         'cday': 'CAL_DAYS({})',
                                         'cdays': 'CAL_DAYS({})',
                                         'w': 'WEEKS({})',
                                         'week': 'WEEKS({})',
                                         'weeks': 'WEEKS({})',
                                         'd': 'DAYS({})',
                                         'day': 'DAYS({})',
                                         'days': 'DAYS({})',
                                         'h': 'HOURS({})',
                                         'hr': 'HOURS({})',
                                         'hrs': 'HOURS({})',
                                         'hour': 'HOURS({})',
                                         'hours': 'HOURS({})',
                                         'm': 'MINUTES({})',
                                         'mins': 'MINUTES({})',
                                         'minute': 'MINUTES({})',
                                         'minutes': 'MINUTES({})',
                                         's': 'SECONDS({})',
                                         'sec': 'SECONDS({})',
                                         'secs': 'SECONDS({})',
                                         'second': 'SECONDS({})',
                                         'seconds': 'SECONDS({})',
                                         'ms': 'MILLISECONDS({})',
                                         'msec': 'MILLISECONDS({})',
                                         'msecs': 'MILLISECONDS({})',
                                         'millisecond': 'MILLISECONDS({})',
                                         'milliseconds': 'MILLISECONDS({})',
                                         'us': 'MICROSECONDS({})',
                                         'usec': 'MICROSECONDS({})',
                                         'usecs': 'MICROSECONDS({})',
                                         'microsecond': 'MICROSECONDS({})',
                                         'microseconds': 'MICROSECONDS({})'}


class OutputStyle(Enum):
    OUTPUT_TABLE = 'TABLE'
    OUTPUT_VIEW = 'VIEW'


class TableOperatorConstants(Enum):
    # Template of the intermediate script that will be generated.
    MAP_TEMPLATE = "dataframe_map.template"
    # In-DB execution mode.
    INDB_EXEC = "IN-DB"
    # Local execution mode.
    LOCAL_EXEC = "LOCAL"
    # Sandbox execution mode.
    SANDBOX_EXEC = "SANDBOX"
    EXEC_MODE = [LOCAL_EXEC, SANDBOX_EXEC, INDB_EXEC]
    # map_row operation.
    MAP_ROW_OP = "map_row"
    # map_partition operation.
    MAP_PARTITION_OP = "map_partition"
    # Template of the script_executor that will be used to generate the temporary script_executor file.
    SCRIPT_TEMPLATE = "script_executor.template"
    # Log Type.
    SCRIPT_LOG = "SCRIPT"
    LOG_TYPE = [SCRIPT_LOG]
    # Query for viewing last n lines of script log.
    SCRIPT_LOG_QUERY = "SELECT * FROM SCRIPT (SCRIPT_COMMAND " \
                       "('tail -n {} /var/opt/teradata/tdtemp/uiflib/scriptlog') " \
                       "RETURNS ('scriptlog VARCHAR({})') )"

    # Check if Python interpretor and add-ons are installed or not.
    CHECK_PYTHON_INSTALLED = """SELECT distinct * FROM SCRIPT(
                                ON (select 1) PARTITION BY ANY
                                SCRIPT_COMMAND('pip3 --version')
                                returns('package VARCHAR(256)'))
                             """

    # Script Query to get Python packages and corresponding versions.
    PACKAGE_VERSION_QUERY = \
                        """ SELECT distinct * FROM SCRIPT(
                            ON (select 1) PARTITION BY ANY
                            SCRIPT_COMMAND('pip3 freeze | {0}awk -F ''=='' ''{{print $1, $2}}''')
                            delimiter(' ')
                            returns('package VARCHAR({1}), version VARCHAR({1})'))
                        """

class ValibConstants(Enum):
    # A dictionary that maps teradataml name of the exposed VALIB function name
    # to Vantage VALIB SQL function name.
    TERADATAML_VALIB_SQL_FUNCTION_NAME_MAP = {
        "AdaptiveHistogram": "AdaptiveHistogram",
        "Explore": "DataExplorer",
        "Frequency": "Frequency",
        "Histogram": "Histogram",
        "Overlap": "Overlap",
        "Statistics": "Statistics",
        "TextAnalyzer": "TextFieldAnalyzer",
        "Values": "Values",
        "Association": "Association",
        "KMeans": "Kmeans",
        "KMeansPredict": "KmeansScore",
        "DecisionTree": "DecisionTree",
        "DecisionTreePredict": "DecisionTreeScore",
        "DecisionTreeEvaluator": "DecisionTreeScore",
        "Matrix": "Matrix",
        "LinReg": "Linear",
        "LinRegPredict": "LinearScore",
        "LinRegEvaluator": "LinearScore",
        "LogReg": "Logistic",
        "LogRegPredict": "LogisticScore",
        "LogRegEvaluator": "LogisticScore",
        "PCA": "Factor",
        "PCAPredict": "FactorScore",
        "PCAEvaluator": "FactorScore",
        "ParametricTest": "ParametricTest",
        "BinomialTest": "BinomialTest",
        "KSTest": "KSTest",
        "ChiSquareTest": "ChiSquareTest",
        "RankTest": "RankTest",
        "BinCode": "vartran",
        "Derive": "vartran",
        "DesignCode": "vartran",
        "fillna": "vartran",
        "Recode": "vartran",
        "Rescale": "vartran",
        "Sigmoid": "vartran",
        "ZScore": "vartran",
        "Transform": "vartran"
    }

    # A dictionary that maps Vantage VALIB SQL function name to a dictionary
    # mapping a teradataml name of input argument to another dictionary containing
    # Vantage SQL equivalent arguments, specified with "database_arg" and
    # "table_arg" keys.
    # In teradataml, input argument is a DataFrame, which contains both database and table name
    # information. We shall just map that to Vantage SQL input table arguments.
    # ---------------------------------------------------------------------------------
    # NOTE:
    #   Add an entry in this map,
    #       1. If and only if VALIB function accepts multiple input arguments.
    #       2. Default argument for input is "data". Don't add an entry for it.
    #       3. Add entry for only other input arguments.
    # ---------------------------------------------------------------------------------
    VALIB_FUNCTION_MULTIINPUT_ARGUMENT_MAP = {
        "ASSOCIATION": {
            "description_data": {
                "database_arg": "descriptiondatabase",
                "table_arg": "descriptiontable"
            },
            "hierarchy_data": {
                "database_arg": "hierarchydatabase",
                "table_arg": "hierarchytable"
            },
            "left_lookup_data": {
                "database_arg": "leftlookupdatabase",
                "table_arg": "leftlookuptable"
            },
            "right_lookup_data": {
                "database_arg": "rightlookupdatabase",
                "table_arg": "rightlookuptable"
            },
            "reduced_data": {
                "database_arg": "reducedinputdatabase",
                "table_arg": "reducedinputtable"
            }
        },

        "KMEANSSCORE": {
            "model": {
                "database_arg": "modeldatabase",
                "table_arg": "modeltablename"
            }
        },

        "DECISIONTREESCORE": {
            "model": {
                "database_arg": "modeldatabase",
                "table_arg": "modeltablename"
            }
        },

        "LINEARSCORE": {
            "model": {
                "database_arg": "modeldatabase",
                "table_arg": "modeltablename"
            }
        },

        "LOGISTIC": {
            "matrix_data": {
                "database_arg": "matrixdatabase",
                "table_arg": "matrixtablename"
            }
        },

        "LOGISTICSCORE": {
            "model": {
                "database_arg": "modeldatabase",
                "table_arg": "modeltablename"
            }
        },

        "FACTORSCORE": {
            "model": {
                "database_arg": "modeldatabase",
                "table_arg": "modeltablename"
            }
        }
    }

    # A dictionary that maps Vantage VALIB SQL function name to a dictionary of SQL output
    # arguments of the function.
    # This values dictionary will map:
    #   1. "db" key to SQL output argument that accepts database name where output
    #      table will be created.
    #   2. "tbls" key to a list of SQL output argument that accepts table name.
    #   3. "mandatory_output_extensions" key to the dictionary of extensions to teradataml
    #      output argument names. The tables in this extension mapper are generated
    #      irrespective of whether the function is scoring/evaluator/any other function.
    #   4. "evaluator_output_extensions" key to the dictionary of extensions to teradataml
    #      output argument names. The tables in this extension mapper are generated
    #      only when the function is evaluator function. When these tables are generated,
    #      tables that do not have extensions will not be generated (feature of evaluator
    #      functions.
    # In teradataml, output arguments are not accepted from user, but are created and used
    # internally.
    # ---------------------------------------------------------------------------------
    # NOTES:
    #   1. Add an entry in this map, if VALIB function
    #       a. Generates multiple output tables OR
    #       b. Output argument names are not same as default output argument names:
    #               'outputdatabase' and 'outputtablename'.
    #   2. No need to add an entry for default argument for output.
    # ---------------------------------------------------------------------------------
    VALIB_FUNCTION_OUTPUT_ARGUMENT_MAP = {
        "DATAEXPLORER": {
            "db": "outputdatabase",
            "tbls": ["frequencyoutputtablename",
                     "histogramoutputtablename",
                     "statisticsoutputtablename",
                     "valuesoutputtablename"]
        },

        "LINEAR": {
            "db": "outputdatabase",
            "tbls": "outputtablename",
            "mandatory_output_extensions": {"_rpt": "statistical_measures",
                                            "_txt": "xml_reports"}
        },

        "LINEARSCORE": {
            "db": "outputdatabase",
            "tbls": "outputtablename",
            "evaluator_output_extensions": {"_txt": "result"}
        },

        "LOGISTIC": {
            "db": "outputdatabase",
            "tbls": "outputtablename",
            "mandatory_output_extensions": {"_rpt": "statistical_measures",
                                            "_txt": "xml_reports"}
        },

        "LOGISTICSCORE": {
            "db": "outputdatabase",
            "tbls": "outputtablename",
            "evaluator_output_extensions": {"_txt": "result"}
        },

        "DECISIONTREESCORE": {
            "db": "outputdatabase",
            "tbls": "outputtablename",
            "mandatory_output_extensions": {"_1": "profile_result_1",
                                            "_2": "profile_result_2"},
            "evaluator_output_extensions": {"_rpt": "result"}
        },

        "FACTORSCORE": {
            "db": "outputdatabase",
            "tbls": "outputtablename",
            "evaluator_output_extensions": {"_rpt": "result"}
        },

        "TEXTFIELDANALYZER": {
            "db": "outputdatabase",
            "tbls": "outputtablename",
            "mandatory_output_extensions": {"_rpt": "data_type_matrix"}
        }
    }

    # A dictionary that maps Vantage VALIB SQL function name to a dictionary mapping
    # SQL Output table argument name to teradataml exposed output argument name.
    # ---------------------------------------------------------------------------------
    # NOTES:
    #   1. Add an entry in this map, if VALIB function generates multiple output tables.
    #   2. No need to add an entry for default argument for output.
    #   3. Default exposed output argument name is "result".
    # ---------------------------------------------------------------------------------
    TERADATAML_VALIB_MULTIOUTPUT_ATTR_MAP = {
        "DATAEXPLORER": {
            "frequencyoutputtablename": "frequency_output",
            "histogramoutputtablename": "histogram_output",
            "statisticsoutputtablename": "statistics_output",
            "valuesoutputtablename": "values_output"
        },

        "LINEAR": {
            "outputtablename": "model",
            "_rpt": "statistical_measures",
            "_txt": "xml_reports"
        },

        "LOGISTIC": {
            "outputtablename": "model",
            "_rpt": "statistical_measures",
            "_txt": "xml_reports"
        },

        "DECISIONTREESCORE": {
            "outputtablename": "result",
            "_1": "profile_result_1",
            "_2": "profile_result_2"
        },

        "TEXTFIELDANALYZER": {
            "outputtablename": "result",
            "_rpt": "data_type_matrix"
        }
    }

    # A dictionary that maps Vantage VALIB Teradataml function name to a dictionary mapping
    # SQL Output table argument name to teradataml exposed output argument name.
    # ---------------------------------------------------------------------------------
    # NOTES:
    #   1. Add an entry in this map, if VALIB evaluator function generates tables with
    #      extension(s) or multiple output tables.
    #   2. This mapper is specific to Evaluator functions. "__multioutput_attr_map" of VALIB
    #      object is replaced with this mapper if the function is evaluator function.
    # ---------------------------------------------------------------------------------
    TERDATAML_EVALUATOR_OUTPUT_ATTR_MAP = {
        "DecisionTreeEvaluator": {
            "_rpt": "result",
            "_1": "profile_result_1",
            "_2": "profile_result_2"
        },

        "LinRegEvaluator": {
            "_txt": "result"
        },

        "LogRegEvaluator": {
            "_txt": "result"
        },

        "PCAEvaluator": {
            "_rpt": "result"
        }
    }

    # A dictionary that maps Vantage VALIB SQL function name to:
    #   1. A dictionary mapping teradataml exposed name of the argument to SQL function
    #      argument name. OR
    #   2. Just a list of SQL function argument names supported by the function.
    # ---------------------------------------------------------------------------------
    # NOTES:
    #   1. Add an entry in this map, if argument names in teradataml are different from
    #   SQL function argument names.
    #   2. No need to add an entry if all argument names are same as that of the SQL Function
    #   argument.
    #   3. The argument "scoring_method" is added internally based on the teradataml function
    #   name.
    # ---------------------------------------------------------------------------------
    TERADATAML_VALIB_FUNCTION_ARGUMENT_MAP = {
        # 'overwrite' argument is not needed, as we will generate table names internally.
        "ADAPTIVEHISTOGRAM": {
            "columns": "columns",
            "bins": "bins",
            "exclude_columns": "columnstoexclude",
            "spike_threshold": "spikethreshold",
            "subdivision_method": "subdivisionmethod",
            "subdivision_threshold": "subdivisionthreshold",
            "filter": "where"
        },

        "DATAEXPLORER": {
            "columns": "columns",
            "bins": "bins",
            "bin_style": "binstyle",
            "max_comb_values": "maxnumcombvalues",
            "max_unique_char_values": "maxuniquecharvalues",
            "max_unique_num_values": "maxuniquenumvalues",
            "min_comb_rows": "minrowsforcomb",
            "restrict_freq": "restrictedfreqproc",
            "restrict_threshold": "restrictedthreshold",
            "statistical_method": "statisticalmethod",
            "stats_options": "statsoptions",
            "distinct": "uniques",
            "filter": "where"
        },

        "FREQUENCY": {
            "columns": "columns",
            "exclude_columns": "columnstoexclude",
            "cumulative_option": "cumulativeoption",
            "agg_filter": "having",
            "min_percentage": "minimumpercentage",
            "pairwise_columns": "pairwisecolumns",
            "stats_columns": "statisticscolumns",
            "style": "style",
            "top_n": "topvalues",
            "filter": "where"
        },

        "HISTOGRAM": {
            "columns": "columns",
            "bins": "bins",	
            "bins_with_boundaries": "binwithminmax",	
            "boundaries": "boundaries",	
            "quantiles": "quantiles",	
            "widths": "widths",
            "exclude_columns": "columnstoexclude",
            "overlay_columns": "overlaycolumns",
            "stats_columns": "statisticscolumns",
            "hist_style": "style",
            "filter": "where"
        },

        "STATISTICS": {
            "columns": "columns",
            "exclude_columns": "columnstoexclude",
            "extended_options": "extendedoptions",
            "group_columns": "groupby",
            "statistical_method": "statisticalmethod",
            "stats_options": "statsoptions",
            "filter": "where"
        },

        "TEXTFIELDANALYZER": {
            "columns": "columns",
            "exclude_columns": "columnstoexclude",
            "analyze_numerics": "extendednumericanalysis",
            "analyze_unicode": "extendedunicodeanalysis"
        },

        "VALUES": {
            "columns": "columns",
            "exclude_columns": "columnstoexclude",
            "group_columns": "groupby",
            "distinct": "uniques",
            "filter": "where"
        },

        "ASSOCIATION": {
            "group_column": "groupcolumn",
            "item_column": "itemcolumn",
            "combinations": "combinations",
            "description_identifier": "descriptionidentifier",
            "description_column": "descriptioncolumn",
            "group_count": "groupcount",
            "low_level_column": "hierarchyitemcolumn",
            "high_level_column": "hierarchycolumn",
            "left_lookup_column": "leftlookupcolumn",
            "right_lookup_column": "rightlookupcolumn",
            "min_confidence": "minimumconfidence",
            "min_lift": "minimumlift",
            "min_support": "minimumsupport",
            "min_zscore": "minimumzscore",
            "order_prob": "orderingprobability",
            "process_type": "processtype",
            "relaxed_order": "relaxedordering",
            "sequence_column": "sequencecolumn",
            "filter": "where",
            "no_support_results": "dropsupporttables",
            "support_result_prefix": "resulttableprefix"
        },

        "KMEANS": {
            "columns": "columns",
            "centers": "kvalue",
            "exclude_columns": "columnstoexclude",
            "continuation": "continuation",
            "max_iter": "iterations",
            "operator_database": "operatordatabase",
            "threshold": "threshold"
        },

        "KMEANSSCORE": {
            "index_columns": "index",
            "cluster_column": "clustername",
            "fallback": "fallback",
            "operator_database": "operatordatabase",
            "accumulate": "retain"
        },

        "DECISIONTREE": {
            "columns": "columns",
            "response_column": "dependent",
            "algorithm": "algorithm",
            "binning": "binning",
            "exclude_columns": "columnstoexclude",
            "max_depth": "max_depth",
            "num_splits": "min_records",
            "operator_database": "operatordatabase",
            "pruning": "pruning"
        },

        "DECISIONTREESCORE": {
            "include_confidence": "includeconfidence",
            "index_columns": "index",
            "response_column": "predicted",
            "profile": "profiletables",
            "accumulate": "retain",
            "targeted_value": "targetedvalue"
        },

        "MATRIX": {
            "columns": "columns",
            "exclude_columns": "columnstoexclude",
            "group_columns": "groupby",
            "matrix_output": "matrixoutput",
            "type": "matrixtype",
            "handle_nulls": "nullhandling",
            "filter": "where"
        },

        "LINEAR": {
            "columns": "columns",
            "response_column": "dependent",
            "backward": "backward",
            "backward_only": "backwardonly",
            "exclude_columns": "columnstoexclude",
            "cond_ind_threshold": "conditionindexthreshold",
            "constant": "constant",
            "entrance_criterion": "enter",
            "forward": "forward",
            "forward_only": "forwardonly",
            "group_columns": "groupby",
            "matrix_input": "matrixinput",
            "near_dep_report": "neardependencyreport",
            "remove_criterion": "remove",
            "stats_output": "statstable",
            "stepwise": "stepwise",
            "use_fstat": "usefstat",
            "use_pvalue": "usepvalue",
            "variance_prop_threshold": "varianceproportionthreshold"
        },

        "LINEARSCORE": {
            "index_columns": "index",
            "response_column": "predicted",
            "residual_column": "residual",
            "accumulate": "retain"
        },

        "LOGISTIC": {
            "columns": "columns",
            "response_column": "dependent",
            "backward": "backward",
            "backward_only": "backwardonly",
            "exclude_columns": "columnstoexclude",
            "cond_ind_threshold": "conditionindexthreshold",
            "constant": "constant",
            "convergence": "convergence",
            "entrance_criterion": "enter",
            "forward": "forward",
            "forward_only": "forwardonly",
            "group_columns": "groupby",
            "lift_output": "lifttable",
            "max_iter": "maxiterations",
            "mem_size": "memorysize",
            "near_dep_report": "neardependencyreport",
            "remove_criterion": "remove",
            "response_value": "response",
            "sample": "sample",
            "stats_output": "statstable",
            "stepwise": "stepwise",
            "success_output": "successtable",
            "start_threshold": "thresholdbegin",
            "end_threshold": "thresholdend",
            "increment_threshold": "thresholdincrement",
            "threshold_output": "thresholdtable",
            "variance_prop_threshold": "varianceproportionthreshold"
        },

        "LOGISTICSCORE": {
            "estimate_column": "estimate",
            "index_columns": "index",
            "prob_column": "probability",
            "accumulate": "retain",
            "prob_threshold": "threshold",
            "start_threshold": "thresholdbegin",
            "end_threshold": "thresholdend",
            "increment_threshold": "thresholdincrement"

            # The following 3 arguments three should not be present for LogRegPredict function
            # where as when the function is LogRegEvaluator, at least one of these should be
            # present. By default (i.e., when these are not provided in LogRegEvaluator SQL), the
            # function takes 'True' for these arguments. So, by commenting these we are providing
            # all three tables in XML that is generated by the LogRegEvaluator function.
            # "threshold_output": "thresholdtable",
            # "lift_output": "lifttable",
            # "success_output": "successtable"
        },

        "FACTOR": {
            "columns": "columns",
            "exclude_columns": "columnstoexclude",
            "cond_ind_threshold": "conditionindexthreshold",
            "min_eigen": "eigenmin",
            "load_report": "factorloadingsreport",
            "vars_load_report": "factorvariablesloadingsreport",
            "vars_report": "factorvariablesreport",
            "gamma": "gamma",
            "group_columns": "groupby",
            "matrix_input": "matrixinput",
            "matrix_type": "matrixtype",
            "near_dep_report": "neardependencyreport",
            "rotation_type": "rotationtype",
            "load_threshold": "thresholdloading",
            "percent_threshold": "thresholdpercent",
            "variance_prop_threshold": "varianceproportionthreshold"
        },

        "FACTORSCORE": {
            "index_columns": "index",
            "accumulate": "retain"
        },

        "PARAMETRICTEST": {
            "columns": "columns",
            "dependent_column": "columnofinterest",
            "equal_variance": "equalvariance",
            "fallback": "fallback",
            "first_column": "firstcolumn",
            "first_column_values": "firstcolumnvalues",
            "group_columns": "groupby",
            "allow_duplicates": "multiset",
            "paired": "paired",
            "second_column": "secondcolumn",
            "second_column_values": "secondcolumnvalues",
            "stats_database": "statsdatabase",
            "style": "teststyle",
            "probability_threshold": "thresholdprobability",
            "with_indicator": "withindicator"
        },

        "BINOMIALTEST": {
            "first_column": "firstcolumn",
            "binomial_prob": "binomialprobability",
            "exact_matches": "exactmatches",
            "fallback": "fallback",
            "group_columns": "groupby",
            "allow_duplicates": "multiset",
            "second_column": "secondcolumn",
            "single_tail": "singletail",
            "stats_database": "statsdatabase",
            "style": "teststyle",
            "probability_threshold": "thresholdprobability"
        },

        "KSTEST": {
            "columns": "columns",
            "dependent_column": "columnofinterest",
            "fallback": "fallback",
            "group_columns": "groupby",
            "allow_duplicates": "multiset",
            "stats_database": "statsdatabase",
            "style": "teststyle",
            "probability_threshold": "thresholdprobability"
        },

        "CHISQUARETEST": {
            "columns": "columns",
            "dependent_column": "columnofinterest",
            "fallback": "fallback",
            "first_columns": "firstcolumns",
            "group_columns": "groupby",
            "allow_duplicates": "multiset",
            "second_columns": "secondcolumns",
            "stats_database": "statsdatabase",
            "style": "teststyle",
            "probability_threshold": "thresholdprobability"
        },

        "RANKTEST": {
            "block_column": "blockcolumn",
            "columns": "columns",
            "dependent_column": "columnofinterest",
            "fallback": "fallback",
            "first_column": "firstcolumn",
            "group_columns": "groupby",
            "include_zero": "includezero",
            "independent": "independent",
            "allow_duplicates": "multiset",
            "second_column": "secondcolumn",
            "single_tail": "singletail",
            "stats_database": "statsdatabase",
            "style": "teststyle",
            "probability_threshold": "thresholdprobability",
            "treatment_column": "treatmentcolumn"
        },

        "VARTRAN": {
            "fallback": "fallback",
            "index_columns": "index",
            "unique_index": "indexunique",
            "key_columns": "keycolumns",
            "allow_duplicates": "multiset",
            "nopi": "noindex",
            "filter": "whereclause"
        }
    }

    # Arguments to ignore - These are the arguments, that are not processed currently.
    # TODO: Support can be added to these in later stages.
    IGNORE_ARGUMENTS = ["overwrite", "ouputstyle", "gensql", "gensqlonly",
                        "dropsupporttables", "resulttableprefix", "samplescoresize"]

    # Output DataFrame default argument name.
    DEFAULT_OUTPUT_VAR = "result"

    # Output DataFrame result list name.
    OUTPUT_DATAFRAME_RESULTS = "_valib_results"

    # Scoring method SQL argument name and values.
    SCORING_METHOD_ARG_NAME = "scoringmethod"
    SCORING_METHOD_ARG_VALUE = {
        "default" : "score",
        # TODO: Replace "scoreandevaluate" with "evaluate" because for FactorScore, using
        # scoringmethod as evaluate is producing result to the console and table is not
        # generated.
        "non-default" : "scoreandevaluate"
    }
