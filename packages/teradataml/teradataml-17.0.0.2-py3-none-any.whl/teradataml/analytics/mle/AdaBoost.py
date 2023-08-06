#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Rohit Khurd (rohit.khurd@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.31
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

class AdaBoost:
    
    def __init__(self,
        attribute_data = None,
        attribute_name_columns = None,
        attribute_value_column = None,
        categorical_attribute_data = None,
        response_data = None,
        id_columns = None,
        response_column = None,
        iter_num = 20,
        num_splits = 10,
        approx_splits = True,
        split_measure = "gini",
        max_depth = 3,
        min_node_size = 100,
        output_response_probdist = False,
        categorical_encoding = "graycode",
        attribute_data_sequence_column = None,
        response_data_sequence_column = None,
        categorical_attribute_data_sequence_column = None):
        """
        DESCRIPTION:
            The AdaBoost function takes a training data set and a single
            decision tree and uses adaptive boosting to produce a strong classifying model
            that can be input to the function AdaBoostPredict.
         
         
        PARAMETERS:
            attribute_data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the
                attributes and values of the data.
         
            attribute_name_columns:
                Required Argument.
                Specifies the names of attribute teradataml DataFrame columns that
                contain the data attributes.
                Types: str OR list of Strings (str)
         
            attribute_value_column:
                Required Argument.
                Specifies the names of attribute teradataml DataFrame columns that
                contain the data values.
                Types: str
         
            categorical_attribute_data:
                Optional Argument.
                Specifies the name of the teradataml DataFrame that contains the
                names of the categorical attributes.
         
            response_data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the
                responses (labels) of the data.
         
            id_columns:
                Required Argument.
                Specifies the names of the columns in the response and attribute
                teradataml DataFrames that specify the identifier of the instance.
                Types: str OR list of Strings (str)
         
            response_column:
                Required Argument.
                Specifies the name of the response teradataml DataFrame column that
                contains the responses (labels) of the data.
                Types: str
         
            iter_num:
                Optional Argument.
                Specifies the number of iterations to boost the weak classifiers,
                which is also the number of weak classifiers in the ensemble (T). The
                iterations must be an int in the range [2, 200].
                Default Value: 20
                Types: int
         
            num_splits:
                Optional Argument.
                Specifies the number of splits to try for each attribute in the node
                splitting.
                Default Value: 10
                Types: int
         
            approx_splits:
                Optional Argument.
                Specifies whether to use approximate percentiles.
                Default Value: True
                Types: bool
         
            split_measure:
                Optional Argument.
                Specifies the type of measure to use in node splitting.
                Default Value: "gini"
                Permitted Values: GINI, ENTROPY
                Types: str
         
            max_depth:
                Optional Argument.
                Specifies the maximum depth of the tree. The max_depth must be an int in
                the range [1, 10].
                Default Value: 3
                Types: int
         
            min_node_size:
                Optional Argument.
                Specifies the minimum size of any particular node within each
                decision tree.
                Default Value: 100
                Types: int
         
            output_response_probdist:
                Optional Argument.
                Specifies the value for the switch to enable/disable output of
                probability distribution for output labels.
                Default Value: False
                Types: bool
         
            categorical_encoding:
                Optional Argument.
                Specifies which encoding method is used for categorical variables.
                Note: categorical_encoding argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Default Value: "graycode"
                Permitted Values: graycode, hashing
                Types: str
         
            attribute_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "attribute_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            response_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "response_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            categorical_attribute_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "categorical_attribute_data". The argument is used
                to ensure deterministic results for functions which produce results
                that vary from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of AdaBoost.
            Output teradataml DataFrames can be accessed using attribute
            references, such as AdaBoostObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. model_table
                2. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("adaboost", ["housing_train", "housing_cat", "housing_train_response", "iris_attribute_train", "iris_response_train"])
         
            # Create teradataml DataFrame objects.
            housing_train = DataFrame.from_table("housing_train")
            housing_cat = DataFrame.from_table("housing_cat")
            housing_train_response = DataFrame.from_table("housing_train_response")
            iris_attribute_train = DataFrame.from_table("iris_attribute_train")
            iris_response_train = DataFrame.from_table("iris_response_train")
         
            # Example 1 -
            # This example uses home sales data to create a model that predicts home style when input to AdaBoostPredict.
         
            # Input description:
            # housing_train                (attribute_data) : teradataml DataFrame containing real estate sales data.
            #                                                 There are six numerical predictors and six categorical predictors.
            #                                                 The response variable is 'homestyle'.
            # housing_cat      (categorical_attribute_data) : teradataml DataFrame that lists all the categorical predictors.
            # housing_response              (response_data) : teradataml DataFrame that lists the responses for each instance
            #                                                 in 'attribute_data' as specified by 'id_columms'.
         
            # The attribute data (housing_train) needs to have the data in the sparse form where each attribute
            # and its corresponding value are specified in an individual row.
            unpivot_out = Unpivot(data=housing_train,
                                  unpivot = ["price", "lotsize", "bedrooms", "bathrms", "stories","driveway", "recroom", "fullbase", "gashw", "airco", "garagepl", "prefarea"],
                                  accumulate = ["sn"])
         
            AdaBoost_out_1 = AdaBoost(attribute_data = unpivot_out.result,
                                    attribute_name_columns = ["attribute"],
                                    attribute_value_column = "value_col",
                                    categorical_attribute_data = housing_cat,
                                    response_data = housing_train_response,
                                    id_columns = ["sn"],
                                    response_column = "response",
                                    iter_num = 2,
                                    num_splits = 10,
                                    max_depth = 3,
                                    min_node_size = 100
                                    )
         
            # Print the results
            print(AdaBoost_out_1.output)
            print(AdaBoost_out_1.model_table)
         
         
            # Example 2 -
            # This example uses the iris flower dataset to create a model that predicts the species when input to AdaBoostPredict.
         
            # Input description:
            # iris_attribute_train  (attribute_data) : teradataml DataFrame containing the iris flower dataset in the sparse format.
            # iris_response_train    (response_data) : teradataml DataFrame specifying the response variable for each instance
            #                                          in 'attribute_data' as specified by 'id_columms'.
         
            AdaBoost_out_2 = AdaBoost(attribute_data = iris_attribute_train,
                                    attribute_name_columns = ["attribute"],
                                    attribute_value_column = "attrvalue",
                                    response_data = iris_response_train,
                                    id_columns = ["pid"],
                                    response_column = "response",
                                    iter_num = 3,
                                    num_splits = 10,
                                    approx_splits = False,
                                    max_depth = 3,
                                    min_node_size = 5,
                                    output_response_probdist = True
                                    )
         
            # Print the results
            print(AdaBoost_out_2.output)
            print(AdaBoost_out_2.model_table)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.attribute_data  = attribute_data 
        self.attribute_name_columns  = attribute_name_columns 
        self.attribute_value_column  = attribute_value_column 
        self.categorical_attribute_data  = categorical_attribute_data 
        self.response_data  = response_data 
        self.id_columns  = id_columns 
        self.response_column  = response_column 
        self.iter_num  = iter_num 
        self.num_splits  = num_splits 
        self.approx_splits  = approx_splits 
        self.split_measure  = split_measure 
        self.max_depth  = max_depth 
        self.min_node_size  = min_node_size 
        self.output_response_probdist  = output_response_probdist 
        self.categorical_encoding  = categorical_encoding 
        self.attribute_data_sequence_column  = attribute_data_sequence_column 
        self.response_data_sequence_column  = response_data_sequence_column 
        self.categorical_attribute_data_sequence_column  = categorical_attribute_data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["attribute_data", self.attribute_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["attribute_name_columns", self.attribute_name_columns, False, (str,list)])
        self.__arg_info_matrix.append(["attribute_value_column", self.attribute_value_column, False, (str)])
        self.__arg_info_matrix.append(["categorical_attribute_data", self.categorical_attribute_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["response_data", self.response_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["id_columns", self.id_columns, False, (str,list)])
        self.__arg_info_matrix.append(["response_column", self.response_column, False, (str)])
        self.__arg_info_matrix.append(["iter_num", self.iter_num, True, (int)])
        self.__arg_info_matrix.append(["num_splits", self.num_splits, True, (int)])
        self.__arg_info_matrix.append(["approx_splits", self.approx_splits, True, (bool)])
        self.__arg_info_matrix.append(["split_measure", self.split_measure, True, (str)])
        self.__arg_info_matrix.append(["max_depth", self.max_depth, True, (int)])
        self.__arg_info_matrix.append(["min_node_size", self.min_node_size, True, (int)])
        self.__arg_info_matrix.append(["output_response_probdist", self.output_response_probdist, True, (bool)])
        self.__arg_info_matrix.append(["categorical_encoding", self.categorical_encoding, True, (str)])
        self.__arg_info_matrix.append(["attribute_data_sequence_column", self.attribute_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["response_data_sequence_column", self.response_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["categorical_attribute_data_sequence_column", self.categorical_attribute_data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.attribute_data, "attribute_data", None)
        self.__awu._validate_input_table_datatype(self.response_data, "response_data", None)
        self.__awu._validate_input_table_datatype(self.categorical_attribute_data, "categorical_attribute_data", None)
        
        # Check for permitted values
        split_measure_permitted_values = ["GINI", "ENTROPY"]
        self.__awu._validate_permitted_values(self.split_measure, split_measure_permitted_values, "split_measure")
        
        categorical_encoding_permitted_values = ["GRAYCODE", "HASHING"]
        self.__awu._validate_permitted_values(self.categorical_encoding, categorical_encoding_permitted_values, "categorical_encoding")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.id_columns, "id_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.id_columns, "id_columns", self.attribute_data, "attribute_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_name_columns, "attribute_name_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_name_columns, "attribute_name_columns", self.attribute_data, "attribute_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_value_column, "attribute_value_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_value_column, "attribute_value_column", self.attribute_data, "attribute_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.response_column, "response_column")
        self.__awu._validate_dataframe_has_argument_columns(self.response_column, "response_column", self.response_data, "response_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_data_sequence_column, "attribute_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_data_sequence_column, "attribute_data_sequence_column", self.attribute_data, "attribute_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.response_data_sequence_column, "response_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.response_data_sequence_column, "response_data_sequence_column", self.response_data, "response_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.categorical_attribute_data_sequence_column, "categorical_attribute_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.categorical_attribute_data_sequence_column, "categorical_attribute_data_sequence_column", self.categorical_attribute_data, "categorical_attribute_data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__model_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_adaboost0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable"]
        self.__func_output_args = [self.__model_table_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("IdColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.id_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("AttributeNameColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_name_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("AttributeValueColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_value_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("ResponseColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.response_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.iter_num is not None and self.iter_num != 20:
            self.__func_other_arg_sql_names.append("IterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.iter_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.num_splits is not None and self.num_splits != 10:
            self.__func_other_arg_sql_names.append("NumSplits")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.num_splits, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.approx_splits is not None and self.approx_splits != True:
            self.__func_other_arg_sql_names.append("ApproxSplits")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.approx_splits, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.split_measure is not None and self.split_measure != "gini":
            self.__func_other_arg_sql_names.append("SplitMeasure")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.split_measure, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.max_depth is not None and self.max_depth != 3:
            self.__func_other_arg_sql_names.append("maxDepth")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_depth, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.min_node_size is not None and self.min_node_size != 100:
            self.__func_other_arg_sql_names.append("MinNodeSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.min_node_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.output_response_probdist is not None and self.output_response_probdist != False:
            self.__func_other_arg_sql_names.append("OutputResponseProbDist")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_response_probdist, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.categorical_encoding is not None and self.categorical_encoding != "graycode":
            self.__func_other_arg_sql_names.append("CategoricalEncoding")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.categorical_encoding, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.attribute_data_sequence_column is not None:
            sequence_input_by_list.append("AttributeTable:" + UtilFuncs._teradata_collapse_arglist(self.attribute_data_sequence_column, ""))
        
        if self.response_data_sequence_column is not None:
            sequence_input_by_list.append("ResponseTable:" + UtilFuncs._teradata_collapse_arglist(self.response_data_sequence_column, ""))
        
        if self.categorical_attribute_data_sequence_column is not None:
            sequence_input_by_list.append("CategoricalAttributeTable:" + UtilFuncs._teradata_collapse_arglist(self.categorical_attribute_data_sequence_column, ""))
        
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
        
        # Process attribute_data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.attribute_data, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("AttributeTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        # Process response_data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.response_data, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("ResponseTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        # Process categorical_attribute_data
        if self.categorical_attribute_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.categorical_attribute_data, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("CategoricalAttributeTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "AdaBoost"
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
        self.model_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__model_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__model_table_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.model_table)
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
        model_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("model_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.model_table  = model_table 
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
        obj.model_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.model_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.model_table))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.model_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a AdaBoost class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ model_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.model_table)
        return repr_string
        
