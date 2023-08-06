#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Bhavana N (bhavana.n@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.14
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

class TextParser:
    
    def __init__(self,
        data = None,
        text_column = None,
        to_lower_case = True,
        stemming = False,
        delimiter = "[ \\t\\f\\r\\n]+",
        total_words_num = False,
        punctuation = "[.,!?]",
        accumulate = None,
        token_column = "token",
        frequency_column = "frequency",
        total_column = "total_count",
        remove_stop_words = False,
        position_column = "location",
        list_positions = False,
        output_by_word = True,
        stemming_exceptions = None,
        stop_words = None,
        data_sequence_column = None,
        data_order_column = None):
        """
        DESCRIPTION:
            The TextParser function tokenizes an input stream of words, optionally
            stems them (reduces them to their root forms), and then outputs them.
            The function can either output all words in one row or output each
            word in its own row with (optionally) the number of times that the word appears.
            The TextParser function uses Porter2 as the stemming algorithm.
            The TextParser function reads a document into a database memory buffer and
            creates a hash table. The dictionary for the document must not exceed available
            memory; however, a million-word dictionary with an average word length of
            ten bytes requires only 10 MB of memory.
            This function can be used with real-time applications.
            Note: TextParser uses files that are preinstalled on the ML Engine.
                  For details, see Preinstalled Files that functions Use.

        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame that contains the text to be tokenized.

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)

            text_column:
                Required Argument.
                Specifies the name of the input column whose contents are to be
                tokenized.
                Types: str

            to_lower_case:
                Optional Argument.
                Specifies whether to convert input text to lowercase.
                Note: The function ignores this argument, if the "stemming" argument has the value
                      True.
                Default Value: True
                Types: bool

            stemming:
                Optional Argument.
                Specifies whether to stem the tokens that is, whether to apply the
                Porter2 stemming algorithm to each token to reduce it to its root
                form. Before stemming, the function converts the input text to
                lowercase and applies the remove_stop_words argument.
                Default Value: False
                Types: bool

            delimiter:
                Optional Argument.
                Specifies a regular expression that represents the word delimiter.
                Default Value: [ \\t\\f\\r\\n]+
                Types: str

            total_words_num:
                Optional Argument.
                Specifies whether to output a column that contains the total number
                of words in the input document.
                Default Value: False
                Types: bool

            punctuation:
                Optional Argument.
                Specifies a regular expression that represents the punctuation
                characters to remove from the input text. With stemming (True), the
                recommended value is "[\\\[.,?!:;~()\\\]]+".
                Default Value: [.,!?]
                Types: str

            accumulate:
                Optional Argument.
                Specifies the names of the input columns to copy to the output teradataml DataFrame.
                By default, the function copies all input columns to the output
                teradtaml DataFrame.
                Note: No accumulate column can be the same as token_column or
                      total_column.
                Types: str OR list of Strings (str)

            token_column:
                Optional Argument.
                Specifies the name of the output column that contains the tokens.
                Default Value: token
                Types: str

            frequency_column:
                Optional Argument.
                Specifies the name of the output column that contains the frequency
                of each token.
                Default Value: frequency
                Types: str

            total_column:
                Optional Argument.
                Specifies the name of the output column that contains the total
                number of words in the input document.
                Default Value: total_count
                Types: str

            remove_stop_words:
                Optional Argument.
                Specifies whether to remove stop words from the input text before
                parsing.
                Default Value: False
                Types: bool

            position_column:
                Optional Argument.
                Specifies the name of the output column that contains the position of
                a word within a document.
                Default Value: location
                Types: str

            list_positions:
                Optional Argument.
                Specifies whether to output the position of a word in list form.
                If the value is True, the function to output a row for each occurrence of the
                word.
                Note: The function ignores this argument if the output_by_word
                      argument has the value False.
                Default Value: False
                Types: bool

            output_by_word:
                Optional Argument.
                Specifies whether to output each token of each input document in its
                own row in the output teradataml DataFrame. If you specify False, then the
                function outputs each tokenized input document in one row of the
                output teradataml DataFrame.
                Default Value: True
                Types: bool

            stemming_exceptions:
                Optional Argument.
                Specifies the location of the file that contains the stemming
                exceptions. A stemming exception is a word followed by its stemmed
                form. The word and its stemmed form are separated by white space.
                Each stemming exception is on its own line in the file.
                For example: bias bias news news goods goods lying lie ugly ugli sky sky early
                earli
                The words "lying", "ugly", and "early" are to become "lie",
                "ugli", and "earli", respectively. The other words are not to change.
                Types: str

            stop_words:
                Optional Argument.
                Specifies the location of the file that contains the stop words
                (words to ignore when parsing text). Each stop word is on its own
                line in the file.
                For example: a an the and this with but will
                Types: str

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of TextParser.
            Output teradataml DataFrames can be accessed using attribute
            references, such as TextParserObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load example data.
            load_example_data("textparser", ["complaints","complaints_mini"])

            # Create teradataml DataFrame objects.
            complaints = DataFrame.from_table("complaints")
            complaints_mini = DataFrame.from_table("complaints_mini")

            # Example 1 - StopWords without StemmingExceptions
            text_parser_out1 = TextParser(data = complaints,
                                     text_column = "text_data",
                                     to_lower_case = True,
                                     stemming = False,
                                     punctuation = "\\\\[.,?\\\\!\\\\]",
                                     accumulate = ["doc_id","category"],
                                     remove_stop_words = True,
                                     list_positions = True,
                                     output_by_word = True,
                                     stop_words = "stopwords.txt"
                                     )
            # Print the result DataFrame.
            print(text_parser_out1.result)

            # Example 2 - StemmingExceptions without StopWords
            text_parser_out2 = TextParser(data = complaints_mini,
                                     text_column = "text_data",
                                     to_lower_case = True,
                                     stemming = True,
                                     punctuation = "\\\\[.,?\\\\!\\\\]",
                                     accumulate = ["doc_id","category"],
                                     output_by_word = False,
                                     stemming_exceptions = "stemmingexception.txt"
                                     )

            # Print the result DataFrame.
            print(text_parser_out2.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.text_column  = text_column 
        self.to_lower_case  = to_lower_case 
        self.stemming  = stemming 
        self.delimiter  = delimiter 
        self.total_words_num  = total_words_num 
        self.punctuation  = punctuation 
        self.accumulate  = accumulate 
        self.token_column  = token_column 
        self.frequency_column  = frequency_column 
        self.total_column  = total_column 
        self.remove_stop_words  = remove_stop_words 
        self.position_column  = position_column 
        self.list_positions  = list_positions 
        self.output_by_word  = output_by_word 
        self.stemming_exceptions  = stemming_exceptions 
        self.stop_words  = stop_words 
        self.data_sequence_column  = data_sequence_column 
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["text_column", self.text_column, False, (str)])
        self.__arg_info_matrix.append(["to_lower_case", self.to_lower_case, True, (bool)])
        self.__arg_info_matrix.append(["stemming", self.stemming, True, (bool)])
        self.__arg_info_matrix.append(["delimiter", self.delimiter, True, (str)])
        self.__arg_info_matrix.append(["total_words_num", self.total_words_num, True, (bool)])
        self.__arg_info_matrix.append(["punctuation", self.punctuation, True, (str)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["token_column", self.token_column, True, (str)])
        self.__arg_info_matrix.append(["frequency_column", self.frequency_column, True, (str)])
        self.__arg_info_matrix.append(["total_column", self.total_column, True, (str)])
        self.__arg_info_matrix.append(["remove_stop_words", self.remove_stop_words, True, (bool)])
        self.__arg_info_matrix.append(["position_column", self.position_column, True, (str)])
        self.__arg_info_matrix.append(["list_positions", self.list_positions, True, (bool)])
        self.__arg_info_matrix.append(["output_by_word", self.output_by_word, True, (bool)])
        self.__arg_info_matrix.append(["stemming_exceptions", self.stemming_exceptions, True, (str)])
        self.__arg_info_matrix.append(["stop_words", self.stop_words, True, (str)])
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
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.text_column, "text_column")
        self.__awu._validate_dataframe_has_argument_columns(self.text_column, "text_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        # Validate that value passed to the output column argument is not empty.
        self.__awu._validate_input_columns_not_empty(self.token_column, "token_column")
        self.__awu._validate_input_columns_not_empty(self.frequency_column, "frequency_column")
        self.__awu._validate_input_columns_not_empty(self.total_column, "total_column")
        self.__awu._validate_input_columns_not_empty(self.position_column, "position_column")
        
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
        
        self.__func_other_arg_sql_names.append("TextColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.text_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.to_lower_case is not None and self.to_lower_case != True:
            self.__func_other_arg_sql_names.append("ToLowerCase")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.to_lower_case, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.stemming is not None and self.stemming != False:
            self.__func_other_arg_sql_names.append("Stemming")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.stemming, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.output_by_word is not None and self.output_by_word != True:
            self.__func_other_arg_sql_names.append("OutputByWord")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_by_word, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.stemming_exceptions is not None:
            self.__func_other_arg_sql_names.append("StemmingExceptions")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.stemming_exceptions, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.remove_stop_words is not None and self.remove_stop_words != False:
            self.__func_other_arg_sql_names.append("RemoveStopWords")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.remove_stop_words, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.stop_words is not None:
            self.__func_other_arg_sql_names.append("StopWords")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.stop_words, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.delimiter is not None and self.delimiter != "[ \\t\\f\\r\\n]+":
            self.__func_other_arg_sql_names.append("Delimiter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.delimiter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.total_words_num is not None and self.total_words_num != False:
            self.__func_other_arg_sql_names.append("TotalWordsNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.total_words_num, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.punctuation is not None and self.punctuation != "[.,!?]":
            self.__func_other_arg_sql_names.append("Punctuation")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.punctuation, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.list_positions is not None and self.list_positions != False:
            self.__func_other_arg_sql_names.append("ListPositions")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.list_positions, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.token_column is not None and self.token_column != "token":
            self.__func_other_arg_sql_names.append("TokenColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.token_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.frequency_column is not None and self.frequency_column != "frequency":
            self.__func_other_arg_sql_names.append("FrequencyColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.frequency_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.total_column is not None and self.total_column != "total_count":
            self.__func_other_arg_sql_names.append("TotalColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.total_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.position_column is not None and self.position_column != "location":
            self.__func_other_arg_sql_names.append("PositionColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.position_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
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
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("ANY")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "TextParser"
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
        Returns the string representation for a TextParser class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
