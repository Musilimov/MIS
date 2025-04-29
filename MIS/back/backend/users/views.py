# myapp/views.py
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserSerializer, MyTokenObtainPairSerializer
# myapp/views.py
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user  # Получаем текущего аутентифицированного пользователя
        return Response({
            "username": user.username,
            "email": user.email,
        })

# Регистрация пользователя
class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

# Логин пользователя (используем стандартный JWT Token)
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
# Обновление токена (если он истек)
class TokenRefreshView(TokenRefreshView):
    pass

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            refresh_token = request.query_params.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Успешный выход из системы"}, status=200)
            return Response({"detail": "Токен обновления не предоставлен"}, status=400)
        except TokenError:
            return Response({"detail": "Недействительный токен"}, status=400)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Успешный выход из системы"}, status=200)
            return Response({"detail": "Токен обновления не предоставлен"}, status=400)
        except TokenError:
            return Response({"detail": "Недействительный токен"}, status=400)
