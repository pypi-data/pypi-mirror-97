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
# Function Version: 1.7
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

class KNNRecommender:
    
    def __init__(self,
        rating_table = None,
        userid_column = None,
        itemid_column = None,
        rating_column = None,
        k = 20,
        learning_rate = 0.001,
        max_iternum = 10,
        threshold = 2.0E-4,
        item_similarity = "Pearson",
        rating_table_sequence_column = None):
        """
        DESCRIPTION:
            The KNNRecommender function trains a interpolation weight model based on
            weighted collaborative filtering approach. It uses the input user
            ratings data to create three model tables: the weights model table,
            the bias model table and the optional nearest items or neighbors table.
            These tables are then used by KNNRecommenderPredict to predict the ratings or
            preferences that users assign to entities like books, songs, movies
            and other products.

        PARAMETERS:
            rating_table:
                Required Argument.
                Specifies the TeraDataMl DataFrame containing the user ratings.

            userid_column:
                Optional Argument.
                Specifies the user id column in the rating table. The default is the first
                column in the rating table.
                Types: str

            itemid_column:
                Optional Argument.
                Specifies the item id column in the rating table. The default is the second
                column in the rating table.
                Types: str

            rating_column:
                Optional Argument.
                Specifies the rating column in the rating table. The default is the third
                column in the rating table.
                Types: str

            k:
                Optional Argument.
                Specifies the number of nearest neighbors used in the calculation of the
                interpolation weights.
                Default Value: 20
                Types: int

            learning_rate:
                Optional Argument.
                Specifies initial learning rate. The learning rate adjusts automatically during
                training based on changes in the rmse.
                Default Value: 0.001
                Types: float

            max_iternum:
                Optional Argument.
                Specifies the maximum number of iterations.
                Default Value: 10
                Types: int

            threshold:
                Optional Argument.
                The function stops when the rmse drops below this level.
                Default Value: 2.0E-4
                Types: float

            item_similarity:
                Optional Argument.
                Specifies the method used to calculate item similarity. Options include: Pearson (Pearson
                correlation coefficient), adjustedcosine (adjusted cosine similarity)
                Default Value: "Pearson"
                Permitted Values: AdjustedCosine, Pearson
                Types: str

            rating_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "rating_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of KNNRecommender.
            Output teradataml DataFrames can be accessed using attribute
            references, such as KNNRecommenderObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. weight_model_table
                2. bias_model_table
                3. nearest_items
                4. output


        RAISES:
            TeradataMlException

        EXAMPLES:

            # Load the data to run the example
            load_example_data("knnrecommender", "ml_ratings")

            # Create teradataml DataFrame objects.
            # The ml_ratings table has movie ratings from 50 users on
            # approximately 2900 movies, with an average of about 150 ratings
            # for each user. The 10 possible ratings range from 0.5 to 5
            # in steps of 0.5. A higher number indicates a better rating.
            ml_ratings = DataFrame.from_table("ml_ratings")

            # Example 1 - Train the KNN Recommender system on the user ratings data
            knn_recommender_out = KNNRecommender(rating_table = ml_ratings,
                                                 userid_column = "userid",
                                                 itemid_column = "itemid",
                                                 rating_column = "rating"
                                                         )

            # Print the result DataFrame
            print(knn_recommender_out)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.rating_table  = rating_table 
        self.userid_column  = userid_column 
        self.itemid_column  = itemid_column 
        self.rating_column  = rating_column 
        self.k  = k 
        self.learning_rate  = learning_rate 
        self.max_iternum  = max_iternum 
        self.threshold  = threshold 
        self.item_similarity  = item_similarity
        self.rating_table_sequence_column  = rating_table_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["rating_table", self.rating_table, False, (DataFrame)])
        self.__arg_info_matrix.append(["userid_column", self.userid_column, True, (str)])
        self.__arg_info_matrix.append(["itemid_column", self.itemid_column, True, (str)])
        self.__arg_info_matrix.append(["rating_column", self.rating_column, True, (str)])
        self.__arg_info_matrix.append(["k", self.k, True, (int)])
        self.__arg_info_matrix.append(["learning_rate", self.learning_rate, True, (float)])
        self.__arg_info_matrix.append(["max_iternum", self.max_iternum, True, (int)])
        self.__arg_info_matrix.append(["threshold", self.threshold, True, (float)])
        self.__arg_info_matrix.append(["item_similarity", self.item_similarity, True, (str)])
        self.__arg_info_matrix.append(["rating_table_sequence_column", self.rating_table_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.rating_table, "rating_table", None)
        
        # Check for permitted values
        item_similarity_permitted_values = ["ADJUSTEDCOSINE", "PEARSON"]
        self.__awu._validate_permitted_values(self.item_similarity, item_similarity_permitted_values, "item_similarity")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.userid_column, "userid_column")
        self.__awu._validate_dataframe_has_argument_columns(self.userid_column, "userid_column", self.rating_table, "rating_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.itemid_column, "itemid_column")
        self.__awu._validate_dataframe_has_argument_columns(self.itemid_column, "itemid_column", self.rating_table, "rating_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.rating_column, "rating_column")
        self.__awu._validate_dataframe_has_argument_columns(self.rating_column, "rating_column", self.rating_table, "rating_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.rating_table_sequence_column, "rating_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.rating_table_sequence_column, "rating_table_sequence_column", self.rating_table, "rating_table", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__weight_model_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_knnrecommender0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__bias_model_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_knnrecommender1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__nearest_items_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_knnrecommender2", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["WeightModelTable", "BiasModelTable", "NearestItemsTable"]
        self.__func_output_args = [self.__weight_model_table_temp_tablename, self.__bias_model_table_temp_tablename, self.__nearest_items_temp_tablename]
        
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
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.itemid_column is not None:
            self.__func_other_arg_sql_names.append("ItemIdColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.itemid_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.rating_column is not None:
            self.__func_other_arg_sql_names.append("RatingColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.rating_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.learning_rate is not None and self.learning_rate != 0.001:
            self.__func_other_arg_sql_names.append("LearningRate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.learning_rate, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.max_iternum is not None and self.max_iternum != 10:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_iternum, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.k is not None and self.k != 20:
            self.__func_other_arg_sql_names.append("K")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.k, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.threshold is not None and self.threshold != 2.0E-4:
            self.__func_other_arg_sql_names.append("StopThreshold")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.threshold, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.item_similarity is not None and self.item_similarity != "Pearson":
            self.__func_other_arg_sql_names.append("SimilarityMethod")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.item_similarity, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.rating_table_sequence_column is not None:
            sequence_input_by_list.append("RatingTable:" + UtilFuncs._teradata_collapse_arglist(self.rating_table_sequence_column, ""))
        
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
        
        # Process rating_table
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.rating_table, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("RatingTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "KNNRecommender"
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
        self.weight_model_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__weight_model_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__weight_model_table_temp_tablename))
        self.bias_model_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__bias_model_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__bias_model_table_temp_tablename))
        self.nearest_items = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__nearest_items_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__nearest_items_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.weight_model_table)
        self._mlresults.append(self.bias_model_table)
        self._mlresults.append(self.nearest_items)
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
        weight_model_table = None,
        bias_model_table = None,
        nearest_items = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("weight_model_table", None)
        kwargs.pop("bias_model_table", None)
        kwargs.pop("nearest_items", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.weight_model_table  = weight_model_table 
        obj.bias_model_table  = bias_model_table 
        obj.nearest_items  = nearest_items 
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
        obj.weight_model_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.weight_model_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.weight_model_table))
        obj.bias_model_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.bias_model_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.bias_model_table))
        obj.nearest_items = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.nearest_items), source_type="table", database_name=UtilFuncs._extract_db_name(obj.nearest_items))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.weight_model_table)
        obj._mlresults.append(obj.bias_model_table)
        obj._mlresults.append(obj.nearest_items)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a KNNRecommender class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ weight_model_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.weight_model_table)
        repr_string="{}\n\n\n############ bias_model_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.bias_model_table)
        repr_string="{}\n\n\n############ nearest_items Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.nearest_items)
        return repr_string
        
