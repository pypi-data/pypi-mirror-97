# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: rameshchandra.d@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

teradataml garbage collector module
----------
The garbage collector functionality helps to collect & cleanup the temporary
output tables, views and scripts generated while executing teradataml.

"""
from os.path import expanduser
import teradataml.common as tdmlutil
import teradataml.context as tdmlctx
from teradataml.common.exceptions import TeradataMlException
from teradataml.common import pylogger
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.options.configure import configure
from teradatasql import OperationalError
import psutil
import getpass
import os

logger = pylogger.getLogger()


class GarbageCollector():
    """
    The class has functionality to add temporary tables/views/scripts/container to
    garbage collection, so that they can be dropped when connection is disconnected/lost.
    Writes to a output file where the database name & table/view/script names and sandbox
    container id are persisted.
    """
    __garbage_persistent_file_name = getpass.getuser() + "_garbagecollect.info"
    __garbagecollector_folder_name = ".teradataml"
    __contentseperator = ","
    __version = "ver1.0"
    __gc_tables = []
    __gc_views = []
    __gc_scripts = []
    __gc_container = []

    @staticmethod
    def _get_temp_dir_name():
        """
        DESCRIPTION:
            Function to return the directory where garbage collector file will be persisted.

        PARAMETERS:
            None.

        RETURNS:
            Garbage collector temporary directory name.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector._get_temp_dir_name()
        """
        tempdir = expanduser("~")
        tempdir = os.path.join(tempdir, GarbageCollector.__garbagecollector_folder_name)
        return tempdir

    @staticmethod
    def __make_temp_file_name():
        """
        DESCRIPTION:
            Builds the temp directory where the garbage collector file will be persisted.

        PARAMETERS:
            None.

        RETURNS:
            Garbage collector temporary file name.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector.__build_temp_directory()
        """
        tempdir = GarbageCollector._get_temp_dir_name()
        os.makedirs(tempdir, exist_ok=True)
        tempfile = os.path.join(os.path.sep, tempdir, GarbageCollector.__garbage_persistent_file_name)
        return tempfile

    @staticmethod
    def __validate_gc_add_object(object_name,
                                 object_type=TeradataConstants.TERADATA_TABLE):
        """
        DESCRIPTION:
            Function to add table/view/script/container to the list of gc
            validations.

        PARAMETERS:
            object_name:
                Required Argument.
                Specifies the name of the table/view/script/container to be
                validated for GC.
                Types: str

            object_type:
                Optional Argument.
                Specifies the type of object (table/view/script/container).
                Default Values: TeradataConstants.TERADATA_TABLE
                Types: TeradataConstants

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector.__validate_gc_add_object(object_name, object_type)
        """
        if object_type == TeradataConstants.TERADATA_TABLE:
            GarbageCollector.__gc_tables.append(object_name)
        elif object_type == TeradataConstants.TERADATA_VIEW:
            GarbageCollector.__gc_views.append(object_name)
        elif object_type == TeradataConstants.CONTAINER:
            GarbageCollector.__gc_container.append(object_name)
        else:
            GarbageCollector.__gc_scripts.append(object_name)

    @staticmethod
    def __validate_gc():
        """
        DESCRIPTION:
            Function validates whether all created tables/views/scripts/container
            are removed or not.

        PARAMETERS:
            None.

        RETURNS:
            None.

        RAISES:
            RuntimeError - If GC is not done properly.

        EXAMPLES:
            GarbageCollector.__validate_gc()
        """
        raise_error = False
        err_msg = ""
        if len(GarbageCollector.__gc_tables) != 0:
            err_msg = "Failed to cleanup following tables: {}\n".format(str(GarbageCollector.__gc_tables))
            raise_error = True
        if len(GarbageCollector.__gc_views) != 0:
            err_msg = "{}Failed to cleanup following views: {}\n".format(err_msg, str(GarbageCollector.__gc_views))
            raise_error = True
        if len(GarbageCollector.__gc_scripts) != 0:
            err_msg = "{}Failed to cleanup following scripts: {}\n".format(err_msg, str(GarbageCollector.__gc_scripts))
            raise_error = True
        if len(GarbageCollector.__gc_container) != 0:
            err_msg = "{}Failed to cleanup sandbox container: {}\n". \
                format(err_msg, GarbageCollector.__gc_container)
            raise_error = True
        if raise_error:
            raise RuntimeError(err_msg)

    @staticmethod
    def _add_to_garbagecollector(object_name,
                                 object_type=TeradataConstants.TERADATA_TABLE):
        """
        DESCRIPTION:
            Add database name & temporary table/view/script name to the garbage collector.

        PARAMETERS:
            object_name:
                Required Argument.
                Name of the temporary table/view/script along with database name, container.
                that needs to be garbage collected.
                Types: str

            object_type:
                Optional Argument.
                Specifies the type of object to be added to Garbage Collector.
                Default Values: TeradataConstants.TERADATA_TABLE
                Types: TeradataConstant

        RETURNS:
            True, if successful.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector._add_to_garbagecollector(object_name = "temp"."temp_table1")
        """
        if object_name and object_type:
            try:
                tempfilename = GarbageCollector.__make_temp_file_name()
                writecontent = str(GarbageCollector.__version) + "," + str(os.getpid())
                if object_type == TeradataConstants.TERADATA_TABLE:
                    writecontent += "," + str(TeradataConstants.TERADATA_TABLE.value)
                elif object_type == TeradataConstants.TERADATA_VIEW:
                    writecontent += "," + str(TeradataConstants.TERADATA_VIEW.value)
                elif object_type == TeradataConstants.TERADATA_LOCAL_SCRIPT:
                    writecontent += "," + str(TeradataConstants.TERADATA_LOCAL_SCRIPT.value)
                elif object_type == TeradataConstants.CONTAINER:
                    writecontent += "," + str(TeradataConstants.CONTAINER.value)
                else:
                    writecontent += "," + str(TeradataConstants.TERADATA_SCRIPT.value)
                writecontent += "," + object_name + "\n"
                with open(tempfilename, 'a+') as fgc:
                    fgc.write(writecontent)
                if configure._validate_gc:
                    GarbageCollector.__validate_gc_add_object(object_name, object_type)
            except TeradataMlException:
                raise
            except Exception as err:
                logger.error(Messages.get_message(MessageCodes.TDMLDF_CREATE_GARBAGE_COLLECTOR) + str(err))
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_CREATE_GARBAGE_COLLECTOR),
                                          MessageCodes.TDMLDF_CREATE_GARBAGE_COLLECTOR) from err
            finally:
                if fgc is not None:
                    fgc.close()
        return True

    @staticmethod
    def __deleterow(content_row):
        """
        DESCRIPTION:
            Deletes an entry from persisted file.

        PARAMETERS:
            content_row:
                Required Argument.
                Specifies the text of row to delete from the persisted file.
                Types: str

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector._deleterow(content_row = 'ver1.0,72136,3,"alice"."temp_table_gbview1"')
        """
        try:
            tempfilename = GarbageCollector.__make_temp_file_name()
            if not os.path.isfile(tempfilename):
                return True
            with open(tempfilename, 'r+') as fgc:
                output = fgc.readlines()
                fgc.seek(0)
                for dbtablename in output:
                    if content_row != dbtablename.strip():
                        fgc.write(dbtablename)
                fgc.truncate()
        except Exception as e:
            raise
        finally:
            if fgc and fgc is not None:
                fgc.close()

    @staticmethod
    def __delete_gc_tempdir_local_file(db_object, file_extension='py'):
        """
        DESCRIPTION:
            Creates path to the file in temp directory on client machine
            and deletes the file.

        PARAMETERS:
            db_object:
                Required Argument.
                Specifies the name of the file/script to be deleted.
                Types: str

            file_extension:
                Optional Argument.
                Specifies extension of the file.
                Default Value: 'py'
                Types: str

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector.__delete_gc_tempdir_local_file(
                'ALICE.ml__script_executor__<uniqueID>','py')
        """
        try:
            tempdir = GarbageCollector._get_temp_dir_name()
            script_alias = tdmlutil.utils.UtilFuncs._teradata_unquote_arg(
                tdmlutil.utils.UtilFuncs._extract_table_name(db_object), quote='"')

            # Currently assumed that the file name will be similar to '<UIF_ID>.py'.
            file_name = os.path.join(tempdir,
                                     '{}.{}'.format(script_alias, file_extension))
            GarbageCollector._delete_local_file(file_name)
        except Exception as e:
            raise

    @staticmethod
    def _delete_object_entry(object_to_delete,
                             object_type=TeradataConstants.TERADATA_TABLE,
                             remove_entry_from_gc_list=False):
        """
        DESCRIPTION:
            Deletes an entry of table/view/script from persisted file.
            This makes sure that the object is not garbage collected.

        PARAMETERS:
            object_to_delete:
                Required Argument.
                Specifies the name of the table/view/script to be deleted.
                Types: str

            object_type:
                Optional Argument.
                Specifies the type of the object (table/view/script) to be deleted.
                Default Value: TeradataConstants.TERADATA_TABLE
                Types: TeradataConstants

            remove_entry_from_gc_list:
                Optional Argument.
                Specifies whether to delete the entry from one of the following:
                * __gc_tables - list of tables created
                * __gc_views - list of views created
                * __gc_scripts - list of scripts installed
                When set to True, the entry is removed from the appropriate list.
                This argument comes in handy for the GC validation to
                make sure that all intended tables/views/scripts are dropped by GC.
                Default Value: False
                Types: bool

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector._delete_table_view_entry(object_to_delete = 'temp.temp_table1')
        """
        try:
            tempfilename = GarbageCollector.__make_temp_file_name()
            if not os.path.isfile(tempfilename):
                return True
            with open(tempfilename, 'r+') as fgc:
                output = fgc.readlines()
                fgc.seek(0)
                for db_object_entry in output:
                    record_parts = db_object_entry.strip().split(GarbageCollector.__contentseperator)
                    contentpid = int(record_parts[1].strip())
                    db_object_type = int(record_parts[2].strip())
                    db_object = record_parts[3].strip()

                    # Avoid substring matches by comparing object names in full.
                    # Also make sure to check for the pid.
                    if not (object_to_delete == db_object
                            and object_type.value == db_object_type
                            and int(os.getpid()) == contentpid):
                        fgc.write(db_object_entry)
                    else:
                        if remove_entry_from_gc_list and configure._validate_gc:
                            # Delete the entry from gc lists if required.
                            GarbageCollector.__delete_object_from_gc_list(object_to_delete,
                                                                          object_type)

                        # If object is a script, also delete the local copy of the file.
                        if object_type == TeradataConstants.TERADATA_SCRIPT:
                            GarbageCollector.__delete_gc_tempdir_local_file(db_object,
                                                                            "py")
                        elif object_type == TeradataConstants.TERADATA_LOCAL_SCRIPT:
                            GarbageCollector.__delete_gc_tempdir_local_file(db_object, "py")
                fgc.truncate()
        except Exception as e:
            raise
        finally:
            if fgc and fgc is not None:
                fgc.close()

    @staticmethod
    def __delete_object_from_gc_list(object_name, object_type=TeradataConstants.TERADATA_TABLE):
        """
        DESCRIPTION:
            Deletes an entry of table/view/script from gc list when configure option
            '_validate_gc' is set to 'True'.

        PARAMETERS:
            object_name:
                Required Argument.
                Specifies the name of the table/view/script to be deleted.
                Types: str

            object_type:
                Optional Argument.
                Specifies the type of the object (table/view/script) to be deleted.
                Default value: TeradataConstants.TERADATA_TABLE
                Types: TeradataConstant

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector._delete_object_from_gc_list(object_name = 'temp.temp_table1')
            GarbageCollector._delete_object_from_gc_list(object_name = 'temp.temp_view1',
                                                         object_type = TeradataConstants.TERADATA_VIEW)
            GarbageCollector._delete_object_from_gc_list(object_name = 'temp.temp_script1',
                                                         object_type = TeradataConstants.TERADATA_SCRIPT)
            GarbageCollector._delete_object_from_gc_list(object_name = 'temp.temp_script1',
                                                         object_type =
                                                         TeradataConstants.TERADATA_LOCAL_SCRIPT)
            GarbageCollector._delete_object_from_gc_list(object_name = '7efhghsghg',
                                                         object_type =
                                                         TeradataConstants.CONTAINER)
        """
        if configure._validate_gc:
            if TeradataConstants.TERADATA_TABLE == object_type:
                GarbageCollector.__gc_tables.remove(object_name)
            elif TeradataConstants.TERADATA_VIEW == object_type:
                GarbageCollector.__gc_views.remove(object_name)
            elif TeradataConstants.CONTAINER == object_type:
                GarbageCollector.__gc_container.remove(object_name)
            else:
                GarbageCollector.__gc_scripts.remove(object_name)

    @staticmethod
    def _delete_local_file(file_path):
        """
        DESCRIPTION:
            Function to delete the specified local file.

        PARAMETERS:
            file_path:
                Required Argument.
                Specifies the path of the file to be deleted.
                Types: str

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector._delete_local_file(file_path = '.teradataml/ml__1603874893436650.py')
        """
        try:
            os.remove(file_path)
        except:
            pass

    @staticmethod
    def __delete_docker_sandbox_env(sandbox_env_object):
        """
        DESCRIPTION:
            Function to delete the specified sandbox container.

        PARAMETERS:
            sandbox_env_object:
                Required Argument.
                Specifies a string containing container id or '|' separated container id and image name
                that needs to be cleaned up.
                Types: str

        RETURNS:
            None.

        RAISES:
            docker.errors.NotFound, docker.errors.APIError.

        EXAMPLES:
            GarbageCollector.__delete_docker_sandbox_env(sandbox_env_object = '7efjglkfl'|'stoimage1').
            GarbageCollector.__delete_docker_sandbox_env(sandbox_env_object = '7efjglkfl').
        """
        try:
            import docker
            client = docker.APIClient()
            # Splitting it with '|' as most often image names doesn't contain it.
            res = sandbox_env_object.split('|')
            # Stop and remove the container using the container id, i.e., the first element in 'res'.
            client.stop(res[0])
            client.remove_container(res[0])
            if len(res) == 2:
                # Remove the image using the using image name, i.e., the second element in 'res'.
                client.remove_image(res[1])
        except docker.errors.NotFound as err1:
            raise err1
        except docker.errors.APIError as err2:
            raise err2
        except Exception as err3:
            raise err3
        finally:
            # Reset configuration parameters "sandbox_container_id" and
            # "_container_started_by_teradataml" after raising exceptions if any.
            configure._container_started_by_teradataml = None
            if configure.sandbox_container_id == res[0]:
                configure.sandbox_container_id = None

    @staticmethod
    def _cleanup_garbage_collector():
        """
        DESCRIPTION:
            Drops the tables/views/scripts/container that are garbage collected.

        PARAMETERS:
            None.

        RETURNS:
            True, when successful.

        RAISES:
            None.

        EXAMPLES:
            GarbageCollector._cleanup_garbage_collector()
        """
        try:
            td_connection = tdmlctx.context.get_connection()
            tempfilename = GarbageCollector.__make_temp_file_name()
            if not os.path.isfile(tempfilename):
                return True
            with open(tempfilename, 'r+') as fgc:
                content = fgc.readlines()

            for contentrecord in content:
                contentrecord = contentrecord.strip()

                if (td_connection is not None) and (len(contentrecord) > 0):
                    try:
                        recordparts = contentrecord.split(GarbageCollector.__contentseperator)
                        version = recordparts[0]
                        contentpid = int(recordparts[1].strip())
                        # Check and garbage collect even currrent running process at exit.
                        # Check if contentpid is not of current process as well as any
                        # currently running process in the system
                        proceed_to_cleanup = False
                        if contentpid != int(os.getpid()):
                            if not psutil.pid_exists(contentpid):
                                proceed_to_cleanup = True
                        else:
                            proceed_to_cleanup = True
                        if proceed_to_cleanup == True:
                            object_type = int(recordparts[2].strip())
                            database_object = recordparts[3].strip()

                            # Create the TeradataConstant to use with __delete_object_from_gc_list().
                            object_type_enum = TeradataConstants.TERADATA_SCRIPT
                            if object_type == TeradataConstants.TERADATA_TABLE.value:
                                object_type_enum = TeradataConstants.TERADATA_TABLE
                            elif object_type == TeradataConstants.TERADATA_VIEW.value:
                                object_type_enum = TeradataConstants.TERADATA_VIEW
                            elif object_type == TeradataConstants.TERADATA_LOCAL_SCRIPT.value:
                                object_type_enum = TeradataConstants.TERADATA_LOCAL_SCRIPT
                            elif object_type == TeradataConstants.CONTAINER.value:
                                object_type_enum = TeradataConstants.CONTAINER
                            try:
                                # Drop the table/view/script/container based on database object type retrieved from the collector file.
                                # # Drop table.
                                if TeradataConstants.TERADATA_TABLE.value == object_type:
                                    tdmlutil.utils.UtilFuncs._drop_table(database_object,
                                                                         check_table_exist=False)
                                # # Drop view.
                                elif TeradataConstants.TERADATA_VIEW.value == object_type:
                                    tdmlutil.utils.UtilFuncs._drop_view(database_object,
                                                                        check_view_exist=False)

                                # Drop script executor python file generated while
                                # running Script
                                elif TeradataConstants.TERADATA_LOCAL_SCRIPT.value == object_type:
                                    GarbageCollector.__delete_gc_tempdir_local_file(database_object, "py")

                                # Remove sandbox container.
                                elif TeradataConstants.CONTAINER.value == object_type:
                                    GarbageCollector.__delete_docker_sandbox_env(database_object)
                                # # Drop script.
                                else:
                                    tdmlutil.utils.UtilFuncs._delete_script(database_object,
                                                                            check_script_exist=False)
                                    # Delete the script locally
                                    GarbageCollector.__delete_gc_tempdir_local_file(database_object, "py")

                                # Finally, delete the entry from gc lists if required.
                                GarbageCollector.__delete_object_from_gc_list(database_object,
                                                                              object_type_enum)

                                # Remove the entry for a table/view from GC, after it has been dropped.
                                GarbageCollector.__deleterow(contentrecord)
                            except OperationalError as operr:
                                # Remove the entry for a table/view/script even after drop has failed,
                                # if that object does not exist.
                                # Also added additional check for error when the database containing
                                # the object doesn't exist anymore.
                                if "[Teradata Database] [Error 3802] Database" in str(operr) or \
                                        "[Teradata Database] [Error 3807] Object" in str(operr) or \
                                        "[Teradata Database] [Error 9852] The file" in str(operr):
                                    GarbageCollector.__deleterow(contentrecord)
                                    # Delete entry from gc lists of required.
                                    GarbageCollector.__delete_object_from_gc_list(database_object,
                                                                                  object_type_enum)
                            except FileNotFoundError:
                                # This will occur only when the item being deleted is a file,
                                # and it's local copy is not found.
                                GarbageCollector.__deleterow(contentrecord)
                                GarbageCollector.__gc_scripts.remove(database_object)
                    except Exception:
                        pass
                        # logger.error(Messages.get_message(MessageCodes.TDMLDF_DELETE_GARBAGE_COLLECTOR) + str(err))
        except Exception as e:
            logger.error(Messages.get_message(MessageCodes.TDMLDF_DELETE_GARBAGE_COLLECTOR) + str(e))
        finally:
            if configure._validate_gc:
                GarbageCollector.__validate_gc()
        return True