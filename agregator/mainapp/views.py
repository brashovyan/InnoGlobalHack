import json

from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers import *
from .models import *


# отображение всех проектов (и их данных) юзера
class ProjectListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # проекты, в которых есть юзер
        projects = Project.objects.filter(owners__in=[request.user.id])

        # список айдишников проектов, в которых есть юзер
        projects_id = []
        for project in projects:
            projects_id.append(project.id)

        # все спринты каждого проекта
        sprints = Sprint.objects.filter(project__in=projects_id)

        # все айдишники спринтов
        sprints_id = []
        for sprint in sprints:
            sprints_id.append(sprint.id)

        # все таски каждого спринта
        tasks = Task.objects.filter(sprint__in=sprints_id)

        return Response({'projects': ProjectSerializer(projects, many=True).data, 'sprints': SprintSerializer(sprints, many=True).data, 'tasks': TaskSerializer(tasks, many=True).data  })


# Все таски юзера
class TaskListApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        tasks = Task.objects.filter(owner_id=request.user.id)
        return Response({'tasks': TaskSerializer(tasks, many=True).data})


# Изменить таск
class TaskUpdateApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Мои проекты
class MyProjects(APIView):
    def get(self, request):
        projects = Project.objects.filter(owners__in=[request.user.id])
        return Response({'projects': TaskSerializer(projects, many=True).data})


# Получить вообще все таски из бд
class TaskAll(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]


# Получить вообще все спринты
class SprintAll(generics.ListAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated, ]


# Изменить спринт
class SprintUpdateApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


# получить все спринты по айдишнику проекта
class SprintsInProject(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        sprints = Sprint.objects.filter(project_id=pk)
        return Response({'sprints': SprintSerializer(sprints, many=True).data})


# Получить все таски по айдишнику спринта
class TasksInSprint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        tasks = Task.objects.filter(sprint_id=pk)
        return Response({'tasks': TaskSerializer(tasks, many=True).data})


# создание проекта
class CreateProjectApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # сначала я получаю данные с фронта

        project_title = request.data['project_title']

        project_data = {
            'title': project_title,
            'description': "Описание проекта",
            'owners': [request.user.id]
        }
        serializer = ProjectSerializer(data=project_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"answer": "Проект создан"})


# добавление юзера в проект
class AddUserToProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data['user']
        profession = request.data['profession']
        master = request.data['master']
        story_point = request.data['story_point']
        project = Project.objects.all().last()
        user = User.objects.get(username=username)
        user.profession = profession
        user.master = master
        user.story_point = story_point
        user.save()
        project.owners.add(user)

        return Response({"answer": "Юзер добавлен"})




# Создать проект
# class CreateProjectApiView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#
#         # сначала я получаю данные с фронта
#
#         # project_title = request.data['project_title']
#         # project_description = request.data['project_description']
#         # usernames = request.data['usernames']
#         usernames = User.objects.all()
#         usernames_id = []
#         for username in usernames:
#             user = User.objects.get(username=username)
#             usernames_id.append(user.id)
#         # professions = []
#         # scores = []
#
#         # title = request.data['title'],
#         # content = request.data['content'],
#
#         # тут происходит магия и создаётся проект
#
#         usernames_id.append(request.user.id)
#         project_data = {
#             'title': "Тестовый проект название",
#             'description': "Тестовый проект описание",
#             'owners': usernames_id
#         }
#         serializer = ProjectSerializer(data=project_data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         project = Project.objects.all().last()
#         id = project.id
#
#         #project_json = serializer.data
#
#         sprints_json = []
#
#         # и тут по идее в цикле создаётся куча спринтов
#         for i in range(0, 4):
#             sprint1_data = {
#                 'title': f"Тестовый спринт {i}",
#                 'description': "Тестовое описание",
#                 'date_start': '2023-09-30',
#                 'date_end': '2023-09-30',
#                 'project': id,
#                 'status': False
#             }
#
#             serializer = SprintSerializer(data=sprint1_data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             # sprints_json.append(serializer.data)
#
#             # и тут мы создаём таски для спринта
#             for j in range(0, 4):
#                 sprint = Sprint.objects.all().last()
#                 sprint_id = sprint.id
#
#                 task1_data = {
#                     'title': f"Тестовый таск {j}",
#                     'description': "Тестовое описание",
#                     'sprint': sprint_id,
#                     'owner': request.user.id,
#                     'status': "ToDo",
#                 }
#
#                 serializer = TaskSerializer(data=task1_data)
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
#
#         return Response({'answer': "Всё создалось"})

# получить юзернейм по айди
class GetUserById(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        user = User.objects.get(id=pk)
        return Response({'user': user.username})


# получить все таски в проекте
class TasksInProject(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        project = Project.objects.get(id=pk)
        sprints = Sprint.objects.filter(project=project)
        tasks = []
        for sprint in sprints:

            tasks2 = Task.objects.filter(sprint=sprint)

            for task in tasks2:
                d = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "sprint": task.sprint,
                    "owner": task.owner
                }
                tasks.append(d)
        return Response({'tasks': TaskSerializer(tasks, many=True).data})


# Алгоритм агрегации задач
class CreateTasks(APIView):
    def post(self, request):
        project = Project.objects.all().last()
        tasks = request.data["tasks"]

        # сортирую таски по приоритету (первый - самый приоритетный)
        for i in range(0, len(tasks)):
            for j in range(0, len(tasks)):
                if tasks[j]['priority'] < tasks[i]['priority']:
                    tasks[j]['priority'], tasks[i]['priority'] = tasks[i]['priority'], tasks[j]['priority']

        users = project.owners.all()
        # print(users[0])

        for i in range(0, len(tasks), 5):
            # создаю спринт
            sprint1_data = {
                            'title': f"спринт {i}",
                            'description': "Тестовое описание",
                            'date_start': '2023-09-30',
                            'date_end': '2023-09-30',
                            'project': project.id,
                            'status': False
                        }

            serializer = SprintSerializer(data=sprint1_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            sprint = Sprint.objects.all().last()

            # и закидываю в него первые 5 тасков
            for j in range(0, 5):
                if len(tasks) > 0:
                    #id = get_user_for_task()
                    task1_data = {
                            'title': f"{tasks[0]['title']}",
                            'description': "Тестовое описание",
                            'sprint': sprint.id,
                            'priority': f"{tasks[0]['priority']}",
                            'story_point': f"{tasks[0]['story_point']}",
                            'tag': f"{tasks[0]['tag']}",
                            'owner': request.user.id,
                            'status': "ToDo",
                        }

                    serializer = TaskSerializer(data=task1_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    del tasks[0]


        return Response({'answer': "Окей"})


def get_user_for_task():
    return 1


