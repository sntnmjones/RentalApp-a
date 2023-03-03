from django.shortcuts import render
import logging

logger = logging.getLogger()

def index(request):
    logger.info("Hello info!")
    logger.warning("Hello warning!")
    logger.error("Hello error!")
    logger.critical("Hello critical!")
    return render(
        request,
        template_name="home_page/templates/home_page/index.html",
        context={},
        status=200,
    )
