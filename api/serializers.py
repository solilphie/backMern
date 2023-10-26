from rest_framework import serializers
from jobpost.models import Post
from application.models import Application
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author' ,'company','title', 'author', 'excerpt','category','content', 'status', 'published')


class UserSerializer(serializers. ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','adress','usertypes','categoryy','email', 'password']
        extra_kwargs = {'password' : {'write_only':True, 'required': True}}
 
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'author' ,'jobid','name', 'email', 'resume', 'coverletter', 'published')