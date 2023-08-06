#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# 
# Version: 1.2
# Function Version: 1.15
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

class CoxPH:
    
    def __init__(self,
        data = None,
        feature_columns = None,
        time_interval_column = None,
        event_column = None,
        threshold = 1.0E-9,
        max_iter_num = 10,
        categorical_columns = None,
        accumulate = None,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The CoxPH function is named for the Cox proportional hazards model, a 
            statistical survival model. The function estimates coefficients by 
            learning a set of explanatory variables. The output of the CoxPH 
            function is input to the function CoxHazardRatio and CoxSurvFit.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the 
                input parameters.
            
            feature_columns:
                Required Argument.
                Specifies the names of the input teradataml DataFrame columns that 
                contain the features of the input parameters.
                Types: str OR list of Strings (str)
            
            time_interval_column:
                Required Argument.
                Specifies the name of the column in input_table that contains the 
                time intervals of the input parameters; that is, end_time - 
                start_time, in any unit of time (for example, years, months, or days).
                Types: str
            
            event_column:
                Required Argument.
                Specifies the name of the column in input_table that contains 1 if 
                the event occurred by end_time and 0 if it did not. (0 represents 
                survival or right-censorship.) The function ignores values other than 
                1 and 0.
                Types: str
            
            threshold:
                Optional Argument.
                Specifies the convergence threshold. 
                Default Value: 1.0E-9
                Types: float
            
            max_iter_num:
                Optional Argument.
                Specifies the maximum number of iterations that the function runs 
                before finishing, if the convergence threshold has not been met. 
                Default Value: 10
                Types: int
            
            categorical_columns:
                Optional Argument.
                Specifies the names of the input teradataml DataFrame columns that 
                contain categorical predictors. Each categorical_column must also be 
                a feature_column. By default, the function detects the categorical 
                columns by their SQL data types.
                Types: str OR list of Strings (str)
            
            accumulate:
                Optional Argument.
                Specifies the names of the columns in input_table that the function 
                copies to linear_predictor_table.
                Types: str OR list of Strings (str)
            
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of CoxPH.
            Output teradataml DataFrames can be accessed using attribute
            references, such as CoxPHObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. coefficient_table
                2. linear_predictor_table
                3. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example
            load_example_data("coxph", "lungcancer")
         
            # Create teradataml DataFrame objects.
            lungcancer = DataFrame.from_table("lungcancer")
         
            # Example 1 -
            coxph_out = CoxPH(data = lungcancer,
                             feature_columns = ["trt","celltype","karno","diagtime","age","prior"],
                             time_interval_column = "time_int",
                             event_column = "status",
                             categorical_columns = ["trt","celltype","prior"]
                             )
         
            # Print the results
            print(coxph_out.coefficient_table)
            print(coxph_out.linear_predictor_table)
            print(coxph_out.output)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.feature_columns  = feature_columns 
        self.time_interval_column  = time_interval_column 
        self.event_column  = event_column 
        self.threshold  = threshold 
        self.max_iter_num  = max_iter_num 
        self.categorical_columns  = categorical_columns 
        self.accumulate  = accumulate 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["feature_columns", self.feature_columns, False, (str,list)])
        self.__arg_info_matrix.append(["time_interval_column", self.time_interval_column, False, (str)])
        self.__arg_info_matrix.append(["event_column", self.event_column, False, (str)])
        self.__arg_info_matrix.append(["threshold", self.threshold, True, (float)])
        self.__arg_info_matrix.append(["max_iter_num", self.max_iter_num, True, (int)])
        self.__arg_info_matrix.append(["categorical_columns", self.categorical_columns, True, (str,list)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        
        if inspect.stack()[1][3] != '_from_model_catalog':
            # Perform the function validations
            self.__validate()
            # Generate the ML query
            self.__form_tdml_query()
            # Process output table schema
            self.__process_output_column_info()
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
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.time_interval_column, "time_interval_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_interval_column, "time_interval_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.event_column, "event_column")
        self.__awu._validate_dataframe_has_argument_columns(self.event_column, "event_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.feature_columns, "feature_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.feature_columns, "feature_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.categorical_columns, "categorical_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.categorical_columns, "categorical_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__coefficient_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_coxph0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__linear_predictor_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_coxph1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["CoefficientTable", "LinearPredictorTable"]
        self.__func_output_args = [self.__coefficient_table_temp_tablename, self.__linear_predictor_table_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("TimeIntervalColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.time_interval_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("EventColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.event_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("FeatureColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.feature_columns,"\""),"'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.categorical_columns is not None:
            self.__func_other_arg_sql_names.append("CategoricalColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.categorical_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.max_iter_num is not None and self.max_iter_num != 10:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_iter_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.threshold is not None and self.threshold != 1.0E-9:
            self.__func_other_arg_sql_names.append("StopThreshold")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.threshold, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("inputtable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
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
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("inputtable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "CoxPH"
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
        Function to generate AED nodes for output tables.
        This makes a call aed_ml_query() and then output table dataframes are created.
        """
        # Create a list of input node ids contributing to a query.
        self.__input_nodeids = []
        self.__input_nodeids.append(self.data._nodeid)
        
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__func_output_args.insert(0, sqlmr_stdout_temp_tablename)
        try:
            # Call aed_ml_query and generate AED nodes.
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "CoxPH", self.__aqg_obj._multi_query_input_nodes)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, str(emsg)), MessageCodes.AED_EXEC_FAILED)
        
        
        # Update output table data frames.
        self._mlresults = []
        self.coefficient_table = self.__awu._create_data_set_object(df_input=node_id_list[1], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[1], self.__coefficient_table_column_info))
        self.linear_predictor_table = self.__awu._create_data_set_object(df_input=node_id_list[2], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[2], self.__linear_predictor_table_column_info))
        self.output = self.__awu._create_data_set_object(df_input=node_id_list[0], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[0], self.__stdout_column_info))
        self._mlresults.append(self.coefficient_table)
        self._mlresults.append(self.linear_predictor_table)
        self._mlresults.append(self.output)
        
    def __process_output_column_info(self):
        """ 
        Function to process the output schema for all the ouptut tables.
        This function generates list of column names and column types
        for each generated output tables, which can be used to create metaexpr.
        """
        # Collecting STDOUT output column information.
        stdout_column_info_name = []
        stdout_column_info_type = []
        stdout_column_info_name.append("predictor")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        stdout_column_info_name.append("category")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        stdout_column_info_name.append("coefficient")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        stdout_column_info_name.append("exp_coef")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        stdout_column_info_name.append("std_error")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        stdout_column_info_name.append("z_score")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        stdout_column_info_name.append("p_value")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        stdout_column_info_name.append("significance")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        self.__stdout_column_info = zip(stdout_column_info_name, stdout_column_info_type)
        
        # Collecting coefficient_table output column information.
        coefficient_table_column_info_name = []
        coefficient_table_column_info_type = []
        coefficient_table_column_info_name.append("id")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
        
        coefficient_table_column_info_name.append("predictor")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        coefficient_table_column_info_name.append("category")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        coefficient_table_column_info_name.append("coefficient")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        coefficient_table_column_info_name.append("exp_coef")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        coefficient_table_column_info_name.append("std_error")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        coefficient_table_column_info_name.append("z_score")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        coefficient_table_column_info_name.append("p_value")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        coefficient_table_column_info_name.append("significance")
        coefficient_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        self.__coefficient_table_column_info = zip(coefficient_table_column_info_name, coefficient_table_column_info_type)
        
        # Collecting linear_predictor_table output column information.
        linear_predictor_table_column_info_name = []
        linear_predictor_table_column_info_type = []
        linear_predictor_table_column_info_name.append("linear_predictor")
        linear_predictor_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        linear_predictor_table_column_info_name.append("event")
        linear_predictor_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
        
        linear_predictor_table_column_info_name.append("time_interval")
        linear_predictor_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
        
        if self.accumulate is not None:
            for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.accumulate, columns=None):
                linear_predictor_table_column_info_name.append(column_name)
                linear_predictor_table_column_info_type.append(column_type)
                
        self.__linear_predictor_table_column_info = zip(linear_predictor_table_column_info_name, linear_predictor_table_column_info_type)
        
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
        coefficient_table = None,
        linear_predictor_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("coefficient_table", None)
        kwargs.pop("linear_predictor_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.coefficient_table  = coefficient_table 
        obj.linear_predictor_table  = linear_predictor_table 
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
        obj.coefficient_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.coefficient_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.coefficient_table))
        obj.linear_predictor_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.linear_predictor_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.linear_predictor_table))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.coefficient_table)
        obj._mlresults.append(obj.linear_predictor_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a CoxPH class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ coefficient_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.coefficient_table)
        repr_string="{}\n\n\n############ linear_predictor_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.linear_predictor_table)
        return repr_string
        
