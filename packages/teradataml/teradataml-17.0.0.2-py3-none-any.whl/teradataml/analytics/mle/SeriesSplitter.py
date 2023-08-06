#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.13
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

class SeriesSplitter:
    
    def __init__(self,
        data = None,
        partition_columns = None,
        duplicate_rows_count = 1,
        order_by_columns = None,
        split_count = 4,
        rows_per_split = 1000,
        accumulate = None,
        split_id_column = "split_id",
        return_stats_table = True,
        values_before_first = "-1",
        values_after_last = "null",
        duplicate_column = None,
        partial_split_id = False,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The SeriesSplitter function splits partitions into subpartitions 
            (called splits) to balance the partitions for time series 
            manipulation. The function creates an additional column that contains 
            split identifiers. Each row contains the identifier of the split to 
            which the row belongs. Optionally, the function also copies a 
            specified number of boundary rows to each split.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the input teradataml DataFrame to be split.
            
            partition_columns:
                Required Argument.
                Specifies the partitioning columns of teradataml DataFrame.
                These columns determines the identity of a partition.
                Types: str OR list of Strings (str)
         
            duplicate_rows_count:
                Optional Argument.
                Specifies the number of rows to duplicate across split boundaries.
                By default, the function duplicates one row from the previous
                partition and one row from the next partition. If you specify
                only one value v1, then the function duplicates v1 rows from the
                previous partition and v1 rows from the next partition. If you
                specify two values v1 and v2, then the function duplicates v1
                rows from the previous partition and v2 rows from the next
                partition. Each argument value must be non-negative integer
                less than or equal to 1000.
                Default Value: 1
                Types: int or list of Integers (int)
         
            order_by_columns:
                Optional Argument.
                Specifies the ordering columns of teradataml DataFrame. These
                columns establish the order of the rows and splits. Without
                this argument, the function can split the rows in any order.
                Types: str OR list of Strings (str)
         
            split_count:
                Optional Argument.
                Specifies the desired number of splits in a partition of the output
                table. The value of "split_count" must be a positive int, and
                its upper bound is the number of rows in the partition.
                Note:  If underlying table on Vantage, pointed by 'data', has
                       multiple partitions, then you cannot specify "split_count". Instead,
                       specify "rows_per_split". Base the value of "split_count" on the
                       desired amount of parallelism.
                       For example, for a cluster with 10 vworkers, make "split_count"
                       a multiple of 10. If the number of rows in teradataml DataFrame
                       (n) is not exactly divisible by "split_count", then the function
                       estimates the number of splits in the partition, using this formula:
                       ceiling (n / ceiling (n / split_count) )
                Default Value: 4
                Types: int
         
            rows_per_split:
                Optional Argument.
                Specifies the desired maximum number of rows in each split in
                the output teradataml DataFrame. If the number of rows in
                input table is not exactly divisible by "rows_per_split", then
                the last split contains fewer than "rows_per_split" rows, but
                no row contains more than "rows_per_split" rows. The value of
                "rows_per_split" must be a positive int.
                Note: If underlying table on Vantage, pointed by 'data', has
                      multiple partitions, then specify "rows_per_split" instead of
                      "split_count".
                Default Value: 1000
                Types: int
         
            accumulate:
                Optional Argument.
                Specifies the names of teradataml DataFrame columns (other than
                those specified by "partition_columns" and "order_by_columns") to
                copy to the output teradataml DataFrame. By default, only the
                columns specified by "partition_columns" and "order_by_columns" are
                copied to the output teradataml DataFrame.
                Types: str OR list of Strings (str)
         
            split_id_column:
                Optional Argument.
                Specifies the name for the output teradataml DataFrame column
                to contain the split identifiers. If the output teradataml
                DataFrame  has another column name as that specified in
                "split_id_column", the function returns an error. Therefore, if
                the output teradataml DataFrame has a column named 'split_id'
                (specified by "accumulate", "partition_columns", or
                "order_by_columns"), you must use "split_id_column" to specify
                a different value.
                Default Value: "split_id"
                Types: str
         
            return_stats_table:
                Optional Argument.
                Specifies whether the function returns the data in "stats_table"
                output teradataml DataFrame. When this value is "False", the
                function returns only the data in "output_table" output
                teradataml DataFrame.
                Default Value: True
                Types: bool
         
            values_before_first:
                Optional Argument.
                If "duplicate_rows_count" is nonzero and "order_by_columns" is
                specified, then "values_before_first" specifies the values to be
                stored in the ordering columns that precede the first row of
                the first split in a partition as a result of duplicating rows
                across split boundaries. If "values_before_first" specifies only
                one value and "order_by_columns" specifies multiple ordering columns,
                then the specified value is stored in every ordering column.
                If "values_before_first" specifies multiple values, then it must
                specify a value for each ordering column. The value and the
                ordering column must have the same data type. For the data type
                str, the values are case-insensitive. The values for different
                data types are:
                    int: -1,
                    str : "-1",
                    Date or time-based: 1900-01-01 0:00:00,
                    Boolean: False
                Default Value: "-1"
                Types: str
         
            values_after_last:
                Optional Argument.
                If "duplicate_rows_count" is nonzero and orde_by_columns is
                specified, then "values_after_last" specifies the values to be
                stored in the ordering columns that follow the last row of the
                last split in a partition as a result of duplicating rows across
                split boundaries. If "values_after_last" specifies only one value
                and "order_by_columns" specifies multiple ordering columns, then
                the specified value is stored in every ordering column. If
                "values_after_last" specifies multiple values, then it must specify
                a value for each ordering column. The value and the ordering
                column must have the same data type.  For the data type str, the
                values are case-insensitive.
                Default Value: "null"
                Types: str
         
            duplicate_column:
                Optional Argument.
                Specifies the name of the column that indicates whether a row is
                duplicated from the neighboring split. If the row is duplicated,
                this column contains 1; otherwise it contains 0.
                Types: str
         
            partial_split_id:
                Optional Argument.
                Specifies whether "split_id_column" contains only the numeric split
                identifier. If the value is "True", then "split_id_column"
                contains a numeric representation of the split identifier that
                is unique for each partition. To distribute the output
                teradataml DataFrame by split, use a combination of all
                partitioning columns and "split_id_column". If the value is "False",
                then "split_id_column" contains a string representation of the
                split that is unique across all partitions. The function
                generates the string representation by concatenating the
                partitioning columns with the order of the split inside the
                partition (the numeric representation). In the string
                representation, hyphens separate partitioning column names from
                each other and from the order. For example, "pcol1- pcol2-3".
                Default Value: False
                Types: bool
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of SeriesSplitter.
            Output teradataml DataFrames can be accessed using attribute
            references, such as SeriesSplitterObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. output_table
                2. stats_table
                3. output
         
            When the argument "return_stats_table" is set to True, all the three
            output teradataml DataFrames are generated. But, when the argument
            'return_stats_table' is False, the "stats_table" output teradataml
            DataFrame will not be generated.
         
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("seriessplitter", "ibm_stock")
         
            # Create teradataml DataFrame objects.
            # The input table has the daily stock prices from 1961 to 1962.
            ibm_stock = DataFrame.from_table("ibm_stock")
         
            # Example 1 - This examples splits the time series stock data into
            # subpartitions.
            SeriesSplitter_out1 = SeriesSplitter(data = ibm_stock,
                                                partition_columns = ["name"],
                                                order_by_columns = ["period"],
                                                split_count = 50,
                                                accumulate = ["stockprice"]
                                                )
         
            # Print the results
            print(SeriesSplitter_out1.output_table)
            print(SeriesSplitter_out1.stats_table)
            print(SeriesSplitter_out1.output)
         
           # Example 2 - In the example "return_stats_table" is False which returns
           # only the output_table.
           SeriesSplitter_out2 = SeriesSplitter(data=ibm_stock,
                                                partition_columns='name',
                                                order_by_columns = 'period',
                                                split_count = 9,
                                                split_id_column = 'split_id',
                                                duplicate_rows_count = [1,1],
                                                return_stats_table = False,
                                                accumulate = 'stockprice',
                                                values_before_first = "1961-01-01",
                                                values_after_last = "NULL",
                                                partial_split_id = False
                                                )
           # Print the results
           print(SeriesSplitter_out1.output_table)
           print(SeriesSplitter_out1.output)
         
           # Note: When argument return_stats_table is False output teradataml DataFrame,
           #       (stats_table) is not created. If tried to access this attribute
           #       an INFO message will be thrown mentioning the same.
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.partition_columns  = partition_columns 
        self.duplicate_rows_count  = duplicate_rows_count 
        self.order_by_columns  = order_by_columns 
        self.split_count  = split_count 
        self.rows_per_split  = rows_per_split 
        self.accumulate  = accumulate 
        self.split_id_column  = split_id_column 
        self.return_stats_table  = return_stats_table 
        self.values_before_first  = values_before_first 
        self.values_after_last  = values_after_last 
        self.duplicate_column  = duplicate_column 
        self.partial_split_id  = partial_split_id 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["partition_columns", self.partition_columns, False, (str,list)])
        self.__arg_info_matrix.append(["duplicate_rows_count", self.duplicate_rows_count, True, (int,list)])
        self.__arg_info_matrix.append(["order_by_columns", self.order_by_columns, True, (str,list)])
        self.__arg_info_matrix.append(["split_count", self.split_count, True, (int)])
        self.__arg_info_matrix.append(["rows_per_split", self.rows_per_split, True, (int)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["split_id_column", self.split_id_column, True, (str)])
        self.__arg_info_matrix.append(["return_stats_table", self.return_stats_table, True, (bool)])
        self.__arg_info_matrix.append(["values_before_first", self.values_before_first, True, (str,list)])
        self.__arg_info_matrix.append(["values_after_last", self.values_after_last, True, (str,list)])
        self.__arg_info_matrix.append(["duplicate_column", self.duplicate_column, True, (str)])
        self.__arg_info_matrix.append(["partial_split_id", self.partial_split_id, True, (bool)])
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
        self.__awu._validate_input_columns_not_empty(self.partition_columns, "partition_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.partition_columns, "partition_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.order_by_columns, "order_by_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.order_by_columns, "order_by_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        # Validate that value passed to the output column argument is not empty.
        self.__awu._validate_input_columns_not_empty(self.split_id_column, "split_id_column")
        self.__awu._validate_input_columns_not_empty(self.duplicate_column, "duplicate_column")
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__output_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_seriessplitter0", use_default_database = True, gc_on_quit = True, quote=False, table_type = TeradataConstants.TERADATA_TABLE)
        self.__stats_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_seriessplitter1", use_default_database = True, gc_on_quit = True, quote=False, table_type = TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable", "StatsTable"]
        self.__func_output_args = [self.__output_table_temp_tablename, self.__stats_table_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("PartitionByColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.partition_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.order_by_columns is not None:
            self.__func_other_arg_sql_names.append("OrderByColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.order_by_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.split_count is not None and self.split_count != 4:
            self.__func_other_arg_sql_names.append("SplitCount")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.split_count, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        if self.rows_per_split is not None and self.rows_per_split != 1000:
            self.__func_other_arg_sql_names.append("RowsPerSplit")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.rows_per_split, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        if self.duplicate_rows_count is not None and self.duplicate_rows_count != 1:
            self.__func_other_arg_sql_names.append("DuplicateRowsCount")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.duplicate_rows_count, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        if self.split_id_column is not None and self.split_id_column != "split_id":
            self.__func_other_arg_sql_names.append("SplitIdColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.split_id_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.return_stats_table is not None and self.return_stats_table != True:
            self.__func_other_arg_sql_names.append("ReturnStatsTable")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.return_stats_table, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.values_before_first is not None and self.values_before_first != "-1":
            self.__func_other_arg_sql_names.append("ValuesBeforeFirst")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.values_before_first, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.values_after_last is not None and self.values_after_last != "null":
            self.__func_other_arg_sql_names.append("ValuesAfterLast")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.values_after_last, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.duplicate_column is not None:
            self.__func_other_arg_sql_names.append("DuplicateColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.duplicate_column, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.partial_split_id is not None and self.partial_split_id != False:
            self.__func_other_arg_sql_names.append("PartialSplitId")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.partial_split_id, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
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
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("InputTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "SeriesSplitter"
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
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix = "td_sqlmr_out_", use_default_database = True, gc_on_quit = True, quote = False, table_type = TeradataConstants.TERADATA_TABLE)
        try:
            # Generate the output.
            UtilFuncs._create_table(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.output_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__output_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__output_table_temp_tablename))
        self._mlresults.append(self.output_table)
        if self.return_stats_table:
            self.stats_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__stats_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__stats_table_temp_tablename))
            self._mlresults.append(self.stats_table)
        else:
            self.stats_table = "INFO: 'stats_table' output DataFrame is not created, when 'return_stats_table' is set to False."
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
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
        output_table = None,
        stats_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("output_table", None)
        kwargs.pop("stats_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.output_table  = output_table 
        obj.stats_table  = stats_table 
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
        obj.output_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output_table))
        obj._mlresults.append(obj.output_table)
        if obj.stats_table is None:
            obj.stats_table = "INFO: 'stats_table' output DataFrame is not created, when 'return_stats_table' is set to False."
        else:
            obj.stats_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.stats_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.stats_table))
            obj._mlresults.append(obj.stats_table)
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a SeriesSplitter class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ output_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.output_table)
        repr_string="{}\n\n\n############ stats_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.stats_table)
        return repr_string
        
