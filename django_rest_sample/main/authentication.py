import jwt

from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)

from django.conf import settings

from rest_framework_jwt.utils import jwt_decode_handler


# jwt_decode_handler = settings.JWT_AUTH['JWT_DECODE_HANDLER']
# jwt_get_username_from_payload = settings.JWT_AUTH['JWT_PAYLOAD_GET_USERNAME_HANDLER']


class BaseJSONWebTokenAuthentication(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """
    def get_jwt_value(self, request):
        pass

    def authenticate(self, request):
        print('3333')
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
            # payload = {}
        except jwt.ExpiredSignature:
            msg = _('Signature has expired...')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature...')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        print('4444')
        """
        Returns an active user that matches the payload's user id and email.
        """
        # User = get_user_model()
        # username = jwt_get_username_from_payload(payload)
        phone = payload.get('phone')        # 如果更新用戶信息時更改到手機號，則要重新登錄獲取新的token

        if not phone:
            msg = _('Invalid payload...')
            raise exceptions.AuthenticationFailed(msg)

        # try:
        #     # user = User.objects.get_by_natural_key(username)
        #     user = User.objects.get(phone=phone)
        # except User.DoesNotExist:
        #     msg = _('Invalid signature.')
        #     raise exceptions.AuthenticationFailed(msg)

        # if not user.is_active:
        #     msg = _('User account is disabled.')
        #     raise exceptions.AuthenticationFailed(msg)
        user = 'sample user'
        return user


class MyJSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    """
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string specified in the setting
    `JWT_AUTH_HEADER_PREFIX`. For example:

        Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """
    www_authenticate_realm = 'api'

    def get_jwt_value(self, request):

        print('1111')
        auth = get_authorization_header(request).split()
        auth_header_prefix = settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX'].lower()

        if not auth:
            if settings.JWT_AUTH['JWT_AUTH_COOKIE']:
                return request.COOKIES.get(settings.JWT_AUTH['JWT_AUTH_COOKIE'])
            return None

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_header(self, request):
        print('2222')
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX'], self.www_authenticate_realm)
