import copy
from urllib.parse import urlencode


class QueryParamsInjectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        query_params = copy.deepcopy(request.GET)
        if 'page' in query_params:
            del query_params['page']
        request.query_params = urlencode(query_params)
        response = self.get_response(request)

        return response
