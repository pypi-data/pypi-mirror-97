from django.conf import settings
from psu_base.classes.Log import Log
log = Log()

__version__ = '1.0.0'

__all__ = []

# Default settings
_DEFAULTS = {
    # Data is exported to S3, not displayed on screen, and is called from outside a user session (scheduled)
    'EXPORT_PUBLIC_URLS': ['export/models'],

    # Admin Menu Items
    'PSU_EXPORT_ADMIN_LINKS': [
        {
            'url': "export:status", 'label': "Cognos Export - Status", 'icon': "fa-database",
            'authorities': "~SuperUser"
        },
    ]
}

# Assign default setting values
log.debug("Setting default settings for PSU_export")
for key, value in list(_DEFAULTS.items()):
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError as ee:
        log.debug(f"Error importing {key}: {ee}")
