#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: N Bhavana (bhavana.n@teradata.com)
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
from teradataml.analytics.mle.KNNRecommender import KNNRecommender

class KNNRecommenderPredict:
    
    def __init__(self,
        object = None,
        ratings_data = None,
        weights_data = None,
        bias_data = None,
        userid_column = None,
        itemid_column = None,
        rating_column = None,
        topk = 3,
        showall = True,
        ratings_data_sequence_column = None,
        weights_data_sequence_column = None,
        bias_data_sequence_column = None,
        ratings_data_partition_column = None,
        ratings_data_order_column = None,
        weights_data_order_column = None,
        bias_data_order_column = None):
        """
        DESCRIPTION:
            The KNNRecommenderPredict function applies the model output by the KNNRecommender
            function to predict the ratings or preferences that users would assign to
            entities like books, songs, movies and other products.


        PARAMETERS:
            object:
                Optional Argument, when 'weights_data' and 'bias_data' provided.
                Specifies the instance of KNNRecommender containing the
                weights_data and bias_data.

            ratings_data:
                Required Argument.
                Specifies the teradataml DataFrame containing the user ratings.

            ratings_data_partition_column:
                Required Argument.
                Specifies the Partition By columns for ratings_data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)

            ratings_data_order_column:
                Optional Argument.
                Specifies Order By columns for ratings_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            weights_data:
                Optional Argument.
                Specifies the teradataml DataFrame (produced by KNNRecommender function)
                containing the interpolation weights. Optional argument if
                object is provided. If the value is provided along with object this value
                will be overwritten with the weigths_data of object value.

            weights_data_order_column:
                Optional Argument.
                Specifies Order By columns for weights_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            bias_data:
                Optional Argument.
                Specifies the teradataml DataFrame (produced by KNNRecommender function)
                containing the global, user, and item bias statistics. Optional argument if
                object is provided. If the value is provided along with object this value
                will be overwritten with the bias_data of object value.

            bias_data_order_column:
                Optional Argument.
                Specifies Order By columns for bias_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            userid_column:
                Optional Argument.
                Specifies the user id column in the rating table. The default is the first
                column in the rating table.
                Types: str OR list of Strings (str)

            itemid_column:
                Optional Argument.
                Specifies the item id column in the rating table. The default is the second
                column in the rating table.
                Types: str OR list of Strings (str)

            rating_column:
                Optional Argument.
                Specifies the rating column in the rating table. The default is the third
                column in the rating table.
                Types: str OR list of Strings (str)

            topk:
                Optional Argument.
                Specifies the number of items to recommend for each user. The topk highest-rated
                items are recommended.
                Default Value: 3
                Types: int
         
            showall:
                Optional Argument.
                Specifies whether the function outputs only the top k values or all
                the values in case many recommendations have the same predicted
                rating.
                When set to True, and multiple items have the same predicted rating,
                the function outputs all these items, regardless of the value of topk.
                Otherwise, the function outputs at most topk items.
                Note:
                    "showall" argument support is only available
                     when teradataml is connected to Vantage 1.1.1 or later.
                Default Value: True
                Types: bool

            ratings_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "ratings_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            weights_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "weights_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            bias_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "bias_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of KNNRecommenderPredict.
            Output teradataml DataFrames can be accessed using attribute
            references, such as KNNRecommenderPredictObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load the data to run the example
            load_example_data("knnrecommenderpredict", ["ml_ratings", "ml_ratings_10"])

            # Create teradataml DataFrame objects.
            ml_ratings = DataFrame.from_table("ml_ratings")

            # Example 1 - Train the KNN Recommender system on the user ratings data
            knn_recommender_out = KNNRecommender(rating_table = ml_ratings,
                                                 userid_column = "userid",
                                                 itemid_column = "itemid",
                                                 rating_column = "rating"
                                                 )

            # ml_ratings_10 table has movie ratings from a subset of users from the ml_ratings
            # table. The ml_bias and ml_weights table has the weights and bias values
            # from the trained KNN Recommender model.
            ml_weights = knn_recommender_out.weight_model_table
            ml_bias = knn_recommender_out.bias_model_table

            # Here "bias_data" and "weights_data" have been made optional with the argument "object"
            # having the knn_recommender_out output object
            # Create teradataml DataFrame objects.
            ml_ratings_10 = DataFrame.from_table("ml_ratings_10")

            knn_recommender_predict_out = KNNRecommenderPredict(object = knn_recommender_out,
                                                                ratings_data = ml_ratings_10,
                                                                ratings_data_partition_column = "userid",
                                                                topk = 5
                                                                )
            # Print the result DataFrame
            print(knn_recommender_predict_out)


            # Use the generated model to make user rating predictions. Here the argument "object"
            # has been made optional with the specification of both the arguments "bias_data" and
            # "weights_data"
            knn_recommender_predict_out2 = KNNRecommenderPredict(ratings_data = ml_ratings_10,
                                                                 ratings_data_partition_column = "userid",
                                                                 weights_data = ml_weights,
                                                                 bias_data = ml_bias,
                                                                 topk = 5
                                                                 )

            # Print the result DataFrame
            print(knn_recommender_predict_out2)

        """
        
        # Start the timer to get the build time
        _start_time = time.time()

        self.object = object
        self.ratings_data  = ratings_data 
        self.weights_data  = weights_data 
        self.bias_data  = bias_data 
        self.userid_column  = userid_column 
        self.itemid_column  = itemid_column 
        self.rating_column  = rating_column 
        self.topk  = topk 
        self.showall  = showall 
        self.ratings_data_sequence_column  = ratings_data_sequence_column 
        self.weights_data_sequence_column  = weights_data_sequence_column 
        self.bias_data_sequence_column  = bias_data_sequence_column 
        self.ratings_data_partition_column  = ratings_data_partition_column 
        self.ratings_data_order_column  = ratings_data_order_column 
        self.weights_data_order_column  = weights_data_order_column 
        self.bias_data_order_column  = bias_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["ratings_data", self.ratings_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["ratings_data_partition_column", self.ratings_data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["ratings_data_order_column", self.ratings_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["weights_data", self.weights_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["weights_data_order_column", self.weights_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["bias_data", self.bias_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["bias_data_order_column", self.bias_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["userid_column", self.userid_column, True, (str)])
        self.__arg_info_matrix.append(["itemid_column", self.itemid_column, True, (str)])
        self.__arg_info_matrix.append(["rating_column", self.rating_column, True, (str)])
        self.__arg_info_matrix.append(["topk", self.topk, True, (int)])
        self.__arg_info_matrix.append(["showall", self.showall, True, (bool)])
        self.__arg_info_matrix.append(["ratings_data_sequence_column", self.ratings_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["weights_data_sequence_column", self.weights_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["bias_data_sequence_column", self.bias_data_sequence_column, True, (str,list)])
        
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
        # Make sure either object or (weights_.data and bias_data) is provided.
        if not self.object and not (self.weights_data and self.bias_data):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT, "object", "weights_data and bias_data"),
                MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

        # If object is not NULL, and if weights_data or bias_data is NULL, then initialize them from object
        if self.object and self.__awu._validate_argument_types([["object", self.object, True, (KNNRecommender)]]):
            self.weights_data = self.object._mlresults[0]
            self.bias_data = self.object._mlresults[1]

        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.ratings_data, "ratings_data", None)
        self.__awu._validate_input_table_datatype(self.weights_data, "weights_data", None)
        self.__awu._validate_input_table_datatype(self.bias_data, "bias_data", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.userid_column, "userid_column")
        self.__awu._validate_dataframe_has_argument_columns(self.userid_column, "userid_column", self.ratings_data, "ratings_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.itemid_column, "itemid_column")
        self.__awu._validate_dataframe_has_argument_columns(self.itemid_column, "itemid_column", self.ratings_data, "ratings_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.rating_column, "rating_column")
        self.__awu._validate_dataframe_has_argument_columns(self.rating_column, "rating_column", self.ratings_data, "ratings_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.ratings_data_sequence_column, "ratings_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.ratings_data_sequence_column, "ratings_data_sequence_column", self.ratings_data, "ratings_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.weights_data_sequence_column, "weights_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.weights_data_sequence_column, "weights_data_sequence_column", self.weights_data, "weights_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.bias_data_sequence_column, "bias_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.bias_data_sequence_column, "bias_data_sequence_column", self.bias_data, "bias_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.ratings_data_partition_column, "ratings_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.ratings_data_partition_column, "ratings_data_partition_column", self.ratings_data, "ratings_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.ratings_data_order_column, "ratings_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.ratings_data_order_column, "ratings_data_order_column", self.ratings_data, "ratings_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.weights_data_order_column, "weights_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.weights_data_order_column, "weights_data_order_column", self.weights_data, "weights_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.bias_data_order_column, "bias_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.bias_data_order_column, "bias_data_order_column", self.bias_data, "bias_data", False)
        
        
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
        
        if self.userid_column is not None:
            self.__func_other_arg_sql_names.append("UserIdColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.userid_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.itemid_column is not None:
            self.__func_other_arg_sql_names.append("ItemIdColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.itemid_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.rating_column is not None:
            self.__func_other_arg_sql_names.append("RatingColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.rating_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.topk is not None and self.topk != 3:
            self.__func_other_arg_sql_names.append("Topk")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.topk, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.showall is not None and self.showall != True:
            self.__func_other_arg_sql_names.append("ShowAll")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.showall, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.ratings_data_sequence_column is not None:
            sequence_input_by_list.append("ratings:" + UtilFuncs._teradata_collapse_arglist(self.ratings_data_sequence_column, ""))
        
        if self.weights_data_sequence_column is not None:
            sequence_input_by_list.append("weights:" + UtilFuncs._teradata_collapse_arglist(self.weights_data_sequence_column, ""))
        
        if self.bias_data_sequence_column is not None:
            sequence_input_by_list.append("bias:" + UtilFuncs._teradata_collapse_arglist(self.bias_data_sequence_column, ""))
        
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
        
        # Process ratings_data
        self.ratings_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.ratings_data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.ratings_data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("ratings")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.ratings_data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.ratings_data_order_column, "\""))
        
        # Process weights_data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.weights_data, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("weights")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.weights_data_order_column, "\""))
        
        # Process bias_data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.bias_data, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("bias")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.bias_data_order_column, "\""))
        
        function_name = "KNNRecommenderPredict"
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
        Returns the string representation for a KNNRecommenderPredict class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
