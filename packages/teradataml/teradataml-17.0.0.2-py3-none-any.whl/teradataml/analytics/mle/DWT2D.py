#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Adithya Avvaru (adithya.avvaru@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.6
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

class DWT2D:
    
    def __init__(self,
        data = None,
        input_columns = None,
        index_columns = None,
        range = None,
        wavelet = None,
        wavelet_filter = None,
        level = None,
        extension_mode = "sym",
        compact_output = True,
        partition_columns = None,
        data_sequence_column = None,
        wavelet_filter_sequence_column = None):
        """
        DESCRIPTION:
            The DWT2D function implements the Mallat algorithm (an iterative
            algorithm in the Discrete Wavelet Transform field) on 2-dimensional
            matrices and applies wavelet transform on multiple sequences
            simultaneously.
         
            The input is a set of sequences. Typically, each sequence is a matrix
            that contains a position in 2-dimensional space (y and x indexes or
            coordinates) and its corresponding values. You specify the wavelet
            name or wavelet filter teradataml DataFrame, transform level, and
            (optionally) extension mode. The function returns the transformed
            sequences in Hilbert space with the corresponding component
            identifiers and indices. (The transformation is also called the
            decomposition.)
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the
                sequences to be transformed.
         
            input_columns:
                Required Argument.
                Specifies the names of the columns in the input teradataml DataFrame
                that contain the data to be transformed. These columns must contain
                numeric values between -1e308 and 1e308. The function treats
                NULL in columns as 0.
                Types: str OR list of Strings (str)
         
            index_columns:
                Required Argument.
                Specifies the columns that contain the indexes of the input
                sequences. This argument should have exactly two column names.
                One column contains the x coordinates and the other
                contains y coordinates.
                Types: str OR list of Strings (str)
         
            range:
                Optional Argument.
                Specifies the start and end indexes of the input data, all of which
                must be integers. The default values for each sequence are:
                    • starty: minimum y index
                    • startx: minimum x index
                    • endy: maximum y index
                    • endx: maximum x index.
                The function treats any NULL value as 0.
                The range can specify a maximum of 1,000,000 cells.
                Types: str
         
            wavelet:
                Optional Argument.
                Specifies a wavelet filter name.
                    Wavelet Family       Supported Wavelet Names (wavelet values)
                    Daubechies           'db1' or 'haar', 'db2', .... ,'db10'
                    Coiflets             'coif1', ... , 'coif5'
                    Symlets              'sym1', ... ,' sym10'
                    Discrete Meyer       'dmey'
                    Biorthogonal         'bior1.1', 'bior1.3', 'bior1.5',
                                         'bior2.2', 'bior2.4', 'bior2.6', 'bior2.8',
                                         'bior3.1', 'bior3.3', 'bior3.5', 'bior3.7', 'bior3.9',
                                         'bior4.4', 'bior5.5'
                    Reverse Biorthogonal 'rbio1.1', 'rbio1.3', 'rbio1.5'
                                         'rbio2.2', 'rbio2.4', 'rbio2.6', 'rbio2.8',
                                         'rbio3.1', 'rbio3.3', 'rbio3.5', 'rbio3.7','rbio3.9',
                                         'rbio4.4', 'rbio5.5'
                Permitted values for wavelet are under column 'Supported Wavelet Names' above.
                Types: str
         
            wavelet_filter:
                Optional Argument.
                Specifies the name of the teradataml DataFrame that contains the
                coefficients of the wave filters.
         
            level:
                Required Argument.
                Specifies the wavelet transform level. The value level must be an
                integer in the range [1, 1000].
                Types: int
         
            extension_mode:
                Optional Argument.
                Specifies the method for handling border distortion
                Supported Extension Modes (extension_mode values):
                    • "sym" : Symmetrically replicate boundary values, mirroring
                              the points near the boundaries.
                              For example: 4 4 3 2 1 | 1 2 3 4 | 4 3 2 1 1
                    • "zpd" : Zero-pad boundary values with zero.
                              For example: 0 0 0 0 0 | 1 2 3 4 | 0 0 0 0 0
                    • "ppd" : Periodic extension, fill boundary values as the
                              input sequence is a periodic one.
                              For example: 4 1 2 3 4 | 1 2 3 4 | 1 2 3 4 1
                Default Value: "sym"
                Permitted Values: sym, zpd, ppd
                Types: str
         
            compact_output:
                Optional Argument.
                Specifies whether to ignore (not output) rows in which all
                coefficient values are very small (having an absolute value less
                than 1e-12). For a sparse input matrix, ignoring such rows
                reduces the output teradataml DataFrame size.
                Default Value: True
                Types: bool
         
            partition_columns:
                Optional Argument.
                Specifies the names of the partition_columns, which identify the
                sequences. Rows with the same partition_columns values belong to
                the same sequence. If you specify multiple partition_columns,
                then the function treats the first one as the distribute key of
                the output and meta teradataml DataFrames. By default, all rows
                belong to one sequence, and the function generates a distribute
                key column named dwt_idrandom_name in both the output teradataml
                DataFrame and the meta teradataml DataFrame. In both teradataml
                DataFrames, every cell of dwt_idrandom_name has the value 1.
                Types: str OR list of Strings (str)
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to asensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            wavelet_filter_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "wavelet_filter". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of DWT2D.
            Output teradataml DataFrames can be accessed using attribute
            references, such as DWT2DObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. coefficient
                2. meta_table
                3. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # This example uses climate data in many cities in the states of
            # California (CA), Texas (TX), and Washington (WA). The cities are
            # represented by two-dimensional coordinates (latitude and
            # longitude). The data are temperature (in degrees Fahrenheit),
            # pressure (in Mbars), and dew point (in degrees Fahrenheit). The
            # function generates a coefficient model teradataml DataFrame and a
            # meta_table teradataml DataFrame, which are used as input to the
            # function IDWT2D.
            # The table 'wft_testing' contains wavelet filter information
            # needed to generate coefficient model teradataml DataFrame and a
            # meta_table teradataml DataFrame.
         
            # Load example data.
            load_example_data("dwt2d", ["twod_climate_data", "wft_testing"])
         
            # Create teradataml DataFrame objects.
            twod_climate_data = DataFrame.from_table("twod_climate_data")
            wft_testing = DataFrame.from_table("wft_testing")
         
            # Example 1 : Using 'db2' wavelet to apply DWT2D function on columns,
            #             "temp_f", "pressure_mbar" and "dewpoint_f" (of DataFrame
            #             'twod_climate_data') partitioned by the column "state".
            DWT2D_out = DWT2D(data = twod_climate_data,
                              input_columns = ["temp_f","pressure_mbar","dewpoint_f"],
                              index_columns = ["latitude","longitude"],
                              wavelet = "db2",
                              level = 2,
                              compact_output = True,
                              partition_columns = ["state"]
                              )
            # Print the results
            print(DWT2D_out.coefficient) # Prints coefficient DataFrame which stores
                                         # the coefficients generated by the wavelet
                                         # transform.
            print(DWT2D_out.meta_table)  # Prints meta_table DataFrame which stores
                                         # the meta information for the wavelet
                                         # transform.
            print(DWT2D_out.output)      # Prints output teradataml DataFrame.
         
         
            # Example 2 : Using wavelet_filter DataFrame to apply DWT2D function
            #             on columns, "temp_f", "pressure_mbar" and "dewpoint_f" (of
            #             DataFrame 'twod_climate_data') partitioned by the column
            #             "state".
            DWT2D_out = DWT2D(data = twod_climate_data,
                              input_columns = ["temp_f","pressure_mbar","dewpoint_f"],
                              wavelet_filter = wft_testing,
                              index_columns = ["latitude","longitude"],
                              level = 2,
                              partition_columns = "state",
                              wavelet_filter_sequence_column="filtername"
                          )
         
            # Print the results
            print(DWT2D_out.coefficient) # Prints coefficient DataFrame which stores
                                         # the coefficients generated by the wavelet
                                         # transform.
            print(DWT2D_out.meta_table)  # Prints meta_table DataFrame which stores
                                         # the meta information for the wavelet
                                         # transform.
            print(DWT2D_out.output)      # Prints output teradataml DataFrame.
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.input_columns  = input_columns 
        self.index_columns  = index_columns 
        self.range  = range 
        self.wavelet  = wavelet 
        self.wavelet_filter  = wavelet_filter 
        self.level  = level 
        self.extension_mode  = extension_mode 
        self.compact_output  = compact_output 
        self.partition_columns  = partition_columns 
        self.data_sequence_column  = data_sequence_column 
        self.wavelet_filter_sequence_column  = wavelet_filter_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["input_columns", self.input_columns, False, (str,list)])
        self.__arg_info_matrix.append(["index_columns", self.index_columns, False, (str,list)])
        self.__arg_info_matrix.append(["range", self.range, True, (str)])
        self.__arg_info_matrix.append(["wavelet", self.wavelet, True, (str)])
        self.__arg_info_matrix.append(["wavelet_filter", self.wavelet_filter, True, (DataFrame)])
        self.__arg_info_matrix.append(["level", self.level, False, (int)])
        self.__arg_info_matrix.append(["extension_mode", self.extension_mode, True, (str)])
        self.__arg_info_matrix.append(["compact_output", self.compact_output, True, (bool)])
        self.__arg_info_matrix.append(["partition_columns", self.partition_columns, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["wavelet_filter_sequence_column", self.wavelet_filter_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.wavelet_filter, "wavelet_filter", None)
        
        # Check for permitted values
        extension_mode_permitted_values = ["SYM", "ZPD", "PPD"]
        self.__awu._validate_permitted_values(self.extension_mode, extension_mode_permitted_values, "extension_mode")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.index_columns, "index_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.index_columns, "index_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.input_columns, "input_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.input_columns, "input_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.partition_columns, "partition_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.partition_columns, "partition_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.wavelet_filter_sequence_column, "wavelet_filter_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.wavelet_filter_sequence_column, "wavelet_filter_sequence_column", self.wavelet_filter, "wavelet_filter", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__coefficient_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_dwt2d0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__meta_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_dwt2d1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable", "MetaTable"]
        self.__func_output_args = [self.__coefficient_temp_tablename, self.__meta_table_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("IndexColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.index_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("TargetColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.input_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.partition_columns is not None:
            self.__func_other_arg_sql_names.append("PartitionColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.partition_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("WaveletTransformLevel")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.level, "'"))
        self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.range is not None:
            self.__func_other_arg_sql_names.append("Range")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.range, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.compact_output is not None and self.compact_output != True:
            self.__func_other_arg_sql_names.append("CompactOutput")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.compact_output, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.wavelet is not None:
            self.__func_other_arg_sql_names.append("Wavelet")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.wavelet, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.extension_mode is not None and self.extension_mode != "sym":
            self.__func_other_arg_sql_names.append("ExtensionMode")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.extension_mode, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.wavelet_filter_sequence_column is not None:
            sequence_input_by_list.append("WaveletFilterTable:" + UtilFuncs._teradata_collapse_arglist(self.wavelet_filter_sequence_column, ""))
        
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
        
        # Process wavelet_filter
        if self.wavelet_filter is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.wavelet_filter, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("WaveletFilterTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "DWT2D"
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
        self.coefficient = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__coefficient_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__coefficient_temp_tablename))
        self.meta_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__meta_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__meta_table_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.coefficient)
        self._mlresults.append(self.meta_table)
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
        coefficient = None,
        meta_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("coefficient", None)
        kwargs.pop("meta_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.coefficient  = coefficient 
        obj.meta_table  = meta_table 
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
        obj.coefficient = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.coefficient), source_type="table", database_name=UtilFuncs._extract_db_name(obj.coefficient))
        obj.meta_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.meta_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.meta_table))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.coefficient)
        obj._mlresults.append(obj.meta_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a DWT2D class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ coefficient Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.coefficient)
        repr_string="{}\n\n\n############ meta_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.meta_table)
        return repr_string
        
