import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.compat import Serializer
from rest_framework_jwt.utils import jwt_encode_handler, jwt_decode_handler
from .jwt_payload_handler import jwt_payload_handler
from rest_framework_jwt.views import JSONWebTokenAPIView


class MRCUserSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(MRCUserSerializer, self).__init__(*args, **kwargs)
        self.fields["phone"] = serializers.CharField()  # 手機號
        self.fields['remember'] = serializers.IntegerField(default=60, allow_null=True)  # 過期時間

    def validate(self, attrs):
        print('-------')

        credentials = {
            'phone': attrs.get('phone'),
            'remember': attrs.get('remember'),
        }

        if all(credentials.values()):
            user = 'test user'
            # try:
            #     user = User.objects.get(phone=credentials.get('phone')) # 自己新建的model，不是django裏的User
            # except User.DoesNotExist:
            #     msg = _('the validate code is error')
            #     raise serializers.ValidationError(msg)

            if user:
                exp = datetime.utcnow() + timedelta(seconds=credentials.get('remember'))  # 過期時間
                payload = jwt_payload_handler(attrs.get('phone'))

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }

            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            # msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    print("====")
    serializer_class = MRCUserSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
