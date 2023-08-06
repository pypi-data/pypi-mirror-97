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

class NaiveBayesTextClassifier:
    
    def __init__(self,
        data = None,
        token_column = None,
        doc_id_columns = None,
        doc_category_column = None,
        model_type = "MULTINOMIAL",
        categories = None,
        category_column = "[0:0]",
        prediction_categories = None,
        stopwords = None,
        stopwords_column = None,
        stopwords_list = None,
        data_sequence_column = None,
        stopwords_sequence_column = None,
        categories_sequence_column = None,
        data_partition_column = None,
        data_order_column = None,
        stopwords_order_column = None,
        categories_order_column = None):
        """
        DESCRIPTION:
            The NaiveBayesTextClassifierTrainer function takes training data as
            input and outputs a model table.
         
        PARAMETERS:
            data:
                Required Argument.
                The teradataml DataFrame defining the training tokens.
         
            data_partition_column:
                Required Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            token_column:
                Required Argument.
                Specifies the name of the token_table column that contains the tokens
                to be classified.
                Types: str
         
            doc_id_columns:
                Optional Argument. Required when "model_type" argument is 'BERNOULLI'.
                Specifies the names of the token_table columns that contain the
                document identifier.
                Types: str OR list of Strings (str)
                Note:
                    This argument should not be provided when "model_type" is 'MULTINOMIAL'.
         
            doc_category_column:
                Required Argument.
                Specifies the name of the token_table column that contains the
                document category.
                Types: str
         
            model_type:
                Optional Argument.
                Specifies the model type of the text classifier. The formulas for the
                two model types follow this table.
                Default Value: "MULTINOMIAL"
                Permitted Values: MULTINOMIAL, BERNOULLI
                Types: str
         
            categories:
                Optional Argument.
                The teradataml DataFrame defining allowed categories.
         
            categories_order_column:
                Optional Argument.
                Specifies Order By columns for categories.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            category_column:
                Optional Argument.
                Specifies the name of the categories_table column that contains the
                prediction categories. The default value is the first column of
                categories_table.
                Default Value: "[0:0]"
                Types: str
         
            prediction_categories:
                Optional Argument.
                Specifies the prediction categories.
                Note: Specify either this argument or the categories_table, but not both.
                Types: str OR list of Strings (str)
         
            stopwords:
                Optional Argument.
                The teradataml DataFrame defining stop words.
         
            stopwords_order_column:
                Optional Argument.
                Specifies Order By columns for stopwords.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            stopwords_column:
                Optional Argument.
                Specifies the name of the stop_words_table column that contains the
                stop words. The default value is the first column of stop_words_table.
                Types: str
         
            stopwords_list:
                Optional Argument.
                Specifies words to ignore (such as a, an, and the).
                Note: Specify either this argument or the stop_words_table, but not both.
                Types: str OR list of Strings (str)
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            stopwords_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "stopwords". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            categories_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "categories". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of NaiveBayesTextClassifier.
            Output teradataml DataFrames can be accessed using attribute
            references, such as NaiveBayesTextClassifierObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example
            load_example_data("NaiveBayesTextClassifier","token_table")
         
            # Create teradataml DataFrame
            token_table = DataFrame.from_table("token_table")
         
            # Example 1 -
            nbt_result = NaiveBayesTextClassifier(data = token_table,
                                                  token_column = 'token',
                                                  doc_id_columns = 'doc_id',
                                                  doc_category_column = 'category',
                                                  model_type = "BERNOULLI",
                                                  data_partition_column = 'category')
         
            # Print the result DataFrame
            print(nbt_result.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.token_column  = token_column 
        self.doc_id_columns  = doc_id_columns 
        self.doc_category_column  = doc_category_column 
        self.model_type  = model_type 
        self.categories  = categories 
        self.category_column  = category_column 
        self.prediction_categories  = prediction_categories 
        self.stopwords  = stopwords 
        self.stopwords_column  = stopwords_column 
        self.stopwords_list  = stopwords_list 
        self.data_sequence_column  = data_sequence_column 
        self.stopwords_sequence_column  = stopwords_sequence_column 
        self.categories_sequence_column  = categories_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.data_order_column  = data_order_column 
        self.stopwords_order_column  = stopwords_order_column 
        self.categories_order_column  = categories_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["token_column", self.token_column, False, (str)])
        self.__arg_info_matrix.append(["doc_id_columns", self.doc_id_columns, True, (str,list)])
        self.__arg_info_matrix.append(["doc_category_column", self.doc_category_column, False, (str)])
        self.__arg_info_matrix.append(["model_type", self.model_type, True, (str)])
        self.__arg_info_matrix.append(["categories", self.categories, True, (DataFrame)])
        self.__arg_info_matrix.append(["categories_order_column", self.categories_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["category_column", self.category_column, True, (str)])
        self.__arg_info_matrix.append(["prediction_categories", self.prediction_categories, True, (str,list)])
        self.__arg_info_matrix.append(["stopwords", self.stopwords, True, (DataFrame)])
        self.__arg_info_matrix.append(["stopwords_order_column", self.stopwords_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["stopwords_column", self.stopwords_column, True, (str)])
        self.__arg_info_matrix.append(["stopwords_list", self.stopwords_list, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["stopwords_sequence_column", self.stopwords_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["categories_sequence_column", self.categories_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.stopwords, "stopwords", None)
        self.__awu._validate_input_table_datatype(self.categories, "categories", None)
        
        # Check for permitted values
        model_type_permitted_values = ["MULTINOMIAL", "BERNOULLI"]
        self.__awu._validate_permitted_values(self.model_type, model_type_permitted_values, "model_type")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.token_column, "token_column")
        self.__awu._validate_dataframe_has_argument_columns(self.token_column, "token_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.doc_category_column, "doc_category_column")
        self.__awu._validate_dataframe_has_argument_columns(self.doc_category_column, "doc_category_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.doc_id_columns, "doc_id_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.doc_id_columns, "doc_id_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.category_column, "category_column")
        
        self.__awu._validate_input_columns_not_empty(self.stopwords_column, "stopwords_column")
        self.__awu._validate_dataframe_has_argument_columns(self.stopwords_column, "stopwords_column", self.stopwords, "stopwords", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.stopwords_sequence_column, "stopwords_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.stopwords_sequence_column, "stopwords_sequence_column", self.stopwords, "stopwords", False)
        
        self.__awu._validate_input_columns_not_empty(self.categories_sequence_column, "categories_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.categories_sequence_column, "categories_sequence_column", self.categories, "categories", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.stopwords_order_column, "stopwords_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.stopwords_order_column, "stopwords_order_column", self.stopwords, "stopwords", False)
        
        self.__awu._validate_input_columns_not_empty(self.categories_order_column, "categories_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.categories_order_column, "categories_order_column", self.categories, "categories", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("TokenColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.token_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("DocCategoryColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.doc_category_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.doc_id_columns is not None:
            self.__func_other_arg_sql_names.append("DocIdColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.doc_id_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.category_column is not None and self.category_column != "[0:0]":
            self.__func_other_arg_sql_names.append("CategoryColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.category_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.stopwords_column is not None:
            self.__func_other_arg_sql_names.append("StopwordsColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.stopwords_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.model_type is not None and self.model_type != "MULTINOMIAL":
            self.__func_other_arg_sql_names.append("ModelType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.model_type, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.prediction_categories is not None:
            self.__func_other_arg_sql_names.append("PredictionCategories")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.prediction_categories, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.stopwords_list is not None:
            self.__func_other_arg_sql_names.append("StopwordsList")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.stopwords_list, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.stopwords_sequence_column is not None:
            sequence_input_by_list.append("stopwords:" + UtilFuncs._teradata_collapse_arglist(self.stopwords_sequence_column, ""))
        
        if self.categories_sequence_column is not None:
            sequence_input_by_list.append("categories:" + UtilFuncs._teradata_collapse_arglist(self.categories_sequence_column, ""))
        
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
        
        # Process stopwords
        if self.stopwords is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.stopwords, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("stopwords")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.stopwords_order_column, "\""))
        
        # Process categories
        if self.categories is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.categories, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("categories")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.categories_order_column, "\""))
        
        function_name = "NaiveBayesTextClassifierInternal"
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
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__aqg_obj._gen_sqlmr_invocation_sql())
        self.__func_input_dataframe_type.append("TABLE")
        self.__func_input_partition_by_cols.append("1")
        self.__func_input_order_by_cols.append("NA_character_")
        
        # Create instance for mapreduce SQLMR.
        function_name = "NaiveBayesTextClassifierTrainer"
        self.__aqg_obj = AnalyticQueryGenerator(function_name,
                self.__func_input_arg_sql_names, 
                self.__func_input_table_view_query, 
                self.__func_input_dataframe_type, 
                self.__func_input_distribution, 
                self.__func_input_partition_by_cols, 
                self.__func_input_order_by_cols, 
                [], 
                [], 
                [], 
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
        Returns the string representation for a NaiveBayesTextClassifier class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
