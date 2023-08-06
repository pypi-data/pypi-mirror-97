"""
cdf_helpers.py

High level functionality built on top of Cognite's Python SDK

Most functions require the global cdf client to be set up before using them.
"""
import time
import sys
import os 
import json
from shutil import make_archive, unpack_archive

from cognite.client.exceptions import CogniteNotFoundError, CogniteAPIError

from akerbp.mlops.core import logger, config

logging=logger.get_logger(name='mlops_cdf')

global_client = {}
api_keys=config.api_keys

env_vars = {k.upper():str(v) for k,v in config.envs_dic.items() if v}
env_vars.update({'PLATFORM':'cdf'})
try:
    env_vars.pop('GOOGLE_PROJECT_ID')
except KeyError:
    pass


def set_up_cdf_client(context='run'):
    """
    Set up the global client used by most helpers. This needs to be called
    before using any helper. 

    Input:
      - context: string either 'run' (access to data and functions) or 'deploy'
        (access to 'functions' also).
    """
    if context == 'run':
        api_key_labels=["data", "files"]
    elif context == 'deploy':
        api_key_labels=["data", "files", "functions"]
    else:
        raise ValueError("Context should be either 'run' or 'deploy'")

    for k in api_key_labels:
        if k not in global_client:
            global_client[k] = get_client(api_keys[k], k)
        
    logging.info("CDF client was set up correctly")


def get_client(api_key, api_key_label=None):
    """
    Create a CDF client with a given api key
    """
    if api_key_label == 'functions':
        from cognite.experimental import CogniteClient
        logging.warning("Imported CogniteClient from cognite.experimental")
    else:
        from cognite.client import CogniteClient
    
    client = CogniteClient(
        api_key=api_key,
        project='akbp-subsurface',
        client_name="mlops-client",
        base_url='https://api.cognitedata.com'
    )
    assert client.login.status().logged_in
    logging.debug(f"{client.version=}")
    return client


def create_function(
    function_name, 
    folder, 
    handler_path,  
    description='',
    owner='',
    secrets={}
):
    """
    Create a Cognite function from a folder. Any existing function with the same
    name is deleted first.

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - secrets: api keys or similar that should be passed to the function
    """
    client = global_client["functions"]
    try:
        client.functions.delete(external_id=function_name)
        logging.debug(f"Deleted function {function_name}")
    except CogniteNotFoundError:
        pass
    
    function = client.functions.create( 
        name=function_name, 
        folder=folder, 
        function_path=handler_path,
        external_id=function_name,
        description=description,
        owner=owner,
        secrets=secrets,
        env_vars=env_vars
    )
    logging.debug(
        f"Created {function_name}: {folder=}, {handler_path=}, {env_vars=}"
    )

    return function


def deploy_function(
    function_name,
    folder='.',
    handler_path='handler.py',
    secrets=api_keys,
    info={'description':'', 'owner':''}
):
    """
    Deploys a Cognite function from a folder. The function is created first,
    and then it waits until the function status is ready or failed. If it fails,
    it will try again `max_error` times

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - secrets: api keys or similar that should be passed to the function
    """
    max_errors = 3

    for trial in range(max_errors):
        function = create_function(
            function_name, 
            folder, 
            handler_path, 
            info['description'],
            info['owner'],
            secrets
        )
        status = wait_function_status(function)
        logging.debug(f"Function status is {status}")
        if function.status == 'Ready':
            break
        if function.status == 'Failed' and trial < max_errors-1:
            logging.warning(f"Function failed: {function.id=}")
            logging.debug(f"Error was: {function.error=}")
            logging.debug(f"Try to create function again")
        else:
            raise Exception(f"Function deployment error: {function.error=}")


def call_function(function_name, data):
    """
    Call a function deployed in CDF
    """
    client = global_client["functions"]
    function = client.functions.retrieve(external_id=function_name)
    logging.debug(f"Retrieved function {function_name}")
    call = function.call(data)
    logging.debug(f"Called function (call_id={call.id})")
    response = call.get_response()
    logging.debug(f"Called function: {response=}")
    return response


def test_function(function_name, data):
    """
    Call a function with data and verify that the response's 
    status is 'ok'
    """
    logging.debug(f"Test function {function_name}")
    output = call_function(function_name, data)
    assert output['status'] == 'ok'
    logging.info(f"Test call was successful :)")


def wait_function_status(function, status=["Ready", "Failed"]):
    """
    Wait until function status is in `status`
    By default it waits for Ready or Failed, which is useful when deploying.
    It implements some control logic, since polling status can fail.
    """
    polling_wait_seconds_base = 10
    polling_wait_seconds = polling_wait_seconds_base
    max_api_errors_base = 5
    max_api_errors = max_api_errors_base
    
    logging.debug(f"Wait for function to be ready or to fail")
    while not (function.status in status):
        try:
            time.sleep(polling_wait_seconds)
            function.update()
            logging.debug(f"{function.status=}")
            polling_wait_seconds = polling_wait_seconds_base
            max_api_errors = max_api_errors_base
        except CogniteAPIError as e:
            max_api_errors -= 1
            logging.warning(f"Could not update function status, will try again")
            polling_wait_seconds *= 1.2          
            if not max_api_errors:
                logging.error(f"Could not update function status.")
                raise e

    return function.status


def download_file(id, path):
    """
    Download file from Cognite
    
    Params:
        - id: dictionary with id type (either "id" or "external_id") as key
        - path: path of local file to write
    """
    client = global_client["files"]
    
    logging.debug(f"Download file with {id=} to {path}")
    client.files.download_to_path(path, **id)


def upload_file(
    external_id, 
    path, 
    metadata={}, 
    directory='/',
    overwrite=True):
    """
    Upload file to Cognite
    
    Params:
        - external_id: external id
        - path: path of local file to upload
        - metadata: dictionary with file metadata
        - overwrite: what to do when the external_id exists already
    """
    client = global_client["files"]
    
    metadata = {k:v if isinstance(v, str) else json.dumps(v) 
        for k,v in metadata.items()}

    logging.debug(f"Upload file {path} with {external_id=} and {metadata=}")
    file_info = client.files.upload(
        path, 
        external_id, 
        metadata=metadata, 
        directory=directory, 
        overwrite=overwrite
    )
    logging.info(f"Uploaded file: {file_info=}")
    return file_info


def upload_folder(
    external_id, 
    path, 
    metadata={}, 
    overwrite=False, 
    target_folder='/'
):
    """
    Upload folder content to Cognite. It compresses the folder and uploads it.
    
    Params:
        - external_id: external id (should be unique in the CDF project)
        - path: (Path) path of local folder where content is stored
        - metadata: dictionary with file metadata
        - target_folder: path where compressed file should be stored
        - overwrite: if overwrite==False and `external_id` exists => exception
    """
    base_name = path / 'archive'
    archive_name = make_archive(base_name, 'gztar', path)
    file_info = upload_file(
        external_id, 
        archive_name, 
        metadata=metadata,
        overwrite=overwrite,
        directory=target_folder
    )
    os.remove(archive_name)
    logging.info(f"Folder content uploaded: {file_info=}")
    return file_info


def download_folder(external_id, path):
    """
    Download content from Cognite to a folder. It is assumed to have been
    uploaded using `upload_folder()`, so it downloads a file and decompresses
    it.

    Params:
    - external_id: external id
    - path: (Path) path of local folder where content will be stored
    """
    base_name = path / 'archive.tar.gz'
    download_file(dict(external_id=external_id), base_name)
    unpack_archive(base_name, base_name.parent)
    os.remove(base_name)
    logging.info(f"Model file/s downloaded to {path}")


def log_system_info():
    """
    Can be called from a handler to log CDF environment information
    """
    logging.debug(f"Python version:\n{os.popen('python --version').read()}")
    logging.debug(f"Python path:\n{sys.path}")
    logging.debug(f"Current working directory:\n{os.getcwd()}")
    logging.debug(f"Content:\n{os.popen('ls -la *').read()}")
    logging.debug(f"Packages:\n{os.popen('pip freeze').read()}")


def count_files(
    external_id_prefix, 
    directory_prefix='/'
):
    """
    How many files have the given `external_id_prefix` and `directory_prefix`
    This can be used for file versioning.

    Returns an integer (>=0)
    """
    client = global_client["files"]
    result = client.files.aggregate(filter={
        "external_id_prefix": external_id_prefix, 
        "directory_prefix": directory_prefix
    })
    return result[0]["count"]


def query_file_versions(
    directory_prefix, 
    external_id_prefix, 
    metadata={}, 
    uploaded=True):
    """
    Find all file versions that match a query. 

    Input:
        -directory_prefix
        -external_id_prefix
        -metadata: query to the metadata (dictionary)
    Output:
        - list of versions (dataframe)
    """
    client = global_client["files"]
    file_list = client.files.list(
        limit=-1, 
        directory_prefix=directory_prefix, 
        external_id_prefix=external_id_prefix,
        metadata=metadata,
        uploaded=uploaded
    ).to_pandas()

    return file_list
