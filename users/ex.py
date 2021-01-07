from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """Handle Django ValidationError as an accepted exception
    Must be set in settings:
    >>> REST_FRAMEWORK = {
    ...     # ...
    ...     'EXCEPTION_HANDLER': 'mtp.apps.common.drf.exception_handler',
    ...     # ...
    ... }
    For the parameters, see ``exception_handler``
    """

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            exc = DRFValidationError(detail={'error': exc.message_dict})
        elif hasattr(exc, 'message'):
            exc = DRFValidationError(detail={'error': exc.message})
        elif hasattr(exc, 'messages'):
            exc = DRFValidationError(detail={'error': exc.messages})

    return drf_exception_handler(exc, context)