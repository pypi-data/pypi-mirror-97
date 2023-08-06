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
# Function Version: 1.20
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

class GLM:
    
    def __init__(self,
        formula = None,
        family = "gaussian",
        linkfunction = "CANONICAL",
        data = None,
        weights = "1.0",
        threshold = 0.01,
        maxit = 25,
        step = False,
        intercept = True,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The generalized linear model (GLM) is an extension of the linear 
            regression model that enables the linear equation to be related to
            the dependent variables by a link function. GLM performs linear
            regression analysis for distribution functions using a user-specified
            distribution family and link function. GLM selects the link function
            based upon the distribution family and the assumed nonlinear
            distribution of expected outcomes. The teradataml DataFrame in
            Background describes the supported link function combinations.
         
         
        PARAMETERS:
            formula:
                Required Argument.
                A string consisting of "formula". Specifies the model to be fitted. Only
                basic formula of the "col1 ~ col2 + col3 +..." form is supported and
                all variables must be from the same virtual data frame object. The
                response should be column of type real, numeric, integer or boolean.
                Types: str
         
            family:
                Optional Argument.
                Specifies the distribution exponential family
                Default Value: "gaussian"
                Permitted Values: LOGISTIC, BINOMIAL, POISSON, GAUSSIAN, GAMMA,
                INVERSE_GAUSSIAN, NEGATIVE_BINOMIAL
                Types: str
         
            linkfunction:
                Optional Argument.
                The canonical link functions (default link functions) and the link
                functions that are allowed.
                Default Value: "CANONICAL"
                Permitted Values: CANONICAL, IDENTITY, INVERSE, LOG,
                COMPLEMENTARY_LOG_LOG, SQUARE_ROOT, INVERSE_MU_SQUARED, LOGIT,
                PROBIT, CAUCHIT
                Types: str
         
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the
                columns.
         
            weights:
                Optional Argument.
                Specifies the name of an input teradataml DataFrame column that
                contains the weights to assign to responses. The default value is
                1.You can use non-NULL weights to indicate that different
                observations have different dispersions (with the weights being
                inversely proportional to the dispersions).Equivalently, when the
                weights are positive integers wi, each response yi is the mean of wi
                unit-weight observations. A binomial GLM uses prior weights to give
                the number of trials when the response is the proportion of
                successes. A Poisson GLM rarely uses weights. If the weight is less
                than the response value, then the function throws an exception.
                Therefore, if the response value is greater than 1 (the default
                weight), then you must specify a weight that is greater than or equal
                to the response value.
                Default Value: "1.0"
                Types: str
         
            threshold:
                Optional Argument.
                Specifies the convergence threshold.
                Default Value: 0.01
                Types: float
         
            maxit:
                Optional Argument.
                Specifies the maximum number of iterations that the algorithm runs
                before quitting if the convergence threshold has not been met.
                Default Value: 25
                Types: int
         
            step:
                Optional Argument.
                Specifies whether the function uses a step. If the function uses a
                step, then it runs with the GLM model that has the lowest Akaike
                information criterion (AIC) score, drops one predictor from the
                current predictor group, and repeats this process until no predictor
                remains.
                Default Value: False
                Types: bool
         
            intercept:
                Optional Argument.
                Specifies whether the function uses an intercept. For example, in
                ß0+ß1*X1+ß2*X2+ ....+ßpXp, the intercept is ß0.
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
            Instance of GLM.
            Output teradataml DataFrames can be accessed using attribute
            references, such as GLMObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                1. coefficients
                2. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("GLM", ["admissions_train", "housing_train"])
         
            # Create teradataml DataFrame objects.
            admissions_train = DataFrame.from_table("admissions_train")
            housing_train = DataFrame.from_table("housing_train")
         
            # Example 1 -
            glm_out1 = GLM(formula = "admitted ~ stats + masters + gpa + programming",
                           family = "LOGISTIC",
                           linkfunction = "LOGIT",
                           data = admissions_train,
                           weights = "1",
                           threshold = 0.01,
                           maxit = 25,
                           step = False,
                           intercept = True
                           )
         
            # Print the output dataframes
            # STDOUT DataFrame
            print(glm_out1.output)
         
            # GLM Model, coefficients DataFrame
            print(glm_out1.coefficients)
         
            # Example 2 -
            glm_out2 = GLM(formula = "admitted ~ stats + masters + gpa + programming",
                           family = "LOGISTIC",
                           linkfunction = "LOGIT",
                           data = admissions_train,
                           weights = "1",
                           threshold = 0.01,
                           maxit = 25,
                           step = True,
                           intercept = True
                           )
         
            # Print all output dataframes
            print(glm_out2.output)
         
            # Example 3 -
            glm_out3 = GLM(formula = "price ~ recroom + lotsize + stories + garagepl + gashw + bedrooms + driveway + airco + homestyle + bathrms + fullbase + prefarea",
                           family = "GAUSSIAN",
                           linkfunction = "IDENTITY",
                           data = housing_train,
                           weights = "1",
                           threshold = 0.01,
                           maxit = 25,
                           step = False,
                           intercept = True
                           )
         
            # Print all output dataframes
            print(glm_out3.output)
            print(glm_out1.coefficients)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.formula  = formula 
        self.family  = family 
        self.linkfunction  = linkfunction 
        self.data  = data 
        self.weights  = weights 
        self.threshold  = threshold 
        self.maxit  = maxit 
        self.step  = step 
        self.intercept  = intercept 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["formula", self.formula, False, "formula"])
        self.__arg_info_matrix.append(["family", self.family, True, (str)])
        self.__arg_info_matrix.append(["linkfunction", self.linkfunction, True, (str)])
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["weights", self.weights, True, (str)])
        self.__arg_info_matrix.append(["threshold", self.threshold, True, (float)])
        self.__arg_info_matrix.append(["maxit", self.maxit, True, (int)])
        self.__arg_info_matrix.append(["step", self.step, True, (bool)])
        self.__arg_info_matrix.append(["intercept", self.intercept, True, (bool)])
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
        
        # Check for permitted values
        family_permitted_values = ["LOGISTIC", "BINOMIAL", "POISSON", "GAUSSIAN", "GAMMA", "INVERSE_GAUSSIAN", "NEGATIVE_BINOMIAL"]
        self.__awu._validate_permitted_values(self.family, family_permitted_values, "family")
        
        linkfunction_permitted_values = ["CANONICAL", "IDENTITY", "INVERSE", "LOG", "COMPLEMENTARY_LOG_LOG", "SQUARE_ROOT", "INVERSE_MU_SQUARED", "LOGIT", "PROBIT", "CAUCHIT"]
        self.__awu._validate_permitted_values(self.linkfunction, linkfunction_permitted_values, "linkfunction")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.weights, "weights")
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__coefficients_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_glm0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable"]
        self.__func_output_args = [self.__coefficients_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        if self.weights is not None and self.weights != "1.0":
            self.__func_other_arg_sql_names.append("WeightColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.weights, "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.family is not None:
            self.__func_other_arg_sql_names.append("Family")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.family, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.linkfunction is not None and self.linkfunction != "CANONICAL":
            self.__func_other_arg_sql_names.append("LinkFunction")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.linkfunction, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.threshold is not None and self.threshold != 0.01:
            self.__func_other_arg_sql_names.append("StopThreshold")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.threshold, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.maxit is not None and self.maxit != 25:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.maxit, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.intercept is not None and self.intercept != True:
            self.__func_other_arg_sql_names.append("Intercept")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.intercept, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.step is not None and self.step != False:
            self.__func_other_arg_sql_names.append("Step")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.step, "'"))
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
        # Target Column
        self._target_column = self.formula._get_dependent_vars()
        # all input columns
        __all_columns = self.__awu._get_columns_by_type(self.formula, self.data, "all")
        if len(__all_columns) > 0:
            self.__func_other_arg_sql_names.append("InputColumns")
            all_columns_list = UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__all_columns, "\""), "'")
            self.__func_other_args.append(all_columns_list)
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
            self._sql_specific_attributes["InputColumns"] = all_columns_list
            self._sql_formula_attribute_mapper["InputColumns"] = "__all_columns"

        # categorical input columns
        __categorical_columns = self.__awu._get_columns_by_type(self.formula, self.data, "categorical")
        if len(__categorical_columns) > 0:
            self.__func_other_arg_sql_names.append("CategoricalColumns")
            categorical_columns_list = UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__categorical_columns, "\""), "'")
            self.__func_other_args.append(categorical_columns_list)
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
            self._sql_specific_attributes["CategoricalColumns"] = categorical_columns_list
            self._sql_formula_attribute_mapper["CategoricalColumns"] = "__categorical_columns"
        
        
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
        
        function_name = "GLM"
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
        self.coefficients = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__coefficients_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__coefficients_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.coefficients)
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
        coefficients = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("coefficients", None)
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
        obj.coefficients  = coefficients 
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
        obj.coefficients = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.coefficients), source_type="table", database_name=UtilFuncs._extract_db_name(obj.coefficients))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.coefficients)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a GLM class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ coefficients Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.coefficients)
        return repr_string

