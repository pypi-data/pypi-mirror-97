import os
import docker
import warnings
from teradataml.common.constants import TeradataConstants
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.garbagecollector import GarbageCollector
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.utils.validators import _Validators
from teradataml.options.configure import configure

def setup_sandbox_env(sandbox_image_location=None, sandbox_image_name=None,
                      container_id=None, timeout=5000):
    """
    DESCRIPTION:
        Function to either load sandbox image and start a new docker container by passing
        the "sandbox_image_location" and "sandbox_image_name" or
        start an existing container using the argument "container_id".
        Note:
            1. Teradata recommends to run this function once before running
               test_script() method of Script.
            2. Sandbox image loading on user's system is skipped if the image is already
               loaded.
            3. There can be only one container started from within teradataml at any given
               point.
            4. At the end of the session image loaded / container started by the function
               will be cleaned up.
            5. If the user wishes to manually cleanup image / container started by the
               function, they can use cleanup_sandbox_env().
            6. User should be careful while providing "sandbox_image_location" and
               "sandbox_image_name". If an incorrect "sandbox_image_name" is provided that
               does not match with the name / tag of the image to be loaded then:
                   a. The image will not be loaded. User should re-run the function with
                      correct "sandbox_image_name".
                   b. If the user's system already has an image with the image name / tag
                      same as the image specified in "sandbox_image_location" then the new image
                      will be loaded and it might replace the old image.

    PARAMETERS:
        sandbox_image_location:
            Optional Argument.
            Specifies the path to the sandbox image on user's system.
            Types: str
            Notes:
                1. For location to download sandbox image refer teradataml User Guide.
                2. After loading the image, a container will be created and started.
                3. "sandbox_image_location" and "sandbox_image_name" must be
                   specified together.

        sandbox_image_name:
            Optional Argument.
            Specifies the name of the sandbox image that was used for generating the image.
            This will be used for starting a container.
            Types: str
            Note:
                1. "sandbox_image_location" and "sandbox_image_name" must be
                   specified together.
                2. If the "sandbox_image_name" is incorrect then the image will not be
                   loaded.

        container_id:
            Optional Argument. Required if "sandbox_image_location" and
            "sandbox_image_name" are not specified.
            Specifies id of an existing docker container.
            Types: str
            Note:
                User should be careful while specifying this argument.
                If this argument is specified to start the container then this container
                will be cleaned up at the end of the session.

        timeout:
            Optional Argument.
            Specifies timeout value for docker API calls. This is particularly useful
            while loading large sandbox images. User should increase the "timeout" value
            if image loading fails because of timeout.
            Default Value: 5000
            Types: int

    RETURNS:
        None.

    RAISES:
        Warning, docker.errors.APIError, docker.errors.NotFound, TeradataMlException,
        Exception.

    EXAMPLES:
        >>> from teradataml.table_operators.sandbox_container_util import setup_sandbox_env
        # Example 1: Load the image from the location specified in "sandbox_image_location"
        # argument and start a container.
        # This is useful when the user wants to setup sandbox environment with a new image.
        >>> setup_sandbox_env(sandbox_image_location='/tmp/stosandbox.tar.gz',
                              sandbox_image_name='stosandbox:1.0')
            Loading image from /tmp/stosandbox.tar.gz. It may take few minutes.
            Image loaded successfully.
            Container c1dd4d4b722cc54b643ab2bdc57540a3a3e6db98c299defc672227de97d2c345
            started successfully.

        # Example 2: Start an existing container specified in "container_id" argument.
        # This is useful when the user wants to run user script in an existing container.
        >>> setup_sandbox_env(container_id='3fadb1e8bac3')
            Container 3fadb1e8bac3 started successfully.
    """
    awu_matrix_test = []
    awu_matrix_test.append((["sandbox_image_location", sandbox_image_location, True,
                             (str), True]))
    awu_matrix_test.append((["sandbox_image_name", sandbox_image_name, True,
                             (str), True]))
    awu_matrix_test.append((["container_id", container_id, True, (str), True]))
    awu_matrix_test.append((["timeout", timeout, True, (int), True]))

    _Validators._validate_function_arguments(awu_matrix_test)
    _Validators._validate_positive_int(timeout, "timeout")

    if all([sandbox_image_location is None, sandbox_image_name is None, container_id is None])\
            or (any([sandbox_image_location, sandbox_image_name]) and container_id):
        message = Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                       "sandbox_image_location and sandbox_image_name",
                                       "container_id")
        raise TeradataMlException(message, MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

    if configure._container_started_by_teradataml:
        message = Messages.get_message(MessageCodes.CONTAINER_STARTED_BY_TERADATAML_EXISTS)
        raise TeradataMlException(message,
                                  MessageCodes.CONTAINER_STARTED_BY_TERADATAML_EXISTS)

    if sandbox_image_location and sandbox_image_name is None:
            message = Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                           "sandbox_image_name", "sandbox_image_location")
            raise TeradataMlException(message, MessageCodes.DEPENDENT_ARG_MISSING)

    if sandbox_image_name and sandbox_image_location is None:
            message = Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                           "sandbox_image_location", "sandbox_image_name")
            raise TeradataMlException(message, MessageCodes.DEPENDENT_ARG_MISSING)

    import docker
    client = docker.APIClient(timeout=timeout)

    # Check if the image with the tag is present then only start the container.
    # Give a message to the user that image with <tag> is already present,
    # starting only the container. Container started---container_id.
    # If the image is not present then load the image.

    # Variable for image name/tag returned by __load_docker_image().
    image_tag = None
    if sandbox_image_location is not None:
        list_image = client.images(name=sandbox_image_name)
        if not list_image:
            # Load sandbox image if the image is not present.
            image_tag = __load_docker_image(sandbox_image_location, timeout)
        else:
            # Skip loading image if it is already present.
            warnings.warn(Messages.get_message(MessageCodes.SANDBOX_SKIP_IMAGE_LOAD).
                          format(sandbox_image_name))

        # This check is required in case the user wants to start a container from an
        # existing image.
        if sandbox_image_name:
            # Check if sandbox image exists on the system.
            if not client.images(sandbox_image_name, quiet=True):
                try:
                    # Remove image if incorrect "sandbox_image_name" is provided by the
                    # user.
                    if image_tag is not None:
                        __remove_docker_image(client, image_tag)
                finally:
                    message = \
                        Messages.get_message(
                            MessageCodes.SANDBOX_CONTAINER_CAN_NOT_BE_STARTED,
                            "sandbox_image_name")
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_CONTAINER_CAN_NOT_BE_STARTED)
            else:
                # Start container if "sandbox_image_name" matches with the loaded image.
                try:
                    print("Starting a container for {} image.".format(sandbox_image_name))
                    # Start container.
                    client, container, container_id = \
                        __start_docker_container(sandbox_image_name=sandbox_image_name,
                                                 client=client)
                    print("Container {} started successfully.".format(container_id))

                    configure._container_started_by_teradataml = container_id
                    configure.sandbox_container_id = container_id
                    if image_tag is not None:
                        # Add container_id|sandbox_image_name to GC
                        gc_entry = "{0}|{1}".format(container_id, sandbox_image_name)
                        # Set configuration parameter _container_started_by_teradataml to
                        # actual container_id and image name if image is loaded by
                        # teradataml prior to starting the container.
                        configure._container_started_by_teradataml = gc_entry
                    else:
                        # Add only container_id to GC when image is not loaded from
                        # teradataml.
                        gc_entry = container_id
                    GarbageCollector. \
                        _add_to_garbagecollector(gc_entry, TeradataConstants.CONTAINER)

                except Exception as err:
                    raise err

    # Start an existing container.
    elif container_id is not None:
        try:
            container_status=client.inspect_container(container_id)['State']['Status']
            client, container, container_id = \
                __start_docker_container(client=client, container_id=container_id,
                                         container_status=container_status)
            # Check status after starting the container.
            container_status = client.inspect_container(container_id)['State']['Status']
            if container_status == 'running':
                print("Container {} started successfully.".format(container_id))
                # Add container_id to GC
                GarbageCollector._add_to_garbagecollector(container_id,
                                                          TeradataConstants.CONTAINER)

                # Set configuration parameters sandbox_container_id and
                # _container_started_by_teradataml to actual container_id to indicate that
                # a container exists.
                configure.sandbox_container_id = container_id
                configure._container_started_by_teradataml = container_id

        except Exception as err:
            raise err

def __start_docker_container(sandbox_image_name=None, client=None, container_status=None,
                             container_id=None):
    """
    DESCRIPTION:
        Function to start a sandbox container.

    PARAMETERS:
        sandbox_image_name:
            Required Argument.
            Specifies the name of the sandbox image.
            Types: str

        client:
            Required Argument.
            Specifies the object of class 'docker.api.client.APIClient' for communicating
            with Docker Engine API.
            Types: Object of class 'docker.api.client.APIClient'

        container_status:
            Optional Argument.
            Specifies the status of container specified in "container_id" argument.
            Types: str

        container_id:
            Optional Argument.
            Specifies the id of an existing docker container.
            Types: str

    RETURNS:
        Client required to communicate to the docker daemon, container object and
        container id.

    RAISES:
        docker.errors.APIError, docker.errors.NotFound, Exception.

    EXAMPLES:
        >>> __start_docker_container(sandbox_image_name='stosandbox:1.0', client=client,
                                     container_status='paused', container_id='7efsdjkjk')
    """
    # Create and start container.
    if sandbox_image_name is not None:
        try:
            # Create container.
            container = client.create_container(sandbox_image_name,
                                                stdin_open=True,
                                                tty=True,
                                                detach=True)
            # Find container id.
            container_id = container.get('Id')
            # Start container.
            client.start(container_id)
            return client, container, container_id
        except Exception as err:
            raise err
    else:
        # Start an existing container.
        if container_status and container_id:
            try:
                if container_status == 'paused':
                    client.unpause(container_id)
                elif container_status == 'exited':
                    client.start(container_id)
                container = client.containers(filters={"id":container_id})
                return client, container, container_id
            except Exception as err:
                raise err

def __load_docker_image(sandbox_image_location, timeout):
    """
    DESCRIPTION:
        Function to load a docker image.

    PARAMETERS:
        sandbox_image_location
            Required Argument.
            Specifies the path to sandbox image on user's system.
            Types: str

        timeout:
            Required Argument.
            Specifies timeout value for docker API calls. This is particularly useful
            while loading large sandbox images. User should increase the "timeout" value
            if image loading fails because of timeout.
            Types: int

    RETURNS:
        str (image tag).

    RAISES:
        docker.errors.APIError, Exception.

    EXAMPLES:
        >>> __load_docker_image(sandbox_image_location='/tmp/stosandbox.tar.gz',
                                timeout=3000)

    """
    # Check if file exists.
    _Validators._validate_file_exists(sandbox_image_location)

    client = docker.from_env(timeout=timeout)

    # Load image from user provided location.
    try:
        msg = "Loading image from {0}. It may take few minutes."
        print(msg.format(sandbox_image_location))
        with open(sandbox_image_location, 'rb') as f:
            image_obj = client.images.load(f)
            # Get  the image tag of loaded image.
            image_tag = image_obj.pop().tags[0]
        print("Image loaded successfully.")
        return image_tag
    except Exception as err:
        raise err

def __remove_docker_image(client, sandbox_image_name):
    """
        DESCRIPTION:
            Function to remove a docker image.

        PARAMETERS:
            client:
                Required Argument.
                Specifies the object of class 'docker.api.client.APIClient' for communicating
                with Docker Engine API.
                Types: Object of class 'docker.api.client.APIClient'

            sandbox_image_name
                Required Argument.
                Specifies the name of the sandbox image to be removed.
                Types: str

        RETURNS:
            None.

        RAISES:
            Exception.

        EXAMPLES:
            >>> __remove_docker_image(client=client,
                                    sandbox_image_name='stosandbox:1.0')

        """
    try:
        # Remove sandbox image.
        client.remove_image(sandbox_image_name)
    except Exception as err:
        raise err

def cleanup_sandbox_env():
    """
    DESCRIPTION:
        Function to clean up sandbox environment setup by teradataml. Function will
        remove the image and/or container used to setup the sandbox environment
        using setup_sandbox_env().

    PARAMETERS:
        None.

    RETURNS:
        None.

    RAISES:
        None.

    EXAMPLES:
        >>> from teradataml.table_operators.sandbox_container_util import *
        # Example 1: Setup sandbox environment using the setup_sandbox_env()
        #            and clean it up using cleanup_sandbox_env() function.
        #            This cleans up image and container created by
        #            setup_sandbox_env().
        >>> setup_sandbox_env(sandbox_image_location='/tmp/stosandbox.tar.gz',
                              sandbox_image_name='stosandbox:1.0')
            Loading image from /tmp/stosandbox.tar.gz. It may take few minutes.
            Image loaded successfully.
            Container c1dd4d4b722cc54b643ab2bdc57540a3a3e6db98c299defc672227de97d2c345
            started successfully.
        >>> cleanup_sandbox_env()
            Removed container: c1dd4d4b722cc54b643ab2bdc57540a3a3e6db98c299defc672227de97d2c345
            Removed image: stosandbox:1.0

        # Example 2: Set configure.sandbox_container_id manually then run
        #            setup_sandbox_env() and clean it up using cleanup_sandbox_env()
        #            function. This only cleans up image and container created
        #            by setup_sandbox_env() and does not cleanup the container
        #            specified in 'configure.sandbox_container_id'.
        >>> configure.sandbox_container_id = 'container_id_set_by_user'
        >>> setup_sandbox_env(sandbox_image_location='/tmp/stosandbox.tar.gz',
                              sandbox_image_name='stosandbox:1.0')
            Loading image from /tmp/stosandbox.tar.gz. It may take few minutes.
            Image loaded successfully.
            Container c1dd4d4b722cc54b643ab2bdc57540a3a3e6db98c299defc672227de97d2c345
            started successfully.
        >>> cleanup_sandbox_env()
            Removed container: c1dd4d4b722cc54b643ab2bdc57540a3a3e6db98c299defc672227de97d2c345
            Removed image: stosandbox:1.0
    """

    sandbox_env_object = configure._container_started_by_teradataml
    if not sandbox_env_object:
        print("No container started using \"setup_sandbox_env()\". Nothing to clean up.")
    else:
        GarbageCollector._GarbageCollector__delete_docker_sandbox_env(sandbox_env_object)
        GarbageCollector._GarbageCollector__delete_object_from_gc_list(sandbox_env_object,
                                                  TeradataConstants.CONTAINER)
        container_record = str(GarbageCollector._GarbageCollector__version) + "," + str(os.getpid()) + "," \
                   + str(TeradataConstants.CONTAINER.value) + "," + sandbox_env_object
        # Remove the entry for container id and/or image name from GC,
        # after it has been deleted.
        GarbageCollector._GarbageCollector__deleterow(container_record)
        res = sandbox_env_object.split("|")
        print("Removed container: {0}\n".format(res[0]))
        if len(res) == 2:
            client = docker.APIClient()
            image_present = client.images(name=res[1])
            if not image_present:
                print("Removed image: {0}".format(res[1]))

def copy_files_from_container(files_to_copy, container_id=None):
    """
    DESCRIPTION:
        Function to copy file(s) from container specified by "container_id" or container
        indicated by 'configure.sandbox_container_id' to local filesystem.
        Notes:
            1. Files will be copied to a directory in .teradataml directory under
               user's home directory.
            2. User is responsible for cleaning up this directory.

    PARAMETERS:
        files_to_copy:
            Required Argument.
            Specifies the filename(s) to be copied from container.
            Type: str OR list of Strings (str)
            Note:
                Files should be in "/home/tdatuser" inside the container.

        container_id:
            Optional Argument.
            Specifies the container from which files are to be copied.
            If not specified, then files are copied from container in
            'configure.sandbox_container_id'.
            Types: str

    RETURNS:
        None.

    RAISES:
        docker.errors.APIError, TeradataMlException, Exception.

    EXAMPLES:
        # Copy files from "/home/tdatuser" inside container started by teradataml to
        local host.
        >>> from teradataml.table_operators.sandbox_container_util
        import copy_files_from_container

        >>> copy_files_from_container(files_to_copy="file1.txt")
        Files copied to: /<user's home directory>/.teradataml/files_from_container_210110_193943

        >>> copy_files_from_container(files_to_copy=["output/file1.txt", "file2.txt"])
        Files copied to: /<user's home directory>/.teradataml/files_from_container_210110_193943

    """
    awu_matrix_copy=[]
    awu_matrix_copy.append((["files_to_copy", files_to_copy, False, (str, list), True]))
    awu_matrix_copy.append((["container_id", container_id, True, (str), True]))

    # Validate missing arguments.
    _Validators._validate_missing_required_arguments(awu_matrix_copy)

    # Validate argument types.
    _Validators._validate_function_arguments(awu_matrix_copy)

    if files_to_copy is not None:
        if isinstance(files_to_copy, str):
            files_to_copy = [files_to_copy]

        if len(files_to_copy) == 0 \
                or any(file in [None, "None", ""] for file in files_to_copy):
            raise ValueError(
                Messages.get_message(MessageCodes.LIST_SELECT_NONE_OR_EMPTY,
                                     'files_to_copy'))

    import docker
    client = docker.APIClient()
    # User must either provide container_id or make sure configure.sandbox_container_id
    # is set.
    if all([container_id is None, configure.sandbox_container_id is None]):
        message = Messages.get_message(MessageCodes.SPECIFY_AT_LEAST_ONE_ARG,
                                      "container_id", "set configure.sandbox_container_id")
        raise TeradataMlException(message, MessageCodes.SPECIFY_AT_LEAST_ONE_ARG)

    # If container_id is None then copy files from container indicated by
    # configure.sandbox_container_id.
    if container_id is None:
        container_id = configure.sandbox_container_id
    # Check status of container.
    container_status = client.inspect_container(container_id)['State']['Status']
    # Copy files if container is running.
    if container_status == 'running':
        # Create a directory under .teradataml.
        import datetime, os, shutil
        base_destination = GarbageCollector._get_temp_dir_name()
        basename = "files_from_container"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        dest_dir = "{}_{}".format(basename, suffix)
        destination = os.path.join(base_destination, dest_dir)
        try:
            os.makedirs(os.path.join(base_destination, basename))
        except OSError:
            pass

        from io import BytesIO
        import tarfile

        # Copy files from container.
        try:
            for fname in files_to_copy:
                cmd = client.exec_create(container_id, 'ls {}'.format(fname))
                cmd_output = client.exec_start(cmd, demux=True)

                # Inspect the output for success or failure.
                inspect_out = client.exec_inspect(cmd)

                # Extract the exit code.
                exit_code = inspect_out['ExitCode']
                executor_error = ""

                # Check the exit code for success.
                if exit_code == 0:
                    file_list = cmd_output[0].decode().split()
                    for file in file_list:
                        strm, status = client.get_archive(container_id, "/home/tdatuser/{}".format(file))
                        data_obj = BytesIO(b"".join(b for b in strm))
                        tar = tarfile.open(fileobj=data_obj, mode='r')
                        try:
                            tar.extract(member=file, path=destination)
                        finally:
                            data_obj.close()
                            tar.close()
                elif exit_code == 2:
                    if cmd_output[1] is not None:
                        executor_error = cmd_output[1].decode()
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_CONTAINER_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_CONTAINER_ERROR)

            print("Files copied to: {}".format(destination))
        except docker.errors.APIError as exp:
            raise exp
        except TeradataMlException:
            raise
        except Exception as exp:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.SANDBOX_CONTAINER_ERROR).format(str(exp)),
                MessageCodes.SANDBOX_CONTAINER_ERROR)
    else:
        raise TeradataMlException(
            Messages.get_message(MessageCodes.SANDBOX_CONTAINER_NOT_RUNNING).
                format(container_id), MessageCodes.SANDBOX_CONTAINER_NOT_RUNNING)
