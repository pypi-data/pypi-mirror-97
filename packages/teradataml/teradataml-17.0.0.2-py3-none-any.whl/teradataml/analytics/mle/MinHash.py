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
# Function Version: 2.10
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

class MinHash:
    
    def __init__(self,
        data = None,
        id_column = None,
        items_column = None,
        hash_num = None,
        key_groups = None,
        seed_table = None,
        input_format = "integer",
        mincluster_size = 3,
        maxcluster_size = 5,
        delimiter = " ",
        data_sequence_column = None,
        seed_table_sequence_column = None):
        """
        DESCRIPTION:
            The MinHash function uses transaction history to cluster similar 
            items or users together. For example, the function can cluster items 
            that are frequently bought together or users that bought the same 
            items.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the input teradataml DataFrame.
         
            id_column:
                Required Argument.
                Specifies the name of the input teradataml DataFrame column that
                contains the values to be hashed into the same cluster. Typically
                these values are customer identifiers.
                Types: str
         
            items_column:
                Required Argument.
                Specifies the name of the input column that contains the values
                for hashing.
                Types: str
         
            hash_num:
                Required Argument.
                Specifies the number of hash functions to generate. The hash_num
                determines the number and size of clusters generated.
                Types: int
         
            key_groups:
                Required Argument.
                Specifies the number of key groups to generate. The
                number of key groups must be a divisor of hash_num. A
                large number of key groups decreases the probability that multiple
                users will be assigned to the same cluster identifier.
                Types: int
         
            seed_table:
                Optional Argument.
                Specifies the name of the teradataml DataFrame that contains the
                seeds to use for hashing. Typically, this teradataml DataFrame was
                created by an earlier MinHash call that is accessed by attribute
                'save_seed_to'.
         
            input_format:
                Optional Argument.
                Specifies the format of the values to be hashed (the values in
                items_column).
                Default Value: "integer"
                Permitted Values: bigint, integer, hex, string
                Types: str
         
            mincluster_size:
                Optional Argument.
                Specifies the minimum cluster size.
                Default Value: 3
                Types: int
         
            maxcluster_size:
                Optional Argument.
                Specifies the maximum cluster size.
                Default Value: 5
                Types: int
         
            delimiter:
                Optional Argument.
                Specifies the delimiter used between hashed values (typically
                customer identifiers) in the output. The default value is the space
                character.
                Default Value: " "
                Types: str
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            seed_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "seed_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of MinHash.
            Output teradataml DataFrames can be accessed using attribute
            references, such as MinHashObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. output_table
                2. save_seed_to
                3. output
         
            Note: When argument seed_table is used, output teradataml DataFrame,
                  save_seed_to, is not created. If tried to access this attribute
                  an INFO message will be thrown mentioning the same.
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("minhash", "salesdata")
         
            # Create teradataml DataFrame objects.
            salesdata = DataFrame.from_table("salesdata")
         
            # Example 1 - Create clusters of users based on items purchased.
            MinHash_out1 = MinHash(data = salesdata,
                                   id_column = "userid",
                                   items_column = "itemid",
                                   hash_num = 1002,
                                   key_groups = 3
                                   )
         
            # Print the results
            print(MinHash_out1.output_table)
            print(MinHash_out1.save_seed_to)
            print(MinHash_out1.output)
         
            # Example 2 - Use the previously generated seed table as input.
            MinHash_out2 = MinHash(data = salesdata,
                                   id_column = "userid",
                                   items_column = "itemid",
                                   hash_num = 1002,
                                   key_groups = 3,
                                   seed_table = MinHash_out1.save_seed_to
                                   )
         
            # Print the results
            print(MinHash_out2.output_table)
            print(MinHash_out2.output)
         
            # Note: When argument seed_table is used, output teradataml DataFrame,
            #       save_seed_to, is not created. If tried to access this attribute
            #       an INFO message will be thrown mentioning the same.
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.id_column  = id_column 
        self.items_column  = items_column 
        self.hash_num  = hash_num 
        self.key_groups  = key_groups 
        self.seed_table  = seed_table 
        self.input_format  = input_format 
        self.mincluster_size  = mincluster_size 
        self.maxcluster_size  = maxcluster_size 
        self.delimiter  = delimiter 
        self.data_sequence_column  = data_sequence_column 
        self.seed_table_sequence_column  = seed_table_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["id_column", self.id_column, False, (str)])
        self.__arg_info_matrix.append(["items_column", self.items_column, False, (str)])
        self.__arg_info_matrix.append(["hash_num", self.hash_num, False, (int)])
        self.__arg_info_matrix.append(["key_groups", self.key_groups, False, (int)])
        self.__arg_info_matrix.append(["seed_table", self.seed_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["input_format", self.input_format, True, (str)])
        self.__arg_info_matrix.append(["mincluster_size", self.mincluster_size, True, (int)])
        self.__arg_info_matrix.append(["maxcluster_size", self.maxcluster_size, True, (int)])
        self.__arg_info_matrix.append(["delimiter", self.delimiter, True, (str)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["seed_table_sequence_column", self.seed_table_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.seed_table, "seed_table", None)
        
        # Check for permitted values
        input_format_permitted_values = ["BIGINT", "INTEGER", "HEX", "STRING"]
        self.__awu._validate_permitted_values(self.input_format, input_format_permitted_values, "input_format")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.id_column, "id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.id_column, "id_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.items_column, "items_column")
        self.__awu._validate_dataframe_has_argument_columns(self.items_column, "items_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.seed_table_sequence_column, "seed_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.seed_table_sequence_column, "seed_table_sequence_column", self.seed_table, "seed_table", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__output_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_minhash0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        # Check is manually added here. This output will be produced only when no argument is passed to seed.table
        if self.seed_table is None:
            self.__save_seed_to_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_minhash1",
                                                                                     use_default_database=True,
                                                                                     gc_on_quit=True, quote=False,
                                                                                     table_type=TeradataConstants.TERADATA_TABLE)
        else:
            self.__save_seed_to_temp_tablename = None
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable", "SaveSeedTo"]
        self.__func_output_args = [self.__output_table_temp_tablename, self.__save_seed_to_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("UserIDColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.id_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("ItemIDColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.items_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("HashNum")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.hash_num, "'"))
        self.__func_other_arg_json_datatypes.append("INTEGER")
        
        self.__func_other_arg_sql_names.append("KeyGroups")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.key_groups, "'"))
        self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.input_format is not None and self.input_format != "integer":
            self.__func_other_arg_sql_names.append("InputFormat")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.input_format, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.mincluster_size is not None and self.mincluster_size != 3:
            self.__func_other_arg_sql_names.append("MinClusterSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mincluster_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.maxcluster_size is not None and self.maxcluster_size != 5:
            self.__func_other_arg_sql_names.append("MaxClusterSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.maxcluster_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.delimiter is not None and self.delimiter != " ":
            self.__func_other_arg_sql_names.append("Delimiter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.delimiter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.seed_table_sequence_column is not None:
            sequence_input_by_list.append("SeedTable:" + UtilFuncs._teradata_collapse_arglist(self.seed_table_sequence_column, ""))
        
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
        
        # Process seed_table
        if self.seed_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.seed_table, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("SeedTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "MinHash"
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
        self._mlresults.append(self.output_table)
        if self.seed_table is None:
            self.save_seed_to = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__save_seed_to_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__save_seed_to_temp_tablename))
            self._mlresults.append(self.save_seed_to)
        else:
            self.save_seed_to = "INFO: 'save_seed_to' output DataFrame is not created, in case of seed_table argument is used."
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
        save_seed_to = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("output_table", None)
        kwargs.pop("save_seed_to", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.output_table  = output_table 
        obj.save_seed_to  = save_seed_to 
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

        if obj.save_seed_to is not None:
            obj.save_seed_to = obj.__awu._create_data_set_object(df_input = UtilFuncs._extract_table_name(obj.save_seed_to), source_type="table", database_name=UtilFuncs._extract_db_name(obj.save_seed_to))
            obj._mlresults.append(obj.save_seed_to)
        else:
            obj.save_seed_to = "INFO: 'save_seed_to' output DataFrame is not created, in case of seed_table argument is used."

        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a MinHash class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ output_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.output_table)
        repr_string="{}\n\n\n############ save_seed_to Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.save_seed_to)
        return repr_string
        
