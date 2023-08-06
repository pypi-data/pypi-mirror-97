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
# Function Version: 1.8
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

class HMMEvaluator:
    
    def __init__(self,
        init_state_prob = None,
        state_transition_prob = None,
        emission_prob = None,
        observation = None,
        state_model_key = None,
        state_key = None,
        state_prob_key = None,
        trans_model_key = None,
        trans_from_key = None,
        trans_to_key = None,
        trans_prob_key = None,
        emit_model_key = None,
        emit_state_key = None,
        emit_observed_key = None,
        emit_prob_key = None,
        model_key = None,
        sequence_key = None,
        observed_key = None,
        incremental = True,
        show_rate_change = True,
        seq_prob_key = None,
        skip_key = None,
        accumulate = None,
        observation_sequence_column = None,
        init_state_prob_sequence_column = None,
        state_transition_prob_sequence_column = None,
        emission_prob_sequence_column = None,
        observation_partition_column = None,
        init_state_prob_partition_column = None,
        state_transition_prob_partition_column = None,
        emission_prob_partition_column = None,
        observation_order_column = None,
        init_state_prob_order_column = None,
        state_transition_prob_order_column = None,
        emission_prob_order_column = None):
        """
        DESCRIPTION:
            The HMMEvaluator function measures the probabilities of sequences,
            with respect to each trained HMM.
         
         
        PARAMETERS:
            init_state_prob:
                Required Argument.
                Specifies the teradataml DataFrame representing the initial state table.
         
            init_state_prob_partition_column:
                Required Argument.
                Specifies Partition By columns for init_state_prob.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            init_state_prob_order_column:
                Optional Argument.
                Specifies Order By columns for init_state_prob.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            state_transition_prob:
                Required Argument.
                Specifies the teradataml DataFrame representing the state transition table.
         
            state_transition_prob_partition_column:
                Required Argument.
                Specifies partition By columns for state_transition_prob.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            state_transition_prob_order_column:
                Optional Argument.
                Specifies Order By columns for state_transition_prob.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            emission_prob:
                Required Argument.
                Specifies the teradataml DataFrame representing the emission probability table.
         
            emission_prob_partition_column:
                Required Argument.
                Specifies partition By columns for emission_prob.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            emission_prob_order_column:
                Optional Argument.
                Specifies Order By columns for emission_prob.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            observation:
                Required Argument.
                Specifies the teradataml DataFrame representing the observation table for which
                the probabilities of sequences are to be found.
         
            observation_partition_column:
                Required Argument.
                Specifies partition By columns for observation.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            observation_order_column:
                Required Argument.
                Specifies order By columns for observation.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            state_model_key:
                Required Argument.
                Specifies the name of the model attribute column in the init_state_prob table.
                Types: str OR list of Strings (str)
         
            state_key:
                Required Argument.
                Specifies the name of the state attribute column in the init_state_prob table.
                Types: str OR list of Strings (str)
         
            state_prob_key:
                Required Argument.
                Specifies the name of the initial probability column in the init_state_prob
                table.
                Types: str OR list of Strings (str)
         
            trans_model_key:
                Required Argument.
                Specifies the name of the model attribute column in the state_transition_prob
                table.
                Types: str OR list of Strings (str)
         
            trans_from_key:
                Required Argument.
                Specifies the name of the source of the state transition column in the
                state_transition_prob table.
                Types: str OR list of Strings (str)
         
            trans_to_key:
                Required Argument.
                Specifies the name of the target of the state transition column in the
                state_transition_prob table.
                Types: str OR list of Strings (str)
         
            trans_prob_key:
                Required Argument.
                Specifies the name of the state transition probability column in the
                state_transition_prob table.
                Types: str OR list of Strings (str)
         
            emit_model_key:
                Required Argument.
                Specifies the name of the model attribute column in the emission_prob table.
                Types: str OR list of Strings (str)
         
            emit_state_key:
                Required Argument.
                Specifies the name of the state attribute in the emission_prob table.
                Types: str OR list of Strings (str)
         
            emit_observed_key:
                Required Argument.
                Specifies the name of the observation attribute column in the emission_prob
                table.
                Types: str OR list of Strings (str)
         
            emit_prob_key:
                Required Argument.
                Specifies the name of the emission probability in the emission_prob table.
                Types: str OR list of Strings (str)
         
            model_key:
                Required Argument.
                Specifies the name of the column that contains the model attribute. If you
                specify this argument, then model_attribute must match a model_key in
                the observation_partition_column.
                Types: str
         
            sequence_key:
                Required Argument.
                Specifies the name of the column that contains the sequence attribute. The
                sequence_attribute must be a sequence attribute in the
                observation_partition_column.
                Types: str
         
            observed_key:
                Required Argument.
                Specifies the name of the column that contains the observed symbols.
                Note: Observed symbols are case-sensitive.
                Types: str
         
            incremental:
                Optional Argument.
                Specifies whether only new sequence probabilities are computed. If
                "True", only new sequence probabilities are computed.
                If "False", all probabilities are computed.
                Note: If the seq_prob_key argument is not specified, the function cannot
                      determine whether the observed sequence is new; therefore, all model sequences
                      in the input tables are treated as new.
                Default Value: True
                Types: bool
         
            show_rate_change:
                Optional Argument.
                Specifies the value to show the percentage change that corresponds to the
                applied model with the difference from previous predicted probability.
                Function shows the percentage change, when this is set to "True".
                Default Value: True
                Types: bool
         
            seq_prob_key:
                Optional Argument.
                Specifies the column to calculate the change rate. The function uses the
                previous value under this column.
                Types: str
         
            skip_key:
                Optional Argument.
                Specifies the name of the column whose values determine whether the function
                skips the row. The function skips the row if the value is "true",
                "yes", "y", or "1". The function does not skip the row if the value
                is "false", "f", "no", "n", "0", or None.
                Types: str
         
            accumulate:
                Optional Argument.
                Specifies the names of the columns in "observation" input teradataml DataFrame
                that the function copies to the output table.
                Types: str OR list of Strings (str)
         
            observation_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "observation". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            init_state_prob_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "init_state_prob". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            state_transition_prob_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "state_transition_prob". The argument is used to
                ensure deterministic results for functions which produce results that
                vary from run to run.
                Types: str OR list of Strings (str)
         
            emission_prob_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "emission_prob". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of HMMEvaluator.
            Output teradataml DataFrames can be accessed using attribute
            references, such as HMMEvaluatorObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("hmmunsupervised", "loan_prediction")
            load_example_data("hmmevaluator", ["Pi_loan", "A_loan", "B_loan", "test_loan_prediction"])
         
            # Create teradataml DataFrame objects.
            pi_loan = DataFrame.from_table("pi_loan")
            A_loan = DataFrame.from_table("A_loan")
            B_loan = DataFrame.from_table("B_loan")
            test_loan_prediction = DataFrame.from_table("test_loan_prediction")
            loan_prediction = DataFrame.from_table("loan_prediction")
         
            # Example 1
            # Train a HMM Unsupervised model on the loan prediction dataset
            HMMUnsupervised_out = HMMUnsupervised(vertices = loan_prediction,
                                                  vertices_partition_column = ["model_id", "seq_id"],
                                                  vertices_order_column = ["seq_vertex_id"],
                                                  model_key = "model_id",
                                                  sequence_key = "seq_id",
                                                  observed_key = "observed_id",
                                                  hidden_states_num = 3,
                                                  init_methods = ["random"]
                                                  )
         
            # Use the output of the trained model to make the evaluation for probabilities of sequences.
            # Note: Similarly, output of a trained supervised HMM model can also be used to make evaluation.
            HMMEvaluator_out1 = HMMEvaluator(init_state_prob = HMMUnsupervised_out.output_initialstate_table,
                                            init_state_prob_partition_column = ["model_id"],
                                            state_transition_prob = HMMUnsupervised_out.output_statetransition_table,
                                            state_transition_prob_partition_column = ["model_id"],
                                            emission_prob = HMMUnsupervised_out.output_emission_table,
                                            emission_prob_partition_column = ["model_id"],
                                            observation = test_loan_prediction,
                                            observation_partition_column = ["model_id"],
                                            observation_order_column = ["seq_id", "seq_vertex_id"],
                                            state_model_key = ["model_id"],
                                            state_key = ["state"],
                                            state_prob_key = ["probability"],
                                            trans_model_key = ["model_id"],
                                            trans_from_key = ["from_state"],
                                            trans_to_key = ["to_state"],
                                            trans_prob_key = ["probability"],
                                            emit_model_key = ["model_id"],
                                            emit_state_key = ["state"],
                                            emit_observed_key = ["observed"],
                                            emit_prob_key = ["probability"],
                                            model_key = "model_id",
                                            sequence_key = "seq_id",
                                            observed_key = "observed_id"
                                            )
            # Print the results
            print(HMMEvaluator_out1)
         
            # Example 2 - Alternatively, load the trained model data from the database tables to make the evaluations
            HMMEvaluator_out2 = HMMEvaluator(init_state_prob = pi_loan,
                                            init_state_prob_partition_column = ["model_id"],
                                            state_transition_prob = A_loan,
                                            state_transition_prob_partition_column = ["model_id"],
                                            emission_prob = B_loan,
                                            emission_prob_partition_column = ["model_id"],
                                            observation = test_loan_prediction,
                                            observation_partition_column = ["model_id"],
                                            observation_order_column = ["seq_id", "seq_vertex_id"],
                                            state_model_key = ["model_id"],
                                            state_key = ["state"],
                                            state_prob_key = ["probability"],
                                            trans_model_key = ["model_id"],
                                            trans_from_key = ["from_state"],
                                            trans_to_key = ["to_state"],
                                            trans_prob_key = ["probability"],
                                            emit_model_key = ["model_id"],
                                            emit_state_key = ["state"],
                                            emit_observed_key = ["observed"],
                                            emit_prob_key = ["probability"],
                                            model_key = "model_id",
                                            sequence_key = "seq_id",
                                            observed_key = "observed_id"
                                            )
            # Print the results
            print(HMMEvaluator_out2)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.init_state_prob  = init_state_prob 
        self.state_transition_prob  = state_transition_prob 
        self.emission_prob  = emission_prob 
        self.observation  = observation 
        self.state_model_key  = state_model_key 
        self.state_key  = state_key 
        self.state_prob_key  = state_prob_key 
        self.trans_model_key  = trans_model_key 
        self.trans_from_key  = trans_from_key 
        self.trans_to_key  = trans_to_key 
        self.trans_prob_key  = trans_prob_key 
        self.emit_model_key  = emit_model_key 
        self.emit_state_key  = emit_state_key 
        self.emit_observed_key  = emit_observed_key 
        self.emit_prob_key  = emit_prob_key 
        self.model_key  = model_key 
        self.sequence_key  = sequence_key 
        self.observed_key  = observed_key 
        self.incremental  = incremental 
        self.show_rate_change  = show_rate_change 
        self.seq_prob_key  = seq_prob_key 
        self.skip_key  = skip_key 
        self.accumulate  = accumulate 
        self.observation_sequence_column  = observation_sequence_column 
        self.init_state_prob_sequence_column  = init_state_prob_sequence_column 
        self.state_transition_prob_sequence_column  = state_transition_prob_sequence_column 
        self.emission_prob_sequence_column  = emission_prob_sequence_column 
        self.observation_partition_column  = observation_partition_column 
        self.init_state_prob_partition_column  = init_state_prob_partition_column 
        self.state_transition_prob_partition_column  = state_transition_prob_partition_column 
        self.emission_prob_partition_column  = emission_prob_partition_column 
        self.observation_order_column  = observation_order_column 
        self.init_state_prob_order_column  = init_state_prob_order_column 
        self.state_transition_prob_order_column  = state_transition_prob_order_column 
        self.emission_prob_order_column  = emission_prob_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["init_state_prob", self.init_state_prob, False, (DataFrame)])
        self.__arg_info_matrix.append(["init_state_prob_partition_column", self.init_state_prob_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["init_state_prob_order_column", self.init_state_prob_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["state_transition_prob", self.state_transition_prob, False, (DataFrame)])
        self.__arg_info_matrix.append(["state_transition_prob_partition_column", self.state_transition_prob_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["state_transition_prob_order_column", self.state_transition_prob_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["emission_prob", self.emission_prob, False, (DataFrame)])
        self.__arg_info_matrix.append(["emission_prob_partition_column", self.emission_prob_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["emission_prob_order_column", self.emission_prob_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["observation", self.observation, False, (DataFrame)])
        self.__arg_info_matrix.append(["observation_partition_column", self.observation_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["observation_order_column", self.observation_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["state_model_key", self.state_model_key, False, (str,list)])
        self.__arg_info_matrix.append(["state_key", self.state_key, False, (str,list)])
        self.__arg_info_matrix.append(["state_prob_key", self.state_prob_key, False, (str,list)])
        self.__arg_info_matrix.append(["trans_model_key", self.trans_model_key, False, (str,list)])
        self.__arg_info_matrix.append(["trans_from_key", self.trans_from_key, False, (str,list)])
        self.__arg_info_matrix.append(["trans_to_key", self.trans_to_key, False, (str,list)])
        self.__arg_info_matrix.append(["trans_prob_key", self.trans_prob_key, False, (str,list)])
        self.__arg_info_matrix.append(["emit_model_key", self.emit_model_key, False, (str,list)])
        self.__arg_info_matrix.append(["emit_state_key", self.emit_state_key, False, (str,list)])
        self.__arg_info_matrix.append(["emit_observed_key", self.emit_observed_key, False, (str,list)])
        self.__arg_info_matrix.append(["emit_prob_key", self.emit_prob_key, False, (str,list)])
        self.__arg_info_matrix.append(["model_key", self.model_key, False, (str)])
        self.__arg_info_matrix.append(["sequence_key", self.sequence_key, False, (str)])
        self.__arg_info_matrix.append(["observed_key", self.observed_key, False, (str)])
        self.__arg_info_matrix.append(["incremental", self.incremental, True, (bool)])
        self.__arg_info_matrix.append(["show_rate_change", self.show_rate_change, True, (bool)])
        self.__arg_info_matrix.append(["seq_prob_key", self.seq_prob_key, True, (str)])
        self.__arg_info_matrix.append(["skip_key", self.skip_key, True, (str)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["observation_sequence_column", self.observation_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["init_state_prob_sequence_column", self.init_state_prob_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["state_transition_prob_sequence_column", self.state_transition_prob_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["emission_prob_sequence_column", self.emission_prob_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.observation, "observation", None)
        self.__awu._validate_input_table_datatype(self.init_state_prob, "init_state_prob", None)
        self.__awu._validate_input_table_datatype(self.state_transition_prob, "state_transition_prob", None)
        self.__awu._validate_input_table_datatype(self.emission_prob, "emission_prob", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.state_model_key, "state_model_key")
        self.__awu._validate_dataframe_has_argument_columns(self.state_model_key, "state_model_key", self.init_state_prob, "init_state_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.state_key, "state_key")
        self.__awu._validate_dataframe_has_argument_columns(self.state_key, "state_key", self.init_state_prob, "init_state_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.state_prob_key, "state_prob_key")
        self.__awu._validate_dataframe_has_argument_columns(self.state_prob_key, "state_prob_key", self.init_state_prob, "init_state_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.trans_model_key, "trans_model_key")
        self.__awu._validate_dataframe_has_argument_columns(self.trans_model_key, "trans_model_key", self.state_transition_prob, "state_transition_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.trans_from_key, "trans_from_key")
        self.__awu._validate_dataframe_has_argument_columns(self.trans_from_key, "trans_from_key", self.state_transition_prob, "state_transition_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.trans_to_key, "trans_to_key")
        self.__awu._validate_dataframe_has_argument_columns(self.trans_to_key, "trans_to_key", self.state_transition_prob, "state_transition_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.trans_prob_key, "trans_prob_key")
        self.__awu._validate_dataframe_has_argument_columns(self.trans_prob_key, "trans_prob_key", self.state_transition_prob, "state_transition_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.emit_model_key, "emit_model_key")
        self.__awu._validate_dataframe_has_argument_columns(self.emit_model_key, "emit_model_key", self.emission_prob, "emission_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.emit_state_key, "emit_state_key")
        self.__awu._validate_dataframe_has_argument_columns(self.emit_state_key, "emit_state_key", self.emission_prob, "emission_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.emit_observed_key, "emit_observed_key")
        self.__awu._validate_dataframe_has_argument_columns(self.emit_observed_key, "emit_observed_key", self.emission_prob, "emission_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.emit_prob_key, "emit_prob_key")
        self.__awu._validate_dataframe_has_argument_columns(self.emit_prob_key, "emit_prob_key", self.emission_prob, "emission_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.model_key, "model_key")
        self.__awu._validate_dataframe_has_argument_columns(self.model_key, "model_key", self.observation, "observation", False)
        
        self.__awu._validate_input_columns_not_empty(self.sequence_key, "sequence_key")
        self.__awu._validate_dataframe_has_argument_columns(self.sequence_key, "sequence_key", self.observation, "observation", False)
        
        self.__awu._validate_input_columns_not_empty(self.observed_key, "observed_key")
        self.__awu._validate_dataframe_has_argument_columns(self.observed_key, "observed_key", self.observation, "observation", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.observation, "observation", False)
        
        self.__awu._validate_input_columns_not_empty(self.seq_prob_key, "seq_prob_key")
        self.__awu._validate_dataframe_has_argument_columns(self.seq_prob_key, "seq_prob_key", self.observation, "observation", False)
        
        self.__awu._validate_input_columns_not_empty(self.skip_key, "skip_key")
        self.__awu._validate_dataframe_has_argument_columns(self.skip_key, "skip_key", self.observation, "observation", False)
        
        self.__awu._validate_input_columns_not_empty(self.observation_sequence_column, "observation_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.observation_sequence_column, "observation_sequence_column", self.observation, "observation", False)
        
        self.__awu._validate_input_columns_not_empty(self.init_state_prob_sequence_column, "init_state_prob_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.init_state_prob_sequence_column, "init_state_prob_sequence_column", self.init_state_prob, "init_state_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.state_transition_prob_sequence_column, "state_transition_prob_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.state_transition_prob_sequence_column, "state_transition_prob_sequence_column", self.state_transition_prob, "state_transition_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.emission_prob_sequence_column, "emission_prob_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.emission_prob_sequence_column, "emission_prob_sequence_column", self.emission_prob, "emission_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.observation_partition_column, "observation_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.observation_partition_column, "observation_partition_column", self.observation, "observation", True)
        
        self.__awu._validate_input_columns_not_empty(self.init_state_prob_partition_column, "init_state_prob_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.init_state_prob_partition_column, "init_state_prob_partition_column", self.init_state_prob, "init_state_prob", True)
        
        self.__awu._validate_input_columns_not_empty(self.state_transition_prob_partition_column, "state_transition_prob_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.state_transition_prob_partition_column, "state_transition_prob_partition_column", self.state_transition_prob, "state_transition_prob", True)
        
        self.__awu._validate_input_columns_not_empty(self.emission_prob_partition_column, "emission_prob_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.emission_prob_partition_column, "emission_prob_partition_column", self.emission_prob, "emission_prob", True)
        
        self.__awu._validate_input_columns_not_empty(self.observation_order_column, "observation_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.observation_order_column, "observation_order_column", self.observation, "observation", False)
        
        self.__awu._validate_input_columns_not_empty(self.init_state_prob_order_column, "init_state_prob_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.init_state_prob_order_column, "init_state_prob_order_column", self.init_state_prob, "init_state_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.state_transition_prob_order_column, "state_transition_prob_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.state_transition_prob_order_column, "state_transition_prob_order_column", self.state_transition_prob, "state_transition_prob", False)
        
        self.__awu._validate_input_columns_not_empty(self.emission_prob_order_column, "emission_prob_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.emission_prob_order_column, "emission_prob_order_column", self.emission_prob, "emission_prob", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        
        # Output table arguments list
        self.__func_output_args_sql_names = []
        self.__func_output_args = []
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("InitStateModelColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.state_model_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("InitStateColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.state_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("InitStateProbColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.state_prob_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TransAttributeColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.trans_model_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TransFromStateColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.trans_from_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TransToStateColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.trans_to_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TransProbColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.trans_prob_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("EmitModelColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.emit_model_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("EmitStateColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.emit_state_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("EmitObsColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.emit_observed_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("EmitProbColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.emit_prob_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("ModelColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.model_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("SeqColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.sequence_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("ObsColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.observed_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.seq_prob_key is not None:
            self.__func_other_arg_sql_names.append("SeqProbColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.seq_prob_key, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.skip_key is not None:
            self.__func_other_arg_sql_names.append("SkipColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.skip_key, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.show_rate_change is not None and self.show_rate_change != True:
            self.__func_other_arg_sql_names.append("ShowChangeRate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.show_rate_change, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.incremental is not None and self.incremental != True:
            self.__func_other_arg_sql_names.append("Incremental")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.incremental, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.observation_sequence_column is not None:
            sequence_input_by_list.append("observation:" + UtilFuncs._teradata_collapse_arglist(self.observation_sequence_column, ""))
        
        if self.init_state_prob_sequence_column is not None:
            sequence_input_by_list.append("InitStateProb:" + UtilFuncs._teradata_collapse_arglist(self.init_state_prob_sequence_column, ""))
        
        if self.state_transition_prob_sequence_column is not None:
            sequence_input_by_list.append("TransProb:" + UtilFuncs._teradata_collapse_arglist(self.state_transition_prob_sequence_column, ""))
        
        if self.emission_prob_sequence_column is not None:
            sequence_input_by_list.append("EmissionProb:" + UtilFuncs._teradata_collapse_arglist(self.emission_prob_sequence_column, ""))
        
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
        
        # Process observation
        self.observation_partition_column = UtilFuncs._teradata_collapse_arglist(self.observation_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.observation, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("observation")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.observation_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.observation_order_column, "\""))
        
        # Process init_state_prob
        self.init_state_prob_partition_column = UtilFuncs._teradata_collapse_arglist(self.init_state_prob_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.init_state_prob, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("InitStateProb")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.init_state_prob_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.init_state_prob_order_column, "\""))
        
        # Process state_transition_prob
        self.state_transition_prob_partition_column = UtilFuncs._teradata_collapse_arglist(self.state_transition_prob_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.state_transition_prob, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("TransProb")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.state_transition_prob_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.state_transition_prob_order_column, "\""))
        
        # Process emission_prob
        self.emission_prob_partition_column = UtilFuncs._teradata_collapse_arglist(self.emission_prob_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.emission_prob, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("EmissionProb")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.emission_prob_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.emission_prob_order_column, "\""))
        
        function_name = "HMMEvaluator"
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
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False)
        try:
            # Generate the output.
            UtilFuncs._create_view(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.result = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.result)
        
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
        result = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("result", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.result  = result 
        
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
        obj.result = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.result), source_type="table", database_name=UtilFuncs._extract_db_name(obj.result))
        obj._mlresults.append(obj.result)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a HMMEvaluator class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
