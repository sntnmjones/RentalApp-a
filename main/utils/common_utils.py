from django.core.handlers.asgi import ASGIRequest
import logging
import os

logger = logging.getLogger()

def add_error_to_session_cookie(error: str, request: ASGIRequest):
    if 'errors' in request.session:
        request.session['errors'] += error
    else:
        request.session['errors'] = [error]

def is_prod():
    logger.info(f"STAGE: {str(os.getenv('STAGE'))}")
    return str(os.getenv("STAGE")) == 'prod'