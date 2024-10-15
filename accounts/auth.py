from rest_framework.exceptions import AuthenticationFailed, APIException
from accounts.models import User
from companies.models import Enterprise, Employee
from django.contrib.auth.hashers import check_password, make_password


class Authentication:
    # Função para realizar o Login do usuário
    def signin(self, email=None, password=None):
        exception_auth = AuthenticationFailed(
            'E-mail ou senha estão incorretos')

        # Verificando se o usuário existe
        user_exist = User.objects.filter(email=email).exists()

        if not user_exist:
            raise exception_auth

        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise exception_auth

        return user

    # Função para realizar o cadastro de usuário
    def signup(self, name, email, password, type_account='owner', company_id=False):
        if not name or name == '':
            raise APIException('O nome não deve ser nulo.')

        if not email or email == '':
            raise APIException('O e-mail não deve ser nulo.')

        if not password or password == '':
            raise APIException('A senha não deve ser nulo.')

        if type_account == 'employee' and not company_id:
            raise APIException('O id da empresa não deve ser nulo.')

        # Verificando se já existe um usuário com este e-mail
        user = User.objects.filter(email=email).exists()
        if user:
            raise APIException('Este e-mail já está cadastrado.')

        # Criando o hash da senha
        password_hashed = make_password(password)

        created_user = User.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=0 if type_account == "employee" else 1
        )

        if type_account == 'owner':
            created_enterprise = Enterprise.objects.create(
                name='Nome da empresa',
                user_id=created_user.id
            )

        if type_account == 'employee':
            Employee.objects.create(
                enterprise_id=company_id or created_enterprise,
                user_id=created_user.id
            )

        return created_user
