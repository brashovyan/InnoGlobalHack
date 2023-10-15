from django.contrib.auth.models import AbstractUser
from django.db import models





class User(AbstractUser):
    # В теории так можно вместо юзернейма использовать уникальный email
    # username = None
    # email = models.EmailField(_('email address'), unique=True)
    # USERNAME_FIELD = 'email'

    # дополняем к обычному джанговскому юзеру дополнительные поля
    phone = models.CharField(max_length=255, null=True, blank=True)

    profession = models.CharField(max_length=255, null=True, blank=True)

    master = models.IntegerField(null=True)

    story_point = models.IntegerField(null=True)

    # это нужно, чтобы djoser выводил всю инфу о пользователе
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'email']


class Project(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    owners = models.ManyToManyField(User, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.title


class Sprint(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    status = models.BooleanField(default=True)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.PROTECT, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=255, null=True, default="BackLog")
    priority = models.IntegerField(null=True)
    story_point = models.IntegerField(null=True)
    tag = models.CharField(max_length=255, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.title






