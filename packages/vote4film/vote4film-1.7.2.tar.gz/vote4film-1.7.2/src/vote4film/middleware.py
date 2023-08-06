from django.contrib.auth.decorators import login_required

from vote4film.log import global_context_filter


def add_request_logging_context(get_response):
    """Set additional request-related information for logging.

    This should be the first middleware that is called.
    """

    def middleware(request):
        global_context_filter.start_request(request)
        response = get_response(request)
        global_context_filter.end_request()
        return response

    return middleware


def add_user_logging_context(get_response):
    """Set additional request-related information for logging.

    This should be after the authentication middleware.
    """

    def middleware(request):
        global_context_filter.update_user_info()
        return get_response(request)

    return middleware


def login_required_middleware(get_response):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL.

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    exceptions = {"/login/", "/logout/", "/admin/login/", "/admin/logout/"}

    def middleware(request):
        if request.path in exceptions:
            return get_response(request)
        return login_required(get_response)(request)

    return middleware
