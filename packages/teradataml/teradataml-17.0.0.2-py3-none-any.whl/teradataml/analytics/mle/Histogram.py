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
# Function Version: 1.5
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

class Histogram:
    
    def __init__(self,
        data = None,
        auto_bin = None,
        custom_bin_table = None,
        custom_bin_column = None,
        bin_size = None,
        start_value = None,
        end_value = None,
        value_column = None,
        inclusion = "left",
        groupby_columns = None,
        data_sequence_column = None,
        custom_bin_table_sequence_column = None):
        """
        DESCRIPTION:
            Histograms are used to assess the shape of a data distribution.
            The Histogram function calculates the frequency distribution of a
            data set using sophisticated binning techniques that can
            automatically calculate the bin width and number of bins. The
            function maps each input row to one bin and returns the frequency
            (row count) and proportion (percentage of rows) of each bin.
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the input data.
         
            auto_bin:
                Optional Argument.
                Specifies either the algorithm to be used for selecting bin
                boundaries or the approximate number of bins to be found. The
                permitted values are STURGES, SCOTT, or a positive integer. If
                this argument is present, the arguments custom_bin_table,
                custom_bin_column, start_value, bin_size, and end_value cannot
                be present.
                Types: str
         
            custom_bin_table:
                Optional Argument.
                Specifies a teradataml DataFrame containing the boundary
                points between bins. If this argument is present, the argument
                custom_bin_column must also be present and the arguments
                auto_bin, start_value, bin_size, and end_value cannot be
                present.
         
            custom_bin_column:
                Optional Argument.
                Specifies the column, in the custom_bin_table, containing the
                boundary values. Input columns must contain values with numeric
                Python data types (int, float). If this argument is present, the
                argument custom_bin_table must also be present and the
                arguments auto_bin, start_value, bin_size, and end_value cannot
                be present.
                Types: str
         
            bin_size:
                Optional Argument.
                For equally sized bins, a double value specifying the width of
                the bin. Omit this argument if you are not using equally sized
                bins. The input value must be greater than 0.0. If this
                argument is present, the arguments start_value and end_value
                must also be present and the arguments auto_bin,
                custom_bin_table and custom_bin_column cannot be present.
                Types: float
         
            start_value:
                Optional Argument.
                Specifies the smallest value to be used in binning. If this
                argument is present, the arguments bin_size and end_value must
                also be present and the arguments auto_bin, custom_bin_table
                and custom_bin_column cannot be present.
                Types: float
         
            end_value:
                Optional Argument.
                Specifies the largest value to be used in binning. If this
                argument is present, the arguments start_value and bin_size
                must also be present and the arguments auto_bin,
                custom_bin_table and custom_bin_column cannot be present.
                Types: float
         
            value_column:
                Required Argument.
                Specifies the column in the input teradataml DataFrame for
                which statistics will be computed. Column must contain a values
                with numeric Python data types (int, float).
                Types: str
         
            inclusion:
                Optional Argument.
                Indicates whether points on bin boundaries should be included
                in the bin on the left or the bin on the right.
                Default Value: "left"
                Permitted Values: left, right
                Types: str
         
            groupby_columns:
                Optional Argument.
                Specifies the columns in the input teradataml DataFrame used to
                group values for binning. These columns cannot contain values
                with double or float data types.
                Types: str OR list of Strings (str)
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            custom_bin_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "custom_bin_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of Histogram.
            Output teradataml DataFrames can be accessed using attribute
            references, such as HistogramObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                1. output
                2. output_table
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("histogram", ['bin_breaks', 'cars_hist'])
         
            # The 'cars_hist' table has the cylinder (cyl) and horsepower (hp)
            # data for different car models.
            # The 'bin_breaks' table has the boundary values for the custom
            # bins to be used while generating the histogram.
         
            # Create TeradataML DataFrame objects.
            cars_hist = DataFrame.from_table('cars_hist')
            custom_bin = DataFrame.from_table('bin_breaks')
         
            # Example 1: Using auto_bin.
            result = Histogram( data = cars_hist,
                                value_column = 'hp',
                                auto_bin = 'Sturges'
                                )
            # Print the results
            print(result.output_table)
         
            # Example 2: Using start_value, end_value and bin_size.
            result = Histogram( data = cars_hist,
                                value_column = 'hp',
                                inclusion = 'left',
                                start_value = 100.0,
                                end_value = 400.0,
                                bin_size = 100.0
                                )
            # Print the results
            print(result.output_table)
         
            # Example 3: Using custom_bin_table.
            result = Histogram( data = cars_hist,
                                value_column = 'hp',
                                inclusion = 'left',
                                custom_bin_table = custom_bin,
                                custom_bin_column ='break'
                                )
            # Print the results
            print(result.output_table)
         
            # Example 4: Using groupby_columns on auto_bin feature.
            result = Histogram( data = cars_hist,
                                value_column = 'hp',
                                inclusion = 'left',
                                auto_bin = 'STURGES',
                                groupby_columns = 'cyl'
                                )
            # Print the results
            print(result.output_table)
         
            # Example 5: Using right 'inclusion' feature.
            result = Histogram( data = cars_hist,
                                bin_size = 50.0,
                                start_value = 20.0,
                                end_value = 400.0,
                                value_column = 'hp',
                                inclusion = 'right'
                                )
            # Print the results
            print(result.output_table)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.auto_bin  = auto_bin 
        self.custom_bin_table  = custom_bin_table 
        self.custom_bin_column  = custom_bin_column 
        self.bin_size  = bin_size 
        self.start_value  = start_value 
        self.end_value  = end_value 
        self.value_column  = value_column 
        self.inclusion  = inclusion 
        self.groupby_columns  = groupby_columns 
        self.data_sequence_column  = data_sequence_column 
        self.custom_bin_table_sequence_column  = custom_bin_table_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["auto_bin", self.auto_bin, True, (str)])
        self.__arg_info_matrix.append(["custom_bin_table", self.custom_bin_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["custom_bin_column", self.custom_bin_column, True, (str)])
        self.__arg_info_matrix.append(["bin_size", self.bin_size, True, (float)])
        self.__arg_info_matrix.append(["start_value", self.start_value, True, (float)])
        self.__arg_info_matrix.append(["end_value", self.end_value, True, (float)])
        self.__arg_info_matrix.append(["value_column", self.value_column, False, (str)])
        self.__arg_info_matrix.append(["inclusion", self.inclusion, True, (str)])
        self.__arg_info_matrix.append(["groupby_columns", self.groupby_columns, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["custom_bin_table_sequence_column", self.custom_bin_table_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.custom_bin_table, "custom_bin_table", None)
        
        # Check for permitted values
        inclusion_permitted_values = ["LEFT", "RIGHT"]
        self.__awu._validate_permitted_values(self.inclusion, inclusion_permitted_values, "inclusion")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.value_column, "value_column")
        self.__awu._validate_dataframe_has_argument_columns(self.value_column, "value_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.custom_bin_column, "custom_bin_column")
        self.__awu._validate_dataframe_has_argument_columns(self.custom_bin_column, "custom_bin_column", self.custom_bin_table, "custom_bin_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.groupby_columns, "groupby_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.groupby_columns, "groupby_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.custom_bin_table_sequence_column, "custom_bin_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.custom_bin_table_sequence_column, "custom_bin_table_sequence_column", self.custom_bin_table, "custom_bin_table", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__output_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_histogram0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
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
        
        self.__func_other_arg_sql_names.append("TargetColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.value_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.custom_bin_column is not None:
            self.__func_other_arg_sql_names.append("CustomBinColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.custom_bin_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.groupby_columns is not None:
            self.__func_other_arg_sql_names.append("GroupbyColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.groupby_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.inclusion is not None and self.inclusion != "left":
            self.__func_other_arg_sql_names.append("Inclusion")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.inclusion, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.auto_bin is not None:
            self.__func_other_arg_sql_names.append("AutoBin")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.auto_bin, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.start_value is not None:
            self.__func_other_arg_sql_names.append("StartValue")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.start_value, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.end_value is not None:
            self.__func_other_arg_sql_names.append("EndValue")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.end_value, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.bin_size is not None:
            self.__func_other_arg_sql_names.append("BinSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.bin_size, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.custom_bin_table_sequence_column is not None:
            sequence_input_by_list.append("CustomBinTable:" + UtilFuncs._teradata_collapse_arglist(self.custom_bin_table_sequence_column, ""))
        
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
        
        # Process custom_bin_table
        if self.custom_bin_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.custom_bin_table, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("CustomBinTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "Histogram"
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
        Returns the string representation for a Histogram class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ output_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.output_table)
        return repr_string
        
