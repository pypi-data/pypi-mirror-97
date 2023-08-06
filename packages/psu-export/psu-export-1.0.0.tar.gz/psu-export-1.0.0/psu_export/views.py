from django.shortcuts import render
from django.http import JsonResponse
from psu_base.classes.Log import Log
from psu_export.services import export_service
from psu_scheduler.decorators import scheduled_job
from psu_base.services import utility_service
log = Log()


def export_status(request):
    """
    Export status of models
    """
    log.trace()
    exportable_models = export_service.get_export_map()

    # Check for existence of access and secret keys (boolean only)
    access_key = bool(utility_service.get_setting('BI_EXPORT_ACCESS_KEY'))
    secret_key = bool(utility_service.get_setting('BI_EXPORT_SECRET_KEY'))

    export_settings = {}
    for app, models in exportable_models.items():
        setting_name = f"{app.upper()}_EXPORT_MODELS"
        export_settings[app] = utility_service.get_setting(setting_name)
        if 'psu_' not in app and not export_settings[app]:
            setting_name = "EXPORT_MODELS"
        export_settings[app] = {'name': setting_name, 'value': utility_service.get_setting(setting_name)}

    log.end()
    return render(
        request, 'psu_export/export_status.html', {
            'exportable_models': exportable_models,
            'export_settings': export_settings,
            'access_key': access_key,
            'secret_key': secret_key,
        }
    )


@scheduled_job()
def export_models(request):
    """
    Export all models (as configured in settings)
    """
    log.trace()
    return JsonResponse(export_service.export_models())
