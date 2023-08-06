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
# Function Version: 1.3
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

class ChangePointDetectionRT:
    
    def __init__(self,
        data = None,
        value_column = None,
        accumulate = None,
        segmentation_method = "normal_distribution",
        window_size = 10,
        threshold = 10.0,
        output_option = "CHANGEPOINT",
        data_sequence_column = None,
        data_partition_column = None,
        data_order_column = None):
        """
        DESCRIPTION:
            The ChangePointDetectionRT function detects change points in a
            stochastic process or time series, using real-time change-point
            detection, implemented with these algorithms:
            • Search algorithm: sliding window
            • Segmentation algorithm: normal distribution
         
            Use this function when the input data cannot be stored in Teradata
            Vantage memory, or when the application requires a real-time
            response. If the input data can be stored in Teradata Vantage memory
            and the application does not require a real-time response, use the
            function ChangePointDetection.
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame defining the input time series
                data.
         
            data_partition_column:
                Required Argument.
                Specifies Partition By columns for data. Values to this argument
                can be provided as list, if multiple columns are used for
                partitioning.
                Types: str OR list of Strings (str)
         
            data_order_column:
                Required Argument.
                Specifies Order By columns for data. Values to this argument can
                be provided as list, if multiple columns are used for ordering.
                Types: str OR list of Strings (str)
         
            value_column:
                Required Argument.
                Specifies the name of the input teradataml DataFrame column that
                contains the time series data.
                Types: str OR list of Strings (str)
         
            accumulate:
                Optional Argument.
                Specifies the names of the input teradataml DataFrame columns to
                copy to the output teradataml DataFrame.
                Tip: To identify change points in the output teradataml DataFrame,
                specify the columns that appear in data_partition_column and
                data_order_column.
                Note:
                    'accumulate' argument is required when teradataml is connected to
                    Vantage version prior to 1.1.1.
                Types: str OR list of Strings (str)
         
            segmentation_method:
                Optional Argument.
                Specifies the segmentation method, normal distribution (in each
                segment, the data is in a normal distribution).
                Default Value: normal_distribution
                Permitted Values: normal_distribution
                Types: str
         
            window_size:
                Optional Argument.
                Specifies the size of the sliding window. The ideal window size
                depends heavily on the data. You might need to experiment with
                this value.
                Default Value: 10
                Types: int
         
            threshold:
                Optional Argument.
                A double threshold value. Specifies a float value that the function
                compares to ln(L1) - ln(L0). The definition of Log(L1) and Log(L0)
                are in "Background". They are the logarithms of L1 and L0.
                Default Value: 10.0
                Types: float
         
            output_option:
                Optional Argument.
                Specifies the output teradataml DataFrame columns.
                Default Value: CHANGEPOINT
                Permitted Values: CHANGEPOINT, SEGMENT, VERBOSE
                Types: str
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row
                of the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of ChangePointDetectionRT.
            Output teradataml DataFrames can be accessed using attribute
            references, such as ChangePointDetectionRTObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("changepointdetectionRT", "cpt")
         
            # Provided example table, 'cpt' contains time series data in
            # column 'val', each of which is identified by columns 'sid'
            # and 'id'.
         
            # Create teradataml DataFrame objects.
            cpt = DataFrame.from_table('cpt')
         
            # Example 1 : With default window_size, threshold, output_option
            ChangePointDetectionRT_out = ChangePointDetectionRT(data = cpt,
                                                                value_column = "val",
                                                                data_partition_column = 'sid',
                                                                data_order_column = 'id',
                                                                accumulate = ["sid","id"]
                                                                )
            # Print the results
            print(ChangePointDetectionRT_out.result)
         
            # Example 2 : With window_size 3, threshold 20, VERBOSE output
            ChangePointDetectionRT_out = ChangePointDetectionRT(data = cpt,
                                                                value_column = "val",
                                                                data_partition_column = 'sid',
                                                                data_order_column = 'id',
                                                                accumulate = ["sid","id"],
                                                                window_size = 3,
                                                                threshold = 20.0,
                                                                output_option = "verbose"
                                                                )
            # Print the results
            print(ChangePointDetectionRT_out.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.value_column  = value_column 
        self.accumulate  = accumulate 
        self.segmentation_method  = segmentation_method 
        self.window_size  = window_size
        self.threshold  = threshold 
        self.output_option  = output_option 
        self.data_sequence_column  = data_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["value_column", self.value_column, False, (str)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["segmentation_method", self.segmentation_method, True, (str)])
        self.__arg_info_matrix.append(["window_size", self.window_size, True, (int)])
        self.__arg_info_matrix.append(["threshold", self.threshold, True, (float)])
        self.__arg_info_matrix.append(["output_option", self.output_option, True, (str)])
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
        segmentation_method_permitted_values = ["NORMAL_DISTRIBUTION"]
        self.__awu._validate_permitted_values(self.segmentation_method, segmentation_method_permitted_values, "segmentation_method")
        
        output_option_permitted_values = ["CHANGEPOINT", "SEGMENT", "VERBOSE"]
        self.__awu._validate_permitted_values(self.output_option, output_option_permitted_values, "output_option")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.value_column, "value_column")
        self.__awu._validate_dataframe_has_argument_columns(self.value_column, "value_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        
        # Output table arguments list
        self.__func_output_args_sql_names = []
        self.__func_output_args = []
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("TargetColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.value_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.segmentation_method is not None and self.segmentation_method != "normal_distribution":
            self.__func_other_arg_sql_names.append("SegmentationMethod")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.segmentation_method, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.window_size is not None and self.window_size != 10:
            self.__func_other_arg_sql_names.append("WindowSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.window_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.threshold is not None and self.threshold != 10.0:
            self.__func_other_arg_sql_names.append("ChangePointThreshold")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.threshold, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.output_option is not None and self.output_option != "CHANGEPOINT":
            self.__func_other_arg_sql_names.append("OutputType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_option, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
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
        self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "ChangePointDetectionRT"
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
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False)
        try:
            # Generate the output.
            UtilFuncs._create_view(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.result = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.result)
        
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
        result = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("result", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.result  = result 
        
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
        obj.result = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.result), source_type="table", database_name=UtilFuncs._extract_db_name(obj.result))
        obj._mlresults.append(obj.result)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a ChangePointDetectionRT class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
