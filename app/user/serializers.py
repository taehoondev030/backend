"""
Serializers for the user API View
"""
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['student_id', 'email', 'password', 'name', 'description']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def validate_student_id(self, value):
        if not value.isdigit() or len(value) != 9:
            raise serializers.ValidationError("유효한 학번을 입력하세요.")
        return value

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
    def create(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace = False
        )
    student_id = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        student_id = attrs.get('student_id')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password,
        )
        if not user or user.student_id != student_id:
            msg = _('Unable to authenticate with provide credentials')
            raise serializers.ValidationError(msg, code = 'authorization')

        attrs['user'] = user
        return attrs
