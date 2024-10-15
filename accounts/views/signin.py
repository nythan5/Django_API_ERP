from accounts.views.base import Base
from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class Signin(Base):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signin(self, email=email, password=password)

        # Criando o refreshToken e implicitamente criando o token de acesso.
        # O Refresh Token é o token “principal”.
        # Ele automaticamente contém um Access Token vinculado.
        # Quem fica validando se o token esta valido ou
        # precisa de um novo é quem usa o token para consumir dados.
        token = RefreshToken.for_user(user)

        enterprise = self.get_enterprise_user(user.id)

        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data,
            "enterprise": enterprise,
            "refresh": str(token),
            "access": str(token.access_token)
        })
