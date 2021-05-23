import json


def jwt_response_payload_handler(token, user=None, request=None):
    print('22222222')
    print(request.data)
    data = request.data
    return {
        'token': token,
        'name': data.get('name')
    }
