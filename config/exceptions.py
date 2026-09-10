from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and hasattr(exc, 'get_codes'):
        response.data = {
            'detail': response.data.get('detail'),
            'code': exc.get_codes(),
        }

    return response