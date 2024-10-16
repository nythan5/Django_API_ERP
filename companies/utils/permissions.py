from rest_framework import permissions
from accounts.models import UserGroup, GroupPermission
from django.contrib.auth.models import Permission


def check_permission(user, method, permission_to):
    if not user.is_authenticated:
        return False

    if user.is_owner:
        return True

    required_permission = 'view_'+permission_to
    if method == 'POST':
        required_permission = 'add_'+permission_to
    elif method == 'PUT':
        required_permission = 'change_'+permission_to
    elif method == 'DELETE':
        required_permission = 'delete_'+permission_to

    # Quando utilizamos o .values estamos sendo específicos,
    # pegando apenas uma coluna indicada entre ().
    # Filtrando os grupos que o usuário esta vinculado
    groups = UserGroup.objects.values(
        'group_id').filter(user_id=user.id).all()

    for group in groups:
        # Filtrando apenas as permissões que tem o mesmo Group_ID do usuário
        permissions = GroupPermission.objects.values(
            'permission_id').filter(group_id=group['group_id']).all()

        for permission in permissions:
            if Permission.objects.filter(

                id=permission['permission_id'],
                codename=required_permission

            ).exists():
                return True


class EmployeesPermission (permissions.BasePermission):
    message = 'O usuário não tem permissão para gerenciar os funcionários'

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='employee')


class GroupsPermission (permissions.BasePermission):
    message = 'O usuário não tem permissão para gerenciar os grupos'

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='group')


class GroupsPermissionsPermission (permissions.BasePermission):
    message = 'O usuário não tem permissão para gerenciar as permissões'

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='permission')


class TaskPermission (permissions.BasePermission):
    message = 'O usuário não tem permissão para gerenciar as tarefas de todos os funcionários'

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='task')
