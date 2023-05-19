from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import ContactUserSerializer

from .models import *


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}
        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response({'активация': 'активация аккаунта прошла успешно'})



class ContactUserApiView(ModelViewSet):
    '''
    Создание и редактирование Контактов Пользователя

    '''
    permission_classes = [IsAuthenticated]
    queryset = ContactUser.objects.all()
    serializer_class = ContactUserSerializer

    def get_queryset(self):
        return ContactUser.objects.filter(user=self.request.user)