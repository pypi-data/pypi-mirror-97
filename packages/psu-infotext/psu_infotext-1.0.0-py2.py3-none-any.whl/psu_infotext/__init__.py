from django.conf import settings
from psu_base.classes.Log import Log
log = Log()

__version__ = '1.0.0'

__all__ = []

# Default settings
_DEFAULTS = {
    # Admin Menu Items
    'PSU_INFOTEXT_ADMIN_LINKS': [
        {
            'url': "infotext:index", 'label': "Infotext", 'icon': "fa-pencil-square-o",
            'authorities': ["admin", "infotext", "developer"]
        },
    ]
}

# Assign default setting values
log.debug("Setting default settings for PSU_INFOTEXT")
for key, value in list(_DEFAULTS.items()):
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError as ee:
        log.debug(f"Error importing {key}: {ee}")
