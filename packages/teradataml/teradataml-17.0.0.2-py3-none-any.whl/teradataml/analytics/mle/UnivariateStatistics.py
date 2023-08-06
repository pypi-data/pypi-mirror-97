#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Adithya Avvaru (adithya.avvaru@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.2
# 
# ################################################################## 

import inspect
import time
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.context.context import *
from teradataml.dataframe.dataframe import DataFrame
from teradataml.common.aed_utils import AedUtils
from teradataml.analytics.analytic_query_generator import AnalyticQueryGenerator
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.options.display import display

class UnivariateStatistics:
    
    def __init__(self,
        data = None,
        target_columns = None,
        exclude_columns = None,
        statistics = None,
        partition_columns = None,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The UnivariateStatistics function calculates descriptive statistics 
            for a set of target columns.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame that contains columns
                to calculate descriptive statistics.
         
            target_columns:
                Optional Argument.
                Specifies the input teradataml DataFrame columns that contain
                numeric values to calculate statistics for.
                Types: str OR list of Strings (str)
         
            exclude_columns:
                Optional Argument.
                Specifies the teradataml DataFrame columns which should be
                ignored, the rest of numeric columns in the teradataml
                DataFrame will be used as target variables.
                Types: str OR list of Strings (str)
         
            statistics:
                Optional Argument.
                Specifies the groups of statistical measures to include in the
                response.
                Permitted Values: MOMENTS, BASIC, QUANTILES
                Types: str
         
            partition_columns:
                Optional Argument.
                Specifies the columns which define groups for which statistics
                is calculated.
                Types: str OR list of Strings (str)
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each
                row of the input argument "data". The argument is used to
                ensure deterministic results for functions which produce
                results that vary from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of UnivariateStatistics.
            Output teradataml DataFrames can be accessed using attribute
            references, such as UnivariateStatisticsObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. moments_table
                2. basic_table
                3. quantiles_table
                4. output
         
            When the argument 'statistics' is None, all the four output
            teradataml DataFrames are generated. When the argument 'statistics'
            is given one of the permitted values (not None), the instance of
            UnivariateStatistics has the corresponding output teradataml
            DataFrame along with 'output' teradataml DataFrame.
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("univariatestatistics", "finance_data3")
         
            # Provided example table 'finance_data3' contains the columns
            # 'expenditure', 'income' and 'investment' for which the below
            # examples try to generate descriptive statistics.
         
            # Create teradataml DataFrame objects.
            finance_data3 = DataFrame.from_table("finance_data3")
         
            # Example 1 : UnivariateStatistics for all the numeric columns except 'id' and 'period'.
            US_out1 = UnivariateStatistics(data = finance_data3, exclude_columns = ["id","period"])
         
            # Print the results
            print(US_out1.moments_table)   # Prints 'moments_table' teradataml DataFrame.
            print(US_out1.basic_table)     # Prints 'basic_table' teradataml DataFrame.
            print(US_out1.quantiles_table) # Prints 'quantiles_table' teradataml DataFrame.
            print(US_out1.output)          # Prints 'output' teradataml DataFrame.
         
         
            # Example 2 : UnivariateStatistics for columns 'expenditure', 'income' and
            #              'investment' partitioned by the column 'id'.
            US_out2 = UnivariateStatistics(data = finance_data3,partition_columns = ["id"],
                                           target_columns = ["expenditure","income","investment"])
         
            # Print the results
            print(US_out2.moments_table)   # Prints 'moments_table' teradataml DataFrame.
            print(US_out2.basic_table)     # Prints 'basic_table' teradataml DataFrame.
            print(US_out2.quantiles_table) # Prints 'quantiles_table' teradataml DataFrame.
            print(US_out2.output)          # Prints 'output' teradataml DataFrame.
         
         
            # Example 3 : UnivariateStatistics for generating only BASIC statistics for all the
            #              numeric columns except 'id' and 'period'.
            US_out3 = UnivariateStatistics(data = finance_data3, exclude_columns = ["id","period"],
                                           statistics = "BASIC")
         
            # US_out3 doesn't have teradataml DataFrames 'moments_table' and 'output' as the
            # 'statistics' argument has only 'BASIC'.
            # Print the results
            print(US_out3.basic_table)     # Prints 'basic_table' teradataml DataFrame.
            print(US_out3.output)          # Prints 'output' teradataml DataFrame.
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.target_columns  = target_columns 
        self.exclude_columns  = exclude_columns 
        self.statistics  = statistics 
        self.partition_columns  = partition_columns 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["target_columns", self.target_columns, True, (str,list)])
        self.__arg_info_matrix.append(["exclude_columns", self.exclude_columns, True, (str,list)])
        self.__arg_info_matrix.append(["statistics", self.statistics, True, (str,list)])
        self.__arg_info_matrix.append(["partition_columns", self.partition_columns, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        
        if inspect.stack()[1][3] != '_from_model_catalog':
            # Perform the function validations
            self.__validate()
            # Generate the ML query
            self.__form_tdml_query()
            # Execute ML query
            self.__execute()
            # Get the prediction type
            self._prediction_type = self.__awu._get_function_prediction_type(self)
        
        # End the timer to get the build time
        _end_time = time.time()
        
        # Calculate the build time
        self._build_time = (int)(_end_time - _start_time)
        
    def __validate(self):
        """
        Function to validate sqlmr function arguments, which verifies missing 
        arguments, input argument and table types. Also processes the 
        argument values.
        """
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        
        # Check for permitted values
        statistics_permitted_values = ["MOMENTS", "BASIC", "QUANTILES"]
        self.__awu._validate_permitted_values(self.statistics, statistics_permitted_values, "statistics")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.target_columns, "target_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.target_columns, "target_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.exclude_columns, "exclude_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.exclude_columns, "exclude_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.partition_columns, "partition_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.partition_columns, "partition_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__moments_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_univariatestatistics0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__basic_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_univariatestatistics1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__quantiles_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_univariatestatistics2", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)

        # Output table arguments list
        if self.statistics is None:
            self.__func_output_args_sql_names = ["MomentsTableName", "BasicTableName", "QuantilesTableName"]
            self.__func_output_args = [self.__moments_table_temp_tablename, self.__basic_table_temp_tablename, self.__quantiles_table_temp_tablename]
        elif self.statistics.upper() == "MOMENTS":
            self.__func_output_args_sql_names = ["MomentsTableName"]
            self.__func_output_args = [self.__moments_table_temp_tablename]
        elif self.statistics.upper() == "BASIC":
            self.__func_output_args_sql_names = ["BasicTableName"]
            self.__func_output_args = [self.__basic_table_temp_tablename]
        else:  # if self.statistics.upper() == "QUANTILES"
            self.__func_output_args_sql_names = ["QuantilesTableName"]
            self.__func_output_args = [self.__quantiles_table_temp_tablename]

        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None

        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []

        if self.target_columns is not None:
            self.__func_other_arg_sql_names.append("TargetColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.target_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")

        if self.exclude_columns is not None:
            self.__func_other_arg_sql_names.append("ExcludeColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.exclude_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")

        if self.partition_columns is not None:
            self.__func_other_arg_sql_names.append("PartitionColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.partition_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")

        if self.statistics is not None:
            self.__func_other_arg_sql_names.append("StatisticsGroups")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.statistics, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")

        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))

        if len(sequence_input_by_list) > 0:
            self.__func_other_arg_sql_names.append("SequenceInputBy")
            sequence_input_by_arg_value = UtilFuncs._teradata_collapse_arglist(sequence_input_by_list, "'")
            self.__func_other_args.append(sequence_input_by_arg_value)
            self.__func_other_arg_json_datatypes.append("STRING")
            self._sql_specific_attributes["SequenceInputBy"] = sequence_input_by_arg_value


        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []

        # Process data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("InputTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")

        function_name = "UnivariateStatistics"
        # Create instance to generate SQLMR.
        self.__aqg_obj = AnalyticQueryGenerator(function_name,
                self.__func_input_arg_sql_names,
                self.__func_input_table_view_query,
                self.__func_input_dataframe_type,
                self.__func_input_distribution,
                self.__func_input_partition_by_cols,
                self.__func_input_order_by_cols,
                self.__func_other_arg_sql_names,
                self.__func_other_args,
                self.__func_other_arg_json_datatypes,
                self.__func_output_args_sql_names,
                self.__func_output_args,
                engine="ENGINE_ML")
        # Invoke call to SQL-MR generation.
        self.sqlmr_query = self.__aqg_obj._gen_sqlmr_select_stmt_sql()

        # Print SQL-MR query if requested to do so.
        if display.print_sqlmr_query:
            print(self.sqlmr_query)

        # Set the algorithm name for Model Cataloging.
        self._algorithm_name = self.__aqg_obj._get_alias_name_for_function(function_name)

    def __execute(self):
        """
        Function to execute SQL-MR queries.
        Create DataFrames for the required SQL-MR outputs.
        """
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        try:
            # Generate the output.
            UtilFuncs._create_table(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)

        # Update output table data frames.
        self._mlresults = []
        output_attr_info_message = "INFO: '{0}' output DataFrame is not created, when 'statistics' is set to '{1}'."
        self.moments_table = output_attr_info_message.format('moments_table', str(self.statistics).upper())
        self.basic_table = output_attr_info_message.format('basic_table', str(self.statistics).upper())
        self.quantiles_table = output_attr_info_message.format('quantiles_table', str(self.statistics).upper())

        if str(self.statistics).upper() not in ["BASIC", "QUANTILES"]:
            self.moments_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__moments_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__moments_table_temp_tablename))
            self._mlresults.append(self.moments_table)
        if str(self.statistics).upper() not in ["MOMENTS", "QUANTILES"]:
            self.basic_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__basic_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__basic_table_temp_tablename))
            self._mlresults.append(self.basic_table)
        if str(self.statistics).upper() not in ["BASIC", "MOMENTS"]:
            self.quantiles_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__quantiles_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__quantiles_table_temp_tablename))
            self._mlresults.append(self.quantiles_table)

        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.output)

    def show_query(self):
        """
        Function to return the underlying SQL query.
        When model object is created using retrieve_model(), then None is returned.
        """
        return self.sqlmr_query

    def get_prediction_type(self):
        """
        Function to return the Prediction type of the algorithm.
        When model object is created using retrieve_model(), then the value returned is 
        as saved in the Model Catalog.
        """
        return self._prediction_type

    def get_target_column(self):
        """
        Function to return the Target Column of the algorithm.
        When model object is created using retrieve_model(), then the value returned is 
        as saved in the Model Catalog.
        """
        return self._target_column

    def get_build_time(self):
        """
        Function to return the build time of the algorithm in seconds.
        When model object is created using retrieve_model(), then the value returned is 
        as saved in the Model Catalog.
        """
        return self._build_time

    def _get_algorithm_name(self):
        """
        Function to return the name of the algorithm.
        """
        return self._algorithm_name

    def _get_sql_specific_attributes(self):
        """
        Function to return the dictionary containing the SQL specific attributes of the algorithm.
        """
        return self._sql_specific_attributes

    @classmethod
    def _from_model_catalog(cls,
        moments_table = None,
        basic_table = None,
        quantiles_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("moments_table", None)
        kwargs.pop("basic_table", None)
        kwargs.pop("quantiles_table", None)
        kwargs.pop("output", None)

        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.moments_table  = moments_table
        obj.basic_table  = basic_table
        obj.quantiles_table  = quantiles_table
        obj.output  = output

        # Initialize the sqlmr_query class attribute.
        obj.sqlmr_query = None

        # Initialize the SQL specific Model Cataloging attributes.
        obj._sql_specific_attributes = None
        obj._target_column = target_column
        obj._prediction_type = prediction_type
        obj._algorithm_name = algorithm_name
        obj._build_time = build_time

        # Update output table data frames.
        obj._mlresults = []
        output_attr_info_message = "INFO: '{0}' output DataFrame is not created, when 'statistics' is set to '{1}'."
        if obj.moments_table is not None:
            obj.moments_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.moments_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.moments_table))
            obj._mlresults.append(obj.moments_table)
        else:
            obj.moments_table = output_attr_info_message.format('moments_table', "BASIC' or 'QUANTILES")

        if obj.basic_table is not None:
            obj.basic_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.basic_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.basic_table))
            obj._mlresults.append(obj.basic_table)
        else:
            obj.basic_table = output_attr_info_message.format('basic_table', "MOMENTS' or 'QUANTILES")

        if obj.quantiles_table is not None:
            obj.quantiles_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.quantiles_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.quantiles_table))
            obj._mlresults.append(obj.quantiles_table)
        else:
            obj.quantiles_table = output_attr_info_message.format('quantiles_table', "BASIC' or 'MOMENTS")

        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.output)
        return obj

    def __repr__(self):
        """
        Returns the string representation for a UnivariateStatistics class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ moments_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.moments_table)
        repr_string="{}\n\n\n############ basic_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.basic_table)
        repr_string="{}\n\n\n############ quantiles_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.quantiles_table)
        return repr_string
        
