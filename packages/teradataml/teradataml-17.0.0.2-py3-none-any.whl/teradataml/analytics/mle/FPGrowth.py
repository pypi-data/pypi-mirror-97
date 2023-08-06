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

class FPGrowth:
    
    def __init__(self,
        data = None,
        tran_item_columns = None,
        tran_id_columns = None,
        patterns_or_rules = "both",
        group_by_columns = None,
        pattern_distribution_key_column = None,
        rule_distribution_key_column = None,
        compress = "nocompress",
        group_size = 4,
        min_support = 0.05,
        min_confidence = 0.8,
        max_pattern_length = "2",
        antecedent_count_range = "1-INFINITE",
        consequence_count_range = "1-1",
        delimiter = ",",
        data_sequence_column = None):
        """
        DESCRIPTION:
            The FPGrowth (frequent pattern growth) function uses an FP-growth 
            algorithm to create association rules from patterns in a data set, 
            and then determines their interestingness.
        
        
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the data 
                set.

            tran_item_columns:
                Required Argument.
                Specifies the names of the columns that contain transaction items to
                analyze.
                Types: str OR list of Strings (str)

            tran_id_columns:
                Required Argument.
                Specifies the names of the columns that contain identifiers for the
                transaction items.
                Types: str OR list of Strings (str)

            patterns_or_rules:
                Optional Argument.
                Specifies whether the function outputs patterns, rules, or both. An
                example of a pattern is {onions, potatoes, hamburger}.
                Default Value: "both"
                Permitted Values: both, patterns, rules
                Types: str

            group_by_columns:
                Optional Argument.
                Specifies the names of columns that define the partitions into which
                the function groups the input data and calculates output for it. At
                least one column must be usable as a distribution key. If you omit
                this argument, then the function considers all input data to be in a
                single partition.
                Note: Do not specify the same column in both this
                      argument and the tran_id_columns argument, because this causes
                      incorrect counting in the partitions.
                Types: str OR list of Strings (str)

            pattern_distribution_key_column:
                Optional Argument.
                Specifies the name of the column to use as the distribution key for
                output_pattern_table.
                The default value is the first column name - "pattern_<tran_item_columns>"
                as generated in the "output_pattern_table" table.
                Note: only one column name can be specified.
                Types: str

            rule_distribution_key_column:
                Optional Argument.
                Specifies the name of the column to use as the distribution key for
                output_rule_table.
                The default value is the first column name - "antecedent_<tran_item_columns>"
                as generated in the "output_rule_table" table.
                Note: only one column name can be specified.
                Types: str

            compress:
                Optional Argument.
                Specifies the compression level the output tables. Realized
                compression ratios depend on both this value and the data
                characteristics. These ratios typically range from 3x to 12x.
                Default Value: "nocompress"
                Permitted Values: low, medium, high, nocompress
                Types: str

            group_size:
                Optional Argument.
                Specifies the number of transaction items to be assigned to each
                worker. This value must be an int in the range from 1 to the number
                of distinct transaction items, inclusive. For a machine with limited
                RAM, use a relatively small value.
                Default Value: 4
                Types: int

            min_support:
                Optional Argument.
                Specifies the minimum support value of returned patterns (including
                the specified support value). This value must be a DECIMAL in the
                range [0, 1].
                Default Value: 0.05
                Types: float

            min_confidence:
                Optional Argument.
                Specifies the minimum confidence value of returned patterns
                (including the specified confidence value). This value must be a
                DECIMAL in the range [0, 1].
                Default Value: 0.8
                Types: float

            max_pattern_length:
                Optional Argument.
                Specifies the maximum length of returned patterns. The length of a
                pattern is the sum of the item numbers in the antecedent and
                consequence columns. This value must be an int greater than 2.
                max_pattern_length also limits the length of
                returned rules to this value.
                Default Value: "2"
                Types: str

            antecedent_count_range:
                Optional Argument.
                Specifies the range for na, the number of items in the antecedent.
                The function returns only patterns for which na is in the range
                [lower_bound, upper_bound]. The lower_bound must be greater an
                integer greater than 0. The lower_bound and upper_bound can be equal.
                Default Value: "1-INFINITE"
                Types: str

            consequence_count_range:
                Optional Argument.
                Specifies the range for nc, the number of items in the consequence.
                The function returns only patterns for which nc is in the range
                [lower_bound, upper_bound]. The lower_bound must be greater an
                integer greater than 0. The lower_bound and upper_bound can be equal.
                Default Value: "1-1"
                Types: str

            delimiter:
                Optional Argument.
                Specifies the delimiter that separates items in the output.
                Default Value: ","
                Types: str

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of FPGrowth.
            Output teradataml DataFrames can be accessed using attribute
            references, such as FPGrowthObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. output_pattern_table
                2. output_rule_table
                3. output

            Note:
                Based on the value passed to 'patterns_or_rules', output teradataml
                DataFrames are created.
                    - When value is 'BOTH', all three output teradataml dataframes are
                      created.
                    - When it is 'PATTERNS', 'output_rule_table' output teradataml
                      dataframe is not created.
                    - When it is 'RULES', 'output_pattern_table' output teradataml
                      dataframe is not created.


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load example data.
            load_example_data("fpgrowth", "sales_transaction")

            # Create teradataml DataFrame objects.
            # Sales transaction data of an office supply chain store.
            # The column "product" specifies the items that are purchased by a
            # customer in a given transaction (column "orderid")
            sales_transaction = DataFrame.from_table("sales_transaction")

            # Example - Compute association rules based on the pattern in the "product" column
            FPGrowth_out = FPGrowth(data = sales_transaction,
                                    tran_item_columns = ["product"],
                                    tran_id_columns = ["orderid"],
                                    patterns_or_rules = "both",
                                    group_by_columns = ["region"],
                                    min_support = 0.01,
                                    min_confidence = 0.0,
                                    max_pattern_length = "4"
                                    )

            # Print the results.
            print(FPGrowth_out)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.tran_item_columns  = tran_item_columns 
        self.tran_id_columns  = tran_id_columns 
        self.patterns_or_rules  = patterns_or_rules 
        self.group_by_columns  = group_by_columns 
        self.pattern_distribution_key_column  = pattern_distribution_key_column 
        self.rule_distribution_key_column  = rule_distribution_key_column 
        self.compress  = compress 
        self.group_size  = group_size 
        self.min_support  = min_support 
        self.min_confidence  = min_confidence 
        self.max_pattern_length  = max_pattern_length 
        self.antecedent_count_range  = antecedent_count_range 
        self.consequence_count_range  = consequence_count_range 
        self.delimiter  = delimiter 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["tran_item_columns", self.tran_item_columns, False, (str,list)])
        self.__arg_info_matrix.append(["tran_id_columns", self.tran_id_columns, False, (str,list)])
        self.__arg_info_matrix.append(["patterns_or_rules", self.patterns_or_rules, True, (str)])
        self.__arg_info_matrix.append(["group_by_columns", self.group_by_columns, True, (str,list)])
        self.__arg_info_matrix.append(["pattern_distribution_key_column", self.pattern_distribution_key_column, True, (str)])
        self.__arg_info_matrix.append(["rule_distribution_key_column", self.rule_distribution_key_column, True, (str)])
        self.__arg_info_matrix.append(["compress", self.compress, True, (str)])
        self.__arg_info_matrix.append(["group_size", self.group_size, True, (int)])
        self.__arg_info_matrix.append(["min_support", self.min_support, True, (float)])
        self.__arg_info_matrix.append(["min_confidence", self.min_confidence, True, (float)])
        self.__arg_info_matrix.append(["max_pattern_length", self.max_pattern_length, True, (str)])
        self.__arg_info_matrix.append(["antecedent_count_range", self.antecedent_count_range, True, (str)])
        self.__arg_info_matrix.append(["consequence_count_range", self.consequence_count_range, True, (str)])
        self.__arg_info_matrix.append(["delimiter", self.delimiter, True, (str)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        
        if inspect.stack()[1][3] != '_from_model_catalog':
            # Perform the function validations
            self.__validate()
            # Generate the ML query
            self.__form_tdml_query()
            # Process output table schema
            self.__process_output_column_info()
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
        
        # Check for permitted values
        patterns_or_rules_permitted_values = ["BOTH", "PATTERNS", "RULES"]
        self.__awu._validate_permitted_values(self.patterns_or_rules, patterns_or_rules_permitted_values, "patterns_or_rules", False)
        
        compress_permitted_values = ["LOW", "MEDIUM", "HIGH", "NOCOMPRESS"]
        self.__awu._validate_permitted_values(self.compress, compress_permitted_values, "compress")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.tran_item_columns, "tran_item_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.tran_item_columns, "tran_item_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.tran_id_columns, "tran_id_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.tran_id_columns, "tran_id_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.group_by_columns, "group_by_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.group_by_columns, "group_by_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        # Validate that value passed to the output column argument is not empty.
        self.__awu._validate_input_columns_not_empty(self.pattern_distribution_key_column, "pattern_distribution_key_column")
        self.__awu._validate_input_columns_not_empty(self.rule_distribution_key_column, "rule_distribution_key_column")
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__func_output_args_sql_names = []
        self.__func_output_args = []
        if self.patterns_or_rules.lower() in ["both", "patterns"]:
            self.__output_pattern_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_fpgrowth0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
            self.__func_output_args_sql_names.append("OutputPatternTable")
            self.__func_output_args.append(self.__output_pattern_table_temp_tablename)

        if self.patterns_or_rules.lower() in ["both", "rules"]:
            self.__output_rule_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_fpgrowth1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
            self.__func_output_args_sql_names.append("OutputRuleTable")
            self.__func_output_args.append(self.__output_rule_table_temp_tablename)
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("TargetColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.tran_item_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("TransactionIDColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.tran_id_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.group_by_columns is not None:
            self.__func_other_arg_sql_names.append("PartitionColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.group_by_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.patterns_or_rules != "both":
            self.__func_other_arg_sql_names.append("PatternsOrRules")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.patterns_or_rules, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.compress is not None and self.compress != "nocompress":
            self.__func_other_arg_sql_names.append("CompressionLevel")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.compress, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.group_size is not None and self.group_size != 4:
            self.__func_other_arg_sql_names.append("GroupSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.group_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.min_support is not None and self.min_support != 0.05:
            self.__func_other_arg_sql_names.append("MinSupport")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.min_support, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.min_confidence is not None and self.min_confidence != 0.8:
            self.__func_other_arg_sql_names.append("MinConfidence")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.min_confidence, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.max_pattern_length is not None:
            self.__func_other_arg_sql_names.append("MaxPatternLength")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_pattern_length, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.antecedent_count_range is not None and self.antecedent_count_range != "1-INFINITE":
            self.__func_other_arg_sql_names.append("AntecedentCountRange")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.antecedent_count_range, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.consequence_count_range is not None and self.consequence_count_range != "1-1":
            self.__func_other_arg_sql_names.append("ConsequenceCountRange")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.consequence_count_range, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.delimiter is not None and self.delimiter != ",":
            self.__func_other_arg_sql_names.append("Delimiter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.delimiter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.pattern_distribution_key_column is not None:
            self.__func_other_arg_sql_names.append("PatternDistributionKeyColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.pattern_distribution_key_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.rule_distribution_key_column is not None:
            self.__func_other_arg_sql_names.append("RuleDistributionKeyColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.rule_distribution_key_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))

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
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("InputTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "FPGrowth"
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
        Function to generate AED nodes for output tables.
        This makes a call aed_ml_query() and then output table dataframes are created.
        """
        # Create a list of input node ids contributing to a query.
        self.__input_nodeids = []
        self.__input_nodeids.append(self.data._nodeid)
        
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__func_output_args.insert(0, sqlmr_stdout_temp_tablename)
        try:
            # Call aed_ml_query and generate AED nodes.
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "FPGrowth", self.__aqg_obj._multi_query_input_nodes)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, str(emsg)), MessageCodes.AED_EXEC_FAILED)

        # Update output table data frames.
        self._mlresults = []
        self.output_rule_table = "INFO: 'output_rule_table' output DataFrame is not created, when 'patterns_or_rules' is set to 'PATTERNS'."
        self.output_pattern_table = "INFO: 'output_pattern_table' output DataFrame is not created, when 'patterns_or_rules' is set to 'RULES'."
        if self.patterns_or_rules.lower() in ["both", "patterns"]:
            self.output_pattern_table = self.__awu._create_data_set_object(df_input=node_id_list[1], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[1], self.__output_pattern_table_column_info))
            self._mlresults.append(self.output_pattern_table)

        if self.patterns_or_rules.lower() in ["both", "rules"]:
            if self.patterns_or_rules.lower() == "both":
                node_index = 2
            else:
                node_index = 1
            self.output_rule_table = self.__awu._create_data_set_object(df_input=node_id_list[node_index], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[node_index], self.__output_rule_table_column_info))
            self._mlresults.append(self.output_rule_table)

        self.output = self.__awu._create_data_set_object(df_input=node_id_list[0], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[0], self.__stdout_column_info))
        self._mlresults.append(self.output)
        
    def __process_output_column_info(self):
        """ 
        Function to process the output schema for all the ouptut tables.
        This function generates list of column names and column types
        for each generated output tables, which can be used to create metaexpr.
        """
        # Collecting STDOUT output column information.
        stdout_column_info_name = []
        stdout_column_info_type = []
        stdout_column_info_name.append("output_information")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))
        
        self.__stdout_column_info = zip(stdout_column_info_name, stdout_column_info_type)
        
        # Collecting output_pattern_table output column information.
        if self.patterns_or_rules.lower() in ["both", "patterns"]:
            output_pattern_table_column_info_name = []
            output_pattern_table_column_info_type = []
            if self.group_by_columns is not None:
                for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.group_by_columns, columns=None):
                    output_pattern_table_column_info_name.append(column_name)
                    output_pattern_table_column_info_type.append(column_type)

            for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.tran_item_columns, columns=None):
                output_pattern_table_column_info_name.append("pattern_" + column_name)
                output_pattern_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))

            output_pattern_table_column_info_name.append("length_of_pattern")
            output_pattern_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))

            output_pattern_table_column_info_name.append("count")
            output_pattern_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("bigint"))

            output_pattern_table_column_info_name.append("support")
            output_pattern_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            self.__output_pattern_table_column_info = zip(output_pattern_table_column_info_name, output_pattern_table_column_info_type)
        
        # Collecting output_rule_table output column information.
        if self.patterns_or_rules.lower() in ["both", "rules"]:
            output_rule_table_column_info_name = []
            output_rule_table_column_info_type = []
            if self.group_by_columns is not None:
                for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.group_by_columns, columns=None):
                    output_rule_table_column_info_name.append(column_name)
                    output_rule_table_column_info_type.append(column_type)

            for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.tran_item_columns, columns=None):
                output_rule_table_column_info_name.append("antecedent_" + column_name)
                output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))

                output_rule_table_column_info_name.append("consequence_" + column_name)
                output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("varchar"))

            output_rule_table_column_info_name.append("count_of_antecedent")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))

            output_rule_table_column_info_name.append("count_of_consequence")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("integer"))

            output_rule_table_column_info_name.append("cntb")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("bigint"))

            output_rule_table_column_info_name.append("cnt_antecedent")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("bigint"))

            output_rule_table_column_info_name.append("cnt_consequence")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("bigint"))

            output_rule_table_column_info_name.append("score")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            output_rule_table_column_info_name.append("support")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            output_rule_table_column_info_name.append("confidence")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            output_rule_table_column_info_name.append("lift")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            output_rule_table_column_info_name.append("conviction")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            output_rule_table_column_info_name.append("leverage")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            output_rule_table_column_info_name.append("coverage")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            output_rule_table_column_info_name.append("chi_square")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            output_rule_table_column_info_name.append("z_score")
            output_rule_table_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))

            self.__output_rule_table_column_info = zip(output_rule_table_column_info_name, output_rule_table_column_info_type)

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
        output_pattern_table = None,
        output_rule_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("output_pattern_table", None)
        kwargs.pop("output_rule_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.output_pattern_table  = output_pattern_table 
        obj.output_rule_table  = output_rule_table 
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
        if obj.output_pattern_table is None:
            obj.output_pattern_table = "INFO: 'output_pattern_table' output DataFrame is not created, when 'patterns_or_rules' is set to 'RULES'."
        else:
            obj.output_pattern_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output_pattern_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output_pattern_table))
            obj._mlresults.append(obj.output_pattern_table)

        if obj.output_rule_table is None:
            obj.output_rule_table = "INFO: 'output_rule_table' output DataFrame is not created, when 'patterns_or_rules' is set to 'PATTERNS'."
        else:
            obj.output_rule_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output_rule_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output_rule_table))
            obj._mlresults.append(obj.output_rule_table)

        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a FPGrowth class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ output_pattern_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.output_pattern_table)
        repr_string="{}\n\n\n############ output_rule_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.output_rule_table)
        return repr_string
        
