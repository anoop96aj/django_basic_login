from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import boto3
import hmac
import hashlib
import base64
from .constants import AuthConfigConstants, EncodingsConstants, LoginApiConstants
from .settings import CLIENT_SECRET, CLIENT_ID, COGNITO_CLIENT, DEFAULT_REGION_NAME
from .serializers import LoginSerializer


def get_secret_hash(username, client_id, client_secret):
    message = bytes(username + client_id, EncodingsConstants.UTF_8)
    secret_key = bytes(client_secret, EncodingsConstants.UTF_8)
    hash_digest = hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
    return base64.b64encode(hash_digest).decode()


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data[AuthConfigConstants.EMAIL]
            password = serializer.validated_data[AuthConfigConstants.PASSWORD]
            if not User.objects.filter(email=email).first():
                return Response({LoginApiConstants.MESSAGE: LoginApiConstants.EMAIL_NOT_REGISTERED_MESSAGE}, status=401)
            client = boto3.client(COGNITO_CLIENT, region_name=DEFAULT_REGION_NAME)
            client_id = CLIENT_ID
            client_secret = CLIENT_SECRET
            secret_hash = get_secret_hash(email, client_id, client_secret)

            try:
                resp = client.initiate_auth(
                    ClientId=client_id,
                    AuthFlow=LoginApiConstants.USER_PASSWORD_AUTH_FLOW,
                    AuthParameters={
                        LoginApiConstants.USERNAME: email,
                        LoginApiConstants.PASSWORD: password,
                        LoginApiConstants.SECRET_HASH: secret_hash
                    },
                )
                return Response({LoginApiConstants.MESSAGE: LoginApiConstants.LOGIN_SUCCESSFUL_MESSAGE,
                                 LoginApiConstants.DATA: resp})
            except Exception as e:
                return Response({LoginApiConstants.MESSAGE: str(e)}, status=400)
        return Response(serializer.errors, status=400)
