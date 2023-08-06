#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2020 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Gouri Patwardhan (gouri.patwardhan@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
#
# Version: 1.2
# Function Version: 1.2
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

class Correlation2:
    
    def __init__(self,
        data = None,
        target_column_pairs = None,
        target_columns = None,
        partition_columns = None,
        exception_attribute = None,
        vif = False,
        vif_summary = None,
        vif_threshold = 10.0,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The Correlation2 function computes correlations between specified
            pairs of teradataml DataFrame columns. Measuring correlation lets you 
            determine if the value of one variable is useful in predicting the 
            value of another. You can also use Correlation2 to detect and remove
            collinearity in input data by computing variance inflation factor 
            (VIF).
            Note:
                1. This function is supported only on Vantage 1.3 or later.
                2. Teradata recommends to use Correlation2 on Vantage 1.3 instead of Correlation.
        
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame that contains the Xi and Yi pairs.

            target_column_pairs:
                Required when the argument "vif" is set to 'False', disallowed otherwise.
                Specifies pairs of columns for which correlations are to be calculated.
                For each column pair, "col_name1:col_name2", the function calculates
                the correlation between col_name1 and col_name2.
                For each column range, "[col_index1:col_index2]", the function calculates
                the correlation between every pair of columns in the range.
                For example, if you specify "[1:3]", the function calculates the correlation
                between the pairs (1,2), (1,3), (2,3),(1,1),(3,3). The mininum value of
                col_index1 is 0 and col_index1 must be less than col_index2.
                Types: str OR list of Strings (str)

            target_columns:
                Required when the argument "vif" is set to 'True', disallowed otherwise.
                Specifies the names of the target columns for which to compare the VIF
                with the specified vif_threshold.
                Types: str OR list of Strings (str)

            partition_columns:
                Optional Argument.
                Specifies the names of the input columns that define the group for 
                calculating correlation. By default, all input columns belong to a
                single group, for which the function is calculating correlation.
                Types: str OR list of Strings (str)
            
            exception_attribute:
                Optional when argument "vif" is set to 'True', disallowed otherwise.
                Specifies the name of the column that will not be eliminated even if 
                VIF score is larger than the value in "vif_threshold" argument.
                Types: str
                Note:
                    Values in "exception_attribute" must also be specified in the
                    argument "target_columns".
            
            vif:
                Optional Argument.
                Specifies whether the function computes the VIF score or not.
                Default Value: False
                Types: bool

            vif_threshold:
                Optional when the argument "vif" is set to 'True', disallowed otherwise.
                Specifies the threshold for calculated VIF score.
                If the VIF score for a predictor is above this threshold,
                we can eliminate it in the modeling process.
                To detect significant collinearity, specify a vif_threshold in [5.0, 20.0].
                Default Value: 10.0
                Types: float

            
            vif_summary:
                Optional when the argument "vif" is set to 'True', disallowed otherwise.
                Specifies whether to output the final VIF scores or VIF scores from
                each iteration of the algorithm.
                When set to 'True', final VIF score is displayed.
                When set to 'False', VIF score at the end of each iteration is displayed.
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
            Instance of Correlation2.
            Output teradataml DataFrames can be accessed using attribute
            references, such as Correlation2Obj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. correlation_data
                2. output
        
        
        RAISES:
            TeradataMlException
        
        
        EXAMPLES:
            # Load example data.
            load_example_data("correlation", "corr_input")
            
            # Create teradataml DataFrame objects.
            corr_input = DataFrame.from_table("corr_input")
            
            # Example 1: The function calculates the correlation between each pair of columns
            # in the "target_column_pairs" argument. This example compares GDP to GDPdeflator,
            # the employed population to GDP, the number of people unemployed, and the number
            # of people in the armed forces.
            Correlation_out1 = Correlation2(data = corr_input,
                                           target_column_pairs = ["[2:3]", "employed:gdp",
                                           "employed:unemployed", "employed:armedforces"],
                                           partition_columns = ["state"]
                                           )

            # Print the correlation_data DataFrame.
            print(Correlation_out1.correlation_data)

            # Example 2: This example does not use "vif" and omits the "partition_columns"
            # argument, so the function determines the correlation values for the overall
            # population and does not group the data by state.
            Correlation_out2 = Correlation2(data = corr_input,
                                           target_column_pairs = ["[2:3]", "employed:gdp",
                                           "employed:unemployed", "employed:armedforces"]
                                           )

            # Print the correlation_data DataFrame.
            print(Correlation_out2.correlation_data)
            
            # Example 3: This example sets "vif" argument to 'True' but does not specify
            # the "exception_attribute" argument.
            Correlation_out3 = Correlation2(data = corr_input,
                                           target_columns = ["gdp", "unemployed", "armedforces", "employed"],
                                           partition_columns = ["state"],
                                           vif = True,
                                           vif_threshold = 10.0
                                           )

            # Print the correlation_data DataFrame.
            print(Correlation_out3.correlation_data)
            
            # Example 4: This example uses "vif" argument and specifies the
            # "exception_attribute" argument.
            Correlation_out4 = Correlation2(data = corr_input,
                                           target_columns = ["gdp", "unemployed", "armedforces", "employed"],
                                           partition_columns = ["state"],
                                           exception_attribute = "gdp",
                                           vif = True,
                                           vif_threshold = 10.0
                                           )

            # Print the correlation_data DataFrame.
            print(Correlation_out4.correlation_data)

            # Example 5: This example sets "vif" argument to 'True', specifies the
            # "exception_attribute" argument and sets "vif_summary" argument to 'False'
            # to display only final VIF scores.
            Correlation_out5 = Correlation2(data = corr_input,
                                           target_columns = ["gdp", "unemployed", "armedforces", "employed"],
                                           partition_columns = ["state"],
                                           exception_attribute = "gdp",
                                           vif = True,
                                           vif_summary = False,
                                           vif_threshold = 10.0
                                           )

            # Print the correlation_data DataFrame.
            print(Correlation_out5.correlation_data)

            # Example 6: This example uses "target_columns" and "partition_columns"
            # as column ranges to display only final VIF scores.
            Correlation_out6 = Correlation2(data = corr_input,
                                           target_columns = ["gdp:employed"],
                                           partition_columns = ["state:armedforces"],
                                           exception_attribute = "gdp",
                                           vif = True,
                                           vif_summary = False,
                                           vif_threshold = 10.0
                                           )

            # Print the correlation_data DataFrame.
            print(Correlation_out6.correlation_data)

        """
        # Start the timer to get the build time
        _start_time = time.time()

        self.data  = data 
        self.target_column_pairs  = target_column_pairs 
        self.target_columns  = target_columns 
        self.partition_columns  = partition_columns 
        self.exception_attribute  = exception_attribute 
        self.vif  = vif 
        self.vif_summary  = vif_summary
        self.vif_threshold  = vif_threshold
        self.data_sequence_column = data_sequence_column

        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["target_column_pairs", self.target_column_pairs, True, (str,list)])
        self.__arg_info_matrix.append(["target_columns", self.target_columns, True, (str,list)])
        self.__arg_info_matrix.append(["partition_columns", self.partition_columns, True, (str,list)])
        self.__arg_info_matrix.append(["exception_attribute", self.exception_attribute, True, (str)])
        self.__arg_info_matrix.append(["vif", self.vif, True, (bool)])
        self.__arg_info_matrix.append(["vif_summary", self.vif_summary, True, (bool)])
        self.__arg_info_matrix.append(["vif_threshold", self.vif_threshold, True, (float)])
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

        if self.vif:
            if self.target_columns is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                                               'target_columns',
                                                               'vif=True'
                                                               ),
                                          MessageCodes.DEPENDENT_ARG_MISSING)
            if self.target_column_pairs is not None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT,
                                                               'target_column_pairs',
                                                               'vif=False'
                                                               ),
                                          MessageCodes.DEPENDENT_ARGUMENT)

        if not self.vif:
            if self.target_columns is not None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT,
                                                               'target_columns',
                                                               'vif=True'
                                                               ),
                                          MessageCodes.DEPENDENT_ARGUMENT)

            if self.target_column_pairs is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                                               'target_column_pairs',
                                                               'vif=False'
                                                               ),
                                          MessageCodes.DEPENDENT_ARG_MISSING)

            if self.exception_attribute is not None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT,
                                                               'exception_attribute',
                                                               'vif=True'
                                                               ),
                                          MessageCodes.DEPENDENT_ARGUMENT)

            if self.vif_summary is not None and self.vif_summary != True:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT,
                                                               'vif_summary',
                                                               'vif=True'
                                                               ),
                                          MessageCodes.DEPENDENT_ARGUMENT)

            if self.vif_threshold is not None and self.vif_threshold != 10.0:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT,
                                                               'vif_threshold',
                                                               'vif=True'
                                                               ),
                                          MessageCodes.DEPENDENT_ARGUMENT)

        # Check whether the input columns passed to the argument are not empty.
        self.__awu._validate_input_columns_not_empty(self.target_column_pairs, "target_column_pairs")

        self.__awu._validate_input_columns_not_empty(self.target_columns, "target_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.target_columns, "target_columns", self.data,"data", False)

        self.__awu._validate_input_columns_not_empty(self.partition_columns, "partition_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.partition_columns, "partition_columns", self.data, "data",False)

        self.__awu._validate_input_columns_not_empty(self.exception_attribute, "exception_attribute")
        self.__awu._validate_dataframe_has_argument_columns(self.exception_attribute, "exception_attribute", self.data, "data", False)

        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column",
                                                            self.data, "data", False)

    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__output_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix = "td_Correlation20", use_default_database = True, gc_on_quit = True, quote=False, table_type = TeradataConstants.TERADATA_TABLE)
        
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
        
        if self.target_column_pairs is not None:
            self.__func_other_arg_sql_names.append("TargetColumnPairs")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.target_column_pairs,"\""),"'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.target_columns is not None:
            self.__func_other_arg_sql_names.append("TargetColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.target_columns,"\""),"'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.partition_columns is not None:
            self.__func_other_arg_sql_names.append("PartitionColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.partition_columns,"\""),"'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")

        if self.exception_attribute is not None:
            self.__func_other_arg_sql_names.append("ExceptionAttribute")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.exception_attribute,"\""),"'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.vif is not None and self.vif != False:
            self.__func_other_arg_sql_names.append("VIF")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.vif,"'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")

        if self.vif_summary is not None and self.vif_summary != True:
            self.__func_other_arg_sql_names.append("OutputSummary")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.vif_summary,"'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")

        if self.vif_threshold is not None and self.vif_threshold != 10.0:
            self.__func_other_arg_sql_names.append("VIFThreshold")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.vif_threshold,"'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")

        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append(
                "InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))

        if len(sequence_input_by_list) > 0:
            self.__func_other_arg_sql_names.append("SequenceInputBy")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(sequence_input_by_list, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")

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
        
        function_name = "Correlation2"
        # Create instance to generate SQLMR.
        self.__aqg_obj = AnalyticQueryGenerator(function_name
                ,self.__func_input_arg_sql_names 
                ,self.__func_input_table_view_query 
                ,self.__func_input_dataframe_type 
                ,self.__func_input_distribution 
                ,self.__func_input_partition_by_cols 
                ,self.__func_input_order_by_cols 
                ,self.__func_other_arg_sql_names 
                ,self.__func_other_args 
                ,self.__func_other_arg_json_datatypes 
                ,self.__func_output_args_sql_names 
                ,self.__func_output_args 
                ,engine = "ENGINE_ML")
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
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix = "td_sqlmr_out_", use_default_database = True, gc_on_quit = True, quote=False, table_type = TeradataConstants.TERADATA_TABLE)
        try:
            UtilFuncs._create_table(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.correlation_data = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__output_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__output_table_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.correlation_data)
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
        correlation_data = None,
        output = None,
        **kwargs):
        """
        Classmethod which will be used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("correlation_data", None)
        kwargs.pop("output", None)

        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.correlation_data  = correlation_data
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
        obj.correlation_data = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.correlation_data), source_type="table", database_name=UtilFuncs._extract_db_name(obj.correlation_data))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.correlation_data)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a Correlation2 class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ correlation_data Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.correlation_data)
        return repr_string
