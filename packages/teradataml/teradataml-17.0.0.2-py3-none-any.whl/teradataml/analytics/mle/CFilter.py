#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Abhinav Sahu (abhinav.sahu@teradata.com)
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

class CFilter:
    
    def __init__(self,
        data = None,
        input_columns = None,
        join_columns = None,
        add_columns = None,
        partition_key = "col1_item1",
        max_itemset = 100,
        data_sequence_column = None,
        null_handling = True,
        use_basketgenerator = True):

        """
        DESCRIPTION:
            The CFilter function is a general-purpose collaborative filter.


        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the data 
                to filter.

            input_columns:
                Required Argument.
                Specifies the names of the input teradataml DataFrame columns that 
                contain the data to filter.
                Types: str OR list of Strings (str)

            join_columns:
                Required Argument.
                Specifies the names of the input teradataml DataFrame columns to join.
                Types: str OR list of Strings (str)

            add_columns:
                Optional Argument.
                Specifies the names of the input columns to copy to the output table. 
                The function partitions the input data and the output teradataml 
                DataFrame on these columns. By default, the function treats the input 
                data as belonging to one partition.
                Note: Specifying a column as both an add_column and a join_column causes
                      incorrect counts in partitions.
                Types: str OR list of Strings (str)

            partition_key:
                Optional Argument.
                Specifies the names of the output column to use as the partition key.
                Default Value: "col1_item1"
                Types: str

            max_itemset:
                Optional Argument.
                Specifies the maximum size of the item set.
                Default Value: 100
                Types: int

            null_handling:
                Optional Argument.
                Specifies whether to handle null values in the input. If the input
                data contains null values, then this argument should be True.
                Note: "null_handling" is only available when teradataml is connected to
                Vantage 1.3.
                Default Value: True
                Types: bool

            use_basketgenerator:
                Optional Argument.
                Specifies whether to use BasketGenerator function to generate baskets.
                Note: "use_basketgenerator" is only available when teradataml is connected to
                Vantage 1.3.
                Default Value: True
                Types: bool

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of CFilter.
            Output teradataml DataFrames can be accessed using attribute
            references, such as CFilterObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                1. output_table
                2. output


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load example data.
            load_example_data("cfilter", "sales_transaction")

            # Provided example table is: sales_transaction
            # These input table contains data of an office supply chain store. The columns are:
            # orderid: order (transaction) identifier
            # orderdate: order date
            # orderqty: quantity of product ordered
            # region: geographic region of store where order was placed
            # customer_segment: segment of customer who ordered product
            # prd_category: category of product ordered
            # product: product ordered

            # Create teradataml DataFrame objects.
            sales_transaction = DataFrame.from_table("sales_transaction")

            # Example 1 - Collaborative Filtering by Product.
            CFilter_out1 = CFilter(data = sales_transaction,
                                  input_columns = ["product"],
                                  join_columns = ["orderid"],
                                  add_columns = ["region"]
                                  )
            # Print the output data
            print(CFilter_out1)

            # Example 2 - Collaborative Filtering by Customer Segment.
            CFilter_out2 = CFilter(data = sales_transaction,
                                  input_columns = ["customer_segment"],
                                  join_columns = ["product"]
                                  )
            # Print the output data
            print(CFilter_out2)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.input_columns  = input_columns 
        self.join_columns  = join_columns 
        self.add_columns  = add_columns
        self.partition_key = partition_key
        self.max_itemset = max_itemset
        self.data_sequence_column = data_sequence_column
        self.null_handling  = null_handling
        self.use_basketgenerator  = use_basketgenerator
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["input_columns", self.input_columns, False, (str,list)])
        self.__arg_info_matrix.append(["join_columns", self.join_columns, False, (str,list)])
        self.__arg_info_matrix.append(["add_columns", self.add_columns, True, (str,list)])
        self.__arg_info_matrix.append(["partition_key", self.partition_key, True, (str)])
        self.__arg_info_matrix.append(["max_itemset", self.max_itemset, True, (int)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["null_handling", self.null_handling, True, (bool)])
        self.__arg_info_matrix.append(["use_basketgenerator", self.use_basketgenerator, True, (bool)])
        
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
        self.__awu._validate_input_columns_not_empty(self.input_columns, "input_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.input_columns, "input_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.join_columns, "join_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.join_columns, "join_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.add_columns, "add_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.add_columns, "add_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__output_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_cfilter0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable"]
        self.__func_output_args = [self.__output_table_temp_tablename]
        
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
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.input_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("JoinColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.join_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.add_columns is not None:
            self.__func_other_arg_sql_names.append("PartitionColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.add_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.partition_key is not None and self.partition_key != "col1_item1":
            self.__func_other_arg_sql_names.append("PartitionKey")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.partition_key, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.max_itemset is not None and self.max_itemset != 100:
            self.__func_other_arg_sql_names.append("MaxDistinctItems")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_itemset, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.null_handling is not None and self.null_handling != True:
            self.__func_other_arg_sql_names.append("NullHandling")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.null_handling, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.use_basketgenerator is not None and self.use_basketgenerator != True:
            self.__func_other_arg_sql_names.append("UseBasketGenerator")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.use_basketgenerator, "'"))
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
        
        function_name = "CFilter"
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
        self.output_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__output_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__output_table_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.output_table)
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
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("output_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.output_table  = output_table 
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
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.output_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a CFilter class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ output_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.output_table)
        return repr_string
        
