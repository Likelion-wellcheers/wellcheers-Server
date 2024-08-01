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

# 로그인/로그아웃
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate(self, data): # db에 회원 정보가 존재하는지, 저장된 비밀번호와 사용자 입력값이 일치하는지 검증
        username = data.get("username", None)
        password = data.get("password", None)

        user = User.get_user_or_none_by_username(username=username)

        if user is None:
            raise serializers.ValidationError("해당 유저 계정이 존재하지 않습니다.")
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError("비밀번호가 틀렸습니다.")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data

# 유저 내정보 전달 시리얼라이저
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'nickname', 'city', 'gugoon'] # 이름, 나이, 현거주지