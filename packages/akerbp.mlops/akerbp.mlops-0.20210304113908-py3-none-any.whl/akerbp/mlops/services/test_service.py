"""
test_service.py

Generic test for services (training or prediction)
"""
import os
import sys
from importlib import import_module

from akerbp.mlops.core import config, logger
service_name = config.envs.service_name
logging=logger.get_logger(name='MLOps')


api_keys = config.api_keys

def mock_saver(*args, **kargs):
    pass


def test_service(input, check):
   logging.info(f"Test {service_name} service")
   # Add deployment folder to path so that service can load the settings file
   sys.path.append(os.getcwd())
   service = import_module(f"akerbp.mlops.services.{service_name}").service

   if service_name == 'training':
      response = service(data=input, secrets=api_keys, saver=mock_saver)
   elif service_name == 'prediction':
      response = service(data=input, secrets=api_keys)
   else:
      raise Exception("Unknown service name")
   
   assert response['status'] == 'ok'
   assert check(response[service_name])
   