from rest_framework import serializers
from .models import UserProfile , ShoesDetail
from django.contrib.auth.hashers import make_password,check_password

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['firstname','lastname','username','age','state','city','hobbies','image','password', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = UserProfile.objects.create(**validated_data)
            
        instance.password = make_password(password)
        instance.save()
        return instance
        
class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True)
        
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            try:
                user_profile = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                raise serializers.ValidationError('Invalid email or password')
            
            if not check_password(password, user_profile.password):
                raise serializers.ValidationError('Invalid email or password')
            
            data['user_profile'] = user_profile
            
            return data
        
class ShoeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoesDetail
        fields = '__all__'
        
class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)