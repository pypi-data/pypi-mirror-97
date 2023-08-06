#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Rohit Khurd (rohit.khurd@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.1
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

class NPath:
    
    def __init__(self,
        data1 = None,
        mode = None,
        pattern = None,
        symbols = None,
        result = None,
        filter = None,
        data2 = None,
        data3 = None,
        data1_partition_column = None,
        data2_partition_column = None,
        data3_partition_column = None,
        data1_order_column = None,
        data2_order_column = None,
        data3_order_column = None):
        """
        DESCRIPTION:
            The nPath function scans a set of rows, looking for patterns that you
            specify. For each set of input rows that matches the pattern, nPath
            produces a single output row. The function provides a flexible
            pattern-matching capability that lets you specify complex patterns in
            the input data and define the values that are output for each matched
            input set.
         
         
        PARAMETERS:
            data1:
                Required Argument.
                Specifies the input teradataml DataFrame containing the input data set.
         
            data1_partition_column:
                Required Argument.
                Specifies Partition By columns for data1.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)
         
            data1_order_column:
                Required Argument.
                Specifies Order By columns for data1.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            mode:
                Required Argument.
                Specifies the pattern-matching mode:
                    OVERLAPPING: The function finds every occurrence of the pattern in
                                 the partition, regardless of whether it is part of a previously
                                 found match. Therefore, one row can match multiple symbols in a
                                 given matched pattern.
                    NONOVERLAPPING: The function begins the next pattern search at the
                                    row that follows the last pattern match. This is the default
                                    behavior of many commonly used pattern matching utilities, including
                                    the UNIX grep utility.
                Permitted Values: OVERLAPPING, NONOVERLAPPING
                Types: str
         
            pattern:
                Required Argument.
                Specifies the pattern for which the function searches. You compose
                pattern with the symbols that you define in the symbols argument,
                operators, and parentheses.
                When patterns have multiple operators, the function applies
                them in order of precedence, and applies operators of equal
                precedence from left to right. To specify that a subpattern must
                appear a specific number of times, use the Range-Matching
                Feature.
                The basic pattern operators in decreasing order of precedence
                    "pattern", "pattern.", "pattern?", "pattern*", "pattern+",
                    "pattern1.pattern2", "pattern1|pattern2", "^pattern", "pattern$"
                To force the function to evaluate a subpattern first, enclose it in parentheses.
                Example:
                    ^A.(B|C)+.D?.X*.A$
                    The preceding pattern definition matches any set of rows
                    whose first row starts with the definition of symbol A,
                    followed by a non-empty sequence of rows, each of which
                    meets the definition of either symbol B or C, optionally
                    followed by one row that meets the definition of symbol D,
                    followed by any number of rows that meet the definition of
                    symbol X, and ending with a row that ends with the definition of symbol A.
                You can use parentheses to define precedence rules. Parentheses are
                recommended for clarity, even where not strictly required.
                Types: str
         
            symbols:
                Required Argument.
                Defines the symbols that appear in the values of the pattern and
                result arguments. The col_expr is an expression whose value is a
                column name, symbol is any valid identifier, and symbol_predicate is
                a SQL predicate (often a column name).
                For example, the 'symbols' argument for analyzing website visits might
                look like this:
                    Symbols
                    (
                     pagetype = "homepage" AS H,
                     pagetype <> "homepage" AND  pagetype <> "checkout" AS PP,
                     pagetype = "checkout" AS CO
                    )
                The symbol is case-insensitive; however, a symbol of one or two
                uppercase letters is easy to identify in patterns.
                If col_expr represents a column that appears in multiple input
                DataFrames, then you must qualify the ambiguous column name with
                the SQL name corresponding to its teradataml DataFrame name.
                For example:
                    Symbols
                    (
                     input1.pagetype = "homepage" AS H,
                     input1.pagetype = "thankyou" AS T,
                     input2.adname = "xmaspromo" AS X,
                     input2.adname = "realtorpromo" AS R
                    )
                The mapping from teradataml DataFrame name to its corresponding SQL name
                is as shown below:
                    * data1: input1
                    * data2: input2
                    * data3: input3
                You can create symbol predicates that compare a row to a previous
                or subsequent row, using a LAG or LEAD operator.
                LAG Expression Syntax:
                    { current_expr operator LAG (previous_expr, lag_rows [, default]) |
                    LAG (previous_expr, lag_rows [, default]) operator current_expr }
                LAG and LEAD Expression Rules:
                    • A symbol definition can have multiple LAG and LEAD expressions.
                    • A symbol definition that has a LAG or LEAD expression cannot have an OR operator.
                    • If a symbol definition has a LAG or LEAD expression and the input
                      is not a table, you must create an alias of the input query.
                Types: str OR list of Strings (str)
         
            result:
                Required Argument.
                Defines the output columns. The col_expr is an expression whose value
                is a column name; it specifies the values to retrieve from the
                matched rows. The function applies aggregate function to these
                values.
                Supported aggregate functions:
                    • SQL aggregate functions are [AVG, COUNT, MAX, MIN, SUM].
                    • ML Engine nPath sequence aggregate functions.
                The function evaluates this argument once for every matched pattern
                in the partition (that is, it outputs one row for each pattern match).
                Note:
                    For col_expr representing a column that appears in multiple input
                    DataFrames, you must qualify the ambiguous column name with the SQL
                    name corresponding to its teradataml DataFrame name. Please see the
                    description of the 'symbols' parameter for the mapping from teradataml
                    DataFrame name to the SQL name.
                Types: str OR list of Strings (str)
         
            filter:
                Optional Argument.
                Specifies filters to impose on the matched rows. The function
                combines the filter expressions using the AND operator.
                The filter_expression syntax is:
                    symbol_expression comparison_operator symbol_expression
                The two symbol expressions must be type-compatible.
                The symbol_expression syntax is:
                    { FIRST | LAST }(column_with_expression OF [ANY](symbol[,...]))
                The column_with_expression cannot contain the operator AND or OR, and
                all its columns must come from the same input. If the function has
                multiple inputs, then column_with_expression and symbol must come
                from the same input.
                The comparison_operator is either <, >, <=, >=, =, or <>.
                Note:
                    For column_with_expression representing a column that appears in
                    multiple input DataFrames, you must qualify the ambiguous column name with
                    the SQL name corresponding to its teradataml DataFrame name. Please see
                    the description of the 'symbols' parameter for the mapping from teradataml
                    DataFrame name to the SQL name.
                Types: str OR list of Strings (str)
         
            data2:
                Optional Argument.
                Specifies the additional optional input teradataml DataFrame containing the input data set.
         
            data2_partition_column:
                Optional Argument.
                Specifies Partition By columns for data2.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)
         
            data2_order_column:
                Optional Argument.
                Required when data2 teradataml DataFrame is used.
                Specifies Order By columns for data2.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            data3:
                Optional Argument.
                Specifies the additional optional input teradataml DataFrame containing the input data set.
         
            data3_partition_column:
                Optional Argument.
                Specifies Partition By columns for data3.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)
         
            data3_order_column:
                Optional Argument.
                Required when data3 teradataml DataFrame is used.
                Specifies Order By columns for data3.
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of NPath.
            Output teradataml DataFrames can be accessed using attribute
            references, such as NPathObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("NPath",["impressions","clicks2", "tv_spots", "clickstream"])
         
            # Create input teradataml dataframes.
            impressions = DataFrame.from_table("impressions")
            clicks2 = DataFrame.from_table("clicks2")
            tv_spots = DataFrame.from_table("tv_spots")
            clickstream = DataFrame.from_table("clickstream")
         
            # Example1:
            # We will try to search for pattern '(imp|tv_imp)*.click'
            # in the provided data sets(imressions, clicks2, tv_spots).
            # Run NPath function with the required patterns to get the rows which
            # has specified pattern. rows that matches the pattern.
            result = NPath(data1=impressions,
                           data1_partition_column='userid',
                           data1_order_column='ts',
                           data2=clicks2,
                           data2_partition_column='userid',
                           data2_order_column='ts',
                           data3=tv_spots,
                           data3_partition_column='ts',
                           data3_order_column='ts',
                           result=['COUNT(* of imp) as imp_cnt','COUNT(* of tv_imp) as tv_imp_cnt'],
                           mode='nonoverlapping',
                           pattern='(imp|tv_imp)*.click',
                           symbols=['true as imp','true as click','true as tv_imp'])
         
            # Print the result dataframe.
            print(result.result)
         
            # Example2:
            # We will try to search for pattern 'home.clickview*.checkout'
            # in the provided data set clickstream.
            # Run NPath function with the required patterns to get the rows which
            # has specified pattern and filter the rows with the filter,
            # where filter and result have ML Engine nPath sequence aggregate functions
            # like 'FIRST', 'COUNT' and 'LAST'
            result = NPath(data1=clickstream,
                           data1_partition_column='userid',
                           data1_order_column='clicktime',
                           result=['FIRST(userid of ANY(home, checkout, clickview)) AS userid',
                                   'FIRST (sessionid of ANY(home, checkout, clickview)) AS sessioinid',
                                   'COUNT (* of any(home, checkout, clickview)) AS cnt',
                                   'FIRST (clicktime of ANY(home)) AS firsthome',
                                   'LAST (clicktime of ANY(checkout)) AS lastcheckout'],
                           mode='nonoverlapping',
                           pattern='home.clickview*.checkout',
                           symbols=["pagetype='home' AS home",
                                    "pagetype <> 'home' AND pagetype <> 'checkout' AS clickview",
                                    "pagetype='checkout' AS checkout"],
                           filter = "FIRST (clicktime OF ANY (home)) <"
                                    "FIRST (clicktime of any(checkout))"
                           )
         
            # Print the result dataframe.
            print(result.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data1  = data1 
        self.mode  = mode 
        self.pattern  = pattern 
        self.symbols  = symbols 
        self.result  = result 
        self.filter  = filter 
        self.data2  = data2 
        self.data3  = data3 
        self.data1_partition_column  = data1_partition_column
        self.data2_partition_column  = data2_partition_column 
        self.data3_partition_column  = data3_partition_column
        self.data1_order_column  = data1_order_column
        self.data2_order_column  = data2_order_column 
        self.data3_order_column  = data3_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data1", self.data1, False, (DataFrame)])
        self.__arg_info_matrix.append(["data1_partition_column", self.data1_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data1_order_column", self.data1_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["mode", self.mode, False, (str)])
        self.__arg_info_matrix.append(["pattern", self.pattern, False, (str)])
        self.__arg_info_matrix.append(["symbols", self.symbols, False, (str,list)])
        self.__arg_info_matrix.append(["result", self.result, False, (str,list)])
        self.__arg_info_matrix.append(["filter", self.filter, True, (str,list)])
        self.__arg_info_matrix.append(["data2", self.data2, True, (DataFrame)])
        self.__arg_info_matrix.append(["data2_partition_column", self.data2_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["data2_order_column", self.data2_order_column, self.data2 is None, (str,list)])
        self.__arg_info_matrix.append(["data3", self.data3, True, (DataFrame)])
        self.__arg_info_matrix.append(["data3_partition_column", self.data3_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["data3_order_column", self.data3_order_column, self.data3 is None, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.data1, "data1", None)
        self.__awu._validate_input_table_datatype(self.data2, "data2", None)
        self.__awu._validate_input_table_datatype(self.data3, "data3", None)
        
        # Check for permitted values
        mode_permitted_values = ["OVERLAPPING", "NONOVERLAPPING"]
        self.__awu._validate_permitted_values(self.mode, mode_permitted_values, "mode")
        
        self.__awu._validate_input_columns_not_empty(self.data1_partition_column, "data1_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data1_partition_column, "data1_partition_column", self.data1, "data1", True)
        
        self.__awu._validate_input_columns_not_empty(self.data2_partition_column, "data2_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data2_partition_column, "data2_partition_column", self.data2, "data2", True)
        
        self.__awu._validate_input_columns_not_empty(self.data3_partition_column, "data3_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data3_partition_column, "data3_partition_column", self.data3, "data3", True)
        
        self.__awu._validate_input_columns_not_empty(self.data1_order_column, "data1_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data1_order_column, "data1_order_column", self.data1, "data1", False)
        
        self.__awu._validate_input_columns_not_empty(self.data2_order_column, "data2_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data2_order_column, "data2_order_column", self.data2, "data2", False)
        
        self.__awu._validate_input_columns_not_empty(self.data3_order_column, "data3_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data3_order_column, "data3_order_column", self.data3, "data3", False)
        
        # Validate that value passed to the output column argument is not empty.
        self.__awu._validate_input_columns_not_empty(self.result, "result")
        
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
        
        self.__func_other_arg_sql_names.append("Mode")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mode, ""))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("Pattern")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.pattern, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("Symbols")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.symbols, ""))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.filter is not None:
            self.__func_other_arg_sql_names.append("Filter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.filter, ""))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("Result")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.result, ""))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data1
        self.data1_partition_column = UtilFuncs._teradata_collapse_arglist(self.data1_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data1, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input1")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data1_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data1_order_column, "\""))
        
        # Process data2
        if self.data2 is not None:
            data2_distribution = "DIMENSION"
            if self.data2_partition_column is not None:
                data2_distribution = "FACT"
                data2_partition_column = UtilFuncs._teradata_collapse_arglist(self.data2_partition_column, "\"")
            else:
                data2_partition_column = "NA_character_"
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data2, False)
            self.__func_input_distribution.append(data2_distribution)
            self.__func_input_arg_sql_names.append("input2")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(data2_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data2_order_column, "\""))
        
        # Process data3
        if self.data3 is not None:
            data3_distribution = "DIMENSION"
            if self.data3_partition_column is not None:
                data3_distribution = "FACT"
                data3_partition_column = UtilFuncs._teradata_collapse_arglist(self.data3_partition_column, "\"")
            else:
                data3_partition_column = "NA_character_"
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data3, False)
            self.__func_input_distribution.append(data3_distribution)
            self.__func_input_arg_sql_names.append("input3")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(data3_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data3_order_column, "\""))
        
        function_name = "nPath"
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
        Returns the string representation for a NPath class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
