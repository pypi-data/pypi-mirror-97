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
# Function Version: 2.30
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
from teradataml.common.formula import Formula

class DecisionForest:
    
    def __init__(self,
        formula = None,
        data = None,
        maxnum_categorical = 1000,
        tree_type = None,
        ntree = None,
        tree_size = None,
        nodesize = 1,
        variance = 0.0,
        max_depth = 12,
        mtry = None,
        mtry_seed = None,
        seed = None,
        outofbag = False,
        display_num_processed_rows = False,
        categorical_encoding = "graycode",
        data_sequence_column = None,
        id_column = None):
        """
        DESCRIPTION:
            The DecisionForest function uses a training data set to generate a
            predictive model. You can input the model to the DecisionForestPredict
            function, which uses it to make predictions.
        
        
        PARAMETERS:
            formula:
                Required Argument.
                A string consisting of "formula". Specifies the model to be fitted. Only
                basic formula of the "col1 ~ col2 + col3 +..." form is supported and
                all variables must be from the same virtual data frame object. The
                response should be column of type real, numeric, integer or boolean.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the input data set.

            maxnum_categorical:
                Optional Argument.
                Specifies the maximum number of distinct values for a single
                categorical variable. The maxnum_categorical must be a positive int.
                Default Value: 1000
                Types: int

            tree_type:
                Optional Argument.
                Specifies whether the analysis is a regression (continuous response
                variable) or a multiclass classification (predicting result from the
                number of classes). The default value is "regression", if the response
                variable is numeric and "classification", if the response variable is
                non-numeric.
                Types: str

            ntree:
                Optional Argument.
                Specifies the number of trees to grow in the forest model. When
                specified, number of trees must be greater than or equal to the
                number of vworkers. When not specified, the function builds the
                minimum number of trees that provides the input dataset with full
                coverage.
                Types: int

            tree_size:
                Optional Argument.
                Specifies the number of rows that each tree uses as its input data
                set. If not specified, the function builds a tree using either the
                number of rows on a vworker or the number of rows that fits into the
                vworker's memory, whichever is less.
                Types: int

            nodesize:
                Optional Argument.
                Specifies a decision tree stopping criterion, the minimum size of any
                node within each decision tree.
                Default Value: 1
                Types: int

            variance:
                Optional Argument.
                Specifies a decision tree stopping criterion. If the variance within
                any node dips below this value, the algorithm stops looking for splits
                in the branch.
                Default Value: 0.0
                Types: float

            max_depth:
                Optional Argument.
                Specifies a decision tree stopping criterion. If the tree reaches a
                depth past this value, the algorithm stops looking for splits.
                Decision trees can grow to (2(max_depth+1) - 1) nodes. This stopping
                criteria has the greatest effect on the performance of the function.
                Default Value: 12
                Types: int

            mtry:
                Optional Argument.
                Specifies the number of variables to randomly sample from each
                input value. For example, if mtry is 3, then the function randomly
                samples 3 variables from each input at each split. The mtry must be an
                int.
                Types: int

            mtry_seed:
                Optional Argument.
                Specifies a int value to use in determining the random seed for mtry.
                Types: int

            seed:
                Optional Argument.
                Specifies a int value to use in determining the seed for the random
                number generator. If you specify this value, you can specify the same
                value in future calls to this function and the function will build
                the same tree.
                Types: int

            outofbag:
                Optional Argument.
                Specifies whether to output the out-of-bag estimate of error rate.
                Default Value: False
                Types: bool

            display_num_processed_rows:
                Optional Argument.
                Specifies whether to display the number of processed rows of "data".
                Default Value: False
                Types: bool

            categorical_encoding:
                Optional Argument.
                Specifies which encoding method is used for categorical variables.
                Note: "categorical_encoding" argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Default Value: "graycode"
                Permitted Values: graycode, hashing
                Types: str
        
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            id_column:
                Optional Argument. Required when "outofbag" is set to 'True'.
                Specifies the name of the column in "data" that contains the row
                identifier.
                Note:
                    "id_column" argument support is only available when teradataml
                    is connected to Vantage 1.3 or later.
                Types: str
        
        RETURNS:
            Instance of DecisionForest.
            Output teradataml DataFrames can be accessed using attribute
            references, such as DecisionForestObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. predictive_model
                2. monitor_table
                3. output
        
        
        RAISES:
            TeradataMlException
        
        
        EXAMPLES:
            # Load the data to run the example
            load_example_data("decisionforest", ["housing_train", "boston"])

            # Create teradataml DataFrame.
            housing_train = DataFrame.from_table("housing_train")
            boston = DataFrame.from_table("boston")

            # Example 1 -
            decision_forest_out1 = DecisionForest(formula = "homestyle ~ bedrooms + lotsize + gashw + driveway + stories + recroom + price + garagepl + bathrms + fullbase + airco + prefarea",
                                                  data = housing_train,
                                                  tree_type = "classification",
                                                  ntree = 50,
                                                  nodesize = 1,
                                                  variance = 0.0,
                                                  max_depth = 12,
                                                  mtry = 3,
                                                  mtry_seed = 100,
                                                  seed = 100)

            # Print output dataframes
            print(decision_forest_out1.output)
            print(decision_forest_out1.predictive_model)
            print(decision_forest_out1.monitor_table)

            # Example 2 -
            decision_forest_out2 = DecisionForest(formula = "homestyle ~ bedrooms + lotsize + gashw + driveway + stories + recroom + price + garagepl + bathrms + fullbase + airco + prefarea",
                                                  data = housing_train,
                                                  tree_type = "classification",
                                                  ntree = 50,
                                                  nodesize = 2,
                                                  max_depth = 12,
                                                  mtry = 3,
                                                  outofbag = True)

            # Print all output dataframes.
            print(decision_forest_out2.output)
            print(decision_forest_out2.predictive_model)
            print(decision_forest_out2.monitor_table)

            # Example 3 -
            decision_forest_out3 = DecisionForest(formula = "medv ~ indus + ptratio + lstat + black + tax + dis + zn + rad + nox + chas + rm + crim + age",
                                                  data = boston,
                                                  tree_type = "regression",
                                                  ntree = 50,
                                                  nodesize = 2,
                                                  max_depth = 6,
                                                  outofbag = True)

            # Print all output dataframes.
            print(decision_forest_out3.output)
            print(decision_forest_out3.predictive_model)
            print(decision_forest_out3.monitor_table)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.formula  = formula 
        self.data  = data 
        self.maxnum_categorical  = maxnum_categorical 
        self.tree_type  = tree_type 
        self.ntree  = ntree 
        self.tree_size  = tree_size 
        self.nodesize  = nodesize 
        self.variance  = variance 
        self.max_depth  = max_depth 
        self.mtry  = mtry 
        self.mtry_seed  = mtry_seed 
        self.seed  = seed 
        self.outofbag  = outofbag 
        self.display_num_processed_rows  = display_num_processed_rows 
        self.categorical_encoding  = categorical_encoding 
        self.id_column  = id_column 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["formula", self.formula, False, "formula"])
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["maxnum_categorical", self.maxnum_categorical, True, (int)])
        self.__arg_info_matrix.append(["tree_type", self.tree_type, True, (str)])
        self.__arg_info_matrix.append(["ntree", self.ntree, True, (int)])
        self.__arg_info_matrix.append(["tree_size", self.tree_size, True, (int)])
        self.__arg_info_matrix.append(["nodesize", self.nodesize, True, (int)])
        self.__arg_info_matrix.append(["variance", self.variance, True, (float)])
        self.__arg_info_matrix.append(["max_depth", self.max_depth, True, (int)])
        self.__arg_info_matrix.append(["mtry", self.mtry, True, (int)])
        self.__arg_info_matrix.append(["mtry_seed", self.mtry_seed, True, (int)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["outofbag", self.outofbag, True, (bool)])
        self.__arg_info_matrix.append(["display_num_processed_rows", self.display_num_processed_rows, True, (bool)])
        self.__arg_info_matrix.append(["categorical_encoding", self.categorical_encoding, True, (str)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["id_column", self.id_column, True, (str)])
        
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
            self._prediction_type = self.__awu._get_function_prediction_type(self, self.data)
        
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
        categorical_encoding_permitted_values = ["GRAYCODE", "HASHING"]
        self.__awu._validate_permitted_values(self.categorical_encoding, categorical_encoding_permitted_values, "categorical_encoding")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.id_column, "id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.id_column, "id_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__predictive_model_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_decisionforest0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__monitor_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_decisionforest1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable", "MonitorTable"]
        self.__func_output_args = [self.__predictive_model_temp_tablename, self.__monitor_table_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        if self.id_column is not None:
            self.__func_other_arg_sql_names.append("IdColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.id_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.tree_type is not None:
            self.__func_other_arg_sql_names.append("TreeType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.tree_type, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.ntree is not None:
            self.__func_other_arg_sql_names.append("NumTrees")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.ntree, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.tree_size is not None:
            self.__func_other_arg_sql_names.append("TreeSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.tree_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.nodesize is not None and self.nodesize != 1:
            self.__func_other_arg_sql_names.append("MinNodeSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.nodesize, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.variance is not None and self.variance != 0:
            self.__func_other_arg_sql_names.append("Variance")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.variance, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.max_depth is not None and self.max_depth != 12:
            self.__func_other_arg_sql_names.append("MaxDepth")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_depth, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.maxnum_categorical is not None:
            self.__func_other_arg_sql_names.append("MaxNumCategoricalValues")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.maxnum_categorical, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.display_num_processed_rows is not None and self.display_num_processed_rows != False:
            self.__func_other_arg_sql_names.append("DisplayNumProcessedRows")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.display_num_processed_rows, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.mtry is not None:
            self.__func_other_arg_sql_names.append("Mtry")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mtry, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.mtry_seed is not None:
            self.__func_other_arg_sql_names.append("MtrySeed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mtry_seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        if self.seed is not None:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        if self.outofbag is not None and self.outofbag != False:
            self.__func_other_arg_sql_names.append("OutOfBag")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.outofbag, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.categorical_encoding is not None and self.categorical_encoding != "graycode":
            self.__func_other_arg_sql_names.append("CategoricalEncoding")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.categorical_encoding, "'"))
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
        
        # Let's process formula argument
        self.formula = self.__awu._validate_formula_notation(self.formula, self.data, "formula")
        # response variable
        __response_column = self.formula._get_dependent_vars()
        self._target_column = __response_column
        self.__func_other_arg_sql_names.append("ResponseColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__response_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        self._sql_specific_attributes["ResponseColumn"] = __response_column
        self._sql_formula_attribute_mapper["ResponseColumn"] = "__response_column"
        
        # numerical input columns
        __numeric_columns = self.__awu._get_columns_by_type(self.formula, self.data, "numerical")
        if len(__numeric_columns) > 0:
            self.__func_other_arg_sql_names.append("NumericInputs")
            numerical_columns_list = UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__numeric_columns, "\""), "'")
            self.__func_other_args.append(numerical_columns_list)
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
            self._sql_specific_attributes["NumericInputs"] = numerical_columns_list
            self._sql_formula_attribute_mapper["NumericInputs"] = "__numeric_columns"
        
        # categorical input columns
        __categorical_columns = self.__awu._get_columns_by_type(self.formula, self.data, "categorical")
        if len(__categorical_columns) > 0:
            self.__func_other_arg_sql_names.append("CategoricalInputs")
            categorical_columns_list = UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__categorical_columns, "\""), "'")
            self.__func_other_args.append(categorical_columns_list)
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
            self._sql_specific_attributes["CategoricalInputs"] = categorical_columns_list
            self._sql_formula_attribute_mapper["CategoricalInputs"] = "__categorical_columns"
        
        
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
        self.__func_input_arg_sql_names.append("InputTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "DecisionForest"
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
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "DecisionForest", self.__aqg_obj._multi_query_input_nodes)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, str(emsg)), MessageCodes.AED_EXEC_FAILED)
        
        
        # Update output table data frames.
        self._mlresults = []
        self.predictive_model = self.__awu._create_data_set_object(df_input=node_id_list[1], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[1], self.__predictive_model_column_info))
        self.monitor_table = self.__awu._create_data_set_object(df_input=node_id_list[2], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[2], self.__monitor_table_column_info))
        self.output = self.__awu._create_data_set_object(df_input=node_id_list[0], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[0], self.__stdout_column_info))
        self._mlresults.append(self.predictive_model)
        self._mlresults.append(self.monitor_table)
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
        stdout_column_info_name.append("message")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        self.__stdout_column_info = zip(stdout_column_info_name, stdout_column_info_type)
        
        # Collecting predictive_model output column information.
        predictive_model_column_info_name = []
        predictive_model_column_info_type = []
        predictive_model_column_info_name.append("worker_ip")
        predictive_model_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        predictive_model_column_info_name.append("task_index")
        predictive_model_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
        
        predictive_model_column_info_name.append("tree_num")
        predictive_model_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
        
        predictive_model_column_info_name.append("tree")
        predictive_model_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("clob"))
        
        if self.display_num_processed_rows:
            predictive_model_column_info_name.append("num_processed_rows")
            predictive_model_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
            predictive_model_column_info_name.append("num_total_rows")
            predictive_model_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
            
        
        self.__predictive_model_column_info = zip(predictive_model_column_info_name, predictive_model_column_info_type)
        
        # Collecting monitor_table output column information.
        monitor_table_column_info_name = []
        monitor_table_column_info_type = []
        monitor_table_column_info_name.append("message")
        monitor_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        self.__monitor_table_column_info = zip(monitor_table_column_info_name, monitor_table_column_info_type)
        
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
        predictive_model = None,
        monitor_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("predictive_model", None)
        kwargs.pop("monitor_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Initialize the formula attributes.
        __response_column = kwargs.pop("__response_column", None)
        __all_columns = kwargs.pop("__all_columns", None)
        __numeric_columns = kwargs.pop("__numeric_columns", None)
        __categorical_columns = kwargs.pop("__categorical_columns", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.predictive_model  = predictive_model 
        obj.monitor_table  = monitor_table 
        obj.output  = output 
        
        # Initialize the sqlmr_query class attribute.
        obj.sqlmr_query = None
        
        # Initialize the SQL specific Model Cataloging attributes.
        obj._sql_specific_attributes = None
        obj._target_column = target_column
        obj._prediction_type = prediction_type
        obj._algorithm_name = algorithm_name
        obj._build_time = build_time
        
        # Initialize the formula.
        if obj.formula is not None:
            obj.formula = Formula._from_formula_attr(obj.formula,
                                                     __response_column,
                                                     __all_columns,
                                                     __categorical_columns,
                                                     __numeric_columns)
        
        # Update output table data frames.
        obj._mlresults = []
        obj.predictive_model = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.predictive_model), source_type="table", database_name=UtilFuncs._extract_db_name(obj.predictive_model))
        obj.monitor_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.monitor_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.monitor_table))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.predictive_model)
        obj._mlresults.append(obj.monitor_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a DecisionForest class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ predictive_model Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.predictive_model)
        repr_string="{}\n\n\n############ monitor_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.monitor_table)
        return repr_string

