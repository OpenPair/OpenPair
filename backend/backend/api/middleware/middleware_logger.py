import logging
logger = logging.getLogger('middleware_logger')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f'Cookies as start: {request.COOKIES}')
        
        response = self.get_response(request)

        logger.debug(f'Cookies at the end: {response.cookies}')

        return response