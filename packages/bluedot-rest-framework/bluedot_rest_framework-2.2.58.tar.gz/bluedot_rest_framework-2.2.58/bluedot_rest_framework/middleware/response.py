
class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # response.data['status_code'] = response.status_code
        if response.status_code in [201, 204, 500]:
            response.status_code = 200

        # Code to be executed for each request/response after
        # the view is called.
        return response
