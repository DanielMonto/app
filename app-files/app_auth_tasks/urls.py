from . import views
from django.urls import path
urlpatterns = [
    path('',views.principal,name='init'),
    path('sign_in/',views.reguistro,name='reguis'),
    path('tasks/',views.tasks,name='tasks'),
    path('users/',views.mostrarUsuarios,name='users'),
    path('tasks_completed/',views.tasks_completed,name='tasks_com'),
    path('log_out/',views.signout,name='fin_cesson'),
    path('log_in/',views.confirm_user,name='confirm_user'),
    path('tasks/create/',views.create_task,name='create_task'),
    path('tasks/<str:task_name>/<int:task_id>/',views.task_detail,name='task_d'),
    path('tasks/<str:task_name>/<int:task_id>/complete/',views.completeTask,name='task_c'),
    path('tasks/<str:task_name>/<int:task_id>/delete/',views.deleteTask,name='task_del'),
    path('blog/',views.menajes_blog,name='blog'),
    path('blog/<str:M_Mensaje>/<int:M_id>/',views.deleteMensaje,name="mensaje_del"),
    path('tasks/subtask/delete/<str:subtask_name>/<int:subtask_id>/',views.delete_subtask,name='subtask_del'),
    path('task/<str:task_name>/<int:task_id>/subtask/create/',views.create_subtask,name='create_subtask'),
    path('tasks/subtask_detail/<str:subtask_name>/<int:subtask_id>/',views.subtask_detail,name='subtask_d'),
    path('blog/private/<str:name_receptor>/<str:name_talker>/',views.chat_privado,name='private_chat'),
    path('blog/private/delete/<int:pm_id>/<str:pm_mensaje>/<str:name_receptor>/',views.deletePrivateMensaje,name='pm_del')
]
