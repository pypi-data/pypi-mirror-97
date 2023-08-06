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
# Function Version: 1.19
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
from teradataml.common.formula import Formula

class GLML1L2:
    
    def __init__(self,
        formula = None,
        data = None,
        alpha = 0.0,
        lambda1 = 0.0,
        max_iter_num = 10000,
        stop_threshold = 1.0E-7,
        family = "Gaussian",
        randomization = False,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The GLML1L2 function differs from the GLM function in these ways:
                1. GLML1L2 supports the regularization models Ridge, LASSO, and
                   Elastic Net.
                2. GLML1L2 outputs a model teradataml DataFrame and optionally,
                   a factor teradataml DataFrame (GLM outputs only a model).
         
         
        PARAMETERS:
            formula:
                Required Argument.
                A string consisting of "formula". Specifies the model to be fitted.
                Only basic formula of the "col1 ~ col2 + col3 +..." form are
                supported and all variables must be from the same teradataml
                DataFrame object. The response should be column of type float, int or
                bool.
         
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the
                input data.
         
            alpha:
                Optional Argument.
                Specifies whether to use Lasso, Ridge or Elastic Net. If the value is
                0, Ridge is used. If the value is 1, Lasso is used. For any value
                between 0 and 1, Elastic Net is applied.
                Default Value: 0.0
                Types: float
         
            lambda1:
                Optional Argument.
                Specifies the parameter that controls the magnitude of the regularization
                term. The value lambda must be in the range [0.0, 100.0].
                A value of zero disables regularization.
                Default Value: 0.0
                Types: float
         
            max_iter_num:
                Optional Argument.
                Specifies the maximum number of iterations over the data.
                The parameter max_iterations must be a positive int value in
                the range [1, 100000].
                Default Value: 10000
                Types: int
         
            stop_threshold:
                Optional Argument.
                Specifies the convergence threshold.
                Default Value: 1.0E-7
                Types: float
         
            family:
                Optional Argument.
                Specifies the distribution exponential family.
                Default Value: "Gaussian"
                Permitted Values: Binomial, Gaussian
                Types: str
         
            randomization:
                Optional Argument.
                Specify whether to randomize the input teradataml DataFrame data.
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
            Instance of GLML1L2.
            Output teradataml DataFrames can be accessed using attribute
            references, such as GLML1L2Obj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. output
                2. factor_data
         
            Note:
                1. When argument randomization is True or if any categorical columns
                   are provided in formula argument, then and only then output teradataml DataFrame
                   factor_data is created.
                2. factor_data can be used as the input (data) for future GLML1L2
                   function calls, thereby saving the function from repeating the
                   categorical-to-numerical conversion or randomization.
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("GLML1L2", ["admissions_train", "housing_train"])
         
            # Create teradataml DataFrame object.
            admissions_train = DataFrame.from_table("admissions_train")
            housing_train = DataFrame.from_table("housing_train")
         
            # Example 1 - The input DataFrame is admission_train, running GLML1L2 function as
            #             Ridge Regression Analysis. Alpha (0.0) indicates L2 (ridge regression).
         
            glml1l2_out1 = GLML1L2(data=admissions_train,
                                   formula = "admitted ~ masters + gpa + stats + programming",
                                   alpha=0.0,
                                   lambda1=0.02,
                                   family='Binomial',
                                   randomization=True
                                  )
         
            # Print the output DataFrames.
            # STDOUT DataFrame.
            print(glml1l2_out1.output)
         
            # factor_data dataframe.
            print(glml1l2_out1.factor_data)
         
            # Example 2 - The input DataFrame is factor_data DataFrame which is generated by
            #             (GLML1L2 Example 1: Ridge Regression, Binomial Family). In factor_data DataFrame
            #             categorical predictors were converted to integers.
         
            glml1l2_out2 = GLML1L2(data=glml1l2_out1.factor_data,
                                   formula = "admitted ~ masters_yes + stats_beginner + stats_novice + programming_beginner + programming_novice + gpa",
                                   alpha=0.0,
                                   lambda1=0.02,
                                   family='Binomial'
                                  )
         
            # Print the result.
            print(glml1l2_out2)
         
            # Example 3 - The input DataFrame is housing_train, running GLML1L2 function as
            #             LASSO Regression (Family Gaussian distribution). Alpha (1.0) indicates
            #             L1 (LASSO) regularization.
         
            glml1l2_out3 = GLML1L2(data=housing_train ,
                                   formula = "price ~ lotsize + bedrooms + bathrms + stories + garagepl + driveway + recroom + fullbase + gashw + airco + prefarea + homestyle",
                                   alpha=1.0,
                                   lambda1=0.02,
                                   family='Gaussian'
                                  )
         
            # Print all output dataframes.
            print(glml1l2_out3.output)
            print(glml1l2_out3.factor_data)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.formula  = formula 
        self.data  = data 
        self.alpha  = alpha 
        self.lambda1  = lambda1 
        self.max_iter_num  = max_iter_num 
        self.stop_threshold  = stop_threshold 
        self.family  = family 
        self.randomization  = randomization 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["formula", self.formula, False, "formula"])
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["alpha", self.alpha, True, (float)])
        self.__arg_info_matrix.append(["lambda1", self.lambda1, True, (float)])
        self.__arg_info_matrix.append(["max_iter_num", self.max_iter_num, True, (int)])
        self.__arg_info_matrix.append(["stop_threshold", self.stop_threshold, True, (float)])
        self.__arg_info_matrix.append(["family", self.family, True, (str)])
        self.__arg_info_matrix.append(["randomization", self.randomization, True, (bool)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])

        # Internal variable to decide whether to use factor output or not.
        self.__factor_output = True

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
        
        # Check for permitted values
        family_permitted_values = ["BINOMIAL", "GAUSSIAN"]
        self.__awu._validate_permitted_values(self.family, family_permitted_values, "family")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        if self.alpha is not None and self.alpha != 0.0:
            self.__func_other_arg_sql_names.append("Alpha")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.alpha, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.lambda1 is not None and self.lambda1 != 0:
            self.__func_other_arg_sql_names.append("Lambda")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.lambda1, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.max_iter_num is not None and self.max_iter_num != 10000:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_iter_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.stop_threshold is not None and self.stop_threshold != 1.0E-7:
            self.__func_other_arg_sql_names.append("StopThreshold")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.stop_threshold, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.family is not None and self.family != "Gaussian":
            self.__func_other_arg_sql_names.append("Family")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.family, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.randomization is not None and self.randomization != False:
            self.__func_other_arg_sql_names.append("Randomization")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.randomization, "'"))
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
        
        # Let's process formula argument
        self.formula = self.__awu._validate_formula_notation(self.formula, self.data, "formula")
        # response variable
        __response_column = self.formula._get_dependent_vars()
        self._target_column = __response_column
        self.__func_other_arg_sql_names.append("ResponseColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__response_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        self._sql_specific_attributes["ResponseColumn"] = __response_column
        self._sql_formula_attribute_mapper["ResponseColumn"] = "__response_column"
        
        # all input columns
        __all_columns = self.__awu._get_columns_by_type(self.formula, self.data, "all")
        __all_columns.remove(__response_column)
        if len(__all_columns) > 0:
            self.__func_other_arg_sql_names.append("FeatureColumns")
            all_columns_list = UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__all_columns, "\""), "'")
            self.__func_other_args.append(all_columns_list)
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
            self._sql_specific_attributes["FeatureColumns"] = all_columns_list
            self._sql_formula_attribute_mapper["FeatureColumns"] = "__all_columns"
        
        # categorical input columns
        __categorical_columns = self.__awu._get_columns_by_type(self.formula, self.data, "categorical")
        if len(__categorical_columns) > 0:
            self.__func_other_arg_sql_names.append("CategoricalColumns")
            categorical_columns_list = UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__categorical_columns, "\""), "'")
            self.__func_other_args.append(categorical_columns_list)
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
            self._sql_specific_attributes["CategoricalColumns"] = categorical_columns_list
            self._sql_formula_attribute_mapper["CategoricalColumns"] = "__categorical_columns"

        # Generate temp table names for output table parameters if any.
        if self.randomization is True or len(__categorical_columns) > 0:
            self.__factor_data_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_glml1l20", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        else:
            self.__factor_data_temp_tablename = None
            self.__factor_output = False

        # Output table arguments list
        self.__func_output_args_sql_names = ["FactorTable"]
        self.__func_output_args = [self.__factor_data_temp_tablename]
        
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
        
        function_name = "GLML1L2"
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
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.output)
        if self.__factor_output:
            self.factor_data = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__factor_data_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__factor_data_temp_tablename))
            self._mlresults.append(self.factor_data)
        else:
            self.factor_data = "INFO: 'factor_data' output DataFrame is not created, the result is based on either CategoricalColumns or Randomization; " \
                               "therefore, you must also specify either CategoricalColumns in formula or Randomization ('true')."
        
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
        factor_data = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("factor_data", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Initialize the formula attributes.
        __response_column = kwargs.pop("__response_column", None)
        __all_columns = kwargs.pop("__all_columns", None)
        __numeric_columns = kwargs.pop("__numeric_columns", None)
        __categorical_columns = kwargs.pop("__categorical_columns", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.factor_data  = factor_data
        obj.output  = output 
        
        # Initialize the sqlmr_query class attribute.
        obj.sqlmr_query = None
        
        # Initialize the SQL specific Model Cataloging attributes.
        obj._sql_specific_attributes = None
        obj._target_column = target_column
        obj._prediction_type = prediction_type
        obj._algorithm_name = algorithm_name
        obj._build_time = build_time
        
        # Initialize the formula.
        if obj.formula is not None:
            obj.formula = Formula._from_formula_attr(obj.formula,
                                                     __response_column,
                                                     __all_columns,
                                                     __categorical_columns,
                                                     __numeric_columns)
        
        # Update output table data frames.
        obj._mlresults = []
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.output)
        if obj.factor_data is not None:
            obj.factor_data = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.factor_data), source_type="table", database_name=UtilFuncs._extract_db_name(obj.factor_data))
            obj._mlresults.append(obj.factor_data)
        else:
            obj.factor_data = "INFO: 'factor_data' output DataFrame is not created, the result is based on either CategoricalColumns or Randomization; " \
                              "therefore, you must also specify either CategoricalColumns in formula or Randomization ('true')."
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a GLML1L2 class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ factor_data Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.factor_data)
        return repr_string
        
