#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2020 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Rohit Agrawal (rohit.agrawal@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.2
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

class NaiveBayesTextClassifier2:
    
    def __init__(self,
        data = None,
        stopwords = None,
        doc_category_column = None,
        text_column = None,
        model_type = "MULTINOMIAL",
        doc_id_column = None,
        is_tokenized = True,
        convert_to_lower_case = False,
        stem_tokens = True,
        handle_nulls = False,
        data_sequence_column = None,
        stopwords_sequence_column = None):
        """
        DESCRIPTION:
            The NaiveBayesTextClassifier2 function takes training data as
            input and outputs a model teradataml DataFrame. Training data can be
            in the form of either documents or tokens.
            Note:
                1. This function is supported on Vantage 1.3 or later.
                2. Teradata recommends to use NaiveBayesTextClassifier2 instead
                   of NaiveBayesTextClassifier on Vantage 1.3 or later.
        
        
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame defining the training texts or tokens.
            
            stopwords:
                Optional Argument when "is_tokenized" is 'False', disallowed otherwise.
                Specifies the teradataml DataFrame defining the stop words.
            
            doc_category_column:
                Required Argument.
                Specifies the name of the column in "data" teradataml DataFrame that
                contains the document category.
                Types: str
            
            text_column:
                Required Argument.
                Specifies the name of the column in "data" teradataml DataFrame that
                contains the texts or tokens to classify.
                Types: str
            
            model_type:
                Optional Argument.
                Specifies the model type of the text classifier.
                Default Value: "MULTINOMIAL"
                Permitted Values: MULTINOMIAL, BERNOULLI
                Types: str
            
            doc_id_column:
                Optional Argument. Required if "model_type" is 'BERNOULLI'.
                Specifies the name of the column in "data" teradataml DataFrame that
                contain the document identifier.
                Types: str
            
            is_tokenized:
                Optional Argument.
                Specifies whether the input data is tokenized or not.
                When it is set to 'True', input data is tokenized, otherwise input data
                is not tokenized and will be tokenized internally.
                Note:
                    Specifying "is_tokenized" to 'True' with untokenized input data
                    may result in an ambiguous or meaningless model.
                Default Value: True
                Types: bool
            
            convert_to_lower_case:
                Optional Argument when "is_tokenized" is 'False', disallowed otherwise.
                Specifies whether to convert all letters in the input text to lowercase.
                Default Value: False
                Types: bool
            
            stem_tokens:
                Optional Argument when "is_tokenized" is 'False', disallowed otherwise.
                Specifies whether to stem the tokens as part of text tokenization.
                Default Value: True
                Types: bool
            
            handle_nulls:
                Optional Argument.
                Specifies whether to remove null values from input data before processing.
                If the input data contains no null values, setting "handle_nulls" to 'False'
                improves performance.
                Default Value: False
                Types: bool
            
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
        
        RETURNS:
            Instance of NaiveBayesTextClassifier2.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as 
            NaiveBayesTextClassifier2Obj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. model_data
                2. output
        
        
        RAISES:
            TeradataMlException, TypeError, ValueError
        
        
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("NaiveBayesTextClassifier2","complaints")

            # Create teradataml DataFrame.
            complaints = DataFrame.from_table("complaints")

            # Example 1 - "is_tokenized" set to 'False'
            # This function uses the untokenized input 'complaints' to create the
            # Bernoulli model and the data is internally tokenized.
            nbt2_result1 = NaiveBayesTextClassifier2(data=complaints,
                                                  doc_category_column='category',
                                                  text_column='text_data',
                                                  doc_id_column='doc_id',
                                                  model_type='BERNOULLI',
                                                  is_tokenized=False
                                                  )

            # Print the model_data DataFrame.
            print(nbt2_result1.model_data)

            # Print the output DataFrame.
            print(nbt2_result1.output)

            # Example 2 - "is_tokenized" set to 'True'
            # The input teradataml DataFrame 'complaints' is tokenized using
            # TextTokenizer function.
            complaints_tokenized = TextTokenizer(data=complaints,
                                               text_column='text_data',
                                               language='en',
                                               output_delimiter=' ',
                                               output_byword =True,
                                               accumulate=['doc_id', 'category'])

            # This function uses the tokenized input 'complaints_tokenized' to
            # create the Bernoulli model.
            nbt2_result2 = NaiveBayesTextClassifier2(data=complaints_tokenized.result,
                                                  doc_category_column='category',
                                                  text_column='token',
                                                  doc_id_column='doc_id',
                                                  model_type='BERNOULLI',
                                                  is_tokenized=True
                                                  )

            # Print the model_data DataFrame.
            print(nbt2_result2.model_data)

            # Print the output DataFrame.
            print(nbt2_result2.output)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.stopwords  = stopwords 
        self.doc_category_column  = doc_category_column 
        self.text_column  = text_column 
        self.model_type  = model_type 
        self.doc_id_column  = doc_id_column 
        self.is_tokenized  = is_tokenized 
        self.convert_to_lower_case  = convert_to_lower_case 
        self.stem_tokens  = stem_tokens 
        self.handle_nulls  = handle_nulls 
        self.data_sequence_column  = data_sequence_column 
        self.stopwords_sequence_column  = stopwords_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["stopwords", self.stopwords, True, (DataFrame)])
        self.__arg_info_matrix.append(["doc_category_column", self.doc_category_column, False, (str)])
        self.__arg_info_matrix.append(["text_column", self.text_column, False, (str)])
        self.__arg_info_matrix.append(["model_type", self.model_type, True, (str)])
        self.__arg_info_matrix.append(["doc_id_column", self.doc_id_column, True, (str)])
        self.__arg_info_matrix.append(["is_tokenized", self.is_tokenized, True, (bool)])
        self.__arg_info_matrix.append(["convert_to_lower_case", self.convert_to_lower_case, True, (bool)])
        self.__arg_info_matrix.append(["stem_tokens", self.stem_tokens, True, (bool)])
        self.__arg_info_matrix.append(["handle_nulls", self.handle_nulls, True, (bool)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["stopwords_sequence_column", self.stopwords_sequence_column, True, (str,list)])
        
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
        
        # Check for permitted values
        model_type_permitted_values = ["MULTINOMIAL", "BERNOULLI"]
        self.__awu._validate_permitted_values(self.model_type, model_type_permitted_values, "model_type")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.doc_category_column, "doc_category_column")
        self.__awu._validate_dataframe_has_argument_columns(self.doc_category_column, "doc_category_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.text_column, "text_column")
        self.__awu._validate_dataframe_has_argument_columns(self.text_column, "text_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.doc_id_column, "doc_id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.doc_id_column, "doc_id_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.stopwords_sequence_column, "stopwords_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.stopwords_sequence_column, "stopwords_sequence_column", self.stopwords, "stopwords", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__model_data_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_naivebayestextclassifiertrainer20", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["ModelTable"]
        self.__func_output_args = [self.__model_data_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("DocCategoryColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.doc_category_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("TextColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.text_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.doc_id_column is not None:
            self.__func_other_arg_sql_names.append("DocIdColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.doc_id_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.model_type is not None and self.model_type != "MULTINOMIAL":
            self.__func_other_arg_sql_names.append("ModelType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.model_type, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.is_tokenized is not None and self.is_tokenized != True:
            self.__func_other_arg_sql_names.append("IsTokenized")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.is_tokenized, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.convert_to_lower_case is not None and self.convert_to_lower_case != False:
            self.__func_other_arg_sql_names.append("ConvertToLowerCase")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.convert_to_lower_case, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.stem_tokens is not None and self.stem_tokens != True:
            self.__func_other_arg_sql_names.append("StemTokens")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.stem_tokens, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.handle_nulls is not None and self.handle_nulls != False:
            self.__func_other_arg_sql_names.append("NullHandling")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.handle_nulls, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.stopwords_sequence_column is not None:
            sequence_input_by_list.append("StopwordsTable:" + UtilFuncs._teradata_collapse_arglist(self.stopwords_sequence_column, ""))
        
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
        
        # Process stopwords
        if self.stopwords is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.stopwords, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("StopwordsTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "NaiveBayesTextClassifierTrainer2"
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
        self.model_data = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__model_data_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__model_data_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.model_data)
        self._mlresults.append(self.output)
        
    def show_query(self):
        """
        Function to return the underlying SQL query.
        When model object is created using retrieve_model(), the value returned will be None.
        """
        return self.sqlmr_query
        
    def get_prediction_type(self):
        """
        Function to return the Prediction type of the algorithm.
        When model object is created using retrieve_model(), the value returned may be None.
        """
        return self._prediction_type
        
    def get_target_column(self):
        """
        Function to return the Target Column of the algorithm.
        When model object is created using retrieve_model(), the value returned may be None.
        """
        return self._target_column
        
    def get_build_time(self):
        """
        Function to return the build time of the algorithm in seconds.
        When model object is created using retrieve_model(), the value returned may be None.
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
        model_data = None,
        output = None,
        **kwargs):
        """
        Classmethod which will be used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("model_data", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.model_data  = model_data 
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
        obj.model_data = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.model_data), source_type="table", database_name=UtilFuncs._extract_db_name(obj.model_data))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.model_data)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a NaiveBayesTextClassifier2 class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ model_data Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.model_data)
        return repr_string
        
