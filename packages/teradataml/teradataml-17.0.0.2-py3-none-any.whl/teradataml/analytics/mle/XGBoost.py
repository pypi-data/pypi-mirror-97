#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: PavansaiKumar Alladi (pavansaikumar.alladi@teradata.com)
# 
# Version: 1.2
# Function Version: 2.26
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

class XGBoost:
    
    def __init__(self,
        formula = None,
        data = None,
        id_column = None,
        loss_function = "SOFTMAX",
        prediction_type = "CLASSIFICATION",
        reg_lambda = 1.0,
        shrinkage_factor = 0.1,
        iter_num = 10,
        min_node_size = 1,
        max_depth = 5,
        variance = 0.0,
        seed = None,
        attribute_name_column = None,
        num_boosted_trees = None,
        attribute_table = None,
        attribute_value_column = None,
        column_subsampling = 1.0,
        response_column = None,
        data_sequence_column = None,
        attribute_table_sequence_column = None,
        output_accuracy = False):
        """
        DESCRIPTION:
            The XGBoost function takes a training data set and uses gradient 
            boosting to create a strong classifying model that can be input to 
            the function XGBoostPredict. The function supports input tables in 
            both dense and sparse format.
         
         
        PARAMETERS:
            formula:
                Required Argument when input data is in dense format.
                A string consisting of "formula". Specifies the model to be fitted.
                Only basic formula of the "col1 ~ col2 + col3 +..." form are
                supported and all variables must be from the same teradataml
                DataFrame object. The response should be column of type float, int or
                bool. This argument is not supported for sparse format. For sparse data
                format, provide this information using "attribute_table" argument.
         
            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the input data set.
                If the input data set is in dense format, the XGBoost function requires only "data".
         
            id_column:
                Optional Argument.
                Specifies the name of the partitioning column of input table. This
                column is used as a row identifier to distribute data among different
                vworkers for parallel boosted trees.
                Types: str OR list of Strings (str)
         
            loss_function:
                Optional Argument.
                Specifies the learning task and corresponding learning objective.
                Default Value: "SOFTMAX"
                Permitted Values: BINOMIAL, SOFTMAX, MSE
                Note:
                    Permitted value 'MSE' is supported when teradataml is connected to Vantage1.3
                    or later versions.
                Types: str
         
            prediction_type:
                Optional Argument.
                Specifies whether the function predicts the result from the number of classes
                ('classification') or from a continuous response variable ('regression').
                The function supports only 'classification'.
                Default Value: "CLASSIFICATION"
                Permitted Values: CLASSIFICATION, REGRESSION
                Note:
                    Permitted value 'REGRESSION' is supported when teradataml is connected to Vantage1.3
                    or later versions.
                Types: str
         
            reg_lambda:
                Optional Argument.
                Specifies the L2 regularization that the loss function uses
                while boosting trees. The higher the lambda, the stronger the
                regularization effect.
                Default Value: 1.0
                Types: float
         
            shrinkage_factor:
                Optional Argument.
                Specifies the learning rate (weight) of a learned tree in each boosting step.
                After each boosting step, the algorithm multiplies the learner by shrinkage
                to make the boosting process more conservative. The shrinkage is a
                float value in the range [0.0, 1.0].
                The value 1.0 specifies no shrinkage.
                Default Value: 0.1
                Types: float
         
            iter_num:
                Optional Argument.
                Specifies the number of iterations to boost the weak classifiers,
                which is also the number of weak classifiers in the ensemble (T). The
                number must an int in the range [1, 100000].
                Default Value: 10
                Types: int
         
            min_node_size:
                Optional Argument.
                Specifies the minimum size of any particular node within each
                decision tree. The min_node_size must an int.
                Default Value: 1
                Types: int
         
            max_depth:
                Optional Argument.
                Specifies the maximum depth of the tree. The max_depth must be an int in
                the range [1, 100000].
                Default Value: 5
                Types: int
         
            variance:
                Optional Argument.
                Specifies a decision tree stopping criterion. If the variance within
                any node dips below this value, the algorithm stops looking for splits
                in the branch.
                Default Value: 0.0
                Types: float
         
            seed:
                Optional Argument.
                Specifies the seed to use to create a random number.
                If you omit this argument or specify its default value 1, the function
                uses a faster algorithm but does not ensure repeatability.
                This argument must have a int value greater than or equal to 1. To ensure
                repeatability, specify a value greater than 1.
                Types: int
         
            attribute_name_column:
                Optional Argument.
                Required for sparse data format. If the data set is in sparse format,
                this argument indicates the column containing the attributes in the
                input data set.
                Types: str OR list of Strings (str)
         
            num_boosted_trees:
                Optional Argument.
                Specifies the number of boosted trees to be trained. By default, the
                number of boosted trees equals the number of vworkers available for
                the functions.
                Types: int
         
            attribute_table:
                Optional Argument.
                Required if the input data set is in sparse format.
                Specifies the name of the teradataml DataFrame containing the features in the input
                data.
         
            attribute_value_column:
                Optional Argument.
                Required if the input data set is in sparse format.
                If the data is in the sparse format, this argument indicates the
                column containing the attribute values in the input table.
                Types: str OR list of Strings (str)
         
            column_subsampling:
                Optional Argument.
                Specifies the fraction of features to subsample during boosting.
                Default Value: 1.0 (no subsampling)
                Types: float
         
            response_column:
                Optional Argument.
                Specifies the name of the response teradataml DataFrame column that
                contains the responses (labels) of the data.
                Types: str OR list of Strings (str)
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            attribute_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "attribute_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            output_accuracy:
                Optional Argument.
                Specifies whether to show training accuracy over iterations in the
                output model_table DataFrame.
                Note:
                    The argument 'output_accuracy' is available when teradataml is connected to Vantage 1.3
                    or later versions.
                Default Value: False
                Types: bool
         
        RETURNS:
            Instance of XGBoost.
            Output teradataml DataFrames can be accessed using attribute
            references, such as XGBoostObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                1. model_table
                2. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("xgboost", ["housing_train_binary","iris_train","sparse_iris_train","sparse_iris_attribute"])
         
            # Example 1: Binary Classification on the housing data to build a model using training data
            # that contains couple of labels (Responses) - classic and eclectic, specifying the style of a house,
            # based on the 12 other attributes of the house, such as bedrooms, stories, price etc.
            # Create teradataml DataFrame objects.
            housing_train_binary = DataFrame.from_table("housing_train_binary")
            XGBoost_out1 = XGBoost(data=housing_train_binary,
                                id_column='sn',
                                formula = "homestyle ~ driveway + recroom + fullbase + gashw + airco + prefarea + price + lotsize + bedrooms + bathrms + stories + garagepl",
                                num_boosted_trees=2,
                                loss_function='binomial',
                                prediction_type='classification',
                                reg_lambda=1.0,
                                shrinkage_factor=0.1,
                                iter_num=10,
                                min_node_size=1,
                                max_depth=10
                                )
         
            # Print the results.
            print(XGBoost_out1)
         
         
            # Example 2: Multiple-Class Classification
            # Let's use the XGBoost classification algorithm, on one of the famous dataset Iris Data set.
            # Dataset contains 50 samples from three species of Iris flower setosa, virginica and versicolor.
            # Each data point contains measurements of length and width of sepals and petals.
            iris_train = DataFrame.from_table("iris_train")
         
            XGBoost_out2 = XGBoost(data=iris_train,
                                  id_column='id',
                                  formula = "species ~ sepal_length + petal_length + petal_width + species",
                                  num_boosted_trees=2,
                                  loss_function='softmax',
                                  reg_lambda=1.0,
                                  shrinkage_factor=0.1,
                                  iter_num=10,
                                  min_node_size=1,
                                  max_depth=10)
         
            # Print the results.
            print(XGBoost_out2)
         
         
            # Example 3: Sparse Input Format. response_column argument is specified instead of formula.
            sparse_iris_train = DataFrame.from_table("sparse_iris_train")
            sparse_iris_attribute = DataFrame.from_table("sparse_iris_attribute")
         
            XGBoost_out3 = XGBoost(data=sparse_iris_train,
                                   attribute_table=sparse_iris_attribute,
                                   id_column='id',
                                   attribute_name_column='attribute',
                                   attribute_value_column='value_col',
                                   response_column="species",
                                   loss_function='SOFTMAX',
                                   reg_lambda=1.0,
                                   num_boosted_trees=2,
                                   shrinkage_factor=0.1,
                                   column_subsampling=1.0,
                                   iter_num=10,
                                   min_node_size=1,
                                   max_depth=10,
                                   variance=0.0,
                                   seed=1
                                   )
         
            # Print the results.
            print(XGBoost_out3)


            # Example 4: Use optional argument 'output_accuracy'.
            # We will use the teradataml DataFrames, created in the Example 3.
            Note:
                This Example will work only when teradataml is connected to Vantage 1.3
                or later versions.
         
            XGBoost_out4 = XGBoost(data=sparse_iris_train,
                                   attribute_table=sparse_iris_attribute,
                                   id_column='id',
                                   attribute_name_column='attribute',
                                   attribute_value_column='value_col',
                                   response_column="species",
                                   loss_function='SOFTMAX',
                                   reg_lambda=1.0,
                                   num_boosted_trees=2,
                                   shrinkage_factor=0.1,
                                   column_subsampling=1.0,
                                   iter_num=10,
                                   min_node_size=1,
                                   max_depth=10,
                                   variance=0.0,
                                   seed=1,
                                   output_accuracy=True
                                   )
         
            # Print the results.
            print(XGBoost_out3)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.formula  = formula 
        self.data  = data 
        self.id_column  = id_column 
        self.loss_function  = loss_function 
        self.prediction_type  = prediction_type 
        self.reg_lambda  = reg_lambda 
        self.shrinkage_factor  = shrinkage_factor 
        self.iter_num  = iter_num 
        self.min_node_size  = min_node_size 
        self.max_depth  = max_depth 
        self.variance  = variance 
        self.seed  = seed 
        self.attribute_name_column  = attribute_name_column 
        self.num_boosted_trees  = num_boosted_trees 
        self.attribute_table  = attribute_table 
        self.attribute_value_column  = attribute_value_column 
        self.column_subsampling  = column_subsampling 
        self.response_column  = response_column 
        self.data_sequence_column  = data_sequence_column 
        self.attribute_table_sequence_column  = attribute_table_sequence_column 
        self.output_accuracy  = output_accuracy 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["formula", self.formula, True, "formula"])
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["id_column", self.id_column, True, (str)])
        self.__arg_info_matrix.append(["loss_function", self.loss_function, True, (str)])
        self.__arg_info_matrix.append(["prediction_type", self.prediction_type, True, (str)])
        self.__arg_info_matrix.append(["reg_lambda", self.reg_lambda, True, (float)])
        self.__arg_info_matrix.append(["shrinkage_factor", self.shrinkage_factor, True, (float)])
        self.__arg_info_matrix.append(["iter_num", self.iter_num, True, (int)])
        self.__arg_info_matrix.append(["min_node_size", self.min_node_size, True, (int)])
        self.__arg_info_matrix.append(["max_depth", self.max_depth, True, (int)])
        self.__arg_info_matrix.append(["variance", self.variance, True, (float)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["attribute_name_column", self.attribute_name_column, True, (str)])
        self.__arg_info_matrix.append(["num_boosted_trees", self.num_boosted_trees, True, (int)])
        self.__arg_info_matrix.append(["attribute_table", self.attribute_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["attribute_value_column", self.attribute_value_column, True, (str)])
        self.__arg_info_matrix.append(["column_subsampling", self.column_subsampling, True, (float)])
        self.__arg_info_matrix.append(["response_column", self.response_column, True, (str)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["attribute_table_sequence_column", self.attribute_table_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["output_accuracy", self.output_accuracy, True, (bool)])
        
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

        # Either formula or response_column is required
        if (self.formula is None and self.response_column is None) or \
                (self.formula is not None and self.response_column is not None):
            raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                           "formula", "response_column"), MessageCodes.MISSING_ARGS)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        self.__awu._validate_input_table_datatype(self.attribute_table, "attribute_table", None)
        
        # Check for permitted values
        if configure._vantage_version in ["vanatge1.3"]:
            loss_function_permitted_values = ["BINOMIAL", "SOFTMAX", "MSE"]
            prediction_type_permitted_values = ["CLASSIFICATION", "REGRESSION"]
        else:
            loss_function_permitted_values = ["BINOMIAL", "SOFTMAX"]
            prediction_type_permitted_values = ["CLASSIFICATION"]

        self.__awu._validate_permitted_values(self.loss_function, loss_function_permitted_values, "loss_function")
        self.__awu._validate_permitted_values(self.prediction_type, prediction_type_permitted_values, "prediction_type")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.response_column, "response_column")
        self.__awu._validate_dataframe_has_argument_columns(self.response_column, "response_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.id_column, "id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.id_column, "id_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_name_column, "attribute_name_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_name_column, "attribute_name_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_value_column, "attribute_value_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_value_column, "attribute_value_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_table_sequence_column, "attribute_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_table_sequence_column, "attribute_table_sequence_column", self.attribute_table, "attribute_table", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__model_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_xgboost0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
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

        if self.response_column is not None:
            self.__func_other_arg_sql_names.append("ResponseColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.response_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.id_column is not None:
            self.__func_other_arg_sql_names.append("IdColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.id_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.attribute_name_column is not None:
            self.__func_other_arg_sql_names.append("AttributeNameColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_name_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.attribute_value_column is not None:
            self.__func_other_arg_sql_names.append("AttributeValueColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_value_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.num_boosted_trees is not None:
            self.__func_other_arg_sql_names.append("NumBoostedTrees")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.num_boosted_trees, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.output_accuracy is not None and self.output_accuracy != False:
            self.__func_other_arg_sql_names.append("OutputAccuracy")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_accuracy, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.loss_function is not None and self.loss_function != "SOFTMAX":
            self.__func_other_arg_sql_names.append("LossFunction")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.loss_function, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.prediction_type is not None and self.prediction_type != "CLASSIFICATION":
            self.__func_other_arg_sql_names.append("PredictionType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.prediction_type, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.reg_lambda is not None and self.reg_lambda != 1:
            self.__func_other_arg_sql_names.append("RegularizationLambda")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.reg_lambda, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.shrinkage_factor is not None and self.shrinkage_factor != 0.1:
            self.__func_other_arg_sql_names.append("ShrinkageFactor")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.shrinkage_factor, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.column_subsampling is not None and self.column_subsampling != 1.0:
            self.__func_other_arg_sql_names.append("ColumnSubSampling")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.column_subsampling, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.iter_num is not None and self.iter_num != 10:
            self.__func_other_arg_sql_names.append("IterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.iter_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.min_node_size is not None and self.min_node_size != 1:
            self.__func_other_arg_sql_names.append("MinNodeSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.min_node_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.max_depth is not None and self.max_depth != 5:
            self.__func_other_arg_sql_names.append("MaxDepth")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_depth, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.variance is not None and self.variance != 0:
            self.__func_other_arg_sql_names.append("Variance")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.variance, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.seed is not None:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.attribute_table_sequence_column is not None:
            sequence_input_by_list.append("AttributeTable:" + UtilFuncs._teradata_collapse_arglist(self.attribute_table_sequence_column, ""))
        
        if len(sequence_input_by_list) > 0:
            self.__func_other_arg_sql_names.append("SequenceInputBy")
            sequence_input_by_arg_value = UtilFuncs._teradata_collapse_arglist(sequence_input_by_list, "'")
            self.__func_other_args.append(sequence_input_by_arg_value)
            self.__func_other_arg_json_datatypes.append("STRING")
            self._sql_specific_attributes["SequenceInputBy"] = sequence_input_by_arg_value

        # Let's process formula argument
        if self.formula is not None:
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
        
        # Process attribute_table
        if self.attribute_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.attribute_table)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("AttributeTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "XGBoost"
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
        if self.attribute_table is not None:
            self.__input_nodeids.append(self.attribute_table._nodeid)
        
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__func_output_args.insert(0, sqlmr_stdout_temp_tablename)
        try:
            # Call aed_ml_query and generate AED nodes.
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "XGBoost", self.__aqg_obj._multi_query_input_nodes)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, str(emsg)), MessageCodes.AED_EXEC_FAILED)
        
        
        # Update output table data frames.
        self._mlresults = []
        self.model_table = self.__awu._create_data_set_object(df_input=node_id_list[1], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[1], self.__model_table_column_info))
        self.output = self.__awu._create_data_set_object(df_input=node_id_list[0], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[0], self.__stdout_column_info))
        self._mlresults.append(self.model_table)
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
        
        # Collecting model_table output column information.
        model_table_column_info_name = []
        model_table_column_info_type = []
        model_table_column_info_name.append("tree_id")
        model_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
        
        model_table_column_info_name.append("iter")
        model_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
        
        model_table_column_info_name.append("class_num")
        model_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))
        
        model_table_column_info_name.append("tree")
        model_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("clob"))
        
        model_table_column_info_name.append("region_prediction")
        model_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("clob"))
        
        self.__model_table_column_info = zip(model_table_column_info_name, model_table_column_info_type)
        
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
        
        # Initialize the formula attributes.
        __response_column = kwargs.pop("__response_column", None)
        __all_columns = kwargs.pop("__all_columns", None)
        __numeric_columns = kwargs.pop("__numeric_columns", None)
        __categorical_columns = kwargs.pop("__categorical_columns", None)
        
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
        
        # Initialize the formula.
        if obj.formula is not None:
            obj.formula = Formula._from_formula_attr(obj.formula,
                                                     __response_column,
                                                     __all_columns,
                                                     __categorical_columns,
                                                     __numeric_columns)
        
        # Update output table data frames.
        obj._mlresults = []
        obj.model_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.model_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.model_table))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.model_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a XGBoost class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ model_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.model_table)
        return repr_string
        
