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
# Function Version: 2.6
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

class FrequentPaths:
    
    def __init__(self,
        data = None,
        min_support = None,
        time_column = None,
        path_filters = None,
        groupby_columns = None,
        item_column = None,
        item_definition_table = None,
        path_column = None,
        max_length = 2147483647,
        min_length = 1,
        closed_pattern = False,
        item_definition_columns = None,
        partition_columns = None,
        data_sequence_column = None,
        item_definition_table_sequence_column = None):
        """
        DESCRIPTION:
            The FrequentPaths takes a teradataml DataFrame of sequences and 
            outputs a teradataml DataFrame of subsequences (patterns) that 
            frequently appear in the input teradataml DataFrame and, optionally, 
            a teradataml DataFrame of sequence-pattern pairs.
        
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame that contains the
                input sequences. Each row is one item in a sequence.
                Note: The function ignores rows that contain any NULL values.
            
            min_support:
                Required Argument.
                Determines the threshold for whether a sequential pattern is 
                frequent. The min_support must be a positive float number.
                If min_support is in the range (0,1), then it is a relative threshold.
                If N is the total number of input sequences, then the threshold is
                T=N*min_support.
                For example, if there are 1000 sequences in the input
                teradataml DataFrame and min_support is 0.05, then the threshold is 50.
                If min_support is in the range (1,+), then it is an absolute threshold.
                Regardless of N, T=min_support. For example, if min_support is 50, then the
                threshold is 50, regardless of N.
                A pattern is frequent if its support value is at least T.
                Because the function outputs only frequent patterns, min_support controls
                the number of output patterns. If min_support is small, processing time
                increases exponentially; therefore, teradataml recommends starting the
                trial with a larger value. for example, 5% of the total sequence number
                if you know N and 0.05 otherwise.
                If you specify a relative min_support and groupby_columns, then the function
                calculates N and T for each group.
                If you specify a relative min_support and path_filters, then N is the
                number of sequences that meet the constraints of the filters.
                Types: float
            
            time_column:
                Optional Argument. Required when item_column or item_definition_columns
                is specified.
                Specifies the input teradataml DataFrame column that
                determines the order of items in a sequence. Items in the same 
                sequence that have the same timestamp belong to the same set.
                Types: str
            
            path_filters:
                Optional Argument.
                Specifies the filters to use on the input teradataml DataFrame 
                sequences. Only input teradataml DataFrame sequences that satisfy all 
                constraints of at least one filter are input to the function. Each 
                filter has one or more constraints, which are separated by spaces. 
                Each constraint has this syntax:
                constraint (item [symbol ...]).
                By default, symbol is comma (,). If you specify symbol, it applies to
                all filters. The constraint is one of the following:
                    • STW (start-with constraint): The first item set of the sequence
                      must contain at least one item.
                      For example, STW(c,d) requires the first item set of the sequence to
                      contain c or d. Sequence "(a, c), e, (f, d)" meets this constraint
                      because the first item set, (a,c), contains c.
                    • EDW (end-with constraint): The last item set of the sequence must contain
                      at least one item.
                      For example, EDW(f,g) requires the last item set of the sequence to contain
                      f or g. Sequence "(a, b), e, (f, d)" meets this constraint because the last
                      item set, (f,d), contains f.
                    • CTN (containing constraint): The sequence must contain at least one item.
                      For example, CTN(a,b) requires the sequence to contain a or b. The
                      sequence "(a,c), d, (e,f)" meets this constraint but the sequence "d,
                      (e,f)" does not.
                Constraints in the same filter must be different.
                For example, the filter "STW(c,d) EDW(g,k) CTN(e)" is valid, but 
                "STW(c,d) STW(e,h)" is invalid.
                This argument specifies a separator and uses it in two filters:
                path_filters("Separator(#)", "STW(c#d) EDW  (g#k) CTN(e)", "CTN(h#k)")
                Types: str OR list of strs
            
            groupby_columns:
                Optional Argument.
                Specifies the input teradataml DataFrame columns by which to group the
                input teradataml DataFrame sequences. If you specify this argument,
                then the function operates on each group separately and copies each
                column mentioned in the argument to the output teradataml DataFrame.
                Types: str OR list of Strings (str)
            
            item_column:
                Optional Argument. Required if you specify neither item_definition_columns
                nor path_column.
                Specifies the input teradataml DataFrame columns that contain the items.
                Types: str OR list of Strings (str)
            
            item_definition_table:
                Optional Argument. Required if you specify neither item_column nor path_column.
                Specifies the item definition teradataml DataFrame.
            
            path_column:
                Optional Argument. Required if you specify neither item_column nor
                item_definition_columns.
                Specifies the input teradataml DataFrame column that
                contains paths in the form of sequence strings. A sequence string has 
                this syntax: "[item [, ...]]". In the sequence string syntax, you must
                type the outer brackets. The sequence strings in this column
                can be generated by the nPath function. If you specify this argument, 
                then each item set can have only one item.
                Types: str
            
            max_length:
                Optional Argument.
                Specifies the maximum length of the output sequential patterns. The 
                length of a pattern is its number of sets.
                Default Value: 2147483647
                Types: int
            
            min_length:
                Optional Argument.
                Specifies the minimum length of the output sequential patterns. 
                Default Value: 1
                Types: int
            
            closed_pattern:
                Optional Argument.
                Specifies whether to output only closed patterns. 
                Default Value: False
                Types: bool
            
            item_definition_columns:
                Optional Argument. Required if you specify neither item_column
                nor path_column.
                Specifies the names of the index, definition, and item columns of
                the input argument "item_definition_table".
                Types: str
            
            partition_columns:
                Required Argument.
                Specifies the names of the columns that comprise the partition key of 
                the input sequences.
                Types: str OR list of Strings (str)
            
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)
            
            item_definition_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "item_definition_table". The argument is used to 
                ensure deterministic results for functions which produce results that 
                vary from run to run.
                Types: str OR list of Strings (str)
        
        RETURNS:
            Instance of FrequentPaths.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as FrequentPathsObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. subsequence_data
                2. seq_pattern_table
                3. output
        
        
        RAISES:
            TeradataMlException
        
        
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("FrequentPaths", ["bank_web_url", "ref_url", "bank_web_clicks1", "bank_web_clicks2", "sequence_table"])

            # Create teradataml DataFrame.
            bank_web_url = DataFrame.from_table("bank_web_url")
            ref_url = DataFrame.from_table("ref_url")
            bank_web_clicks1 = DataFrame.from_table("bank_web_clicks1")
            bank_web_clicks2 = DataFrame.from_table("bank_web_clicks2")
            sequence_table = DataFrame.from_table("sequence_table")

            # Example 1 : Running FrequentPaths function with item_column argument.
            # data: bank_web_clicks1, which has web clickstream data from a set of users with multiple sessions.
            # We are using users action information as item_column to run FrequentPaths function to select sequences.
            frequentpaths_out1 = FrequentPaths(data=bank_web_clicks1,
                                            partition_columns='session_id',
                                            time_column='datestamp',
                                            item_column='page',
                                            min_support=2.0,
                                            max_length=2147483647,
                                            min_length=1,
                                            closed_pattern=False,
                                            data_sequence_column='datestamp'
                                            )

            # Print the result DataFrame.
            print(frequentpaths_out1.subsequence_data)
            print(frequentpaths_out1.seq_pattern_table)
            print(frequentpaths_out1.output)

            # Example 2 : Running FrequentPaths function with item_definition_table argument.
            # data: bank_web_url, which has the URL of each page browsed by the customer.
            # item_definition_table : ref_url, which has the definitions of the browser pages
            frequentpaths_out2 = FrequentPaths(data=bank_web_url,
                                            item_definition_table=ref_url,
                                            partition_columns='session_id',
                                            time_column='datestamp',
                                            min_support=2.0,
                                            item_definition_columns='[page_id:pagedef:page]',
                                            max_length=2147483647,
                                            min_length=1,
                                            closed_pattern=False,
                                            data_sequence_column='datestamp'
                                            )

            # Print the result DataFrame.
            print(frequentpaths_out2.subsequence_data)
            print(frequentpaths_out2.seq_pattern_table)
            print(frequentpaths_out2.output)

            # Example 3 : Running FrequentPaths function with groupby_columns argument.
            # FrequentPaths function will operates on each group (customer) separately.
            frequentpaths_out3 = FrequentPaths(data=bank_web_clicks2,
                                            partition_columns='session_id',
                                            time_column='datestamp',
                                            item_column='page',
                                            groupby_columns='customer_id',
                                            min_support=2.0,
                                            max_length=2147483647,
                                            min_length=1,
                                            closed_pattern=False,
                                            data_sequence_column='datestamp'
                                            )

            # Print the result DataFrame.
            print(frequentpaths_out3.subsequence_data)
            print(frequentpaths_out3.seq_pattern_table)
            print(frequentpaths_out3.output)

            # Example 4 : Running FrequentPaths function with path_filters argument.
            frequentpaths_out4 = FrequentPaths(data=bank_web_clicks1,
                                            partition_columns='session_id',
                                            time_column='datestamp',
                                            item_column='page',
                                            min_support=2.0,
                                            max_length=2147483647,
                                            path_filters='STW(account summary) EDW(account history)',
                                            min_length=1,
                                            closed_pattern=False,
                                            data_sequence_column='datestamp'
                                            )

            # Print the result DataFrame.
            print(frequentpaths_out4.subsequence_data)
            print(frequentpaths_out4.seq_pattern_table)
            print(frequentpaths_out4.output)

            # Example 5 : Using NPath output to run FrequentPaths function to select sequences.
            # data: npath_output, which the example creates by inputting the teradataml DataFrame
            # "sequence_table", to the NPath function.
            npath_output = NPath(data1=sequence_table,
                           data1_partition_column='id',
                           data1_order_column='datestamp',
                           result=['FIRST(id OF itemA) AS id','Accumulate (item OF ANY(itemA, itemAny, itemC)) AS path'],
                           mode='nonoverlapping',
                           pattern='itemA.itemAny*.itemC',
                           symbols=["item='A' AS itemA","item='C' AS itemC","TRUE AS itemAny"])

            # Passing NPath function output to run FrequentPaths function.
            frequentpaths_out5 = FrequentPaths(data=npath_output.result,
                                            partition_columns='id',
                                            path_column='path',
                                            min_support=2.0,
                                            max_length=2147483647,
                                            min_length=1,
                                            closed_pattern=False
                                            )

            # Print the result DataFrame.
            print(frequentpaths_out5.subsequence_data)
            print(frequentpaths_out5.seq_pattern_table)
            print(frequentpaths_out5.output)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.min_support  = min_support 
        self.time_column  = time_column 
        self.path_filters  = path_filters 
        self.groupby_columns  = groupby_columns 
        self.item_column  = item_column 
        self.item_definition_table  = item_definition_table 
        self.path_column  = path_column 
        self.max_length  = max_length 
        self.min_length  = min_length 
        self.closed_pattern  = closed_pattern 
        self.item_definition_columns  = item_definition_columns 
        self.partition_columns  = partition_columns 
        self.data_sequence_column  = data_sequence_column 
        self.item_definition_table_sequence_column  = item_definition_table_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["min_support", self.min_support, False, (float)])
        self.__arg_info_matrix.append(["time_column", self.time_column, True, (str)])
        self.__arg_info_matrix.append(["path_filters", self.path_filters, True, (str,list)])
        self.__arg_info_matrix.append(["groupby_columns", self.groupby_columns, True, (str,list)])
        self.__arg_info_matrix.append(["item_column", self.item_column, True, (str,list)])
        self.__arg_info_matrix.append(["item_definition_table", self.item_definition_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["path_column", self.path_column, True, (str)])
        self.__arg_info_matrix.append(["max_length", self.max_length, True, (int)])
        self.__arg_info_matrix.append(["min_length", self.min_length, True, (int)])
        self.__arg_info_matrix.append(["closed_pattern", self.closed_pattern, True, (bool)])
        self.__arg_info_matrix.append(["item_definition_columns", self.item_definition_columns, True, (str)])
        self.__arg_info_matrix.append(["partition_columns", self.partition_columns, False, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["item_definition_table_sequence_column", self.item_definition_table_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.item_definition_table, "item_definition_table", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument are valid or not.
        self.__awu._validate_input_columns_not_empty(self.partition_columns, "partition_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.partition_columns, "partition_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.time_column, "time_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_column, "time_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.groupby_columns, "groupby_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.groupby_columns, "groupby_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.item_column, "item_column")
        self.__awu._validate_dataframe_has_argument_columns(self.item_column, "item_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.path_column, "path_column")
        self.__awu._validate_dataframe_has_argument_columns(self.path_column, "path_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.item_definition_table_sequence_column, "item_definition_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.item_definition_table_sequence_column, "item_definition_table_sequence_column", self.item_definition_table, "item_definition_table", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__subsequence_data_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_frequentpaths0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__seq_pattern_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_frequentpaths1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable", "SeqPatternTable"]
        self.__func_output_args = [self.__subsequence_data_temp_tablename, self.__seq_pattern_table_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("PartitionColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.partition_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.time_column is not None:
            self.__func_other_arg_sql_names.append("TimeColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.time_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.groupby_columns is not None:
            self.__func_other_arg_sql_names.append("GroupByColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.groupby_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.item_column is not None:
            self.__func_other_arg_sql_names.append("ItemColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.item_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.path_column is not None:
            self.__func_other_arg_sql_names.append("PathColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.path_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("MinSupport")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.min_support, "'"))
        self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.path_filters is not None:
            self.__func_other_arg_sql_names.append("PathFilters")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.path_filters, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.item_definition_columns is not None:
            self.__func_other_arg_sql_names.append("ItemDefinitionColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.item_definition_columns, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.max_length is not None and self.max_length != 2147483647:
            self.__func_other_arg_sql_names.append("MaxLength")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_length, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.min_length is not None and self.min_length != 1:
            self.__func_other_arg_sql_names.append("MinLength")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.min_length, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.closed_pattern is not None and self.closed_pattern != False:
            self.__func_other_arg_sql_names.append("ClosedPattern")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.closed_pattern, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.item_definition_table_sequence_column is not None:
            sequence_input_by_list.append("ItemDefinitionTable:" + UtilFuncs._teradata_collapse_arglist(self.item_definition_table_sequence_column, ""))
        
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
        
        # Process item_definition_table
        if self.item_definition_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.item_definition_table, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("ItemDefinitionTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "FrequentPaths"
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
        self.subsequence_data = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__subsequence_data_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__subsequence_data_temp_tablename))
        self.seq_pattern_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__seq_pattern_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__seq_pattern_table_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.subsequence_data)
        self._mlresults.append(self.seq_pattern_table)
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
        subsequence_data = None,
        seq_pattern_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("subsequence_data", None)
        kwargs.pop("seq_pattern_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.subsequence_data  = subsequence_data 
        obj.seq_pattern_table  = seq_pattern_table 
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
        obj.subsequence_data = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.subsequence_data), source_type="table", database_name=UtilFuncs._extract_db_name(obj.subsequence_data))
        obj.seq_pattern_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.seq_pattern_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.seq_pattern_table))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.subsequence_data)
        obj._mlresults.append(obj.seq_pattern_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a FrequentPaths class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ subsequence_data Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.subsequence_data)
        repr_string="{}\n\n\n############ seq_pattern_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.seq_pattern_table)
        return repr_string
        
