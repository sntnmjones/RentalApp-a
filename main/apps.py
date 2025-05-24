import logging
from django.apps import AppConfig
from main.utils.common_utils import is_prod

logger = logging.getLogger()

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    _instance = None

    def ready(self):
        if MainConfig._instance is None:
            stage = 'prod' if is_prod() else 'dev'
            logger.info(f"Application has started in {stage}")
            MainConfig._instance = self