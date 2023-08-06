import logging
from ipware.ip import get_client_ip  # type: ignore  # pytype: disable=import-error
from j2fa.models import TwoFactorSession
from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import resolve, reverse

logger = logging.getLogger(__name__)


class Ensure2FactorAuthenticatedMiddleware:
    """
    Ensures that User is 2-factor authenticated.
    Place after session init.
    By default uses User.profile.require_2fa boolean to check if 2FA is required for the user.
    """

    excluded_routes = [
        "j2fa-obtain-auth",
        "logout",
    ]
    require_2fa_view = "j2fa-obtain-auth"

    def __init__(self, get_response=None):
        self.get_response = get_response

    def is_2fa_required(self, user: User) -> bool:
        """
        Checks 2FA should be used for this User.
        By default uses user.profile.require_2fa boolean.
        You can override this if custom toggle location is needed.
        Defaults to True.
        :param user: User
        :return: bool
        """
        if user.is_authenticated and hasattr(user, "profile") and hasattr(user.profile, "require_2fa"):  # type: ignore
            return user.profile.require_2fa  # type: ignore
        return True

    def is_2fa_route(self, path_info: str) -> bool:
        """
        Checks if request path should be require 2FA.
        Default checks route name against excluded_routes (overridable by settings.J2FA_EXCLUDED_ROUTES).
        :return: bool
        """
        route_name = resolve(path_info).url_name
        return route_name not in self.excluded_routes

    def __call__(self, request: HttpRequest):
        user = request.user
        if user.is_authenticated:
            assert isinstance(user, User)
            session = request.session
            assert isinstance(session, SessionBase)
            user_agent = request.META.get("HTTP_USER_AGENT") or ""
            ip = get_client_ip(request)[0] or ""
            path_info = request.path_info
            logger.debug("2FA: IP=%s, path_info=%s, route_name=%s", ip, path_info, resolve(path_info).url_name)

            if self.is_2fa_required(user) and self.is_2fa_route(path_info):
                j2fa_session_id = session.get("j2fa_session") or 0
                j2fa_session = TwoFactorSession.objects.filter(id=j2fa_session_id).first()
                assert j2fa_session is None or isinstance(j2fa_session, TwoFactorSession)
                if j2fa_session is None or not j2fa_session.is_valid(user, ip, user_agent) or not j2fa_session.active:
                    logger.info("2FA: route=%s, j2fa_session_id=%s", self.require_2fa_view, j2fa_session_id)
                    return redirect(reverse(self.require_2fa_view))

        return self.get_response(request)
