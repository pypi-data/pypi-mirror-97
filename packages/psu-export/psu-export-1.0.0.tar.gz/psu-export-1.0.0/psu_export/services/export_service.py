import boto3
from psu_base.services import utility_service, error_service
from django.apps import apps
from psu_base.classes.Log import Log
import pandas
import io

log = Log()


def get_export_map():
    return export_models(audit_mode=True)


def export_models(audit_mode=False):
    """
    Export all models (as defined by settings)

    In audit mode, returns a list of models that would be exported (but does not do the export)
    """
    log.trace({'audit_mode': audit_mode})
    app_code = utility_service.get_app_code().lower()

    results = {}

    # For all installed apps...
    for app, models in apps.all_models.items():
        skip_models = []
        app_enabled = True
        status_desc = "Export Enabled"  # For audit mode

        # Completely ignore some framework models
        if app in [
            'admin', 'contenttypes', 'auth', 'sessions', 'messages',
            'staticfiles', 'django_cas_ng', 'crequest', 'sass_processor'
        ]:
            continue

        # Is this iteration for the current app (rather than a re-usable installed app)
        is_this_app = app == app_code

        # Should this app's models be exported?
        export = utility_service.get_setting(f"{app.upper()}_EXPORT_MODELS")

        # For the deployed app, allow shortened setting of "EXPORT_MODELS"
        if export is None and is_this_app:
            export = utility_service.get_setting("EXPORT_MODELS")

        # Do not export models when not specified for re-usable apps
        if export is None and not is_this_app:
            status_desc = 'Export Not Enabled'
            app_enabled = False
            if not audit_mode:
                # When not in audit mode, no need to list each disabled model within the disabled app
                results[app] = status_desc
                continue

        # If explicitly not exporting models for this app
        elif export is not None and not export:
            status_desc = 'Export Disabled'
            app_enabled = False
            if not audit_mode:
                # When not in audit mode, no need to list each disabled model within the disabled app
                results[app] = status_desc
                continue

        # If export not defined for this (deployed) app, export all by default
        elif not export:
            export = True

        # If given a list of models, make sure format is as expected
        if app_enabled and type(export) in [list, set]:
            # Django formats all models as lowercase
            # and possibly with no underscores. If so, add:   .replace('_', '')
            export = [x.lower() for x in export]

            # In some cases, it may be more convenient to list only models NOT to import
            for x in export:
                if x.startswith('!'):
                    skip_models.append(x.strip('!'))

            # If listing models to skip, then import all other models in this app
            if skip_models:
                export = True

        if app_enabled:
            log.info(f"Exporting models for {app}")
            if skip_models:
                log.info(f"Skipping models: {skip_models}")

        results[app] = {}
        for mm in models:

            # If a list of models to export was provided, only export those models
            if app_enabled and type(export) in [list, set] and mm not in export:
                results[app][mm] = "Skipped"
                continue

            # If skipping any models, check that here
            if app_enabled and skip_models and mm in skip_models:
                results[app][mm] = "Skipped"
                continue

            if audit_mode:
                results[app][mm] = status_desc

            elif export_model(f'{app}.{mm}'):
                results[app][mm] = "Exported"

            else:
                results[app][mm] = "Error"

    return results


def export_model(model_name):
    """
    Example: model_name='dual_credit.IdentityCrisis'
    """
    log.trace([model_name])
    try:
        model_instance = apps.get_model(model_name)
        model_fields = model_instance._meta.fields
        columns = [x.name for x in model_fields]
        data = []
        for result in model_instance.objects.all():
            row_data = []
            for field in model_fields:
                field_value = getattr(result, field.name)

                # If field is empty, no processing needed
                if not field_value:
                    val = field_value

                # If field is a relation, and is mapped by a single key
                elif field.is_relation and field.to_fields and len(field.to_fields) == 1 and field.to_fields[0]:
                    val = getattr(field_value, field.to_fields[0])

                # If field is a relation, and mapped by multiple keys
                elif field.is_relation and field.to_fields and len(field.to_fields) > 1:
                    val = [getattr(field_value, x) for x in field.to_fields]

                # If field is relation with unknown key, assume 'id'
                elif field.is_relation and hasattr(field_value, 'id'):
                    val = getattr(field_value, 'id')

                # Otherwise, use raw field data
                else:
                    val = field_value

                # Add to this row's data
                row_data.append(val)

            # Add to the full data-set
            data.append(row_data)

        # Create an in-memory file to be returned as attachment
        app_code = utility_service.get_app_code().lower()
        env = utility_service.get_environment().lower()
        # Modify model name for a better file name
        if '.' in model_name:
            pp = model_name.split('.')
            model_name = pp[len(pp)-1]
        model_name = utility_service.decamelize(model_name)

        file_name = f'{model_name}.csv'.lower()
        file_path = f'{app_code}/{env}/{file_name}'

        response = io.StringIO()
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        # Write data in CSV format
        df = pandas.DataFrame(data, columns=columns)
        df.to_csv(response, index=False)

        response.seek(0)
        response.seek(0)

        # Save to S3
        status = _export_to_s3(file_path, response.read())
        log.info(f"{file_path} S3 Upload Status:\n{status}\n")
        return status['ResponseMetadata']['HTTPStatusCode'] == 200

    except Exception as ee:
        error_service.record(ee, model_name)
        return False


def _get_s3_resource():
    access_key = utility_service.get_setting('BI_EXPORT_ACCESS_KEY')
    secret_key = utility_service.get_setting('BI_EXPORT_SECRET_KEY')
    return boto3.resource('s3', region_name='us-west-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)


def _export_to_s3(export_path, file_content):
    """
    https://stackoverflow.com/questions/40336918/how-to-write-a-file-or-data-to-an-s3-object-using-boto3
    https://stackoverflow.com/questions/15029666/exporting-items-from-a-model-to-csv-django-python
    """
    s3 = _get_s3_resource()
    bucket_name = 'django-bi-export'
    return s3.Object(bucket_name, export_path).put(Body=file_content)

    # {
    #     'ResponseMetadata': {
    #         'RequestId': 'B2068FBF555F437B',
    #         'HostId': 'JkyniuhAyL462cPy10VEbbE+pgdvMChht5+aZi1w2ni+Vg3O3rd+qWffPitosm+knODVQQpkj0U=',
    #         'HTTPStatusCode': 200,
    #         'HTTPHeaders': {
    #             'x-amz-id-2': 'JkyniuhAyL462cPy10VEbbE+pgdvMChht5+aZi1w2ni+Vg3O3rd+qWffPitosm+knODVQQpkj0U=',
    #             'x-amz-request-id': 'B2068FBF555F437B',
    #             'date': 'Tue, 19 Jan 2021 23:35:03 GMT',
    #             'etag': '"b10a8db164e0754105b7a99be72e3fe5"',
    #             'content-length': '0',
    #             'server': 'AmazonS3'
    #         },
    #         'RetryAttempts': 0
    #     },
    #     'ETag': '"b10a8db164e0754105b7a99be72e3fe5"'
    # }
