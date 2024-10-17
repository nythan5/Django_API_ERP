from django.urls import path
from companies.views.employees import Employees, EmployeeDetail
from companies.views.permissions import PermissionDetail
from companies.views.groups import Groups, GroupDetail
from companies.views.tasks import Tasks, TaskDetail

urlpatterns = [
    # Employees
    path('employees/', Employees.as_view(), name="employes"),
    path('employees/<int:employee_id>/',
         EmployeeDetail.as_view(), name="employes_detail"),

    # Permissions
    path('permissions/', PermissionDetail.as_view(), name="permission"),

    # Groups de Permissions
    path('groups/', Groups.as_view(), name="groups"),
    path('groups/<int:group_id>/', GroupDetail.as_view(), name="groups_detail"),

    # Tasks
    path('tasks/', Tasks.as_view(), name="tasks"),
    path('tasks/<int:task_id>/', TaskDetail.as_view(), name="tasks_detail")


]
