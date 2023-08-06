from django.shortcuts import redirect
from psu_base.classes.Log import Log

log = Log()


def index(request):
    return redirect('export:status')
