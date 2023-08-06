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
# Function Version: 2.8
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

class ConfusionMatrix:
    
    def __init__(self,
        data = None,
        reference = None,
        prediction = None,
        classes = None,
        prevalence = None,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The ConfusionMatrix function shows how often a classification 
            algorithm correctly classifies items. The function takes an input 
            teradataml data frame that includes two columns one containing the
            observed class of an item and the other containing the class
            predicted by the algorithm and outputs three tables mentioned under RETURNS.
         
         
        PARAMETERS:
            data:
                Required Argument.
                The input teradataml data frame of ConfusionMatrix function
         
            reference:
                Required Argument.
                Specifies the name of the input column that contains the observed
                class.
                Types: str
         
            prediction:
                Required Argument.
                Specifies the name of the input column that contains the predicted
                class.
                Types: str
         
            classes:
                Optional Argument.
                Specifies the classes to output in output_table.
                Types: str OR list of Strings (str)
         
            prevalence:
                Optional Argument.
                Specifies the prevalences for the classes to output in
                output_table_3. Therefore, if you specify prevalence, then you must
                also specify classes, and for every class, you must specify a
                prevalence.
                Types: float OR list of floats
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of ConfusionMatrix.
            Output teradataml DataFrames can be accessed using attribute
            references, such as ConfusionMatrixObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. counttable
                2. stattable
                3. accuracytable
                4. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("confusionmatrix", "iris_category_expect_predict")
         
            # Create teradataml Dataframe.
            iris_category_expect_predict = DataFrame.from_table("iris_category_expect_predict")
         
            # Example
            confusion_matrix_output = ConfusionMatrix(data=iris_category_expect_predict,
                                                      reference='expected_value',
                                                      prediction='predicted_value',
                                                      classes='versicolor',
                                                      prevalence=0.5,
                                                      data_sequence_column='id'
                                                      )
         
            # Print the result teradataml DataFrame
            print(confusion_matrix_output.counttable)
            print(confusion_matrix_output.stattable)
            print(confusion_matrix_output.accuracytable)
            print(confusion_matrix_output.output)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.reference  = reference 
        self.prediction  = prediction 
        self.classes  = classes 
        self.prevalence  = prevalence 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["reference", self.reference, False, (str)])
        self.__arg_info_matrix.append(["prediction", self.prediction, False, (str)])
        self.__arg_info_matrix.append(["classes", self.classes, True, (str,list)])
        self.__arg_info_matrix.append(["prevalence", self.prevalence, True, (float,list)])
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
        self.__awu._validate_input_columns_not_empty(self.reference, "reference")
        self.__awu._validate_dataframe_has_argument_columns(self.reference, "reference", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.prediction, "prediction")
        self.__awu._validate_dataframe_has_argument_columns(self.prediction, "prediction", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__counttable_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_confusionmatrix0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__stattable_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_confusionmatrix1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__accuracytable_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_confusionmatrix2", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["CountTable", "StatTable", "AccuracyTable"]
        self.__func_output_args = [self.__counttable_temp_tablename, self.__stattable_temp_tablename, self.__accuracytable_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("ObservationColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.reference, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("PredictColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.prediction, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.classes is not None:
            self.__func_other_arg_sql_names.append("classes")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.classes, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.prevalence is not None:
            self.__func_other_arg_sql_names.append("Prevalence")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.prevalence, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
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
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("1")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "ConfusionMatrix"
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
        self.counttable = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__counttable_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__counttable_temp_tablename))
        self.stattable = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__stattable_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__stattable_temp_tablename))
        self.accuracytable = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__accuracytable_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__accuracytable_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.counttable)
        self._mlresults.append(self.stattable)
        self._mlresults.append(self.accuracytable)
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
        counttable = None,
        stattable = None,
        accuracytable = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("counttable", None)
        kwargs.pop("stattable", None)
        kwargs.pop("accuracytable", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.counttable  = counttable 
        obj.stattable  = stattable 
        obj.accuracytable  = accuracytable 
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
        obj.counttable = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.counttable), source_type="table", database_name=UtilFuncs._extract_db_name(obj.counttable))
        obj.stattable = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.stattable), source_type="table", database_name=UtilFuncs._extract_db_name(obj.stattable))
        obj.accuracytable = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.accuracytable), source_type="table", database_name=UtilFuncs._extract_db_name(obj.accuracytable))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.counttable)
        obj._mlresults.append(obj.stattable)
        obj._mlresults.append(obj.accuracytable)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a ConfusionMatrix class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ counttable Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.counttable)
        repr_string="{}\n\n\n############ stattable Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.stattable)
        repr_string="{}\n\n\n############ accuracytable Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.accuracytable)
        return repr_string
        
