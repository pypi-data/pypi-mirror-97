from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


def get_user_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.FORNTEND_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "FORNTEND_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "FORNTEND_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
        )
