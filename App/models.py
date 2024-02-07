from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):

    """

    Переопределенный класс Manager для моедля пользовтеля

    """

    def create_user(self, number, password, **extra_fileds):
        if not number:
            raise ValidationError("Номер не должен быть пустым")
        user = self.model(number, **extra_fileds)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, number, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(number, password, **extra_fields)


class Users(AbstractBaseUser):
    """

    Переопределённая модель пользовтаеля

    """
    number = PhoneNumberField(unique=True, null=False, blank=False, verbose_name="Номер телефона",
                              help_text="Введите номер телефона", region="RU")
    first_name = models.CharField(max_length=25, verbose_name="Имя пользователя", null=True)
    last_name = models.CharField(max_length=25, verbose_name="Фамилия пользователя", null=True)
    profile_image = models.ImageField(upload_to=f"user?profile", null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "number"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Places(models.Model):
    """

    Модель для хранения нужной информации о местах

    """
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=30, null=False, verbose_name="Название места")
    comment = models.CharField(blank=False, max_length=500, verbose_name="Комментарий к посту")
    longitude = models.FloatField(blank=False, verbose_name="Долгота")
    latitude = models.FloatField(blank=False, verbose_name="Широта")


class Chats(models.Model):
    participants = models.ManyToManyField(Users, related_name='chats')
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Отправитель")
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE, related_name='messages', verbose_name="Чат")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    text = models.TextField(max_length=500, verbose_name="Текст сообщения")
