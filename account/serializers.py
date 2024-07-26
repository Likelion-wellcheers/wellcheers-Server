from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

# 회원가입
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'email']
    
    def save(self, request): # 회원가입 정보 저장

        user = User.objects.create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
                    
        # password 암호화하여 저장
        user.set_password(self.validated_data['password'])
        user.save()

        return user
    
    def validate(self, data): # 중복 email로 가입하는 것을 방지
        email = data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('해당 이메일이 이미 있습니다.')
        
        return data