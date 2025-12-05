from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
import random
import string


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = []  # Убираем аутентификацию для регистрации
    permission_classes = []  # Убираем все разрешения для регистрации

    @swagger_auto_schema(
        responses={
            201: "Registration successful",
            409: "Conflict - email already exists",
            400: "Invalid data"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            buyer = serializer.save()
            # Попытка отправить письмо с данными для входа
            subject = 'Добро пожаловать на платформу GidroAtlas!'

            message = f"""
            Уважаемый(ая) партнёр!

            🎉 Поздравляем с регистрацией на платформе GidroAtlas!

            🔑 Логин: {buyer.email}  
            🔐 Пароль: {request.data["password"]}

            Мы всегда рядом, если нужна помощь или поддержка.

            С уважением, команда GidroAtlas 💼
            -----------------------------------------------

            Құрметті серіктес!

            🎉 GidroAtlas платформасына тіркелуіңізбен құттықтаймыз!

            🔑 Логин: {buyer.email}  
            🔐 Құпия сөз: {request.data["password"]}

            Сұрақтарыңыз болса — біз әрдайым байланыстамыз.

            Құрметпен, GidroAtlas командасы 💼
            """
            from_email = 'noreply@gidroatlas.info'  # Укажите ваш адрес отправителя
            recipient_list = [buyer.email]
            send_mail(subject, message, from_email, recipient_list)

            return Response({
                'id': str(buyer.id),
                'email': buyer.email,
            }, status=status.HTTP_201_CREATED)

        if 'email' in serializer.errors:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserTokenObtainSerializer

    @swagger_auto_schema(
        request_body=UserTokenObtainSerializer,
        responses={
            200: "Login successful",
            400: "Invalid credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = UserTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileUpdateSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(
        responses={
            200: "Profile updated successfully",
            400: "Invalid data"
        }
    )
    def update(self, request, *args, **kwargs):
        # Call the parent update method
        response = super().update(request, *args, **kwargs)

        # Retrieve the updated client instance
        buyer = self.get_object()

        # Check if the necessary fields are present

        return response

class VendorLogoutView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenSerializer

    @swagger_auto_schema(
        responses={
            205: "Logout successful",
            400: "Invalid request"
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    lookup_field = 'id'


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [AllowAny]


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)

                # Генерация временного пароля
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

                # Установка временного пароля
                user.set_password(temp_password)
                user.save()

                # Отправка временного пароля на email
                send_mail(
                    'Password Reset Request',
                    f'Ваш временный пароль для входа: {temp_password}',
                    'noreply@gidroatlas.info',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "Временный пароль отправлен на указанный email."},
                                status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserChangePasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserChangePasswordSerializer

    @swagger_auto_schema(request_body=UserChangePasswordSerializer)
    def post(self, request):
        user_id = request.data.get("user_id")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user_id or not old_password or not new_password:
            return Response({"detail": "user_id, old_password и new_password обязательны"}, status=400)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"detail": "Продавец не найден"}, status=404)

        if not user.check_password(old_password):
            return Response({"detail": "Неверный старый пароль"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Пароль успешно обновлён"})
