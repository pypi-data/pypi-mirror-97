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
# Function Version: 2.8
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
from teradataml.analytics.mle.XGBoost import XGBoost

class XGBoostPredict:
    
    def __init__(self,
        object = None,
        newdata = None,
        id_column = None,
        terms = None,
        iter_num = None,
        num_boosted_trees = None,
        attribute_name_column = None,
        attribute_value_column = None,
        output_response_probdist = False,
        output_responses = None,
        newdata_sequence_column = None,
        object_sequence_column = None,
        newdata_partition_column = "ANY",
        newdata_order_column = None,
        object_order_column = None):
        """
        DESCRIPTION:
            The XGBoostPredict function applies the model output by the XGBoost
            function to a new data set, outputting predicted labels for each data
            point.
         
         
        PARAMETERS:
            object:
                Required Argument.
                Specifies the teradataml DataFrame containing the model data.
         
            object_order_column:
                Required Argument.
                Specifies Order By columns for object.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            newdata:
                Required Argument.
                Specifies the teradataml DataFrame containing the input test data.
         
            newdata_partition_column:
                Optional Argument.
                Specifies Partition By columns for newdata.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
         
            newdata_order_column:
                Optional Argument.
                Specifies Order By columns for newdata.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            id_column:
                Optional Argument.
                Specifies a column containing a unique identifier for each test point
                in the test set.
                Types: str
         
            terms:
                Optional Argument.
                Specifies the names of the input columns to copy to the output table.
                Types: str OR list of Strings (str)
         
            iter_num:
                Optional Argument.
                Specifies the number of iterations for each boosted tree to use for
                prediction. The lower bound is 1. If this argument is not specified,
                the value is the same as used for training model. The number of
                iterations used is upper bounded by the number of iterations used
                during training.
                Types: int
         
            num_boosted_trees:
                Optional Argument.
                Specifies the number of boosted trees to be used for prediction. If
                this argument is not specified, the value is the same as used for
                training model. The number of boosted trees used for prediction is
                upper bounded by the number of boosted trees used during training.
                Types: int
         
            attribute_name_column:
                Optional Argument.
                Required for sparse data format, if the data set is in sparse format,
                this argument indicates the column containing the attributes in the
                input teradataml DataFrame.
                Types: str
         
            attribute_value_column:
                Optional Argument.
                If the data is in the sparse format, this argument indicates the
                column containing the attribute values in the input teradataml DataFrame.
                Types: str
         
            output_response_probdist:
                Optional Argument.
                Specifies whether to output probabilities or not.
                Note: "output_response_probdist" argument support is only available
                      when teradataml is connected to Vantage 1.1.1 or later.
                Default Value: False
                Types: bool
         
            output_responses:
                Optional Argument.
                Specifies the responses in the input teradataml DataFrame.
                output_response_probdist must be set to True in order to use this argument.
                Note: "output_responses" argument support is only available
                      when teradataml is connected to Vantage 1.1.1 or later.
                Types: str OR list of Strings (str)
         
            newdata_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "newdata". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            object_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "object". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of XGBoostPredict.
            Output teradataml DataFrames can be accessed using attribute
            references, such as XGBoostPredictObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("xgboost", ["housing_train_binary","iris_train","sparse_iris_train","sparse_iris_attribute"])
            load_example_data("xgboostpredict", ["housing_test_binary", "iris_test", "sparse_iris_test"])
         
            # Example 1 - Binary Classification: Predict the housing style (classic or eclectic)
            # Create teradataml DataFrame objects.
            housing_train_binary = DataFrame.from_table("housing_train_binary")
            housing_test_binary = DataFrame.from_table("housing_test_binary")
         
            # Generate the XGBoost model, on the housing data, that contains couple of labels
            # classic and eclectic, which specify the housing style based on the 12 other
            # attributes of the house, such as bedrooms, stories, price etc.
            XGBoostOut1 = XGBoost(data=housing_train_binary,
                                  id_column='sn',
                                  formula="homestyle ~ driveway + recroom + fullbase + gashw + airco + prefarea + price + lotsize + bedrooms + bathrms + stories + garagepl",
                                  num_boosted_trees=2,
                                  loss_function='binomial',
                                  prediction_type='classification',
                                  reg_lambda=1.0,
                                  shrinkage_factor=0.1,
                                  iter_num=10,
                                  min_node_size=1,
                                  max_depth=10
                                  )
         
            # Use the generated model to find predict the house style, on the test data.
            XGBoostPredictOut1 = XGBoostPredict(newdata=housing_test_binary,
                                                object=XGBoostOut1,
                                                object_order_column=['tree_id', 'iter', 'class_num'],
                                                id_column='sn',
                                                terms='homestyle',
                                                num_boosted_trees=1
                                                )
         
            # Print the results
            print(XGBoostPredictOut1)
         
            # Example 2: Multiple-Class Classification: Predict the Iris flower species
            #                                           (setosa, virginica or versicolor).
            iris_train = DataFrame.from_table("iris_train")
            iris_test = DataFrame.from_table("iris_test")
         
            # Generate the model on one of the famous dataset Iris Data set, that contains 50 samples
            # from three species of Iris flower setosa, virginica and versicolor. Each data point contains
            # measurements of length and width of sepals and petals.
            XGBoostOut2 = XGBoost(data=iris_train,
                                 id_column='id',
                                  formula="species ~ sepal_length + sepal_width + petal_length + petal_width ",
                                  num_boosted_trees=2,
                                  loss_function='softmax',
                                  reg_lambda=1.0,
                                  shrinkage_factor=0.1,
                                  iter_num=10,
                                  min_node_size=1,
                                  max_depth=10)
         
            # Use the generated model to predict the Iris flower type.
            XGBoostPredictOut2 = XGBoostPredict(newdata=iris_test,
                                newdata_partition_column='id',
                                object=XGBoostOut2,
                                object_order_column=['tree_id', 'iter','class_num'],
                                id_column='id',
                                terms='species',
                                num_boosted_trees=2
                                )
         
            # Print the results
            print(XGBoostPredictOut2)
         
            # Example 3: Sparse Input Format. response_column argument is specified instead of formula.
            sparse_iris_train = DataFrame.from_table("sparse_iris_train")
            sparse_iris_test = DataFrame.from_table("sparse_iris_test")
            sparse_iris_attribute = DataFrame.from_table("sparse_iris_attribute")
         
            # Generate the model
            XGBoostOut3 = XGBoost(data=sparse_iris_train,
                              attribute_table=sparse_iris_attribute,
                              id_column='id',
                              response_column='species',
                              prediction_type='classification',
                              attribute_name_column='attribute',
                              attribute_value_column='value_col',
                              num_boosted_trees=2,
                              loss_function='SOFTMAX',
                              reg_lambda=1.0,
                              shrinkage_factor=0.1,
                              iter_num=10,
                              min_node_size=1,
                              max_depth=10)
         
            # Use the generated model to find prediction.
            XGBoostPredictOut3 = XGBoostPredict(object = XGBoostOut3,
                                                object_order_column = ["tree_id", "iter", "class_num"],
                                                newdata = sparse_iris_test,
                                                newdata_partition_column = ["id"],
                                                id_column = "id",
                                                terms = ["species"],
                                                num_boosted_trees = 2,
                                                attribute_name_column = "attribute",
                                                attribute_value_column = "value_col"
                                                )
         
            # Print the results
            print(XGBoostPredictOut3)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.object  = object
        self.newdata  = newdata
        self.id_column  = id_column
        self.terms  = terms
        self.iter_num  = iter_num
        self.num_boosted_trees  = num_boosted_trees
        self.attribute_name_column  = attribute_name_column
        self.attribute_value_column  = attribute_value_column
        self.output_response_probdist  = output_response_probdist
        self.output_responses  = output_responses
        self.newdata_sequence_column  = newdata_sequence_column
        self.object_sequence_column  = object_sequence_column
        self.newdata_partition_column  = newdata_partition_column
        self.newdata_order_column  = newdata_order_column
        self.object_order_column  = object_order_column
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, False, (DataFrame)])
        self.__arg_info_matrix.append(["object_order_column", self.object_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["newdata", self.newdata, False, (DataFrame)])
        self.__arg_info_matrix.append(["newdata_partition_column", self.newdata_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["newdata_order_column", self.newdata_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["id_column", self.id_column, True, (str)])
        self.__arg_info_matrix.append(["terms", self.terms, True, (str,list)])
        self.__arg_info_matrix.append(["iter_num", self.iter_num, True, (int)])
        self.__arg_info_matrix.append(["num_boosted_trees", self.num_boosted_trees, True, (int)])
        self.__arg_info_matrix.append(["attribute_name_column", self.attribute_name_column, True, (str)])
        self.__arg_info_matrix.append(["attribute_value_column", self.attribute_value_column, True, (str)])
        self.__arg_info_matrix.append(["output_response_probdist", self.output_response_probdist, True, (bool)])
        self.__arg_info_matrix.append(["output_responses", self.output_responses, True, (str,list)])
        self.__arg_info_matrix.append(["newdata_sequence_column", self.newdata_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["object_sequence_column", self.object_sequence_column, True, (str,list)])
        
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
        if isinstance(self.object, XGBoost):
            self.object = self.object._mlresults[0]

        # To use output_responses, output_response_probdist must be set to True
        if self.output_response_probdist is False and self.output_responses is not None:
            raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                                           'output_response_probdist=True',
                                                           'output_responses'),
                                      MessageCodes.DEPENDENT_ARG_MISSING)

        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.newdata, "newdata", None)
        self.__awu._validate_input_table_datatype(self.object, "object", XGBoost)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.id_column, "id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.id_column, "id_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.terms, "terms")
        self.__awu._validate_dataframe_has_argument_columns(self.terms, "terms", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_name_column, "attribute_name_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_name_column, "attribute_name_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_value_column, "attribute_value_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_value_column, "attribute_value_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_sequence_column, "newdata_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_sequence_column, "newdata_sequence_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_sequence_column, "object_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_sequence_column, "object_sequence_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_partition_column, "newdata_partition_column")
        if self.__awu._is_default_or_not(self.newdata_partition_column, "ANY"):
            self.__awu._validate_dataframe_has_argument_columns(self.newdata_partition_column, "newdata_partition_column", self.newdata, "newdata", True)
        self.__awu._validate_input_columns_not_empty(self.newdata_order_column, "newdata_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_order_column, "newdata_order_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_order_column, "object_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_order_column, "object_order_column", self.object, "object", False)
        
        
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
        
        if self.id_column is not None:
            self.__func_other_arg_sql_names.append("IdColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.id_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.terms is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.terms, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.attribute_name_column is not None:
            self.__func_other_arg_sql_names.append("AttributeNameColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_name_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.attribute_value_column is not None:
            self.__func_other_arg_sql_names.append("AttributeValueColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_value_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.iter_num is not None:
            self.__func_other_arg_sql_names.append("IterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.iter_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.num_boosted_trees is not None:
            self.__func_other_arg_sql_names.append("NumBoostedTrees")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.num_boosted_trees, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.output_response_probdist is not None and self.output_response_probdist != False:
            self.__func_other_arg_sql_names.append("OutputProb")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_response_probdist, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.output_responses is not None:
            self.__func_other_arg_sql_names.append("Responses")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_responses, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.newdata_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.newdata_sequence_column, ""))
        
        if self.object_sequence_column is not None:
            sequence_input_by_list.append("ModelTable:" + UtilFuncs._teradata_collapse_arglist(self.object_sequence_column, ""))
        
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
        
        # Process newdata
        if self.__awu._is_default_or_not(self.newdata_partition_column, "ANY"):
            self.newdata_partition_column = UtilFuncs._teradata_collapse_arglist(self.newdata_partition_column, "\"")
        
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.newdata, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.newdata_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.newdata_order_column, "\""))
        
        # Process object
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.object, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("ModelTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.object_order_column, "\""))
        
        function_name = "XGBoostPredict"
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
        Returns the string representation for a XGBoostPredict class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
