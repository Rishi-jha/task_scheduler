import logging
from datetime import timedelta, time, datetime, date

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger("django.request")


def datetime_now() -> datetime:
    return timezone.now().replace(microsecond=0)


def require_valid_password(function):
    """
    Decorator for views that checks that the user is authenticated and has a
    unexpired password, redirecting to the log-in or password change page
    if necessary.

    Usage
    -----

        @require_valid_password
        def staff_only_view(request):
            [...]
    """

    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = request.build_absolute_uri()
            return redirect_to_login(path, reverse("login"))
        return function(request, *args, **kwargs)

    wrapped.__name__ = function.__name__
    return wrapped
