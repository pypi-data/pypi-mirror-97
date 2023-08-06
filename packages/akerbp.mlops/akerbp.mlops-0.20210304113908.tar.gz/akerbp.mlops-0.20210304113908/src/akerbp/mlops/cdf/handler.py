# handler.py
import traceback
from importlib import import_module
import warnings
warnings.simplefilter("ignore")

from akerbp.mlops.core import logger, config
service_name = config.envs.service_name
logging=logger.get_logger("mlops_cdf")

service = import_module(f"akerbp.mlops.services.{service_name}").service


def handle(data, secrets):
   try:
      config.update_cdf_keys(secrets)
      return service(data, secrets)
   except Exception:
      trace = traceback.format_exc()
      error_message = f"{service_name} service failed.\n{trace}"
      logging.critical(error_message)
      return dict(status='error', error_message=error_message)
