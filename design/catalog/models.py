from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.crypto import get_random_string


class AuthUser(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='ФИО', blank=False)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)

    USERNAME_FIELD = 'username'


class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. 3D-design, 2D-design, Sketch etc.)")

    def __str__(self):
        return self.name


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


class Application(models.Model):
    new = 'new'
    accepted = 'accepted'
    done = 'done'

    STATUS_CHOICES = [
        ('new', 'new'),
        ('accepted', 'accepted'),
        ('done', 'done')
    ]

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the application")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo_file = models.ImageField(max_length=254, upload_to=get_name_file, blank=True, null=True, validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']), validate_image])
    status = models.CharField(max_length=254, verbose_name='Статус', choices=STATUS_CHOICES, default='new')
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    user = models.ForeignKey(AuthUser, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    def display_category(self):
        return ', '.join([category.name for category in self.category.all()[:3]])

    display_category.short_description = 'Application'

    def get_absolute_url(self):
        """
        Returns the url to access a particular application.
        """
        return reverse('my-appli', args=[str(self.id)])

    @property
    def photo_file_url(self):
        if self.photo_file and hasattr(self.photo_file, 'url'):
            return self.photo_file.url

    def __str__(self):
        return self.title
