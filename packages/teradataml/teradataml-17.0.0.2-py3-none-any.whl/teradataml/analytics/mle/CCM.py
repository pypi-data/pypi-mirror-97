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
from teradataml.options.display import display

class CCM:
    
    def __init__(self,
        data = None,
        sequence_id_column = None,
        time_column = None,
        cause_columns = None,
        effect_columns = None,
        library_size = [100],
        embedding_dimension = [2],
        time_step = 1,
        bootstrap_iterations = 100,
        predict_step = 1,
        self_predict = False,
        seed = None,
        point_select_rule = "DistanceOnly",
        mode = "Single",
        data_sequence_column = None):
        """
        DESCRIPTION:
            The CCM function takes two or more time series as input and evaluates
            potential cause-effect relationships between them. Each time series
            column can be a single, long time series or a set of shorter
            subsequences that represent the same process. The function returns an
            effect size for each cause-effect pair.
         
         
        PARAMETERS:
            data:
                Required Argument.
                teradataml DataFrame containing the input data.
         
            sequence_id_column:
                Required Argument.
                Specifies column containing the sequence ids. A sequence is a sample of the
                time series.
                Types: str OR list of Strings (str)
         
            time_column:
                Required Argument.
                Specifies column containing the timestamps.
                Types: str OR list of Strings (str)
         
            cause_columns:
                Required Argument.
                Specifies column to be evaluated as potential causes.
                Types: str OR list of Strings (str)
         
            effect_columns:
                Required Argument.
                Specifies column to be evaluated as potential effects.
                Types: str OR list of Strings (str)
         
            library_size:
                Optional Argument.
                The CCM algorithm works by using "libraries" of randomly selected
                points along the potential effect time series to predict values of
                the cause time series. A causal relationship is said to exist if the
                correlation between the predicted values of the cause time series and
                the actual values increases as the size of the library increases.
                Each input value must be greater than 0.
                Default Value: [100]
                Types: int
         
            embedding_dimension:
                Optional Argument.
                The embedding dimension is an estimate of the number of past values
                to use when predicting a given value of the time series. The input
                value must be greater than 0.
                Default Value: [2]
                Types: int
         
            time_step:
                Optional Argument.
                The time_step parameter indicates the number of time steps between
                past values to use when predicting a given value of the time series.
                The input value must be greater than 0.
                Default Value: 1
                Types: int
         
            bootstrap_iterations:
                Optional Argument.
                The number of bootstrap iterations used to predict. The bootstrap
                process is used to estimate the uncertainty associated with the
                predicted values. The input value must be greater than 0.
                Default Value: 100
                Types: int
         
            predict_step:
                Optional Argument.
                If the best embedding dimension is needed to choose, the predict
                step is used for specify the number of time steps into the
                future to make predictions from past observations.
                Default Value: 1
                Types: int
         
            self_predict:
                Optional Argument.
                If self_predict is set to true, the CCM function will attempt to
                predict each attribute using the attribute itself. If an attribute
                can predict its own time series well, the signal-to-noise ratio is
                too low for the CCM algorithm to work effectively.
                Default Value: False
                Types: bool
         
            seed:
                Optional Argument.
                Specifies the random seed used to initialize the algorithm.
                Types: int
         
            point_select_rule:
                Optional Argument.
                The rules to select nearest points if the best embedding dimension
                is needed to choose. Two options are provided. One is
                DistanceAndTime. The other one is DistanceOnly.
                Default Value: "DistanceOnly"
                Permitted Values: DistanceAndTime, DistanceOnly
                Types: str
         
            mode:
                Optional Argument.
                Specifies the execution mode. CCM can be executed in single mode and
                distribute node.
                Default Value: "Single"
                Permitted Values: Single, Distribute
                Types: str
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of CCM.
            Output teradataml DataFrames can be accessed using attribute
            references, such as CCMObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("CCM", ["ccmexample", "ccm_input", "ccm_input2", "ccmprepare_input"])
         
            # Create teradataml DataFrame objects.
            ccmexample = DataFrame.from_table("ccmexample")
            ccm_input = DataFrame.from_table("ccm_input")
            ccm_input2 = DataFrame.from_table("ccm_input2")
            ccmprepare_input = DataFrame.from_table("ccmprepare_input")
         
            # Example 1 -  Identify the optimal value for embedding_dimension.
            # In this call, the cause_columns and effect_columns arguments must
            # have the same value, the argument self_predict must have the value
            # 'true', and the library_size argument must be omitted.
            ccm_out1 = CCM(data = ccmexample,
                          sequence_id_column = "seqid",
                          time_column = "t",
                          cause_columns = ["b"],
                          effect_columns = ["b"],
                          embedding_dimension = [2,3,4,5,6,7,8,9,10],
                          self_predict = True
                          )
         
            # Print the result teradataml DataFrame
            print(ccm_out1)
         
            # Example 2 - Check for a causal relationship between the two time
            # series. This call uses the optimal value for embedding_dimension
            # identified in Example 1.
            ccm_out2 = CCM(data = ccmexample,
                          sequence_id_column = "seqid",
                          time_column = "t",
                          cause_columns = ["a","b"],
                          effect_columns = ["a","b"],
                          embedding_dimension = 2
                          )
         
            # Print the result teradataml DataFrame
            print(ccm_out2.result)
         
            # Example 3 - Find causal-effect relationship between income,
            # expenditure and investiment fields.
            ccm_out3 = CCM(data = ccm_input,
                           sequence_id_column = 'id',
                           time_column = 'period',
                           cause_columns = ['income'],
                           effect_columns = ['expenditure','investment'],
                           seed = 0
                           )
         
            # Print the result teradataml DataFrame
            print(ccm_out3)
         
            # Example 4 - Another example to find the cause-effect relation on
            # a sample market time series data.
            ccm_out4 = CCM(data = ccm_input2,
                           sequence_id_column = 'id',
                           time_column = 'period',
                           cause_columns = ['marketindex','indexval'],
                           effect_columns = ['indexdate','indexchange'],
                           library_size = 10,
                           seed = 0
                           )
         
            # Print the result teradataml DataFrame
            print(ccm_out4.result)
         
            # Example 5 - Alternatively, the below example produces the same
            # output as above by making use of CCMPrepare and then using
            # its output object for CCM.
            ccmprepare_out = CCMPrepare(data=ccmprepare_input,
                                data_partition_column='id'
                                )
         
            ccm_out5 = CCM(data = ccmprepare_out.result,
                           sequence_id_column = 'id',
                           time_column = 'period',
                           cause_columns = 'income',
                           effect_columns = ["expenditure","investment"],
                           seed = 0
                           )
            print(ccm_out5)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.sequence_id_column  = sequence_id_column 
        self.time_column  = time_column 
        self.cause_columns  = cause_columns 
        self.effect_columns  = effect_columns 
        self.library_size  = library_size 
        self.embedding_dimension  = embedding_dimension 
        self.time_step  = time_step 
        self.bootstrap_iterations  = bootstrap_iterations 
        self.predict_step  = predict_step 
        self.self_predict  = self_predict 
        self.seed  = seed 
        self.point_select_rule  = point_select_rule 
        self.mode  = mode 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["sequence_id_column", self.sequence_id_column, False, (str)])
        self.__arg_info_matrix.append(["time_column", self.time_column, False, (str)])
        self.__arg_info_matrix.append(["cause_columns", self.cause_columns, False, (str,list)])
        self.__arg_info_matrix.append(["effect_columns", self.effect_columns, False, (str,list)])
        self.__arg_info_matrix.append(["library_size", self.library_size, True, (int,list)])
        self.__arg_info_matrix.append(["embedding_dimension", self.embedding_dimension, True, (int,list)])
        self.__arg_info_matrix.append(["time_step", self.time_step, True, (int)])
        self.__arg_info_matrix.append(["bootstrap_iterations", self.bootstrap_iterations, True, (int)])
        self.__arg_info_matrix.append(["predict_step", self.predict_step, True, (int)])
        self.__arg_info_matrix.append(["self_predict", self.self_predict, True, (bool)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["point_select_rule", self.point_select_rule, True, (str)])
        self.__arg_info_matrix.append(["mode", self.mode, True, (str)])
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
        point_select_rule_permitted_values = ["DISTANCEANDTIME", "DISTANCEONLY"]
        self.__awu._validate_permitted_values(self.point_select_rule, point_select_rule_permitted_values, "point_select_rule")
        
        mode_permitted_values = ["SINGLE", "DISTRIBUTE"]
        self.__awu._validate_permitted_values(self.mode, mode_permitted_values, "mode")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.sequence_id_column, "sequence_id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.sequence_id_column, "sequence_id_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.time_column, "time_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_column, "time_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.cause_columns, "cause_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.cause_columns, "cause_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.effect_columns, "effect_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.effect_columns, "effect_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("SequenceIdColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.sequence_id_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("TimeColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.time_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("CauseColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.cause_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("EffectColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.effect_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.library_size is not None and self.library_size != [100]:
            self.__func_other_arg_sql_names.append("LibrarySize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.library_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.embedding_dimension is not None and self.embedding_dimension != [2]:
            self.__func_other_arg_sql_names.append("EmbeddingDimensions")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.embedding_dimension, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.time_step is not None and self.time_step != 1:
            self.__func_other_arg_sql_names.append("TimeStep")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.time_step, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.bootstrap_iterations is not None and self.bootstrap_iterations != 100:
            self.__func_other_arg_sql_names.append("BootstrapIterations")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.bootstrap_iterations, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.predict_step is not None and self.predict_step != 1:
            self.__func_other_arg_sql_names.append("PredictStep")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.predict_step, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.self_predict is not None and self.self_predict != False:
            self.__func_other_arg_sql_names.append("SelfPredict")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.self_predict, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.point_select_rule is not None and self.point_select_rule != "DistanceOnly":
            self.__func_other_arg_sql_names.append("PointSelectRule")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.point_select_rule, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.mode is not None and self.mode != "Single":
            self.__func_other_arg_sql_names.append("ExecutionMode")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mode, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.seed is not None:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
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
        
        function_name = "CCM"
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
        Returns the string representation for a CCM class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
