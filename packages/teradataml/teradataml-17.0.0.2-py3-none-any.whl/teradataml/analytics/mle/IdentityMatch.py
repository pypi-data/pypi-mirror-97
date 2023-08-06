#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Rohit Agrawal (rohit.agrawal@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.13
# 
# ################################################################## 

import inspect
import time
import itertools
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

class IdentityMatch:
    
    def __init__(self,
        source_data = None,
        reference_data = None,
        source_id_column=None,
        reference_id_column=None,
        source_nominalmatch_columns=None,
        reference_nominalmatch_columns=None,
        fuzzymatch_columns = None,
        threshold = 0.5,
        source_accumulate=None,
        reference_accumulate=None,
        source_data_sequence_column = None,
        reference_data_sequence_column = None,
        source_data_partition_column = "ANY",
        reference_data_partition_column = None,
        source_data_order_column = None,
        reference_data_order_column = None,
        handle_nulls = "mismatch"):
        """
        DESCRIPTION:
            The IdentityMatch function tries to match source data with reference 
            data, using specified attributes to calculate the similarity score of
            each source-reference pair, and then computes the final similarity score.
            Typically, the source data is about business customers and the reference
            data is from external sources, such as online forums and social networking
            services. The IdentityMatch function is designed to help determine if customers
            with similar identifiers are the same customer. The function supports both
            nominal (exact) matching and weighted fuzzy matching.

        PARAMETERS:
            source_data:
                Required Argument.
                Specifies the source input teradataml DataFrame.
            
            source_data_partition_column:
                Optional Argument.
                Specifies Partition By columns for source_data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
            
            source_data_order_column:
                Optional Argument.
                Specifies Order By columns for source_data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
            
            reference_data:
                Required Argument.
                Specifies the reference input teradataml DataFrame.
            
            reference_data_partition_column:
                Optional Argument.
                Specifies Partition By columns for reference_data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for partition.
                Types: str OR list of Strings (str)
            
            reference_data_order_column:
                Optional Argument.
                Specifies Order By columns for reference_data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
            
            source_id_column:
                Required Argument.
                Specifies the name of the column in the source_data DataFrame
                that contain row identifiers. The function copies this column
                to the output DataFrame.
                Types: str

            reference_id_column:
                Required Argument.
                Specifies the name of the column in the reference_data DataFrame
                that contain row identifiers. The function copies this column
                to the output DataFrame.
                Types: str
            
            source_nominalmatch_columns:
                Optional Argument. Required if you omit fuzzymatch_columns.
                Specifies the names of the columns (attributes) in the source_data DataFrame
                to check for exact matching with the columns specified in
                reference_nominalmatch_columns. If any pair (a column in source_nominalmatch_columns
                and a column in reference_nominalmatch_columns argument) matches exactly,
                then their records are considered to be exact matches, and the function
                does not compare the fuzzy match attributes.
                Note:
                    1. If this argument is provided, the 'reference_nominalmatch_columns' argument
                       should also be provided.
                    2. The number of columns provided in the 'source_nominalmatch_columns' and
                    'reference_nominalmatch_columns' arguments should be equal.
                Types: str OR list of Strings (str)

            reference_nominalmatch_columns:
                Optional Argument. Required if you omit fuzzymatch_columns.
                Specifies the names of the columns (attributes) in the reference_data DataFrame
                to check for exact matching with the columns specified in
                source_nominalmatch_columns. If any pair (a column in source_nominalmatch_columns
                and a column in reference_nominalmatch_columns argument) matches exactly,
                then their records are considered to be exact matches, and the function
                does not compare the fuzzy match attributes.
                Note:
                    1. If this argument is provided, the 'source_nominalmatch_columns' argument
                       should also be provided.
                    2. The number of columns provided in the 'source_nominalmatch_columns' and
                    'reference_nominalmatch_columns' arguments should be equal.
                Types: str OR list of Strings (str)
            
            fuzzymatch_columns:
                Optional Argument. Required if you omit source_nominalmatch_columns and
                reference_nominalmatch_columns.
                Specifies the names of source_data and reference_data columns (attributes)
                and the fuzzy matching parameters match_metric, match_weight, and
                synonym_file (whose descriptions follow). If any pair is a fuzzy match,
                then their records are considered to be fuzzy matches, and the function
                reports the similarity score of these attributes.
                Fuzzy matching parameters:
                1. match_metric:
                   This parameter specifies the similarity metric, which is a function that
                   returns the similarity score (a value between 0 and 1) of two strings.
                   The possible values of match_metric are:
                    * EQUAL: If strings a and b are equal, then their similarity score
                      is 1.0; otherwise it 0.0.
                    * LD: The similarity score of strings a and b is
                      f(a,b)=LD(a,b)/max(len(a),len(b)), where LD(a,b) is the Levenshtein
                      distance between a with b.
                    * D-LD: The similarity score of strings a and b is
                      f(a,b)=LD(a,b)/max(len(a),len(b)), where LD(a,b) is the Damerau-Levenshtein
                      distance between a and b.
                    * JARO: The similarity score of strings a and b is the Jaro distance
                      between them.
                    * JARO-WINKLER: The similarity score of strings a and b
                      is the Jaro-Winkler distance between them.
                    * NEEDLEMAN-WUNSCH: The similarity score of strings a and b is the
                      Needleman-Wunsch distance between them.
                    * JD: The similarity score of strings a and b is the Jaccard distance
                      between them. The function converts the strings a and b to sets s and t
                      by splitting them by space and then uses the formula f(s,t)=|S intersection T|/|s union t|.
                    * COSINE: The similarity score of strings a and b is calculated with
                      their term frequency-inverse document frequency (TF-IDF) and cosine
                      similarity.
                      Note: The function calculates IDF only on the input relation stored in memory.
                2. match_weight:
                   This parameter specifies the weight (relative importance) of the attribute
                   represented by source_data and reference_data columns.
                   The match_weight must be a positive number. The function normalizes each
                   match_weight to a value in the range [0, 1]. Given match_weight values,
                   w1, w2, ..., wn, the normalized value of wi is: wi /(w1+w2+...+ wn).
                   For example, given two pairs of columns, whose match weights are 3 and 7,
                   the function uses the weights 3/(3+7)=0.3 and 7/(3+7)=0.7 to compute the
                   similarity score.
                3. synonym_file:
                   This parameter (optional) specifies the dictionary that the function
                   uses to check the two strings for semantic equality. In the dictionary,
                   each line is a comma-separated list of synonyms.
                   Note: You must install the dictionary before running the function.
                The dictionary has to be of the following form:
                    {
                        "source_column" : <name of column from source_data>,
                        "reference_column" : <name of column from reference_data>,
                        "match_metric": <value of match_metric>,
                        "match_weight" : <weight of the attribute>,
                        "synonym_file": <name of dictionary for semantic check>
                    }
                where the synonym_file key and associated value are optional. You may pass a
                dictionary or list of dictionaries of the above form as a value to this argument.
                Types: dict OR list of Dictionaries (dict)
            
            threshold:
                Optional Argument.
                Specifies the threshold similarity score, a float value between 0 and 1.
                The function outputs only the records whose similarity score exceeds threshold.
                The higher the threshold, the higher the matching accuracy.
                Default Value: 0.5
                Types: float
            
            source_accumulate:
                Optional Argument.
                Specifies source_data teradataml DataFrame columns to copy to the output
                teradataml DataFrame.
                Types: str OR list of Strings (str)

            reference_accumulate:
                Optional Argument.
                Specifies reference_data teradataml DataFrame columns to copy to the output
                teradataml DataFrame.
                Types: str OR list of Strings (str)
            
            source_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "source_data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)
            
            reference_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "reference_data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)

            handle_nulls:
                Optional Argument.
                Specifies what score should be assigned for null/empty value.
                Note:
                    "handle_nulls" argument support is only available when teradataml
                    is connected to Vantage 1.3 version.
                Default Value: "mismatch"
                Permitted Values: mismatch, match-if-null, match-if-both-null
                Types: str
        
        RETURNS:
            Instance of IdentityMatch.
            Output teradataml DataFrame can be accessed using attribute
            references, such as IdentityMatchObj.<attribute_name>.
            The "result" teradataml DataFrame has column names as "a.<column_name1>"
            and "b.<column_name2>", where:
            1. "a.<column_name1>" refers to "<column_name1>" column of "source_data"
               teradataml DataFrame.
            2. "b.<column_name2>" refers to "<column_name2>" column of "reference_data"
               teradataml DataFrame.
            Output teradataml DataFrame attribute name is:
                result
        
        
        RAISES:
            TeradataMlException, TypeError, ValueError
        
        
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("IdentityMatch", ["applicant_reference", "applicant_external"])

            # Create teradataml DataFrame object.
            applicant_reference = DataFrame.from_table("applicant_reference")
            applicant_external = DataFrame.from_table("applicant_external")

            # Example - Find the credit scores of job applicants by matching the information in teradataml
            # DataFrames 'applicant_reference' and 'applicant_external'.
            # The example looks for exact matches (nominalmatch_columns) to the email address and approximate
            # matches (fuzzymatch_columns) for lastname, firstname, zip code, city, and department, with different
            # match metrics and match weights.
            # source_data: applicant_reference, which has hypothetical information from job applicants.
            # reference_data: applicant_external, an external source table, which has missing and incomplete
            # information, but includes credit scores.
            identitymatch_out = IdentityMatch(source_data=applicant_reference,
                                          source_data_partition_column='ANY',
                                          reference_data=applicant_external,
                                          source_id_column="id",
                                          reference_id_column="id",
                                          source_nominalmatch_columns="email",
                                          reference_nominalmatch_columns="email",
                                          fuzzymatch_columns=[ {"source_column" : "lastname", "reference_column" : "lastname",
                                          "match_metric": "JARO-WINKLER", "match_weight" : 3}, {"source_column" : "firstname",
                                          "reference_column" : "firstname", "match_metric": "JARO-WINKLER", "match_weight" : 2},
                                          {"source_column" : "zipcode", "reference_column" : "zipcode", "match_metric": "JD",
                                          "match_weight" : 2}, {"source_column" : "city", "reference_column" : "city",
                                          "match_metric": "LD", "match_weight" : 2}, {"source_column" : "department",
                                          "reference_column" : "department", "match_metric": "COSINE", "match_weight" : 1}],
                                          threshold=0.5,
                                          source_accumulate=["firstname","lastname","email","zipcode"],
                                          reference_accumulate=["lastname","email","zipcode","department","creditscore"],
                                          source_data_sequence_column='id'
                                          )

            # Print the output DataFrames.
            print(identitymatch_out.result)

        """
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.source_data  = source_data 
        self.reference_data  = reference_data
        self.source_id_column = source_id_column
        self.reference_id_column = reference_id_column
        self.source_nominalmatch_columns = source_nominalmatch_columns
        self.reference_nominalmatch_columns = reference_nominalmatch_columns
        self.fuzzymatch_columns  = fuzzymatch_columns 
        self.threshold  = threshold
        self.source_accumulate = source_accumulate
        self.reference_accumulate = reference_accumulate
        self.source_data_sequence_column  = source_data_sequence_column 
        self.reference_data_sequence_column  = reference_data_sequence_column 
        self.source_data_partition_column  = source_data_partition_column 
        self.reference_data_partition_column  = reference_data_partition_column 
        self.source_data_order_column  = source_data_order_column 
        self.reference_data_order_column  = reference_data_order_column
        self.handle_nulls  = handle_nulls
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["source_data", self.source_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["source_data_partition_column", self.source_data_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["source_data_order_column", self.source_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["reference_data", self.reference_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["reference_data_partition_column", self.reference_data_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["reference_data_order_column", self.reference_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["source_id_column", self.source_id_column, False, (str)])
        self.__arg_info_matrix.append(["reference_id_column", self.reference_id_column, False, (str)])
        self.__arg_info_matrix.append(["source_nominalmatch_columns", self.source_nominalmatch_columns, True, (str, list)])
        self.__arg_info_matrix.append(["reference_nominalmatch_columns", self.reference_nominalmatch_columns, True, (str, list)])
        self.__arg_info_matrix.append(["fuzzymatch_columns", self.fuzzymatch_columns, True, (dict,list)])
        self.__arg_info_matrix.append(["threshold", self.threshold, True, (float)])
        self.__arg_info_matrix.append(["source_accumulate", self.source_accumulate, True, (str, list)])
        self.__arg_info_matrix.append(["reference_accumulate", self.reference_accumulate, True, (str, list)])
        self.__arg_info_matrix.append(["source_data_sequence_column", self.source_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["reference_data_sequence_column", self.reference_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["handle_nulls", self.handle_nulls, True, (str)])
        
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
        self.__awu._validate_input_table_datatype(self.source_data, "source_data", None)
        self.__awu._validate_input_table_datatype(self.reference_data, "reference_data", None)

        # Check for permitted values
        handle_nulls_permitted_values = ["MISMATCH", "MATCH-IF-NULL", "MATCH-IF-BOTH-NULL"]
        self.__awu._validate_permitted_values(self.handle_nulls, handle_nulls_permitted_values, "handle_nulls")

        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.source_id_column, "source_id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.source_id_column, "source_id_column", self.source_data,"source_data", False)

        self.__awu._validate_input_columns_not_empty(self.reference_id_column, "reference_id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.reference_id_column, "reference_id_column", self.reference_data, "reference_data", False)

        self.__awu._validate_input_columns_not_empty(self.source_nominalmatch_columns, "source_nominalmatch_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.source_nominalmatch_columns, "source_nominalmatch_columns", self.source_data, "source_data", False)

        self.__awu._validate_input_columns_not_empty(self.reference_nominalmatch_columns, "reference_nominalmatch_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.reference_nominalmatch_columns, "reference_nominalmatch_columns", self.reference_data, "reference_data", False)

        self.__awu._validate_input_columns_not_empty(self.source_accumulate, "source_accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.source_accumulate, "source_accumulate", self.source_data, "source_data", False)

        self.__awu._validate_input_columns_not_empty(self.reference_accumulate, "reference_accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.reference_accumulate, "reference_accumulate", self.reference_data, "reference_data", False)

        self.__awu._validate_input_columns_not_empty(self.source_data_sequence_column, "source_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.source_data_sequence_column, "source_data_sequence_column", self.source_data, "source_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.reference_data_sequence_column, "reference_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.reference_data_sequence_column, "reference_data_sequence_column", self.reference_data, "reference_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.source_data_partition_column, "source_data_partition_column")
        if self.__awu._is_default_or_not(self.source_data_partition_column, "ANY"):
            self.__awu._validate_dataframe_has_argument_columns(self.source_data_partition_column, "source_data_partition_column", self.source_data, "source_data", True)
        self.__awu._validate_input_columns_not_empty(self.reference_data_partition_column, "reference_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.reference_data_partition_column, "reference_data_partition_column", self.reference_data, "reference_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.source_data_order_column, "source_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.source_data_order_column, "source_data_order_column", self.source_data, "source_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.reference_data_order_column, "reference_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.reference_data_order_column, "reference_data_order_column", self.reference_data, "reference_data", False)

        # Check if source_nominalmatch_columns and reference_nominalmatch_columns arguments are passed together or not.
        if (not self.source_nominalmatch_columns and self.reference_nominalmatch_columns) or \
                (self.source_nominalmatch_columns and not self.reference_nominalmatch_columns):
            raise TeradataMlException(Messages.get_message(MessageCodes.MUST_PASS_ARGUMENT,
                                                           'source_nominalmatch_columns',
                                                           'reference_nominalmatch_columns'),
                                      MessageCodes.MUST_PASS_ARGUMENT)

        if isinstance(self.source_nominalmatch_columns, str):
            self.source_nominalmatch_columns = [self.source_nominalmatch_columns]

        if isinstance(self.reference_nominalmatch_columns, str):
            self.reference_nominalmatch_columns = [self.reference_nominalmatch_columns]

        # source_nominalmatch_columns and reference_nominalmatch_columns arguments length should be equal.
        if self.source_nominalmatch_columns and self.reference_nominalmatch_columns and \
                len(self.source_nominalmatch_columns) != len(self.reference_nominalmatch_columns):
            raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_LENGTH_ARGS,
                                                           "'source_nominalmatch_columns' and 'reference_nominalmatch_columns'"),
                                      MessageCodes.INVALID_LENGTH_ARGS)

        # At least one argument source_nominalmatch_columns and reference_nominalmatch_columns or fuzzymatch_columns must be passed.
        if not self.source_nominalmatch_columns and not self.reference_nominalmatch_columns and not self.fuzzymatch_columns:
            raise TeradataMlException(Messages.get_message(MessageCodes.SPECIFY_AT_LEAST_ONE_ARG,
                                                           "'source_nominalmatch_columns' and 'reference_nominalmatch_columns'",
                                                           "fuzzymatch_columns"),
                                      MessageCodes.SPECIFY_AT_LEAST_ONE_ARG)

        if self.fuzzymatch_columns:
            for _fuzzy_column in self.fuzzymatch_columns:
                # Make sure that key's in each dict is valid string.
                if (sorted(_fuzzy_column.keys()) != ["match_metric", "match_weight", "reference_column", "source_column"] and
                        sorted(_fuzzy_column.keys()) != ["match_metric", "match_weight", "reference_column", "source_column", "synonym_file"]):
                    raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                                                   str(sorted(_fuzzy_column.keys())), 'fuzzymatch_columns',
                                                                   "a dictionary or a list of dictionaries with the following keys ['source_column', 'reference_column', 'match_metric', 'match_weight', 'synonym_file']"),
                                              MessageCodes.INVALID_ARG_VALUE)

                __fuzzy_arg_info_matrix = []
                __fuzzy_arg_info_matrix.append(["source_column: {}".format(_fuzzy_column['source_column']), _fuzzy_column['source_column'], False, (str)])
                __fuzzy_arg_info_matrix.append(["reference_column: {}".format(_fuzzy_column['reference_column']), _fuzzy_column['reference_column'], False, (str)])
                __fuzzy_arg_info_matrix.append(["match_metric: {}".format(_fuzzy_column['match_metric']), _fuzzy_column['match_metric'], False, (str)])
                __fuzzy_arg_info_matrix.append(["match_weight: {}".format(_fuzzy_column['match_weight']), _fuzzy_column['match_weight'], False, (int)])
                if len(_fuzzy_column) == 5:
                    __fuzzy_arg_info_matrix.append(["synonym_file: {}".format(_fuzzy_column['synonym_file']), _fuzzy_column['synonym_file'], True, (str)])

                self.__awu._validate_argument_types(__fuzzy_arg_info_matrix)

                # Check whether the input columns passed to the key's in argument fuzzymatch_columns are not empty.
                # Also check whether the input columns passed to the key's in argument fuzzymatch_columns valid or not.
                self.__awu._validate_input_columns_not_empty(_fuzzy_column['source_column'],
                                                             "'source_column' in fuzzy_matchcolumns")
                self.__awu._validate_dataframe_has_argument_columns(_fuzzy_column['source_column'],
                                                                    "'source_column' in fuzzy_matchcolumns", self.source_data,
                                                                    "source_data", False)

                self.__awu._validate_input_columns_not_empty(_fuzzy_column['reference_column'],
                                                             "'reference_column' in fuzzy_matchcolumns")
                self.__awu._validate_dataframe_has_argument_columns(_fuzzy_column['reference_column'],
                                                                    "'reference_column' in fuzzy_matchcolumns",
                                                                    self.reference_data,
                                                                    "reference_data", False)

                self.__awu._validate_input_columns_not_empty(_fuzzy_column['match_metric'],
                                                             "'match_metric' in fuzzy_matchcolumns")

                # Check for permitted values for match_metric key in argument fuzzymatch_columns
                __match_metric_permitted_values = ["EQUAL", "LD", "D-LD", "JARO", "JARO-WINKLER", "NEEDLEMAN-WUNSCH", "JD", "COSINE"]
                self.__awu._validate_permitted_values(_fuzzy_column['match_metric'], __match_metric_permitted_values, "'match_metric' in fuzzy_matchcolumns")

                if len(_fuzzy_column) == 5:
                    self.__awu._validate_input_columns_not_empty(_fuzzy_column['synonym_file'], "'synonym_file' in fuzzy_matchcolumns")


    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """

        if isinstance(self.fuzzymatch_columns, dict):
            self.fuzzymatch_columns = [self.fuzzymatch_columns]

        # Processing id_column to format "a.source_col_name:b.reference_col_name".
        __id_column = "a.{0}:b.{1}".format(self.source_id_column, self.reference_id_column)

        # Processing nominalmatch_columns to format "a.source_col_name:b.reference_col_name".
        if self.source_nominalmatch_columns and self.reference_nominalmatch_columns:
            __nominalmatch_columns = []
            for __source_nominal_col, __reference_nominal_col in zip(self.source_nominalmatch_columns,self.reference_nominalmatch_columns):
                __nominalmatch_columns.append("a.{0}:b.{1}".format(__source_nominal_col, __reference_nominal_col))

        # Processing accumulate to format "a.source_col_name, b.reference_col_name".
        __accumulate = []
        input_names = ['a', 'b']
        for input_name, column_list in zip(input_names, [self.source_accumulate, self.reference_accumulate]):
            if column_list:
                if isinstance(column_list, str):
                    column_list = [column_list]
                for col in column_list:
                    __accumulate.append("{0}.{1}".format(input_name, col))

        # Processing fuzzymatch_columns to format ['a.source_col_name:b.reference_col_name, match_metric, match_weight'].
        if self.fuzzymatch_columns is not None:
            __fuzzymatch_columns = []
            for _fuzzy_column in self.fuzzymatch_columns:
                __fuzzy_temp = "a.{0}:b.{1}, {2}, {3}".format(_fuzzy_column["source_column"], _fuzzy_column["reference_column"],
                                                            _fuzzy_column["match_metric"], _fuzzy_column["match_weight"])
                if len(_fuzzy_column) == 5:
                    __fuzzy_temp = "{0}, {1}".format(__fuzzy_temp, _fuzzy_column["synonym_file"])
                __fuzzymatch_columns.append(__fuzzy_temp)

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
        
        self.__func_other_arg_sql_names.append("IdColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(__id_column, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")

        if self.source_nominalmatch_columns is not None and self.reference_nominalmatch_columns is not None:
            self.__func_other_arg_sql_names.append("NominalMatchColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(__nominalmatch_columns, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.fuzzymatch_columns is not None:
            self.__func_other_arg_sql_names.append("FuzzyMatchColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(__fuzzymatch_columns, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.threshold is not None and self.threshold != 0.5:
            self.__func_other_arg_sql_names.append("ThresholdScore")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.threshold, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.source_accumulate is not None or self.reference_accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(__accumulate, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")

        if self.handle_nulls is not None and self.handle_nulls != "mismatch":
            self.__func_other_arg_sql_names.append("NullHandling")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.handle_nulls, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")

        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.source_data_sequence_column is not None:
            sequence_input_by_list.append("a:" + UtilFuncs._teradata_collapse_arglist(self.source_data_sequence_column, ""))
        
        if self.reference_data_sequence_column is not None:
            sequence_input_by_list.append("b:" + UtilFuncs._teradata_collapse_arglist(self.reference_data_sequence_column, ""))
        
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
        
        # Process source_data
        if self.__awu._is_default_or_not(self.source_data_partition_column, "ANY"):
            self.source_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.source_data_partition_column, "\"")
        
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.source_data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("a")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.source_data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.source_data_order_column, "\""))
        
        # Process reference_data
        reference_data_distribution = "DIMENSION"
        if self.reference_data_partition_column is not None:
            reference_data_distribution = "FACT"
            reference_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.reference_data_partition_column, "\"")
        else:
            reference_data_partition_column = "NA_character_"
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.reference_data, False)
        self.__func_input_distribution.append(reference_data_distribution)
        self.__func_input_arg_sql_names.append("b")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.reference_data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.reference_data_order_column, "\""))
        
        function_name = "IdentityMatch"
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
        Returns the string representation for a IdentityMatch class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
