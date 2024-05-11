from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserAuthorizationSerializer, UserCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from random import randint
from .models import Code
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

class RegistrationAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(username=username, password=password, is_active=False)
        code = int(('').join([str(randint(0, 9)) for i in range(6)]))
        Code.objects.create(user=user, code=code)
        return Response(data={'code': code}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password, is_active=False)
    # Create activation code
    code = int(('').join([str(randint(0,9)) for i in range(6)]))
    Code.objects.create(user=user, code=code)
    return Response(data={'code':code}, status=status.HTTP_201_CREATED)

def activate_code_api_view(request):
    pass

# @api_view(['POST'])
# def authorization_api_view(request):
#     serializer = UserAuthorizationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     user = authenticate(**serializer.validated_data)
#     if user:
#         # try:
#         #     token = Token.obects.get(user=user)
#         # except Token.DoesNotExist:
#         #     token = Token.obects.create(user=user)
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response(data={'key': token.key})
#     return Response(status=status.HTTP_401_UNAUTHORIZED)

class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class ConfirmationAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        try:
            user_code = Code.objects.get(code=code)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_code.user.is_active = True
        user_code.user.save()
        user_code.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def confirmation_api_view(request):
    serializer = UserCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data['code']
    try:
        user_code = Code.objects.get(code=code)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user_code.user.is_active=True
    user_code.user.save()
    user_code.delete()
    return Response(status=status.HTTP_200_OK)