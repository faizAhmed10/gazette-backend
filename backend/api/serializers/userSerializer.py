from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Authors  
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
        
class AuthorRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'name']

    def create(self, validated_data):
        # Extract the name to create an author
        name = validated_data.pop('name')
        
        # Create a user instance
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        
        # Create an author instance linked to the user
        Authors.objects.create(user=user, name=name)
        
        return user

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'username', 'email']
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            email = validated_data['email']
        )
        
        return user
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['user_id'] = user.id
        return token

class AuthorSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(read_only=True)
    class Meta:
        model = Authors
        fields = "__all__"