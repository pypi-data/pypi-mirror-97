from django.conf import settings
from psu_base.classes.Log import Log
log = Log()

__version__ = '1.2.3'

__all__ = []

# Default settings
_DEFAULTS = {
    # Cashnet response landing page should not require authentication
    'CASHNET_PUBLIC_URLS': ['.*/cashnet/response'],

    # When BI Export is enabled, all Cashnet tables should be exported
    'PSU_CASHNET_EXPORT_MODELS': True,

    # Admin Menu Items
    'PSU_CASHNET_ADMIN_LINKS': [
        {
            'url': "cashnet:catalog_index", 'label': "Cashnet Items", 'icon': "fa-tags",
            'authorities': ['cashnet', 'oit-es-manager']
        },
        {
            'url': "cashnet:transaction_index", 'label': "Cashnet Transactions", 'icon': "fa-exchange",
            'authorities': ['cashnet', 'oit-es-manager']
        },
        {
            'url': "cashnet:test_form", 'label': "Cashnet Test", 'icon': "fa-flask",
            'nonprod_only': True
        },
    ]
}

# Assign default setting values
log.debug("Setting default settings for PSU_cashnet")
for key, value in list(_DEFAULTS.items()):
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError as ee:
        log.debug(f"Error importing {key}: {ee}")
