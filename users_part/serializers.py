from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ContactUser, UserAccount

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'person_telephone', 'surname')


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'name', 'person_telephone', 'surname')


class ContactUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUser
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')

    def create(self, validated_data):
        user = self.context['request'].user
        obj = ContactUser.objects.create(**validated_data, user=user)
        return obj


