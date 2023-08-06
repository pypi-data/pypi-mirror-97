"""
Copyright (c) 2020 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: Gouri.Patwardhan@Teradata.com
Secondary Owner: Trupti.Purohit@Teradata.com

teradataml vantage file related utilities/functions.
----------
A teradataml file utility function provides an interface to Teradata Vantage common tasks like
install_file, remove_file, replace_file.
"""

import os
from pathlib import Path
from sqlalchemy import func
from teradatasql import OperationalError as SqlOperationalError
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.dbutils.dbutils import _execute_stored_procedure
from teradataml.utils.validators import _Validators


def install_file(file_identifier, file_path, file_on_client = True, is_binary = False,
                 replace = False, force_replace = False, suppress_output = False):
    """
        DESCRIPTION:
            Function installs or replaces external language script or model files in Vantage.
            On success, prints a message that file is installed or replaced.
            This language script can be executed via execute_script() method in Script.

        PARAMETERS:
            file_identifier:
                Required Argument.
                Specifies the name associated with the user-installed file.
                It cannot have a schema name associated with it,
                as the file is always installed in the current schema.
                The name should be unique within the schema. It can be any valid Teradata identifier.
                Types: str

            file_path:
                Required Argument.
                Specifies the absolute/relative path of file (including file name) to be installed.
                This file is identified in Vantage by file_identifier.
                Types: str

            file_on_client:
                Optional Argument.
                Specifies whether the file is present on client or remote location on Vantage.
                Set this to False if the file to be installed is present at remote location on Vantage.
                Default Value: True
                Types: bool

            is_binary:
                Optional Argument.
                Specifies if file to be installed is a binary file.
                Default Value: False
                Types: bool

            replace:
                Optional Argument.
                Specifies if the file is to be installed or replaced.
                If set to True, then the file is replaced based on the value of force_replace.
                If set to False, then the file is installed.
                Default Value: False
                Types: bool

            force_replace:
                Optional Argument.
                Specifies if system should check for the file being used before replacing it.
                If set to True, then the file is replaced even if it is being executed.
                If set to False, then an error is thrown if it is being executed.
                Default Value: False
                Types: bool
                Note:
                    This argument is ignored if replace is set to False.

            suppress_output:
                Optional Argument.
                Specifies whether to print the output message or not.
                If set to True, then the output message is not printed.
                Default Value: False
                Types: bool

        RETURNS:
             True, if success.

        RAISES:
            TeradataMLException.

        EXAMPLES:
            # Note: File can be on client or remote server.
            # Files mentioned in the examples are part of the package and can be found at package install location
            # followed by the file path mentioned in examples.
            # In first example, file_location is data/scripts/mapper.py, to use this file for installation,
            # one should pass ${tdml_install_location}/data/scripts/mapper.py to file location.
            # Example 1: Install the file mapper.py found at the relative path data/scripts/ using
            #            the default text mode.
            >>> install_file (file_identifier='mapper', file_location='data/scripts/mapper.py')
            File mapper.py installed in Vantage

            # Example 2: Install the file binary_file.dms found at the relative path data/scripts/
            #            using the binary mode.
            >>> install_file (file_identifier='binaryfile', file_location='data/scripts/binary_file.dms', file_on_client = True, is_binary = True)
            File binary_file.dms installed in Vantage

            # Example 3: Replace the file mapper.py with mapper_replace.py found at the relative path data/scripts/
            #            using the default text mode.
            >>> install_file (file_identifier='mapper', file_location='data/scripts/mapper_replace.py', file_on_client=True, is_binary= False, replace=True, force_replace=True)
            File mapper_replace.py replaced in Vantage
    """

    __arg_info_matrix = []
    __arg_info_matrix.append(["file_identifier", file_identifier , False, (str), True])
    __arg_info_matrix.append(["file_path", file_path, False, (str), True])
    __arg_info_matrix.append(["is_binary", is_binary, True, (bool)])
    __arg_info_matrix.append(["file_on_client", file_on_client, True, (bool)])
    __arg_info_matrix.append(["replace_file", replace, True, (bool)])
    __arg_info_matrix.append(["force_replace", force_replace, True, (bool)])
    __arg_info_matrix.append(["suppress_output", suppress_output, True, (bool)])

    # Validate arguments
    _Validators._validate_missing_required_arguments(__arg_info_matrix)
    _Validators._validate_function_arguments(__arg_info_matrix)

    if file_on_client:
        if not Path(file_path).exists():
            raise TeradataMlException(Messages.get_message(MessageCodes.INPUT_FILE_NOT_FOUND).format(file_path),
                                      MessageCodes.INPUT_FILE_NOT_FOUND)

    # Extract file name from path to be used in the stored procedure.
    file_name = os.path.basename(file_path)

    file_location = 'c'
    file_type = 'z'

    if not file_on_client:
        file_location = 's'
    if is_binary:
        file_type = 'b'

    file_path_arg = "{0}{1}!{2}".format(file_location, file_type, file_path)

    if replace:
        # Use FunctionGenerator of sqlalchemy. It generates Function object based on the
        # attributes passed.
        functioncall = func.SYSUIF.replace_file(file_identifier, file_name, file_path_arg, force_replace)
        message_code = MessageCodes.REPLACE_FILE_FAILED
        print_message = "replac"
    else:
        # Use FunctionGenerator of sqlalchemy. It generates Function object based on the
        # attributed passed.
        functioncall = func.SYSUIF.install_file(file_identifier, file_name, file_path_arg)
        message_code = MessageCodes.INSTALL_FILE_FAILED
        print_message = "install"

    try:
        # Execute Stored procedure fetch any warnings and resultset.
        _execute_stored_procedure(functioncall, True)
        if not suppress_output:
            print("File {} {}ed in Vantage".format(file_name, print_message))
        return True

    except SqlOperationalError:
        raise
    except Exception as err:
        raise TeradataMlException(Messages.get_message(message_code, file_identifier) +
                                  '\n' + str(err), message_code)


def remove_file(file_identifier, force_remove = False, suppress_output = False):
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
                Specifies if system should check for the file being used before removing it.
                If set to True, then the file is removed even if it is being executed.
                If set to False, then an error is thrown if it is being executed.
                Default Value: False
                Types: bool

            suppress_output:
                Optional Argument.
                Specifies whether to print the output message or not.
                If set to True, then the output message is not printed.
                Default Value: False
                Types: bool

        RETURNS:
             True, if success.

        RAISES:
            TeradataMLException.

        EXAMPLES:
            # Run install_file example before removing file.
            # Note: File can be on client or remote server. The file location should be specified accordingly.
            # Example 1: Install the file mapper.py found at the relative path data/scripts/ using the default
            #            text mode.
            >>> install_file (file_identifier='mapper', file_location='data/scripts/mapper.py')
            File mapper.py installed in Vantage

            # Example 2: Install the file binary_file.dms found at the relative path data/scripts/
            #            using the binary mode.
            >>> install_file (file_identifier='binaryfile', file_location='data/scripts/binary_file.dms', file_on_client = True, is_binary = True)
            File binary_file.dms installed in Vantage

            # Remove the installed files.
            # Example 1: Remove text file
            >>> remove_file (file_identifier='mapper', force_remove=True)
            File mapper removed from Vantage

            # Example 2: Remove binary file
            >>> remove_file (file_identifier='binaryfile', force_remove=False)
            File binaryfile removed from Vantage

    """
    # Create a matrix with list of arguments for validation.
    __arg_info_matrix = []
    __arg_info_matrix.append(["file_identifier", file_identifier , False, (str), True])
    __arg_info_matrix.append(["force_remove", force_remove, False, (bool)])
    __arg_info_matrix.append(["suppress_output", suppress_output, True, (bool)])

    # Validate arguments
    _Validators._validate_missing_required_arguments(__arg_info_matrix)
    _Validators._validate_function_arguments(__arg_info_matrix)

    try:
        # Function call
        functioncall = func.SYSUIF.remove_file(file_identifier, force_remove)

        # Execute Stored procedure fetch any warnings and resultset.
        _execute_stored_procedure(functioncall, True)
        if not suppress_output:
            print ("File {} removed from Vantage".format(file_identifier))
        return True

    except SqlOperationalError:
        raise
    except Exception as err:
        raise TeradataMlException(Messages.get_message(MessageCodes.REMOVE_FILE_FAILED, file_identifier) +
                                  '\n' + str(err),
                                  MessageCodes.REMOVE_FILE_FAILED)
