#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Abhinav Sahu (abhinav.sahu@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.8
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

class NGramSplitter:
    
    def __init__(self,
        data = None,
        text_column = None,
        delimiter = "[\s]+",
        grams = None,
        overlapping = True,
        to_lower_case = True,
        punctuation = "`~#^&*()-",
        reset = ".,?!",
        total_gram_count = False,
        total_count_column = "totalcnt",
        accumulate = None,
        n_gram_column = "ngram",
        num_grams_column = "n",
        frequency_column = "frequency",
        data_order_column = None):
        """
        DESCRIPTION:
            The NGramSplitter function tokenizes (splits) an input stream of text and 
            outputs n multigrams (called n-grams) based on the specified 
            delimiter and reset parameters. NGramSplitter provides more flexibility than 
            standard tokenization when performing text analysis. Many two-word 
            phrases carry important meaning (for example, "machine learning") 
            that unigrams (single-word tokens) do not capture. This, combined 
            with additional analytical techniques, can be useful for performing 
            sentiment analysis, topic identification and document classification.
         
            Note: This function is only available when teradataml is connected
                  to Vantage 1.1 or later versions.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies input teradataml DataFrame, where each row contains a document 
                to be tokenized. The input teradataml DataFrame can have additional rows, 
                some or all of which the function returns in the output table.
            
            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple columns are 
                used for ordering.
                Types: str OR list of Strings (str)
            
            text_column:
                Required Argument.
                Specifies the name of the column that contains the input text. The column 
                must have a SQL string data type.
                Types: str
            
            delimiter:
                Optional Argument.
                Specifies a character or string that separates words in the input text. The 
                default value is the set of all whitespace characters which includes 
                the characters for space, tab, newline, carriage return and some others.
                Default Value: "[\s]+"
                Types: str
            
            grams:
                Required Argument.
                Specifies a list of integers or ranges of integers that specify the length, in 
                words, of each n-gram (that is, the value of n). A range of values has 
                the syntax integer1 - integer2, where integer1 <= integer2. The values 
                of n, integer1, and integer2 must be positive.
                Types: str OR list of strs
            
            overlapping:
                Optional Argument.
                Specifies whether the function allows overlapping n-grams. 
                When this value is "True", each word in each sentence starts an n-gram, if 
                enough words follow it (in the same sentence) to form a whole n-gram of the 
                specified size. For information on sentences, see the description of the 
                reset argument.
                Default Value: True
                Types: bool
            
            to_lower_case:
                Optional Argument.
                Specifies whether the function converts all letters in the input text 
                to lowercase. 
                Default Value: True
                Types: bool
            
            punctuation:
                Optional Argument.
                Specifies the punctuation characters for the function to remove before 
                evaluating the input text.
                Default Value: "`~#^&*()-"
                Types: str
            
            reset:
                Optional Argument.
                Specifies the character or string that ends a sentence. 
                At the end of a sentence, the function discards any partial n-grams and 
                searches for the next n-gram at the beginning of the next sentence. 
                An n-gram cannot span two sentences.
                Default Value: ".,?!"
                Types: str
            
            total_gram_count:
                Optional Argument.
                Specifies whether the function returns the total number of n-grams in the 
                document (that is, in the row). If you specify "True", then the name of the 
                returned column is specified by the total_count_column argument. 
                Note: The total number of n-grams is not necessarily the number of unique n-grams.
                Default Value: False
                Types: bool
            
            total_count_column:
                Optional Argument.
                Specifies the name of the column to return if the value of the total_gram_count 
                argument is "True". 
                Default Value: "totalcnt"
                Types: str
            
            accumulate:
                Optional Argument.
                Specifies the names of the columns to return for each n-gram. These columns 
                cannot have the same names as those specified by the arguments n_gram_column, 
                num_grams_column, and total_count_column. By default, the function 
                returns all input columns for each n-gram.
                Types: str OR list of Strings (str)
            
            n_gram_column:
                Optional Argument.
                Specifies the name of the column that is to contain the generated n-grams. 
                Default Value: "ngram"
                Types: str
            
            num_grams_column:
                Optional Argument.
                Specifies the name of the column that is to contain the length of n-gram (in 
                words). 
                Default Value: "n"
                Types: str
            
            frequency_column:
                Optional Argument.
                Specifies the name of the column that is to contain the count of each unique 
                n-gram (that is, the number of times that each unique n-gram appears 
                in the document). 
                Default Value: "frequency"
                Types: str
         
        RETURNS:
            Instance of NgramSplitter.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as NgramSplitterObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("NGrams","paragraphs_input")
            
            # Create teradataml DataFrame
            paragraphs_input = DataFrame.from_table("paragraphs_input")
            
            # Example 1
            # Creates output for tokenized data on grams values
            NGramSplitter_out1 = NGramSplitter(data=paragraphs_input,
                                text_column='paratext',
                                delimiter = " ",
                                grams = "4-6",
                                overlapping=True,
                                to_lower_case=True,
                                total_gram_count=True,
                                accumulate=['paraid','paratopic']
                                )
         
            # Print the result DataFrame
            print(NGramSplitter_out1.result)
         
            # Example 2
            # Creates total count column with default column totalcnt if total_gram_count is specified as False
            NGramSplitter_out2 = NGramSplitter(data = paragraphs_input,
                                text_column='paratext',
                                delimiter = " ",
                                grams = "4-6",
                                overlapping=False,
                                to_lower_case=True,
                                total_gram_count=False,
                                accumulate=['paraid','paratopic']
                               )
            
            # Print the result DataFrame
            print(NGramSplitter_out2.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.text_column  = text_column 
        self.delimiter  = delimiter 
        self.grams  = grams 
        self.overlapping  = overlapping 
        self.to_lower_case  = to_lower_case 
        self.punctuation  = punctuation 
        self.reset  = reset 
        self.total_gram_count  = total_gram_count 
        self.total_count_column  = total_count_column 
        self.accumulate  = accumulate 
        self.n_gram_column  = n_gram_column 
        self.num_grams_column  = num_grams_column 
        self.frequency_column  = frequency_column 
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["text_column", self.text_column, False, (str)])
        self.__arg_info_matrix.append(["delimiter", self.delimiter, True, (str)])
        self.__arg_info_matrix.append(["grams", self.grams, False, (str,list)])
        self.__arg_info_matrix.append(["overlapping", self.overlapping, True, (bool)])
        self.__arg_info_matrix.append(["to_lower_case", self.to_lower_case, True, (bool)])
        self.__arg_info_matrix.append(["punctuation", self.punctuation, True, (str)])
        self.__arg_info_matrix.append(["reset", self.reset, True, (str)])
        self.__arg_info_matrix.append(["total_gram_count", self.total_gram_count, True, (bool)])
        self.__arg_info_matrix.append(["total_count_column", self.total_count_column, True, (str)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["n_gram_column", self.n_gram_column, True, (str)])
        self.__arg_info_matrix.append(["num_grams_column", self.num_grams_column, True, (str)])
        self.__arg_info_matrix.append(["frequency_column", self.frequency_column, True, (str)])
        
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
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        # Validate that value passed to the output column argument is not empty.
        self.__awu._validate_input_columns_not_empty(self.n_gram_column, "n_gram_column")
        self.__awu._validate_input_columns_not_empty(self.num_grams_column, "num_grams_column")
        self.__awu._validate_input_columns_not_empty(self.frequency_column, "frequency_column")
        self.__awu._validate_input_columns_not_empty(self.total_count_column, "total_count_column")
        
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
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.text_column, "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.accumulate, "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("Grams")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.grams, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.overlapping is not None and self.overlapping != True:
            self.__func_other_arg_sql_names.append("OverLapping")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.overlapping, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.to_lower_case is not None and self.to_lower_case != True:
            self.__func_other_arg_sql_names.append("ConvertToLowerCase")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.to_lower_case, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.delimiter is not None and self.delimiter != " ":
            self.__func_other_arg_sql_names.append("Delimiter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.delimiter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.punctuation is not None and self.punctuation != "`~#^&*()-":
            self.__func_other_arg_sql_names.append("Punctuation")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.punctuation, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.reset is not None and self.reset != ".,?!":
            self.__func_other_arg_sql_names.append("Reset")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.reset, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.total_gram_count is not None and self.total_gram_count != False:
            self.__func_other_arg_sql_names.append("OutputTotalGramCount")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.total_gram_count, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.n_gram_column is not None and self.n_gram_column != "ngram":
            self.__func_other_arg_sql_names.append("NGramColName")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.n_gram_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.num_grams_column is not None and self.num_grams_column != "n":
            self.__func_other_arg_sql_names.append("GramLengthColName")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.num_grams_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.frequency_column is not None and self.frequency_column != "frequency":
            self.__func_other_arg_sql_names.append("FrequencyColName")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.frequency_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.total_count_column is not None and self.total_count_column != "totalcnt":
            self.__func_other_arg_sql_names.append("TotalCountColName")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.total_count_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        
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
        
        function_name = "ngramsplitter"
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
                engine="ENGINE_SQL")
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
        Returns the string representation for a NgramSplitter class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
