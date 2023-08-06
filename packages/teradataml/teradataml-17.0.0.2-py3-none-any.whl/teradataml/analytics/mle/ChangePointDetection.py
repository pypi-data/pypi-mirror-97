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
# Function Version: 1.6
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
from teradataml.options.configure import configure
from teradataml.options.display import display

class ChangePointDetection:
    
    def __init__(self,
        data = None,
        value_column = None,
        accumulate = None,
        segmentation_method = "normal_distribution",
        search_method = "binary",
        max_change_num = 10,
        penalty = "BIC",
        output_option = "changepoint",
        data_sequence_column = None,
        data_partition_column = None,
        data_order_column = None,
        granularity = 1):
        """
        DESCRIPTION:
            The ChangePointDetection function detects change points in a
            stochastic process or time series, using retrospective change-point
            detection, implemented with these algorithms:
            * Search algorithm: binary search
            * Segmentation algorithm: normal distribution and linear regression
        
        
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the input time
                series data.
         
            data_partition_column:
                Required Argument.
                Specifies Partition By columns for "data".
                Values to this argument can be provided as a list, if multiple 
                columns are used for partition.
                Types: str OR list of Strings (str)
         
            data_order_column:
                Required Argument.
                Specifies Order By columns for "data".
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            value_column:
                Required Argument.
                Specifies the name of the input teradataml DataFrame column
                that contains the time series data.
                Types: str
         
            accumulate:
                Optional Argument. Required when teradataml is connected to
                Vantage 1.0 Maintenance Update 2.
                Specifies the names of the input teradataml DataFrame columns
                to copy to the output table.
                Tip: To identify change points in the output table, specify
                the columns that appear in data_partition_column and
                data_order_column.
                Types: str OR list of Strings (str)
         
            segmentation_method:
                Optional Argument.
                Specifies one of these segmentation methods:
                * normal_distribution : In each segment, the data is in a
                                        normal distribution.
                * linear_regression: In each segment, the data is in linear
                                     regression.
                Default Value: normal_distribution
                Permitted Values: normal_distribution, linear_regression
                Types: str
         
            search_method:
                Optional Argument.
                Specifies the search method, binary segmentation.
                Default Value: binary
                Permitted Values: binary
                Types: str
         
            max_change_num:
                Optional Argument.
                Specifies the maximum number of change points to detect.
                Default Value: 10
                Types: int
         
            penalty:
                Optional Argument.
                Specifies the penalty function, which is used to avoid
                over-fitting.
                Possible values are: BIC , AIC and threshold (a float value).
                * For BIC, the condition for the existence of a change point
                  is: ln(L1) - ln(L0) > (p1 - p0) * ln(n)/2.
                  For normal distribution and linear regression, the condition
                  is: (p1 - p0) * ln(n)/2 = ln(n).
                * For AIC, the condition for the existence of a change point
                  is: ln(L1) - ln(L0) > p1 - p0.
                  For normal distribution and linear regression, the condition
                  is: p1 - p0 = 2.
                * For threshold, the specified value is compared to:
                  ln(L1) - ln(L0).
                L1 and L0 are the maximum likelihood estimation of hypotheses
                H1 and H0. For normal distribution, the definition of
                Log(L1) and Log(L0) are in "Background". 'p' is the number of
                additional parameters introduced by adding a change point. 'p'
                is used in the information criterion BIC or AIC. p1 and p0
                represent this parameter in hypotheses H1 and H0 separately.
                Default Value: BIC
                Types: str
         
            output_option:
                Optional Argument.
                Specifies the output teradataml DataFrame columns.
                Default Value: changepoint
                Permitted Values: changepoint, segment, verbose
                Types: str
            
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each
                row of the input argument "data". The argument is used to
                ensure deterministic results for functions which produce
                results that vary from run to run.
                Types: str OR list of Strings (str)

            granularity:
                Optional Argument.
                Specifies the difference between index of consecutive candidate
                change points.
                Note:
                    "granularity" argument support is only available when teradataml
                    is connected to Vantage 1.3 version.
                Default Value: 1
                Types: int
    
        RETURNS:
            Instance of ChangePointDetection.
            Output teradataml DataFrames can be accessed using attribute
            references, such as ChangePointDetectionObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
        
        
        RAISES:
            TeradataMlException, TypeError, ValueError
        
        
        EXAMPLES:
            #  Load the data to run the example.
            load_example_data('changepointdetection', ['cpt', 'finance_data2'])
         
            # Provided example tables are 'cpt' and 'finance_data2'.
            # These input tables contain time series data like expenditure,
            # income between time periods or power consumption at certain
            # periods or sequence or pulserate etc
         
            # Create teradataml DataFrame objects.
            cpt_table = DataFrame.from_table('cpt')
            print(cpt_table) # Only 10 rows are displayed by default
         
            # Example 1: (Using default parameters)
            cpt_out = ChangePointDetection( data = cpt_table,
                                            data_partition_column = 'sid',
                                            data_order_column = 'id',
                                            value_column = 'val',
                                            accumulate = ['sid','id']
                                            )
            # Print the results
            print(cpt_out.result)
         
            # Example 2: (Using 'VERBOSE' output_option)
            cpt_out = ChangePointDetection( data = cpt_table,
                                            data_partition_column = 'sid',
                                            data_order_column = 'id',
                                            value_column = 'val',
                                            accumulate = ['sid', 'id'],
                                            output_option = 'verbose'
                                            )
            # Print the results
            print(cpt_out.result)
         
            # Example 3: (Using 'AIC' penalty)
            cpt_out = ChangePointDetection( data = cpt_table,
                                            data_partition_column = 'sid',
                                            data_order_column = 'id',
                                            value_column = 'val',
                                            accumulate = ['sid', 'id'],
                                            penalty = 'AIC'
                                            )
            # Print the results
            print(cpt_out.result)
         
            # Example 4: (Using 'threshold' penalty of 20)
            cpt_out = ChangePointDetection( data = cpt_table,
                                            data_partition_column = 'sid',
                                            data_order_column = 'id',
                                            value_column = 'val',
                                            accumulate = ['sid', 'id'],
                                            penalty = '20.0'
                                            )
            # Print the results
            print(cpt_out.result)
         
            # Example 5: (Using 'linear_regression' segmentation_method)
            cpt_out = ChangePointDetection( data = cpt_table,
                                            data_partition_column = 'sid',
                                            data_order_column = 'id',
                                            value_column = 'val',
                                            accumulate = ['sid', 'id'],
                                            segmentation_method = 'linear_regression'
                                            )
            # Print the results
            print(cpt_out.result)
         
            # Example 6 : (Using 'linear_regression' segmentation_method and 'SEGMENT'
            #             output_option)
            cpt_out = ChangePointDetection( data = cpt_table,
                                            data_partition_column = 'sid',
                                            data_order_column = 'id',
                                            value_column = 'val',
                                            accumulate = ['sid', 'id'],
                                            segmentation_method = 'linear_regression',
                                            output_option = 'segment'
                                            )
            # Print the results
            print(cpt_out.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.value_column  = value_column 
        self.accumulate  = accumulate 
        self.segmentation_method  = segmentation_method 
        self.search_method  = search_method 
        self.max_change_num  = max_change_num 
        self.penalty  = penalty 
        self.output_option  = output_option
        self.data_sequence_column  = data_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.data_order_column  = data_order_column
        self.granularity = granularity
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["value_column", self.value_column, False, (str)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, configure._vantage_version!="vantage1.0", (str,list)])
        self.__arg_info_matrix.append(["segmentation_method", self.segmentation_method, True, (str)])
        self.__arg_info_matrix.append(["search_method", self.search_method, True, (str)])
        self.__arg_info_matrix.append(["max_change_num", self.max_change_num, True, (int)])
        self.__arg_info_matrix.append(["penalty", self.penalty, True, (str)])
        self.__arg_info_matrix.append(["output_option", self.output_option, True, (str)])
        self.__arg_info_matrix.append(["granularity", self.granularity, True, (int)])
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
        segmentation_method_permitted_values = ["NORMAL_DISTRIBUTION", "LINEAR_REGRESSION"]
        self.__awu._validate_permitted_values(self.segmentation_method, segmentation_method_permitted_values, "segmentation_method")
        
        search_method_permitted_values = ["BINARY"]
        self.__awu._validate_permitted_values(self.search_method, search_method_permitted_values, "search_method")
        
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
        
        self.__func_other_arg_sql_names.append("ValueColumn")
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
        
        if self.search_method is not None and self.search_method != "binary":
            self.__func_other_arg_sql_names.append("SearchMethod")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.search_method, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.max_change_num is not None and self.max_change_num != 10:
            self.__func_other_arg_sql_names.append("MaxChangeNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_change_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.penalty is not None and self.penalty != "BIC":
            self.__func_other_arg_sql_names.append("Penalty")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.penalty, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.output_option is not None and self.output_option != "changepoint":
            self.__func_other_arg_sql_names.append("OutputOption")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_option, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.granularity is not None and self.granularity != 1:
            self.__func_other_arg_sql_names.append("Granularity")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.granularity, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
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
        
        function_name = "ChangePointDetection"
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
        Returns the string representation for a ChangePointDetection class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
