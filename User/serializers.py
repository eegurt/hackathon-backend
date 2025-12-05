from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.core.mail import get_connection, send_mail, EmailMessage, BadHeaderError
import logging

logger = logging.getLogger(__name__)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        # Создание пользователя с хешированием пароля
        client = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        # Отправка приветственного письма
        subject = 'Добро пожаловать в экосистему GidroAtlas — вместе растём!'
        message = (
            f"Уважаемый партнёр,\n\n"
            f"Благодарим за регистрацию на GidroAtlas!\n"
            )
        connection = get_connection()  # Используйте настройки по умолчанию

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email='noreply@gidroatlas.info',
                to=[client.email],
                connection=connection,
            )
            sent_count = email.send()
            if sent_count:
                logger.info(
                    "Welcome email sent",
                    extra={"user_id": client.id, "email": client.email},
                )
            else:
                logger.warning(
                    "Welcome email not sent (send() returned 0)",
                    extra={"user_id": client.id, "email": client.email},
                )
        except BadHeaderError:
            logger.error(
                "Invalid header in welcome email",
                extra={"user_id": client.id, "email": client.email},
            )
        except Exception as e:
            logger.exception(
                "Error sending welcome email",
                extra={"user_id": client.id, "email": client.email, "error": str(e)},
            )

        return client


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user is None or not isinstance(user, User):
            print(f"Failed to authenticate user with email: {email}")
            raise serializers.ValidationError('Invalid credentials')

        return {
            'user': user,
        }


class UserTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user_type = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user is None or not isinstance(user, User):
            print(f"Failed to authenticate user with email: {email}")
            raise serializers.ValidationError('Invalid credentials')

        refresh = RefreshToken.for_user(user)
        return {
            'id': str(user.id),
            'email': user.email,
            'user_type': user.user_type,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        ref_name = 'UserPasswordResetRequestSerializer'

class UserChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
