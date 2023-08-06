#!/usr/bin/python
# ##################################################################
#
# Copyright 2020 Teradata. All rights reserved.                    #
# TERADATA CONFIDENTIAL AND TRADE SECRET                           #
#
# Primary Owner: Gouri Patwardhan (gouri.patwardhan@teradata.com)  #
# Secondary Owner: Trupti Purohit (trupti.purohit@teradata.com)    #
#
# Function Version: 1.0                                            #
#
# Description: Script is a TeradataML wrapper around Teradata's    #
# Script Table Operator                                            #
# ##################################################################

import docker
import os
import tarfile
import teradataml.dataframe as tdmldf
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from io import StringIO
from teradataml.common.constants import TableOperatorConstants
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.common.constants import OutputStyle, TeradataConstants
from teradataml.context.context import _get_current_databasename
from teradataml.context.context import get_context
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.common.garbagecollector import GarbageCollector
from teradataml.dbutils.filemgr import install_file
from teradataml.dbutils.filemgr import remove_file
from teradataml.table_operators.table_operator_query_generator import \
    TableOperatorQueryGenerator
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.utils.validators import _Validators
from teradataml.options.display import display
from teradataml.options.configure import configure
from teradataml.table_operators.sandbox_container_util import setup_sandbox_env
from teradatasqlalchemy.dialect import dialect as td_dialect
from teradatasqlalchemy import (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT,
                                NUMBER)
from teradatasqlalchemy import (TIMESTAMP, DATE, TIME)
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)
from teradatasqlalchemy import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy import (PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP)
from teradatasqlalchemy import (INTERVAL_YEAR, INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH,
                                INTERVAL_DAY,INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE,
                                INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR,
                                INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND,
                                INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND,
                                INTERVAL_SECOND)

class Script:

    def __init__(self,
                 data=None,
                 script_name=None,
                 files_local_path=None,
                 script_command=None,
                 delimiter="\t",
                 returns=None,
                 auth=None,
                 charset=None,
                 quotechar=None,
                 data_partition_column=None,
                 data_hash_column=None,
                 data_order_column=None,
                 is_local_order=False,
                 sort_ascending=True,
                 nulls_first=True):
        """
        DESCRIPTION:
            The Script table operator function executes a user-installed script or
            any LINUX command inside database on Teradata Vantage.

        PARAMETERS:
            script_command:
                Required Argument.
                Specifies the command/script to run.
                Types: str

            script_name:
                Required Argument.
                Specifies the name of user script.
                User script should have at least permissions of mode 644.
                Types: str

            files_local_path:
                Required Argument.
                Specifies the absolute local path where user script and all supporting
                files like model files, input data file reside.
                Types: str

            returns:
                Required Argument.
                Specifies output column definition.
                Types: Dictionary specifying column name to teradatasqlalchemy type mapping.
                Default: None
                Note:
                    User can pass a dictionary (dict or OrderedDict) to the "returns" argument,
                    with the keys ordered to represent the order of the output columns.
                    Preferred type is OrderedDict.

            data:
                Optional Argument.
                Specifies a teradataml DataFrame containing the input data for the
                script.

            data_hash_column:
                Optional Argument.
                Specifies the column to be used for hashing.
                The rows in the data are redistributed to AMPs based on the hash value of
                the column specified.
                The user-installed script file then runs once on each AMP.
                If there is no "data_partition_column", then the entire result set,
                delivered by the function, constitutes a single group or partition.
                Types: str
                Note:
                    "data_hash_column" can not be specified along with
                    "data_partition_column", "is_local_order" and "data_order_column".

            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for "data".
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
                Note:
                    1) "data_partition_column" can not be specified along with
                       "data_hash_column".
                    2) "data_partition_column" can not be specified along with
                       "is_local_order = True".

            is_local_order:
                Optional Argument.
                Specifies a boolean value to determine whether the input data is to be
                ordered locally or not. Order by specifies the order in which the
                values in a group, or partition, are sorted. Local Order By specifies
                orders qualified rows on each AMP in preparation to be input to a table
                function. This argument is ignored, if "data_order_column" is None. When
                set to True, data is ordered locally.
                Default Value: False
                Types: bool
                Note:
                    1) "is_local_order" can not be specified along with "data_hash_column".
                    2) When "is_local_order" is set to True, "data_order_column" should be
                       specified, and the columns specified in "data_order_column" are
                       used for local ordering.

            data_order_column:
                Optional Argument.
                Specifies Order By columns for "data".
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering. This argument is used with in both cases:
                "is_local_order = True" and "is_local_order = False".
                Types: str OR list of Strings (str)
                Note:
                    "data_order_column" can not be specified along with "data_hash_column".

            sort_ascending:
                Optional Argument.
                Specifies a boolean value to determine if the result set is to be sorted
                on the "data_order_column" column in ascending or descending order.
                The sorting is ascending when this argument is set to True, and descending
                when set to False. This argument is ignored, if "data_order_column" is
                None.
                Default Value: True
                Types: bool

            nulls_first:
                Optional Argument.
                Specifies a boolean value to determine whether NULLS are listed first or
                last during ordering. This argument is ignored, if "data_order_column" is
                None. NULLS are listed first when this argument is set to True, and last
                when set to False.
                Default Value: True
                Types: bool

            delimiter:
                Optional Argument.
                Specifies a delimiter to use when reading columns from a row and
                writing result columns.
                Default Value: "\t" (tab)
                Types: str of length 1 character
                Notes:
                    1) This argument cannot be same as "quotechar" argument.
                    2) This argument cannot be a newline character i.e., '\\n'.

            auth:
                Optional Argument.
                Specifies an authorization to use when running the script.
                Types: str

            charset:
                Optional Argument.
                Specifies the character encoding for data.
                Permitted Values: utf-16, latin
                Types: str

            quotechar:
                Optional Argument.
                Specifies a character that forces all input and output of the script
                to be quoted using this specified character.
                Using this argument enables the Advanced SQL Engine to distinguish
                between NULL fields and empty strings. A string with length zero is
                quoted, while NULL fields are not.
                If this character is found in the data, it will be escaped by a second
                quote character.
                Types: character of length 1
                Notes:
                    1) This argument cannot be same as "delimiter" argument.
                    2) This argument cannot be a newline character i.e., '\\n'.

        RETURNS:
            Script Object

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Note - Refer to User Guide for setting search path and required permissions.
            # Load example data.
            load_example_data("Script", ["barrier"])

            # Example - The script mapper.py reads in a line of text input
            # ("Old Macdonald Had A Farm") from csv and splits the line into individual
            # words, emitting a new row for each word.

            # Create teradataml DataFrame objects.
            >>> barrierdf = DataFrame.from_table("barrier")

            # Set SEARCHUIFDBPATH.
            >>> get_context().execute("SET SESSION SEARCHUIFDBPATH = alice;")

            # Create a Script object that allows us to execute script on Vantage.
            >>> import teradataml, os
            >>> from teradatasqlalchemy import VARCHAR
            >>> td_path = os.path.dirname(teradataml.__file__)
            >>> sto = Script(data=barrierdf,
            ...              script_name='mapper.py',
            ...              files_local_path= os.path.join(td_path, 'data', 'scripts'),
            ...              script_command='python ./alice/mapper.py',
            ...              data_order_column="Id",
            ...              is_local_order=False,
            ...              nulls_first=False,
            ...              sort_ascending=False,
            ...              charset='latin',
            ...              returns=OrderedDict([("word", VARCHAR(15)),("count_input", VARCHAR(2))]))

            # Run user script locally within docker container and using data from csv.
            # This helps the user to fix script level issues outside Vantage.
            # Setup the environment by providing local path to docker image file.
            >>> sto.setup_sto_env(docker_image_location='/tmp/sto_sandbox_docker_image.tar'))
            Loading image from /tmp/sto_sandbox_docker_image.tar. It may take few minutes.
            Image loaded successfully.
            Starting a container for stosandbox:1.0 image.
            Container d7c73cb498c79a082180576bb5b10bb07b52efdd3026856146fc15e91147b19f
            started successfully.

            >>> sto.test_script(input_data_file='../barrier.csv', data_file_delimiter=',')

            ############ STDOUT Output ############

                    word  count_input
            0          1            1
            1        Old            1
            2  Macdonald            1
            3        Had            1
            4          A            1
            5       Farm            1
            >>>

            # Script results look good. Now install file on Vantage.
            >>> sto.install_file(file_identifier='mapper',
            ...                  file_name='mapper.py',
            ...                  is_binary=False)
            File mapper.py installed in Vantage

            # Execute the user script on Vantage.
            >>> sto.execute_script()
            ############ STDOUT Output ############

                    word count_input
            0  Macdonald           1
            1          A           1
            2       Farm           1
            3        Had           1
            4        Old           1
            5          1           1

            # Remove the installed file from Vantage.
            >>> sto.remove_file(file_identifier='mapper', force_remove=True)
            File mapper removed from Vantage
        """
        self.result = None
        self.data = data
        self.script_name = script_name
        self.files_local_path = files_local_path
        self.script_command = script_command
        self.delimiter = delimiter
        self.returns = returns
        self.auth = auth
        self.charset = charset
        self.quotechar = quotechar
        self.data_partition_column = data_partition_column
        self.data_hash_column = data_hash_column
        self.data_order_column = data_order_column
        self.is_local_order = is_local_order
        self.sort_ascending = sort_ascending
        self.nulls_first = nulls_first

        # Create AnalyticsWrapperUtils instance which contains validation functions.
        # This is required for is_default_or_not check.
        # Rest all validation is done using _Validators
        self.__awu = AnalyticsWrapperUtils()

        # Below matrix is a list of lists, where in each row contains following elements:
        # Let's take an example of following, just to get an idea:
        #   [element1, element2, element3, element4, element5, element6]
        #   e.g.
        #       ["join", join, True, (str), True, concat_join_permitted_values]

        #   1. element1 --> Argument Name, a string. ["join" in above example.]
        #   2. element2 --> Argument itself. [join]
        #   3. element3 --> Specifies a flag that mentions argument is optional or not.
        #                   False, means required and True means optional.
        #   4. element4 --> Tuple of accepted types. (str) in above example.
        #   5. element5 --> True, means validate for empty value. Error will be raised,
        #                   if empty value is passed.
        #                   If not specified, means same as specifying False.
        #   6. element6 --> A list of permitted values, an argument can accept.
        #                   If not specified, it is as good as passing None.
        #                   If a list is passed, validation will be
        #                   performed for permitted values.

        self.awu_matrix = []
        self.awu_matrix.append(["data", self.data, True, (tdmldf.dataframe.DataFrame)])
        self.awu_matrix.append(["data_partition_column", self.data_partition_column, True,
                                (str, list), True])
        self.awu_matrix.append(["data_hash_column", self.data_hash_column, True,
                                (str, list), True])
        self.awu_matrix.append(["data_order_column", self.data_order_column, True,
                                (str, list), True])
        self.awu_matrix.append(["is_local_order", self.is_local_order, True, (bool)])
        self.awu_matrix.append(["sort_ascending", self.sort_ascending, True, (bool)])
        self.awu_matrix.append(["nulls_first", self.nulls_first, True, (bool)])
        self.awu_matrix.append(["script_command", self.script_command, False, (str),
                                True])
        self.awu_matrix.append(["script_name", self.script_name, True, (str), True])
        self.awu_matrix.append(["files_local_path", self.files_local_path, True, (str),
                                True])
        self.awu_matrix.append(["delimiter", self.delimiter, True, (str), False])
        self.awu_matrix.append(["returns", self.returns, False, (dict), True])
        self.awu_matrix.append(["auth", self.auth, True, (str), True])
        self.awu_matrix.append(["charset", self.charset, True, (str), True,
                                ["utf-16", "latin"]])
        self.awu_matrix.append(["quotechar", self.quotechar, True, (str), False])

        # Perform the function validations
        self.__validate()

    def __validate(self):
        """
        Function to validate Table Operator Function arguments, which verifies missing
        arguments, input argument and table types. Also processes the argument values.
        """
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        _Validators._validate_missing_required_arguments(self.awu_matrix)

        # Validate argument types.
        _Validators._validate_function_arguments(self.awu_matrix,
                                                 skip_empty_check={"quotechar" : ["\n", "\t"],
                                                                   "delimiter" : ["\n"]})

        # permissible_datatypes in returns
        allowed_datatypes = (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER,
                             TIMESTAMP, DATE, TIME, CHAR, VARCHAR, CLOB, BYTE, VARBYTE,
                             BLOB, PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP,
                             INTERVAL_YEAR, INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH,
                             INTERVAL_DAY, INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE,
                             INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR,
                             INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND,
                             INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND, INTERVAL_SECOND
                             )

        # Validate keys and datatypes in returns.
        self.awu_matrix_returns = []
        for key in self.returns.keys():
            self.awu_matrix_returns.append(["keys in returns", key, False, (str), True])
            self.awu_matrix_returns.append(["value in returns", self.returns[key], False,
                                            allowed_datatypes])
        _Validators._validate_function_arguments(self.awu_matrix_returns)

        if self.data is not None:
            # Hash and order by can be used together as long as is_local_order = True.
            if all([self.data_hash_column,
                    self.data_order_column]) and not self.is_local_order:
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.CANNOT_USE_TOGETHER_WITH,
                                         "data_hash_column' and 'data_order_column",
                                         "is_local_order=False"),
                    MessageCodes.CANNOT_USE_TOGETHER_WITH)

            # Either hash or partition can be used.
            _Validators._validate_mutually_exclusive_arguments(self.data_hash_column,
                                                               "data_hash_column",
                                                               self.data_partition_column,
                                                               "data_partition_column",
                                                               skip_all_none_check=True)

            # Either local order by or partition by can be used.
            _Validators._validate_mutually_exclusive_arguments(self.is_local_order,
                                                               "is_local_order=True",
                                                               self.data_partition_column,
                                                               "data_partition_column",
                                                               skip_all_none_check=True)

            # local order by requires column name.
            if self.is_local_order and self.data_order_column is None:
                message = Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                               "data_order_column", "is_local_order=True")
                raise TeradataMlException(message, MessageCodes.DEPENDENT_ARG_MISSING)

            if self.__awu._is_default_or_not(self.data_partition_column, "ANY"):
                self.__awu._validate_dataframe_has_argument_columns(
                    self.data_partition_column, "data_partition_column", self.data, "data", True)

            if self.data_order_column is not None:
                self.__awu._validate_dataframe_has_argument_columns(
                    self.data_order_column, "data_order_column",self.data, "data", False)

            if self.data_hash_column is not None:
                self.__awu._validate_dataframe_has_argument_columns(
                    self.data_hash_column, "data_hash_column", self.data, "data", False)

            if self.data_partition_column is not None:
                self.__awu._validate_dataframe_has_argument_columns(
                    self.data_partition_column, "data_partition_column", self.data, "data", False)

        # Check for length of the arguments "delimiter" and "quotechar".
        if self.delimiter is not None:
            _Validators._validate_str_arg_length('delimiter', self.delimiter, 'EQ', 1)

        if self.quotechar is not None:
            _Validators._validate_str_arg_length('quotechar', self.quotechar, 'EQ', 1)

        # The arguments 'quotechar' and 'delimiter' cannot take newline character.
        if self.delimiter == '\n':
            message = Messages.get_message(MessageCodes.NOT_ALLOWED_VALUES, "\n", "delimiter")
            raise TeradataMlException(message, MessageCodes.NOT_ALLOWED_VALUES)
        if self.quotechar == '\n':
            message = Messages.get_message(MessageCodes.NOT_ALLOWED_VALUES, "\n", "quotechar")
            raise TeradataMlException(message, MessageCodes.NOT_ALLOWED_VALUES)

        # The arguments 'quotechar' and 'delimiter' cannot have the same value.
        if self.delimiter == self.quotechar:
            message = Messages.get_message(MessageCodes.ARGUMENT_VALUE_SAME, "delimiter",
                                           "quotechar")
            raise TeradataMlException(message, MessageCodes.ARGUMENT_VALUE_SAME)

    def set_data(self,
                 data,
                 data_partition_column=None,
                 data_hash_column=None,
                 data_order_column=None,
                 is_local_order=False,
                 sort_ascending=True,
                 nulls_first=True):
        """
        DESCRIPTION:
            Function enables user to set data and data related arguments without having to
            re-create Script object.

        PARAMETERS:
            data:
                Required Argument.
                Specifies a teradataml DataFrame containing the input data for the script.

            data_hash_column:
                Optional Argument.
                Specifies the column to be used for hashing.
                The rows in the data are redistributed to AMPs based on the
                hash value of the column specified.
                The user installed script then runs once on each AMP.
                If there is no data_partition_column, then the entire result set delivered
                by the function, constitutes a single group or partition.
                Types: str
                Note:
                    "data_hash_column" can not be specified along with
                    "data_partition_column", "is_local_order" and "data_order_column".

            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
                Note:
                    1) "data_partition_column" can not be specified along with
                       "data_hash_column".
                    2) "data_partition_column" can not be specified along with
                       "is_local_order = True".

            is_local_order:
                Optional Argument.
                Specifies a boolean value to determine whether the input data is to be
                ordered locally or not. Order by specifies the order in which the
                values in a group or partition are sorted.  Local Order By specifies
                orders qualified rows on each AMP in preparation to be input to a table
                function. This argument is ignored, if "data_order_column" is None. When
                set to True, data is ordered locally.
                Default Value: False
                Types: bool
                Note:
                    1) "is_local_order" can not be specified along with
                       "data_hash_column".
                    2) When "is_local_order" is set to True, "data_order_column" should be
                       specified, and the columns specified in "data_order_column" are
                       used for local ordering.

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                This argument is used in both cases:
                "is_local_order = True" and "is_local_order = False".
                Types: str OR list of Strings (str)
                Note:
                    "data_order_column" can not be specified along with
                    "data_hash_column".

            sort_ascending:
                Optional Argument.
                Specifies a boolean value to determine if the result set is to be sorted
                on the column specified in "data_order_column", in ascending or descending
                order.
                The sorting is ascending when this argument is set to True, and descending
                when set to False.
                This argument is ignored, if "data_order_column" is None.
                Default Value: True
                Types: bool

            nulls_first:
                Optional Argument.
                Specifies a boolean value to determine whether NULLS are listed first or
                last during ordering.
                This argument is ignored, if "data_order_column" is None.
                NULLS are listed first when this argument is set to True, and
                last when set to False.
                Default Value: True
                Types: bool

        RETURNS:
            None.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Note - Refer to User Guide for setting search path and required permissions.
            # Load example data.
            load_example_data("Script", ["barrier"])

            # Example 1
            # Create teradataml DataFrame objects.
            >>> barrierdf = DataFrame.from_table("barrier")
            >>> barrierdf
                                    Name
            Id
            1   Old Macdonald Had A Farm
            >>>

            # Set SEARCHUIFDBPATH
            >>> get_context().execute("SET SESSION SEARCHUIFDBPATH = alice;")
            >>> import teradataml
            >>> from teradatasqlalchemy import VARCHAR
            >>> td_path = os.path.dirname(teradataml.__file__)

            # The script mapper.py reads in a line of text input
            # ("Old Macdonald Had A Farm") from csv and
            # splits the line into individual words, emitting a new row for each word.
            # Create a Script object without data and its arguments.
            >>> sto = Script(data = barrierdf,
            ...              script_name='mapper.py',
            ...              files_local_path= os.path.join(td_path,'data', 'scripts'),
            ...              script_command='python ./alice/mapper.py',
            ...              charset='latin',
            ...              returns=OrderedDict([("word", VARCHAR(15)),("count_input", VARCHAR(2))]))

            # Test script using data from file
            >>> sto.test_script(input_data_file='../barrier.csv', data_file_delimiter=',')
            ############ STDOUT Output ############
                    word  count_input
            0          1            1
            1        Old            1
            2  Macdonald            1
            3        Had            1
            4          A            1
            5       Farm            1
            >>>

            # Test script using data from DB.
            >>> sto.test_script(password='alice')
            ############ STDOUT Output ############

                    word  count_input
            0          1            1
            1        Old            1
            2  Macdonald            1
            3        Had            1
            4          A            1
            5       Farm            1

            # Test script using data from DB and with data_row_limit.
            >>> sto.test_script(password='alice', data_row_limit=5)
            ############ STDOUT Output ############

                    word  count_input
            0          1            1
            1        Old            1
            2  Macdonald            1
            3        Had            1
            4          A            1
            5       Farm            1

            # Now in order to test / run script on actual data on Vantage user must
            # set data and related arguments.
            # Note:
            #    All data related arguments that are not specified in set_data() are
            #    reset to default values.
            >>> sto.set_data(data=barrierdf,
            ...              data_order_column="Id",
            ...              is_local_order=False,
            ...              nulls_first=False,
            ...              sort_ascending=False)

            # Execute the user script on Vantage.
            >>> sto.execute_script()
            ############ STDOUT Output ############
                    word count_input
            0  Macdonald           1
            1          A           1
            2       Farm           1
            3        Had           1
            4        Old           1
            5          1           1

            # Example 2 -
            # Script is tested using test_script and executed on Vantage.
            # use set_data() to reset arguments.
            # Create teradataml DataFrame objects.
            >>> load_example_data("Script", ["barrier_new"])
            >>> barrierdf_new = DataFrame.from_table("barrier_new")
            >>> barrierdf_new
                                    Name
            Id
            2   On his farm he had a cow
            1   Old Macdonald Had A Farm
            >>>

            # Create a Script object that allows us to execute script on Vantage.
            >>> sto = Script(data=barrierdf_new,
            ...              script_name='mapper.py',
            ...              files_local_path= os.path.join(td_path, 'data', 'scripts'),
            ...              script_command='python ./alice/mapper.py',
            ...              data_order_column="Id",
            ...              is_local_order=False,
            ...              nulls_first=False,
            ...              sort_ascending=False,
            ...              charset='latin',
            ...              returns=OrderedDict([("word", VARCHAR(15)),("count_input", VARCHAR(2))]))
            # Script is tested using test_script and executed on Vantage.
            >>> sto.execute_script()
            ############ STDOUT Output ############
               word count_input
            0   his           1
            1    he           1
            2   had           1
            3     a           1
            4     1           1
            5   Old           1
            6   cow           1
            7  farm           1
            8    On           1
            9     2           1

            # Now in order to run the script with a different dataset,
            # user can use set_data().
            # Re-set data and some data related parameters.
            # Note:
            #     All data related arguments that are not specified in set_data() are
            #     reset to default values.
            >>> sto.set_data(data=barrierdf,
            ...              data_order_column='Id',
            ...              is_local_order=True,
            ...              nulls_first=True)
            >>> sto.execute_script()
                    word count_input
            0  Macdonald           1
            1          A           1
            2       Farm           1
            3        Had           1
            4        Old           1
            5          1           1

            # Example 3
            # Script is tested using test_script and executed on Vantage.
            # In order to run the script with same dataset but different data related
            # arguments, use set_data() to reset arguments.
            # Note:
            #     All data related arguments that are not specified in set_data() are
            #     reset to default values.
            >>> sto.set_data(data=barrierdf_new,
            ...              data_order_column='Id',
            ...              is_local_order = True,
            ...              nulls_first = True)

            >>> sto.execute_script()
            ############ STDOUT Output ############

                    word count_input
            0  Macdonald           1
            1          A           1
            2       Farm           1
            3          2           1
            4        his           1
            5       farm           1
            6         On           1
            7        Had           1
            8        Old           1
            9          1           1
        """

        self.awu_matrix_setter = []
        self.awu_matrix_setter.append(["data", data, True, (tdmldf.dataframe.DataFrame)])
        self.awu_matrix_setter.append(["data_partition_column", data_partition_column,
                                       True, (str, list), True])
        self.awu_matrix_setter.append(["data_hash_column", data_hash_column, True,
                                       (str, list), True])
        self.awu_matrix_setter.append(["data_order_column", data_order_column, True,
                                       (str, list), True])
        self.awu_matrix_setter.append(["is_local_order", is_local_order, True, (bool)])
        self.awu_matrix_setter.append(["sort_ascending", sort_ascending, True, (bool)])
        self.awu_matrix_setter.append(["nulls_first", nulls_first, True, (bool)])

        # Perform the function validations
        _Validators._validate_missing_required_arguments([["data", data, False,
                                                           (tdmldf.dataframe.DataFrame)]])
        _Validators._validate_function_arguments(self.awu_matrix_setter)

        self.data = data
        self.data_partition_column = data_partition_column
        self.data_hash_column = data_hash_column
        self.data_order_column = data_order_column
        self.is_local_order = is_local_order
        self.sort_ascending = sort_ascending
        self.nulls_first = nulls_first

        self.__validate()

    def setup_sto_env(self, docker_image_location):
        """
        DESCRIPTION:
            Function enables user to load already downloaded sandbox image.

        PARAMETERS:
            docker_image_location:
                Required Argument.
                Specifies the location of image on user's system.
                Types: str

                Note:
                    For location to download docker image refer teradataml User Guide.

        RETURNS:
            None.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Note - Refer to User Guide for setting search path and required permissions.
            # Load example data.
            load_example_data("Script", ["barrier"])

            # Example - The script mapper.py reads in a line of text input
            # ("Old Macdonald Had A Farm") from csv and
            # splits the line into individual words, emitting a new row for each word.

            # Create teradataml DataFrame objects.
            >>> barrierdf = DataFrame.from_table("barrier")

            # Set SEARCHUIFDBPATH.
            >>> get_context().execute("SET SESSION SEARCHUIFDBPATH = alice;")

            # Create a Script object that allows us to execute script on Vantage.
            >>> import os
            >>> td_path = os.path.dirname(teradataml.__file__)
            >>> from teradatasqlalchemy import VARCHAR
            >>> sto = Script(data=barrierdf,
            ...              script_name='mapper.py',
            ...              files_local_path= os.path.join(td_path, 'data', 'scripts'),
            ...              script_command='python ./alice/mapper.py',
            ...              data_order_column="Id",
            ...              is_local_order=False,
            ...              nulls_first=False,
            ...              sort_ascending=False,
            ...              charset='latin',
            ...              returns=OrderedDict([("word", VARCHAR(15)),("count_input", VARCHAR(2))]))

            # Run user script locally within docker container and using data from csv.
            # This helps the user to fix script level issues outside Vantage.
            # Setup the environment by providing local path to docker image file.
            >>> sto.setup_sto_env(docker_image_location='/tmp/sto_sandbox_docker_image.tar')
            Loading image from /tmp/sto_sandbox_docker_image.tar. It may take few minutes.
            Image loaded successfully.
            Starting a container for stosandbox:1.0 image.
            Container d7c73cb498c79a082180576bb5b10bb07b52efdd3026856146fc15e91147b19f
            started successfully.

        """
        self.awu_matrix_setup = []
        self.awu_matrix_setup.append((["docker_image_location", docker_image_location,
                                       False, (str), True]))

        # Validate missing arguments.
        _Validators._validate_missing_required_arguments(self.awu_matrix_setup)

        # Validate argument types.
        _Validators._validate_function_arguments(self.awu_matrix_setup)

        from teradataml.table_operators.sandbox_container_util import setup_sandbox_env
        setup_sandbox_env(sandbox_image_location=docker_image_location,
                          sandbox_image_name='stosandbox:1.0')

        # Set _latest_sandbox_exists to True - which indicates sandbox image for STO
        # exists on the system.
        configure._latest_sandbox_exists = True

    def test_script(self, supporting_files=None, input_data_file=None, script_args="",
                    exec_mode ='sandbox', **kwargs):
        """
        DESCRIPTION:
            Function enables user to run script in docker container environment outside
            Vantage.
            Input data for user script is read from file.

        PARAMETERS:
            supporting_files:
                Optional Argument
                Specifies a file or list of supporting files like model files to be
                copied to the container.
                Types: string or list of str

            input_data_file:
                Required Argument.
                Specifies the name of the input data file.
                It should have a path relative to the location specified in
                "files_local_path" argument.
                If set to None, read data from AMP, else from file passed in the argument
                'input_data_file'.
                File should have at least permissions of mode 644.
                Types: str

            script_args:
                Optional Argument.
                Specifies command line arguments required by the user script.
                Types: str

            exec_mode:
                Optional Argument.
                Specifies the mode in which user wants to test the script.
                If set to 'sandbox', the user script will run within the sandbox
                environment, else it will run locally on user's system.
                Permitted Values: 'sandbox', 'local'
                Default Value: 'sandbox'
                Types: str

            kwargs:
                Optional Argument.
                Specifies the keyword arguments required for testing.
                Keys can be:
                    data_row_limit:
                        Optional Argument. Ignored when data is read from file.
                        Specifies the number of rows to be taken from all amps when
                        reading from a table or view on Vantage.
                        Default Value: 1000
                        Types: int

                    password:
                        Optional Argument. Required when reading from database.
                        Specifies the password to connect to vantage where the data
                        resides.
                        Types: str

                    data_file_delimiter:
                        Optional Argument.
                        Specifies the delimiter used in the input data file. This
                        argument can be specified when data is read from file.
                        Default Value: '\t'
                        Types: str

                    data_file_header:
                        Optional Argument.
                        Specifies whether the input data file contains header. This
                        argument can be specified when data is read from file.
                        Default Value: True
                        Types: bool

                    timeout:
                        Optional Argument.
                        Specifies the timeout for docker API calls when running in
                        sandbox mode.
                        Default Value: 5000
                        Types: int

                    data_file_quote_char:
                        Optional Argument.
                        Specifies the quotechar used in the input data file.
                        This argument can be specified when data is read from file.
                        Default Value: '"'
                        
                    logmech:
                        Optional Argument.
                        Specifies the type of logon mechanism to establish a connection to
                        Teradata Vantage.
                        Permitted Values: 'TD2', 'TDNEGO', 'LDAP', 'KRB5' & 'JWT'.
                            TD2:
                                The Teradata 2 (TD2) mechanism provides authentication
                                using a Vantage username and password. This is the default
                                logon mechanism using which the connection is established
                                to Vantage.

                            TDNEGO:
                                A security mechanism that automatically determines the
                                actual mechanism required, based on policy, without user's
                                involvement. The actual mechanism is determined by the
                                TDGSS server configuration and by the security policy's
                                mechanism restrictions.

                            LDAP:
                                A directory-based user logon to Vantage with a directory
                                username and password and is authenticated by the directory.

                            KRB5 (Kerberos):
                                A directory-based user logon to Vantage with a domain
                                username and password and is authenticated by
                                Kerberos (KRB5 mechanism).
                                Note:
                                    User must have a valid ticket-granting ticket in
                                    order to use this logon mechanism.

                            JWT:
                                The JSON Web Token (JWT) authentication mechanism enables
                                single sign-on (SSO) to the Vantage after the user
                                successfully authenticates to Teradata UDA User Service.
                                Note:
                                    User must use logdata parameter when using 'JWT' as
                                    the logon mechanism.
                        Default Value: TD2
                        Types: str

                        Note:
                            teradataml expects the client environments are already setup with appropriate
                            security mechanisms and are in working conditions.
                            For more information please refer Teradata Vantage™ - Advanced SQL Engine
                            Security Administration at https://www.info.teradata.com/

                    logdata:
                        Optional Argument.
                        Specifies parameters to the LOGMECH command beyond those needed by
                        the logon mechanism, such as user ID, password and tokens
                        (in case of JWT) to successfully authenticate the user.
                        Types: str

                Types: dict

        RETURNS:
            Output from user script.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Assumption - sto is Script() object. Please refer to help(Script)
            # for creating Script object.
            # Run user script in sandbox mode with input from data file.

            >>> sto.test_script(input_data_file='../barrier.csv',
            ...                 data_file_delimiter=',',
            ...                 data_file_quote_char='"',
            ...                 data_file_header=True,
            ...                 exec_mode='sandbox')

            ############ STDOUT Output ############
                    word  count_input
            0          1            1
            1        Old            1
            2  Macdonald            1
            3        Had            1
            4          A            1
            5       Farm            1
            >>>

            # Run user script in local mode with input from table.
            >>> sto.test_script(data_row_limit=300, password='alice', exec_mode='local')

            ############ STDOUT Output ############
                    word  count_input
            0          1            1
            1        Old            1
            2  Macdonald            1
            3        Had            1
            4          A            1
            5       Farm            1
            
            # Run user script in sandbox mode with logmech as 'TD2'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice", logmech="TD2")

            # Run user script in sandbox mode with logmech as 'TDNEGO'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice", logmech="TDNEGO")

            # Run user script in sandbox mode with logmech as 'LDAP'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice", logmech="LDAP")

            # Run user script in sandbox mode with logmech as 'KRB5'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice", logmech="KRB5")

            # Run user script in sandbox mode with logmech as 'JWT'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice",
                                logmech='JWT', logdata='token=eyJpc...h8dA')

        """
        logmech_valid_values = ['TD2', 'TDNEGO', 'LDAP', 'KRB5', 'JWT']

        awu_matrix_test=[]
        awu_matrix_test.append((["supporting_files", supporting_files, True,
                                 (str,list), True]))
        awu_matrix_test.append((["input_data_file", input_data_file, True, (str), True]))
        awu_matrix_test.append((["script_args", script_args, True, (str), False]))
        awu_matrix_test.append((["exec_mode", exec_mode, True, (str), True,
                                [TableOperatorConstants.SANDBOX_EXEC.value,
                                 TableOperatorConstants.LOCAL_EXEC.value]]))

        data_row_limit = kwargs.pop("data_row_limit", 1000)
        awu_matrix_test.append((["data_row_limit", data_row_limit, True, (int), True]))

        data_file_delimiter = kwargs.pop("data_file_delimiter", '\t')
        awu_matrix_test.append((["data_file_delimiter", data_file_delimiter, True,
                                 (str), False]))

        data_file_quote_char = kwargs.pop("data_file_quote_char", '"')
        awu_matrix_test.append((["data_file_quote_char", data_file_quote_char, True,
                                 (str), False]))

        data_file_header = kwargs.pop("data_file_header", True)
        awu_matrix_test.append((["data_file_header", data_file_header, True, (bool)]))

        timeout = kwargs.pop("timeout", 5000)
        awu_matrix_test.append((["timeout", timeout, True, (int), True]))

        logmech = kwargs.pop("logmech", "TD2")
        awu_matrix_test.append(
            ["logmech", logmech, True, (str), True, logmech_valid_values])

        logdata = kwargs.pop("logdata", None)
        awu_matrix_test.append(["logdata", logdata, True, (str), True])

        # Validate argument types.
        _Validators._validate_function_arguments(awu_matrix_test)

        # Validate timeout value.
        _Validators._validate_positive_int(timeout, "timeout")

        self.__validate()

        if logmech == "JWT" and not logdata:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING, 'logdata',
                                     'logmech=JWT'),
                MessageCodes.DEPENDENT_ARG_MISSING)

        if data_row_limit <= 0:
            raise ValueError(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).
                             format("data_row_limit", "greater than"))

        # Either of 'input_data_file' or 'password' argument is required.
        password = kwargs.pop("password", None)

        # The check of EITHER_THIS_OR_THAT_ARGUMENT is applicable only when the exec_mode is sandbox.
        # Hence adding the check exec_mode != "local".
        # When exec_mode is local, the connection object is used to get the values in the table.
        if exec_mode != "local" and not (input_data_file or (self.data and password)):
            message = Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                           "input_data_file", "Script data and password")
            raise TeradataMlException(message, MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)
        elif exec_mode == "local" and not (input_data_file or self.data):
            message = Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                           "input_data_file", "Script data")
            raise TeradataMlException(message, MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

        if not self.script_name and self.files_local_path:
            message = Messages.get_message(MessageCodes.MISSING_ARGS,
                                           "script_name and files_local_path")
            raise TeradataMlException(message, MessageCodes.MISSING_ARGS)

        if input_data_file:
            if self.files_local_path is None:
                message = Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                               "files_local_path","input_data_file")
                raise TeradataMlException(message, MessageCodes.DEPENDENT_ARG_MISSING)
            else:
                # Check if file exists.
                fpath = os.path.join(self.files_local_path,
                                     input_data_file)
                _Validators._validate_file_exists(fpath)

        if self.script_name and self.files_local_path:
            # Check if file exists.
            fpath = os.path.join(self.files_local_path,
                                 os.path.basename(self.script_name))
            _Validators._validate_file_exists(fpath)

        if exec_mode.upper() == TableOperatorConstants.LOCAL_EXEC.value:
            user_script_path = os.path.join(self.files_local_path, self.script_name)
            import sys
            cmd = [str(sys.executable), user_script_path]
            cmd.extend(script_args)

            if input_data_file is not None:
                input_file_path = os.path.join(self.files_local_path, input_data_file)

                # Run user script locally with input from a file.
                exec_cmd_output =  self.__local_run_user_script_input_file(
                    cmd, input_file_path, data_file_delimiter, data_file_quote_char, data_file_header)
                try:
                    return self.__process_test_script_output(exec_cmd_output)
                except Exception as exp:
                    raise

            else:
                if self.data.shape[0] > data_row_limit:
                    raise ValueError(
                        Messages.get_message(MessageCodes.DATAFRAME_LIMIT_ERROR,
                                             'data_row_limit', 'data_row_limit',
                                             data_row_limit))

                if not self.data._table_name:
                    self.data._table_name = df_utils._execute_node_return_db_object_name(
                        self.data._nodeid, self.data._metaexpr)

                table_name = UtilFuncs._extract_table_name(self.data._table_name)

                # Run user script locally with input from db.
                exec_cmd_output = self.__local_run_user_script_input_db(cmd, table_name)
                try:
                    return self.__process_test_script_output(exec_cmd_output)
                except Exception as exp:
                    raise
        else:
            # Execution Mode - sandbox.
            # Read container_id from configure.sandbox_container_id, if it is None then
            # raise an exception
            container_id = configure.sandbox_container_id
            if container_id is None:
                message = Messages.get_message(MessageCodes.SANDBOX_CONTAINER_NOT_FOUND)
                raise TeradataMlException(message,
                                          MessageCodes.SANDBOX_CONTAINER_NOT_FOUND)

            # Set path inside docker container. This is where files will be copied to.
            # os.path.join() will not work here because the path is not dependent on
            # client platform. Sandbox environment is linux based here.
            _path_in_docker_container = "/home/tdatuser"
            user_script_path = "{}/{}".format(_path_in_docker_container, self.script_name)

            if input_data_file is not None:
                input_file_name = os.path.basename(input_data_file)
                input_file_path = "{}/{}".format(_path_in_docker_container,
                                                 input_file_name)
                # Create script_executor.
                self.__create_executor_script(user_script_path=user_script_path,
                                              user_script_args=script_args,
                                              data_file_path=input_file_path,
                                              data_file_delimiter=data_file_delimiter,
                                              data_file_quote_char=data_file_quote_char,
                                              data_file_header=data_file_header)
            else:
                # Read input from db.
                if self.data.shape[0] > data_row_limit:
                    raise ValueError(
                        Messages.get_message(MessageCodes.DATAFRAME_LIMIT_ERROR,
                                             'data_row_limit', 'data_row_limit',
                                             data_row_limit))
                db_host = get_context().url.host

                user_name = get_context().url.username

                if not self.data._table_name:
                    self.data._table_name = df_utils._execute_node_return_db_object_name(
                        self.data._nodeid, self.data._metaexpr)
                table_name = UtilFuncs._extract_table_name(self.data._table_name)

                db_name = _get_current_databasename()

                # Create script_executor.
                self.__create_executor_script(user_script_path=user_script_path,
                                              user_script_args=script_args,
                                              db_host=db_host,
                                              user_name=user_name,
                                              passwd=password,
                                              table_name=table_name,
                                              db_name=db_name,
                                              logmech=logmech,
                                              logdata=logdata)

            client = docker.APIClient(timeout=timeout)

            # Copy files to container indicated in configure.sandbox_container_id.
            files_to_copy = [self.script_name]

            if supporting_files is not None:
                if isinstance(supporting_files, str):
                    supporting_files = [supporting_files]

                if len(supporting_files) == 0 \
                        or any(file in [None, "None", ""] for file in supporting_files):
                    raise ValueError(
                        Messages.get_message(MessageCodes.LIST_SELECT_NONE_OR_EMPTY,
                                             'supporting_files'))
                else:
                    files_to_copy.extend(supporting_files)

            if input_data_file is not None:
                files_to_copy.append(input_data_file)

            for filename in files_to_copy:
                file_path = os.path.join(self.files_local_path, filename)
                # Check if file exists.
                _Validators._validate_file_exists(file_path)

                # Copy file to docker container.
                self.__copy_to_docker_container(client, file_path,
                                                _path_in_docker_container,
                                                container_id)

            # Copy script_executor to docker container.
            self.__copy_to_docker_container(client, self.script_path,
                                            _path_in_docker_container,
                                            container_id)

            script_executor_file_name = os.path.basename(self.script_path)
            exec_cmd = ("python3 {0}/{1}".format(_path_in_docker_container,
                                                 script_executor_file_name))

            try:
                # Setup an exec instance in the container.
                exec_cmd_create = client.exec_create(container_id, exec_cmd)

                # Start exec instance and run user script.
                exec_cmd_output = client.exec_start(exec_cmd_create, demux=True)

                # Inspect the output for success or failure.
                inspect_out = client.exec_inspect(exec_cmd_create)

                # Extract the exit code.
                exit_code = inspect_out['ExitCode']

                if exec_cmd_output[0] is not None:
                    executor_output = exec_cmd_output[0].decode()

                executor_error = ""
                if exec_cmd_output[1] is not None:
                    executor_error = exec_cmd_output[1].decode()

                # Exit code 1 indicates any error thrown by subprocess.
                # Exit code 126 indicates permission problem or command is not executable.
                # Exit code 127 indicates possible typos in shell script with
                # unrecognizable characters.
                if exit_code == 1 or exit_code == 126 or exit_code == 127:
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_SCRIPT_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_SCRIPT_ERROR)
                # Exit code 2 indicates either username or password is invalid.
                elif exit_code == 2:
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_CONNECTION_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_CONNECTION_ERROR)
                # Exit code 3 indicates problem with query.
                elif exit_code == 3:
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_QUERY_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_QUERY_ERROR)
                # Exit code 4 indicates all other exceptions / errors.
                elif exit_code == 4:
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_CONTAINER_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_CONTAINER_ERROR)
                elif exit_code != 0:
                    # Any error other than exit code 1, 2, 3, 4
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_CONTAINER_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_CONTAINER_ERROR)
                else:
                    return self.__process_test_script_output(executor_output)
            except Exception as exp:
                message = Messages.get_message(
                    MessageCodes.SANDBOX_CONTAINER_ERROR).format(str(exp))
                raise TeradataMlException(message,
                    MessageCodes.SANDBOX_CONTAINER_ERROR)

    def __local_run_user_script_input_file(self, cmd, input_file_path,
                                           data_file_delimiter='\t',
                                           data_file_quote_char='"',
                                           data_file_header=True):
        """
        DESCRIPTION:
            Function to run the user script in local mode with input from file.

        PARAMETERS:
            cmd:
                Required Argument.
                Specifies the command for running the user script.
                Types: str

            input_file_path:
                Required Argument.
                Specifies the absolute local path of input data file.
                Types: str

            data_file_delimiter:
                Optional Argument.
                Specifies the delimiter used in input data file.
                Default Value: '\t'
                Types: str

            data_file_quote_char:
                Optional Argument.
                Specifies the quote character used in input data file.
                Default Value: '"'
                Types: str

            data_file_header:
                Optional Argument.
                Specifies whether the input data file has header.
                Default Value: True
                Types: bool

        RETURNS:
            The string output of the command that is run on input data file.

        RAISES:
            Exception.

        EXAMPLES:
            self.__local_run_user_script_input_file(cmd ="cmd",
                                                    input_file_path = "input_file_path",
                                                    data_file_delimiter = "data_file_delimiter",
                                                    data_file_quote_char = "data_file_quote_char",
                                                    data_file_header = True)

        """
        with open(input_file_path) as data_file:
            import csv
            from pandas import isna as pd_isna

            data_handle = StringIO()

            # Read data from input file.
            ip_data = csv.reader(data_file,
                                 delimiter=data_file_delimiter,
                                 quotechar=data_file_quote_char)
            # Skip the first row of input file if data_file_header is True.
            if data_file_header:
                next(ip_data)
            for row in ip_data:
                if self.quotechar is not None:
                    # A NULL value should not be enclosed in quotes.
                    # The CSV module has no support for such output with writer,
                    # and hence the custom formatting.
                    line = ['' if pd_isna(s) else "{}{}{}".format(self.quotechar,
                                                                  str(s),
                                                                  self.quotechar)
                            for s in row]
                else:
                    line = ['' if pd_isna(s) else str(s) for s in row]

                complete_line = (self.delimiter.join(line))

                data_handle.write(complete_line)
                data_handle.write("\n")

            return self.__run_user_script_subprocess(cmd, data_handle)

    def __local_run_user_script_input_db(self, cmd, table_name):
        """
        DESCRIPTION:
            Function to run the user script in local mode with input from db.

        PARAMETERS:
            cmd:
                Required Argument.
                Specifies the command for running the user script.
                Types: str

            table_name:
                Required Argument.
                Specifies the table name for input to user script.
                Types: str

        RETURNS:
            The string output of the command that is run on the Vantage table.

        RAISES:
            Exception.

        EXAMPLES:
            self.__local_run_user_script_input_db(cmd = "cmd", table_name = "table_name")

        """
        db_data_handle = StringIO()
        try:
            con = get_context()
            # Query for reading data from DB.
            query = ("SELECT * FROM {} ORDER BY 1;".format(table_name))
            cur = con.execute(query)
            row = cur.fetchone()
            from pandas import isna as pd_isna
            while row:
                if self.quotechar is not None:
                    # A NULL value should not be enclosed in quotes.
                    # The CSV module has no support for such output with writer,
                    # and hence the custom formatting.
                    line = ['' if pd_isna(s) else "{}{}{}".format(self.quotechar,
                                                                  str(s),
                                                                  self.quotechar)
                            for s in row]
                else:
                    line = ['' if pd_isna(s) else str(s) for s in row]

                complete_line = (self.delimiter.join(line))
                db_data_handle.write(complete_line)
                db_data_handle.write("\n")
                row = cur.fetchone()
        except Exception as exp:
            raise exp

        return self.__run_user_script_subprocess(cmd, db_data_handle)

    def __process_test_script_output(self, exec_cmd_output):
        """
        DESCRIPTION:
            Function to format the output of the user script.

        PARAMETERS:
            exec_cmd_output:
                Required Argument.
                Specifies the output returned by the user script.
                Types: str

        RETURNS:
            The test script output as Pandas DataFrame.

        RAISES:
            Exception.

        EXAMPLES:
            self.__process_test_script_output(exec_cmd_output = "exec_cmd_output")
        """
        try:
            kwargs = dict()
            if self.quotechar is not None:
                kwargs['quotechar'] = self.quotechar
                kwargs['quoting'] = 1  # QUOTE_ALL

            output = StringIO(exec_cmd_output)

            from pandas import read_csv as pd_read_csv

            # Form a pandas dataframe.
            df = pd_read_csv(output, sep=self.delimiter, index_col=False, header=None,
                             names=list(self.returns.keys()), **kwargs)
            return df

        except Exception as exp:
            raise exp

    def __run_user_script_subprocess(self, cmd, data_handle):
        """
        DESCRIPTION:
            Function to run the user script in a new process and return the output.

        PARAMETERS:
            cmd:
                Required Argument.
                Specifies the command for running the script.
                Types: str

            data_handle:
                Required Argument.
                Specifies the data handle for the input data required by the user script.

        RETURNS:
            Output of user script on input data supplied in data_handle.

        RAISES:
            None.

        EXAMPLES:
            self.__run_user_script_subprocess(cmd = "exec_cmd_output",
                                              data_handle = data_handle)

        """
        # Launching new process to run the user script.
        try:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
            process_output, process_error = proc.communicate(data_handle.getvalue().encode())
            data_handle.close()

            if proc.returncode == 0:
                return process_output.decode("utf-8").rstrip("\r|\n")
            else:
                message = Messages.get_message(MessageCodes.SCRIPT_LOCAL_RUN_ERROR).\
                    format(process_error)
                raise TeradataMlException(message, MessageCodes.SCRIPT_LOCAL_RUN_ERROR)
        except Exception as e:
            raise e

    def execute_script(self, output_style='VIEW'):
        """
        DESCRIPTION:
            Function enables user to run script on Vantage.

        PARAMETERS:
            output_style:
                Specifies the type of output object to create - a table or a view.
                Permitted Values: 'VIEW', 'TABLE'.
                Default value: 'VIEW'
                Types: str

        RETURNS:
            Output teradataml DataFrames can be accessed using attribute
            references, such as ScriptObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result

        RAISES:
            TeradataMlException, ValueError

        EXAMPLES:
            Refer to help(Script)
        """
        # Validate the output_style.
        permitted_values = [OutputStyle.OUTPUT_TABLE.value,
                            OutputStyle.OUTPUT_VIEW.value]
        _Validators._validate_permitted_values(output_style, permitted_values,
                                               'output_style',
                                               case_insensitive=False, includeNone=False)

        # Validate arguments.
        self.__validate()

        # Generate the Table Operator query.
        self.__form_table_operator_query()

        # Execute Table Operator query and return results.
        return self.__execute(output_style)

    def install_file(self, file_identifier, file_name, is_binary = False,
                     replace = False, force_replace = False):
        """
        DESCRIPTION:
            Function to install script on Vantage.
            On success, prints a message that file is installed.
            This language script can be executed via execute_script() function.

        PARAMETERS:
            file_identifier:
                Required Argument.
                Specifies the name associated with the user-installed file.
                It cannot have a schema name associated with it,
                as the file is always installed in the current schema.
                The name should be unique within the schema. It can be any valid Teradata
                identifier.
                Types: str

            file_name:
                Required Argument:
                Specifies the name of the file user wnats to install.
                Types: str

            is_binary:
                Optional Argument.
                Specifies if file to be installed is a binary file.
                Default Value: False
                Types: bool

            replace:
                Optional Argument.
                Specifies if the file is to be installed or replaced.
                If set to True, then the file is replaced based on value the of
                force_replace.
                If set to False, then the file is installed.
                Default Value: False
                Types: bool

            force_replace:
                Optional Argument.
                Specifies if system should check for the file being used before
                replacing it.
                If set to True, then the file is replaced even if it is being executed.
                If set to False, then an error is thrown if it is being executed.
                Default Value: False
                Types: bool

        RETURNS:
             True, if success

        RAISES:
            TeradataMLException.

        EXAMPLES:
            # Note - Refer to User Guide for setting search path and required permissions.
            # Example 1: Install the file mapper.py found at the relative path
            # data/scripts/ using the default text mode.

            # Set SEARCHUIFDBPATH.
            >>> get_context().execute("SET SESSION SEARCHUIFDBPATH = alice;")

            # Create a Script object that allows us to execute script on Vantage.
            >>> import os
            >>> from teradatasqlalchemy import VARCHAR
            >>> td_path = os.path.dirname(teradataml.__file__)
            >>> sto = Script(data=barrierdf,
            ...              script_name='mapper.py',
            ...              files_local_path= os.path.join(td_path, 'data', "scripts"),
            ...              script_command='python ./alice/mapper.py',
            ...              data_order_column="Id",
            ...              is_local_order=False,
            ...              nulls_first=False,
            ...              sort_ascending=False,
            ...              charset='latin',
            ...              returns=OrderedDict([("word", VARCHAR(15)),("count_input", VARCHAR(2))]))
            >>>

            # Install file on Vantage.

            >>> sto.install_file(file_identifier='mapper',
            ...                  file_name='mapper.py',
            ...                  is_binary=False)
            File mapper.py installed in Vantage

            # Replace file on Vantage.
            >>> sto.install_file(file_identifier='mapper',
            ...                  file_name='mapper.py',
            ...                  is_binary=False,
            ...                  replace=True,
            ...                  force_replace=True)
            File mapper.py replaced in Vantage
        """
        # Install/Replace file on Vantage.
        try:
            file_path = os.path.join(self.files_local_path, file_name)
            # Install file on Vantage.
            install_file(file_identifier=file_identifier, file_path=file_path,
                         is_binary=is_binary,
                         replace=replace, force_replace=force_replace)
        except:
            raise

    def remove_file(self, file_identifier, force_remove=False):
        """
        DESCRIPTION:
            Function to remove user installed files/scripts from Vantage.

        PARAMETERS:
            file_identifier:
                Required Argument.
                Specifies the name associated with the user-installed file.
                It cannot have a database name associated with it,
                as the file is always installed in the current database.
                Types: str

            force_remove:
                Required Argument.
                Specifies if system should check for the file being used before
                removing it.
                If set to True, then the file is removed even if it is being executed.
                If set to False, then an error is thrown if it is being executed.
                Default value: False
                Types: bool

        RETURNS:
             True, if success.

        RAISES:
            TeradataMLException.

        EXAMPLES:
            # Note - Refer to User Guide for setting search path and required permissions.
            # Run install_file example before removing file.

            # Set SEARCHUIFDBPATH.
            >>> get_context().execute("SET SESSION SEARCHUIFDBPATH = alice;")

            # Create a Script object that allows us to execute script on Vantage.
            >>> sto = Script(data=barrierdf,
            ...              script_name='mapper.py',
            ...              files_local_path= os.path.join(td_path, 'data', "scripts"),
            ...              script_command='python ./alice/mapper.py',
            ...              data_order_column="Id",
            ...              is_local_order=False,
            ...              nulls_first=False,
            ...              sort_ascending=False,
            ...              charset='latin',
            ...              returns=OrderedDict([("word", VARCHAR(15)),("count_input", VARCHAR(2))]))
            >>>

            # Install file on Vantage.
            >>> sto.install_file(file_identifier='mapper',
            ...                  file_name='mapper.py',
            ...                  is_binary=False,
            ...                  replace=True,
            ...                  force_replace=True)
            File mapper.py replaced in Vantage

            # Remove the installed file.
            >>> sto.remove_file(file_identifier='mapper', force_remove=True)
            File mapper removed from Vantage

        """
        # Remove file from Vantage
        try:
            remove_file(file_identifier, force_remove)
        except:
            raise

    def __copy_to_docker_container(self, client,
                                   local_file_path,
                                   path_in_docker_container,
                                   container):
        """
        DESCRIPTION:
            Function to copy files to docker container.

        PARAMETERS:
            client:
                Required Argument.
                Specifies the connection object for docker.
                Types: str

            local_file_path:
                Required Argument.
                Specifies the path to the file to be copied.
                Types: str

            path_in_docker_container:
                Required Argument.
                Specifies destination path in the docker container where file will be
                copied to.
                Types: str

            container:
                Required Argument.
                Specifies container id.
                Types: str

            RETURNS:
                None.

            RAISES:
                TeradataMLException.

        """
        # Create tar file.
        tar_file_path = "{}.tar".format(local_file_path)
        file_name = os.path.basename(local_file_path)
        tar = tarfile.open(tar_file_path, mode='w')
        try:
            tar.add(local_file_path, arcname=file_name)
        finally:
            tar.close()
        data = open(tar_file_path, 'rb').read()

        try:
            # Copy file to docker container.
            copy_status = client.put_archive(container, path_in_docker_container, data)
            os.remove(tar_file_path)

            if copy_status:
                return
        except Exception as exp:
            message = Messages.get_message(
                MessageCodes.SANDBOX_CONTAINER_ERROR).format(str(exp))
            raise TeradataMlException(message, MessageCodes.SANDBOX_CONTAINER_ERROR)

    def __form_table_operator_query(self):
        """
        Function to generate the Table Operator queries. The function defines
        variables and list of arguments required to form the query.
        """
        # Output table arguments list.
        self.__func_output_args_sql_names = []
        self.__func_output_args = []

        # Generate lists for rest of the function arguments.
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []

        self.__func_other_arg_sql_names.append("SCRIPT_COMMAND")
        self.__func_other_args.append(
            UtilFuncs._teradata_collapse_arglist(self.script_command, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")

        if self.delimiter is not None:
            self.__func_other_arg_sql_names.append("delimiter")
            self.__func_other_args.append(
                UtilFuncs._teradata_collapse_arglist(self.delimiter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")

        # Generate returns clause.
        ret_vals = []
        returns_clause = ''
        for key in self.returns.keys():
            ret_vals.append('{} {}'.format(key, self.returns[key].compile(td_dialect())))
            returns_clause = ', '.join(ret_vals)

        self.__func_other_arg_sql_names.append("returns")
        self.__func_other_args.append(
            UtilFuncs._teradata_collapse_arglist(returns_clause, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")

        if self.auth is not None:
            self.__func_other_arg_sql_names.append("auth")
            self.__func_other_args.append(
                UtilFuncs._teradata_collapse_arglist(self.auth, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")

        if self.charset is not None:
            self.__func_other_arg_sql_names.append("charset")
            self.__func_other_args.append(
                UtilFuncs._teradata_collapse_arglist(self.charset, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")

        if self.quotechar is not None:
            self.__func_other_arg_sql_names.append("quotechar")
            self.__func_other_args.append(
                UtilFuncs._teradata_collapse_arglist(self.quotechar, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")

        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        self.__func_input_order_by_type = None
        self.__func_input_sort_ascending = self.sort_ascending
        self.__func_input_nulls_first = None

        # Process data.
        if self.data is not None:
            data_distribution = "FACT"
            if self.data_hash_column is not None:
                data_distribution = "HASH"
                data_partition_column = UtilFuncs._teradata_collapse_arglist(
                    self.data_hash_column, "\"")
            else:
                if self.__awu._is_default_or_not(self.data_partition_column, "ANY"):
                    data_partition_column = UtilFuncs._teradata_collapse_arglist(
                        self.data_partition_column, "\"")
                else:
                    data_partition_column = None
            if self.data_order_column is not None:
                if self.is_local_order:
                    self.__func_input_order_by_type = "LOCAL"
                    if not self.data_hash_column:
                        data_distribution = None
                self.__func_input_order_by_cols.append(
                    UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
            else:
                self.__func_input_order_by_cols.append("NA_character_")

            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data,
                                                                             False)
            self.__func_input_distribution.append(data_distribution)
            self.__func_input_arg_sql_names.append("input")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(data_partition_column)
            self.__func_input_nulls_first = self.nulls_first

        function_name = "Script"
        # Create instance to generate Table Operator Query.
        aqg_obj = TableOperatorQueryGenerator(function_name,
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
                                              self.__func_input_order_by_type,
                                              self.__func_input_sort_ascending,
                                              self.__func_input_nulls_first,
                                              engine="ENGINE_SQL"
                                              )

        # Invoke call to Table operator query generation.
        self._tblop_query = aqg_obj._gen_table_operator_select_stmt_sql()

        # Print Table Operator query if requested to do so.
        if display.print_sqlmr_query:
            print(self._tblop_query)

    def __execute(self, output_style='VIEW'):
        """
        DESCRIPTION:
            Function to execute Table Operator queries.
            Create DataFrames for the required Table Operator output.

        PARAMETERS:
            output_style:
                Specifies the type of output object to create - a table of a view.
                Permitted Values: 'VIEW', 'TABLE'.
                Default value: 'VIEW'
                Types: str

        RAISES:
            None.

        RETURNS:
            None.

        EXAMPLES:
            >>> return self.__execute(output_style)
        """
        # Generate STDOUT table name and add it to the output table list.
        if output_style == OutputStyle.OUTPUT_TABLE.value:
            table_type = TeradataConstants.TERADATA_TABLE
        else:
            table_type = TeradataConstants.TERADATA_VIEW

        tblop_stdout_temp_tablename = \
            UtilFuncs._generate_temp_table_name(prefix="td_tblop_out_",
                                                use_default_database=True,
                                                gc_on_quit=True, quote=False,
                                                table_type=table_type)
        try:
            if output_style == OutputStyle.OUTPUT_TABLE.value:
                UtilFuncs._create_table(tblop_stdout_temp_tablename, self._tblop_query)
            else:
                UtilFuncs._create_view(tblop_stdout_temp_tablename, self._tblop_query)
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)),
                MessageCodes.TDMLDF_EXEC_SQL_FAILED)

        self.result = self.__awu._create_data_set_object(
            df_input=UtilFuncs._extract_table_name(tblop_stdout_temp_tablename),
            source_type="table",
            database_name=UtilFuncs._extract_db_name(tblop_stdout_temp_tablename))

        return self.result

    def __create_executor_script(self, user_script_path,
                                 user_script_args=None,
                                 data_file_path=None,
                                 data_file_delimiter='\t',
                                 data_file_quote_char='"',
                                 data_file_header=True,
                                 db_name=None,
                                 db_host=None,
                                 user_name=None,
                                 passwd=None,
                                 logmech=None,
                                 logdata=None,
                                 table_name=None):
        """
        DESCRIPTION:
            Internal function that will generate 'script_executor.py' to be copied to
            sandbox environment.

        PARAMETERS:
            user_script_path:
                Required Argument.
                Specifies the path to user script inside docker container.
                Types: str

            user_script_args:
                Optional Argument.
                Specifies command line arguments required by the user script.
                Types: str

            data_file_path:
                Required Argument.
                Specifies the path to input data file inside docker container.
                Types: str

            data_file_delimiter:
                Optional Argument.
                Specifies the delimiter used in input data file.
                Default Value: "\t" (tab)
                Types: character of length 1

            data_file_quote_char:
                Optional Argument.
                Specifies the quote character used in input data file.
                Default Value: '"'
                Types: character of length 1

            data_file_header:
                Optional Argument.
                Specifies whether the input data file has header.
                Default Value: True
                Types: bool

            db_name:
                Optional Argument.
                Specifies the current database name.
                Default Value: None
                Types: str

            db_host:
                Optional Argument.
                Specifies the host name.
                Default Value: None
                Types: str

            user_name:
                Optional Argument.
                Specifies the user name.
                Default Value: None
                Types: str

            passwd:
                Optional Argument.
                Specifies the password for user name in "user_name".
                Default Value: None
                Types: str

            table_name:
                Optional Argument.
                Specifies the table name where input data is present.
                Default Value: None
                Types: str

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            # Example 1: Create executor script when input data is to be read from a file.

            self.__create_executor_script(user_script_path=user_script_path,
                                          user_script_args=script_args,
                                          data_file_path=input_file_path,
                                          data_file_delimiter=data_file_delimiter,
                                          data_file_quote_char=data_file_quote_char,
                                          data_file_header=data_file_header)

            # Example 2: Create executor script when input data is to be read from db.

            self.__create_executor_script(user_script_path=user_script_path,
                                          user_script_args=script_args,
                                          db_host=db_host,
                                          user_name=user_name,
                                          passwd=password,
                                          table_name=table_name,
                                          db_name=db_name)

        """
        __data_source = "db"
        if data_file_path:
            __data_source = "file"

        temp_script_name = UtilFuncs._generate_temp_script_name(prefix="script_executor",
                                                                use_default_database=True,
                                                                gc_on_quit=True,
                                                                quote=True,
                                                                script_type=TeradataConstants.TERADATA_LOCAL_SCRIPT)

        # Remove quotes from the file name after removing the database name.
        script_alias = UtilFuncs._teradata_unquote_arg(
            UtilFuncs._extract_table_name(temp_script_name), quote='"')

        # script_name is the actual file name (basename).
        script_name = "{script_name}.py".format(script_name=script_alias)

        # Create script in .teradataml directory.
        script_dir = GarbageCollector._get_temp_dir_name()

        # script_path is the actual path where we want to generate the user script at.
        self.script_path = os.path.join(script_dir, script_name)

        template_dir = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))),
            "table_operators", "templates")
        try:
            # Write to the script based on the template.
            executor_file = os.path.join(template_dir,
                                         TableOperatorConstants.SCRIPT_TEMPLATE.value)
            with open(executor_file, 'r') as input_file:
                with open(self.script_path, 'w') as output_file:
                    os.chmod(self.script_path, 0o644)
                    output_file.write(
                        input_file.read().format(
                            DATA_SOURCE=UtilFuncs._serialize_and_encode(__data_source),
                            DELIMITER=UtilFuncs._serialize_and_encode(self.delimiter),
                            QUOTECHAR=UtilFuncs._serialize_and_encode(self.quotechar),
                            USER_SCRIPT_PATH=UtilFuncs._serialize_and_encode(
                                user_script_path),
                            SCRIPT_ARGS=UtilFuncs._serialize_and_encode(user_script_args),
                            DATA_FILE_PATH=UtilFuncs._serialize_and_encode(
                                data_file_path),
                            INPUT_DATA_FILE_DELIMITER=UtilFuncs._serialize_and_encode(
                                data_file_delimiter),
                            INPUT_DATA_FILE_QUOTE_CHAR=UtilFuncs._serialize_and_encode(
                                data_file_quote_char),
                            INPUT_DATA_FILE_HEADER=UtilFuncs._serialize_and_encode(
                                data_file_header),
                            DB_HOST=UtilFuncs._serialize_and_encode(db_host),
                            DB_USER=UtilFuncs._serialize_and_encode(user_name),
                            DB_PASS=UtilFuncs._serialize_and_encode(passwd),
                            DB_NAME=UtilFuncs._serialize_and_encode(db_name),
                            TABLE_NAME=UtilFuncs._serialize_and_encode(table_name),
                            LOGMECH=UtilFuncs._serialize_and_encode(logmech),
                            LOGDATA=UtilFuncs._serialize_and_encode(logdata)
                        ))
        except Exception:
            # Cleanup if we end up here in case of an error.
            GarbageCollector._delete_local_file(self.script_path)
            raise

    def __repr__(self):
        """
        Returns the string representation for a Script class instance.
        """
        if self.result is None:
            repr_string = "Result is empty. Please run execute_script first."
        else:
            repr_string = "############ STDOUT Output ############"
            repr_string = "{}\n\n{}".format(repr_string, self.result)
        return repr_string