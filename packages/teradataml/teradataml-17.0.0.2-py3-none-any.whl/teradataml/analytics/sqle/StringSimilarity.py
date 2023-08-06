#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Rohit Khurd (rohit.khurd@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.1
# Function Version: 1.0
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

class StringSimilarity:
    
    def __init__(self,
        data = None,
        comparison_columns = None,
        case_sensitive = None,
        accumulate = None,
        data_order_column = None):
        """
        DESCRIPTION:
            The StringSimilarity function calculates the similarity between two
            strings, using the specified comparison method.
            The similarity is a value in the range [0, 1].
         
            Note: This function is only available when teradataml is connected
                  to Vantage 1.1 or later versions.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame that contains the string pairs
                to be compared.
            
            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            comparison_columns:
                Required Argument.
                Specifies pairs of input teradataml DataFrame columns that contain 
                strings to be compared (column1 and column2), how to compare them 
                (comparison_type), and (optionally) a constant and the name of the 
                output column for their similarity (output_column). The similarity is 
                a value in the range [0, 1].
                For comparison_type, use one of these values:
                    * "jaro": Jaro distance.
                    * "jaro_winkler": Jaro-Winkler distance (1 for an exact match, 0 otherwise).
                      If you specify this comparison type, you can specify the value of
                      factor p with constant. 0 ≤ p ≤ 0.25.
                      Default: p = 0.1
                    * "n_gram": N-gram similarity.
                      If you specify this comparison type, you can specify the value of N with
                      constant.
                      Default: N = 2
                    * "LD": Levenshtein distance
                      The number of edits needed to transform one string into the other,
                      where edits include insertions, deletions, or substitutions of
                      individual characters.
                    * "LDWS": Levenshtein distance without substitution.
                      Number of edits needed to transform one string into the other using only
                      insertions or deletions of individual characters.
                    * "OSA": Optimal string alignment distance.
                      Number of edits needed to transform one string into the other.
                      Edits are insertions, deletions, substitutions, or transpositions of
                      characters. A substring can be edited only once.
                    * "DL": Damerau-Levenshtein distance.
                      Like OSA, except that a substring can be edited any number of times.
                    * "hamming": Hamming distance.
                      Number of positions where corresponding characters differ (that is,
                      minimum number of substitutions needed to transform one string into the
                      other) for strings of equal length, otherwise -1 for strings of unequal
                      length.
                    * "LCS": Longest common substring.
                      Length of longest substring common to both strings.
                    * "jaccard": Jaccard index-based comparison.
                    * "cosine": Cosine similarity.
                    * "soundexcode": Only for English strings. -1 if either string has a
                      non-English character, otherwise, 1 if their soundex codes are the same
                      and 0 otherwise.
                You can specify a different comparison_type for every pair of columns.
                The default output_column is "sim_i", where i is the sequence number of the
                column pair.
                Types: str OR list of strs
            
            case_sensitive:
                Optional Argument.
                Specifies whether string comparison is case-sensitive.
                You can specify either one value for all pairs or
                one value for each pair. If you specify one value for each pair, then 
                the ith value applies to the ith pair.
                Default value: "False".
                Types: bool OR list of bools
            
            accumulate:
                Optional Argument.
                Specifies the names of input teradataml DataFrame columns to be 
                copied to the output teradataml DataFrame.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of StringSimilarity.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as StringSimilarityObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("stringsimilarity", "strsimilarity_input")
         
            # Create teradataml DataFrame objects.
            strsimilarity_input = DataFrame.from_table("strsimilarity_input")
         
            # Example -
            stringsimilarity_out = StringSimilarity(data = strsimilarity_input,
                                                    comparison_columns=['jaro (src_text1, tar_text) AS jaro1_sim',
                                                                        'LD (src_text1, tar_text) AS ld1_sim',
                                                                        'n_gram (src_text1, tar_text, 2) AS ngram1_sim',
                                                                        'jaro_winkler (src_text1, tar_text, 0.1) AS jw1_sim'],
                                                    case_sensitive = True,
                                                    accumulate = ["id","src_text1","tar_text"]
                                                   )
         
            # Print result DataFrame.
            print(stringsimilarity_out.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.comparison_columns  = comparison_columns 
        self.case_sensitive  = case_sensitive 
        self.accumulate  = accumulate 
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["comparison_columns", self.comparison_columns, False, (str,list)])
        self.__arg_info_matrix.append(["case_sensitive", self.case_sensitive, True, (bool,list)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        
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
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        
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
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.accumulate, "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("ComparisonColumnPairs")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.comparison_columns, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.case_sensitive is not None:
            self.__func_other_arg_sql_names.append("Casesensitive")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.case_sensitive, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        
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
        
        function_name = "StringSimilarity"
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
        Returns the string representation for a StringSimilarity class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
