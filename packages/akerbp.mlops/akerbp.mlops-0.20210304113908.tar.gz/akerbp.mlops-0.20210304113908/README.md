# MLOps Framework
This is a framework for MLOps that deploys models as functions in Cognite Data
Fusion or api's in Google Cloud Run.

# User Guide 

## Getting Started:
Follow these steps:
- Install package: `pip install akerbp.mlops`
- Set up pipeline file `bitbucket-pipelines.yml` and config file
  `mlops_settings.yaml` by running this command from your repo's root folder:
  ```bash
  python -m akerbp.mlops.deployment.setup
  ```
- Fill in user settings and then validate them by running this (from repo root):
  ```python
  from akerbp.mlops.core.config import validate_user_settings
  validate_user_settings()
  ```
  alternatively, run the setup again:
  ```bash
  python -m akerbp.mlops.deployment.setup
  ```
- Commit the pipeline and settings files to your repo
- Become familiar with the model template (see folder `model_code`) and make
  sure your model follows the same interface and file structure (described
  later)   
- Follow or request the Bitbucket setup (described later)

A this point every git push in master branch will trigger a deployment in the
test environment. More information about the deployments pipelines is provided
later.

## Updating MLOps
Follow these steps:
- Install a new version using pip, e.g. `pip install akerbp.mlops==x`
- Run this command from your repo's root folder:
  ```bash
  python -m akerbp.mlops.deployment.setup
  ```
  That will update the pipeline and validate your settings. Commit changes and
  you're ready to go!

## General Guidelines
Users should consider the following general guidelines:
- Model artifacts should not be committed to the repo. Folder `model_artifact`
  does store model artifacts for the model defined in `model_code`, but it is
  just to help users understand the framework 
- Follow the recommended file and folder structure (described later)
- There can be several models in your repo: they need to be registered in the
  settings, and then they need to have their own model and test files
- Follow the import guidelines (described later)
- Make sure the prediction service gets access to model artifacts (described
  later)

## Configuration
MLOps configuration is stored in `mlops_settings.yaml`. Example for a project
with a single model:
```yaml
model_name: model1
model_file: model_code/model1.py
req_file: model_code/requirements.model
artifact_folder: model_artifact
test_file: model_code/test_model1.py
platform: cdf
info:
    prediction: &desc
        description: 'Description prediction service, model1'
        owner: data@science.com
    training:
        << : *desc
        description: 'Description training service, model1'
```
Field description:
 - model_name: a suitable name for your model. No spaces allowed.
 - model_file: model file path relative to the repo's root folder. All required
   model code should be under the top folder in that path (`model_code` in the
   example above).
 - req_file: model requirement file. Do not use `.txt` extension!  
 - artifact_folder: model artifact folder. It can be the name of an existing
   local folder (note that it should not be committed to the repo). In that case
   it will be used in local deployment. It still needs to be uploaded so that it
   can be used in Test or Prod. If the folder does not exist locally, the
   framework will try to create that folder and download the artifacts there. 
 - test_file: test file to use. Set to `null` for no testing before deployment
   (not recommended).
 - platform: deployment platforms, either `cdf` (Cognite) or `gc` (Google).
 - info: description and owner information for the prediction and training
   services. Training field can be discarded if there's no such service.
Note: all **paths** should be **unix style**, regardless of the platform.

If there are multiple models, model configuration should be separated using
`---`. Example:
```yaml
model_name: model1
model_file: model_code/model1.py
(...)
--- # <- this separates model1 and model2 :)
model_name: model2
model_file: model_code/model2.py
(...)
```

## Files and Folders Structure
All the model code and files should be under a single folder, e.g. `model_code`.
**Required** files in this folder:
- `model.py`: implements the standard model interface
- `test_model.py`: tests to verify that the model code is correct and to verify
  correct deployment
- `requirements.model`: libraries needed (with specific **version numbers**),
  can't be called `requirements.txt`. Add the MLOps framework like this:
  ```bash
  # requirements.model
  (...) # your other reqs
  akerbp.mlops==MLOPS_VERSION
  ```
  During deployment `MLOPS_VERSION` will be automatically replaced by the
  specific version that you have installed.

The following structure is recommended for projects with multiple models:
- `model_code/model1/`
- `model_code/model2/`
- `model_code/common_code/` 

This is because when deploying a model, e.g. `model1`, the top folder in the
path (`model_code` in the example above) is copied and deployed, i.e.
`common_code` folder (assumed to be needed by `model1`) is included. Note that
`model2` folder would also be deployed (this is assumed to be unnecessary but
harmless).

## Import Guidelines
The repo's root folder is the base folder when importing. For example, assume
you have these files in the folder with model code: 
 - `model_code/model.py`
 - `model_code/helper.py` 
 - `model_code/data.csv` 

If `model.py` needs to import `helper.py`, use: `import model_code.helper`. If
`model.py` needs to read `data.csv`, the right path is
`os.path.join('model_code', 'data.csv')`. 

It's of course possible to import from the Mlops package, e.g. its logger:
``` python
from akerbp.mlops.core import logger 
logging=logger.get_logger("logger_name")
logging.debug("This is a debug log")
```

## Deployment Platform
Model services (described below) can be deployed to either CDF or GCR,
independently. 

## Services
We consider two types of services: prediction and training. 

Deployed services can be called with 
```python
from akerbp.mlops.xx.helpers import call_function
output = call_function(function_name, data)
```
Where `xx` is either `'cdf'` or `'gc'`, and `function_name` follows the
structure `model-service-env`:
 - `model`: model name given by the user (settings file)
 - `service`: either `training` or `prediction`
 - `env`: either `dev`, `test` or `prod` (depending on the deployment
   environment)

The output has a status field (`ok` or `error`). If they are 'ok', they have
also a `prediction` or `training` field (depending on the type of service). The
former is determined by the `predict` method of the model, while the latter
combines artifact metadata and model metadata produced by the `train` function.
Prediction services have also a `model_id` field to keep track of which model
was used to predict.

## Model Artifacts for the Prediction Service
Prediction services are deployed with model artifacts so that they are available
at prediction time (downloading would require waiting time, and files written
during run time consume ram memory). 

Model artifacts are segregated by environment (e.g. only production models can
be deployed to production). Model artifacts are versioned and stored in CDF
Files together with user-defined metadata. Uploading a new model increases the
version count by 1 for that model and environment. It's important not to delete
model files manually, since that would mess with the model manager. When
deploying a model service, the latest model version is chosen (however, we can
discuss the possibility of deploying specific versions or filtering by
metadata).

The general rule is that model artifacts have to be uploaded manually before
deployment. If there are multiple models, you need to do this one at at time.
Code example: 
```python 
import akerbp.mlops.model_manager as mm

metadata = train(model_dir, secrets) # or define it directly
mm.setup()
folder_info = mm.upload_new_model_version(
  model_name, 
  env,
  folder_path, 
  metadata
)
```
This requires `COGNITE_API_KEY_*` environmental variables (see next section) or
you can give a suitable key to the model manager setup function. Note that
`model_name` corresponds to one of the elements in `model_names` defined in
`mlops_settings.py`, `env` is the target environment (where the model should be
available), `folder_path` is the local model artifact folder and `metadata` is a
dictionary with artifact metadata, e.g. performance, git commit, etc. Each model
update adds a new version (environment dependent) and note that updating a model
doesn't modify the models used in existing prediction services.

Recommended process to update a model:
1. New model features implemented in a feature branch
2. New artifact generated and uploaded to test environment
3. Feature branch merged with master
4. Test deployment is triggered automatically: prediction service is deployed to
   test with the latest artifacts
5. Prediction service in test is verified, and if things go well
6. New artifact uploaded to prod environment
7. Production deployment is triggered manually: prediction service is deployed
   to prod with the latest artifacts

However, in projects with a training service, you can rely on it to upload a
first version of the model. The first prediction service deployment will fail,
but you can deploy again after the training service has produced a model.

Another exception is that, when you deploy from the development environment
(covered later in this document), the model artifacts in the settings file can
point to existing local folders. These will then be used for the deployment.
Version is then fixed to `model_name/dev/1`. Note that these artifacts are not
uploaded to CDF Files.

## Local Testing and Deployment
It's possible to tests the functions locally, which can help you debug errors
quickly. This is recommended before a deployment. 

Define the following environmental variables (e.g. in `.bashrc`):
```bash
export ENV=dev
export COGNITE_API_KEY_PERSONAL=xxx
export COGNITE_API_KEY_FUNCTIONS=$COGNITE_API_KEY_PERSONAL
export COGNITE_API_KEY_DATA=$COGNITE_API_KEY_PERSONAL
export COGNITE_API_KEY_FILES=$COGNITE_API_KEY_PERSONAL
export GOOGLE_PROJECT_ID=xxx # If deploying to Google Cloud Run
```

From your repo's root folder:
- `python -m pytest model_code` (replace `model_code` by your model code folder
  name)
- `deploy_prediction_service.sh`
- `deploy_training_service.sh` (if there's a training service)

The first one will run your model tests. The last two run model tests but also
the service tests implemented in the framework and simulate deployment.

If you really want to deploy from your development environment, you can run
this: `LOCAL_DEPLOYMENT=True deploy_prediction_service.sh`

## Automated Deployments from Bitbucket
Deployments to the test environment are triggered by commits (you need to push
them). Deployments to the production environment are enabled manually from the
Bitbucket pipeline dashboard. Branches that match 'deploy/*' behave as master. 

It is assumed that most projects won't include a training service. A branch that
matches 'mlops/*' deploys both prediction and training services. If a project
includes both services, the pipeline file could instead be edited so that master
deployed both services.

It is possible to schedule the training service in CDF, and then it can make
sense to schedule the deployment pipeline of the model service (as often as new
models are trained)

## Bitbucket Setup
The following environments need to be defined in `repository settings >
deployments`: 
- test deployments: `test-prediction` and `test-training`, each with `ENV=test`
- production deployments: `production-prediction` and `production-training`,
  each with `ENV=prod`

The following need to be defined in `respository settings > repository
variables`: `COGNITE_API_KEY_DATA`, `COGNITE_API_KEY_FUNCTIONS`,
`COGNITE_API_KEY_FILES` (these should be CDF keys with access to data, functions
and files). If deployment to GCR is needed, you need in addition:
`ENABLE_GC_DEPLOYMENT` (set to `True`), `GOOGLE_SERVICE_ACCOUNT_FILE` (content
of the service account id file) and `GOOGLE_PROJECT_ID` (name of the project)

The pipeline needs to be enabled.


# Developer/Admin Guide

## MLOps Files and Folders
These are the files and folders in the MLOps repo:
- `src` contains the MLOps framework package
- `mlops_settings.yaml` contains the user settings for the dummy model
- `model_code` is a model template included to show the model interface.
  It is not needed by the framework, but it is recommended to become familiar
  with it.
- `model_artifact` stores the artifacts for the model shown in  `model_code`.
  This is to help to test the model and learn the framework.
- `bitbucket-pipelines.yml` describes the deployment pipeline in Bitbucket
- `build.sh` is the script to build and upload the package
- `setup.py` is used to build the package
- `LICENSE` is the package's license

## Build and Upload Package
Create an account in pypi, then create a token and a `$HOME/.pypirc` file. Edit `setup.py` file and note the following:
- Dependencies need to be registered
- Bash scripts will be installed in a `bin` folder in the `PATH`. 

The pipeline is setup to build the library from Bitbucket, but it's possible to
build and upload the library from the development environment as well:
```bash
bash build.sh
```
In general this is required before `LOCAL_DEPLOYMENT=True bash
deploy_xxx_service.sh`. The exception is if local changes affect only the
deployment part of the library, and the library has been installed in developer
mode with: 
```bash
pip install -e .
```
In this mode, the installed package links to the source code, so that it can be
modified without the need to reinstall).

## Bitbucket Setup
In addition to the user setup, the following is needed to build the package:
- `test-pypi`: `ENV=test`, `TWINE_USERNAME=__token__` and `TWINE_PASSWORD`
  (token generated from pypi)
- `prod-pypi`: `ENV=prod`, `TWINE_USERNAME=__token__` and `TWINE_PASSWORD`
  (token generated from pypi, can be the same as above)


## Google Cloud Setup
In order to deploy to Google Cloud Run, you need to create a service account
with the following rights: 
 - Cloud Build Service Account
 - Service Account Admin
 - Service Account User
 - Cloud Run Admin
 - Viewer

You also need to create the CDF secret `mlops-cdf-keys`. It's a string that can
be evaluated in python to get a dictionary (same used in the cdf helpers file).
This is because:
 - It needs to be passed to prediction and training services
 - Model registry uses CDF Files in its


## Calling FastApi services
Bash: install httpie, then:
```bash
http -v POST http://127.0.0.1:8000/train data='{"x": [1,-1],"y":[1,0]}'
```
Python: challenging when posting nested json with requests. This works:
```python
import requests, json
data = {"x":[1,-1], "y":[1,0]}
requests.post(model_api, json={'data': json.dumps(data)})
```
   
## Notes on the code

Model deployment happens in an independent process (multiprocessing library) to
avoid import/setup problems when testing services. Specifically, when deploying
multiple models the service had to be reloaded before testing it, otherwise it
would be the first model's service. In addition, model initialization in
the prediction service is designed to load artifacts only once in the process.
