from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from uuid import uuid4

from users.models.users import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        )
    
    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        username = attrs.get('username').strip().lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email is already exists.')
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User with this username is already exists.')
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            pay_id = uuid4(),
            is_active = False,
            is_verification = False,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username').lower()
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Please give both username and password.")

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('username does not exist.')

        user = authenticate(request=self.context.get('request'), username=username,
                            password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs