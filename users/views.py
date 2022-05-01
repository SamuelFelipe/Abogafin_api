from AbogafinAPI.permissions import AdminOrSelf
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users import serializer

from users.models import CustomUser
from users.serializer import CustomUserSerializer


class SelfMethods(APIView):

    permission_classes = [AdminOrSelf]
    serializer_class = CustomUserSerializer

    def get(self, request, format=None):
        return Response(self.serializer_class(request.user).data)

    def post(self, request, format=None):
        self.serializer_class()


class CustomUserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all().order_by('-date_joined')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserSerializer
