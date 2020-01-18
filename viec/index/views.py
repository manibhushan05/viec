from tokenize import Token

from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from index.serializers import UserSerializer


class IndexViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    def get(self, request, *args, **kwargs):
        return Response(data={}, status=status.HTTP_200_OK, template_name='index/login.html')


class UserLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_serializer = UserSerializer(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': 'success',
                'msg': 'Login Successful',
                'token': token.key,
                'data': user_serializer.data,
                'status_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        response = Response({
            'status': 'failure',
            'msg': 'Login Unsuccessful',
            'data': serializer.errors,
            'status_code': status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST)
        return response


class UserLogout(APIView):
    queryset = User.objects.all()

    def delete(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({'status': 'success', 'msg': 'Logout Successfull'}, status=status.HTTP_200_OK)
