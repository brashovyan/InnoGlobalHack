from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from mainapp.views import *
from rest_framework import routers


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('create_project/', CreateProjectApiView.as_view()), # создать проект
    path('projects/', ProjectListApiView.as_view()), # cписок всей хуйни
    path('tasks/', TaskListApiView.as_view()), # только таски юзера
    path('all_tasks/', TaskAll.as_view()), # все таски
    path('tasks/<int:pk>', TaskUpdateApiView.as_view()), # обновление таска по айдишнику
    path('sprints/<int:pk>', SprintUpdateApiView.as_view()), # обновление спринта по айдишнику
    path('sprints/', SprintAll.as_view()), # вообще все спринты
    path('sprints_in_project/<int:pk>', SprintsInProject.as_view()), # спринты в проекте по айди
    path('my_projects/', MyProjects.as_view()), # получить мои проекты
    path('tasks_in_sprint/<int:pk>', TasksInSprint.as_view()), # получить все таски в спринте по айди
    path('get_user/<int:pk>', GetUserById.as_view()), # получить username по его айди
    path('tasks_in_project/<int:pk>', TasksInProject.as_view()), # получить все таски проекта (бэклог)
    path('add_user_to_project/', AddUserToProject.as_view()),
    path('create_tasks/', CreateTasks.as_view()),
]