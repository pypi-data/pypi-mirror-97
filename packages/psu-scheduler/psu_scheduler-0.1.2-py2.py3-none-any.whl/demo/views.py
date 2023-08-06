from django.shortcuts import render
from psu_base.classes.Log import Log

log = Log()


def index(request):
    """
    A landing page
    """
    log.trace()

    return render(
        request, 'landing.html', {}
    )
