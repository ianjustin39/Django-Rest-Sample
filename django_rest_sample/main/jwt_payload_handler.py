
from calendar import timegm
from datetime import datetime

from django.conf import settings


def jwt_payload_handler(phone):

    print(settings.JWT_AUTH)

    payload = {
        'exp': datetime.utcnow() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
    }

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if settings.JWT_AUTH['JWT_ALLOW_REFRESH']:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if settings.JWT_AUTH['JWT_AUDIENCE'] is not None:
        payload['aud'] = settings.JWT_AUTH['JWT_AUDIENCE']

    if settings.JWT_AUTH['JWT_ISSUER'] is not None:
        payload['iss'] = settings.JWT_AUTH['JWT_ISSUER']

    payload['phone'] = phone

    return payload
