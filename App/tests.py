from django.test import TestCase, Client
from django.urls import reverse, resolve

from .views import *
from .forms import *

# Create your tests here.

TEMPLATES = {'login': 'login.html',
             'about': 'about_us.html'}

CLASS_VIEW = {
    'login': Login
}
FUNC_VIEW = {
    'about': about_us
}
USERS = (
    {
        "message": "sign-up",
        "first_name": "Макс",
        "last_name": "Тетюшкин",
        "number": "+79683456798",
        "password1": "tnkdiatheo",
        "password2": "tnkdiatheo"
    },
    {
        "message": "sign-up",
        "first_name": "Иван",
        "last_name": "Иванов",
        "number": "+79671236574",
        "password1": "dndfjkgdfkjghdfgf",
        "password2": "dndfjkgdfkjghdfgf"
    },
    {
        "message": "sign-up",
        "first_name": "Константин",
        "last_name": "Константинов",
        "number": "+79067845612",
        "password1": "gfdgjsdgkjldsfgkd",
        "password2": "gfdgjsdgkjldsfgkd"
    },
    {
        "message": "sign-up",
        "first_name": "Дарья",
        "last_name": "Волкова",
        "number": "+79688760923",
        "password1": "qldnkscaxssa",
        "password2": "qldnkscaxssa"
    },
    {
        "message": "sign-up",
        "first_name": "Наташа",
        "last_name": "Рубцова",
        "number": "+79606156848",
        "password1": "uiwhncklap",
        "password2": "uiwhncklap"
    },

)

DATA_FOR_USER_CREATION_FORM = (
    {
        "first_name": "Максим",
        "last_name": "Тетюшкин",
        "number": "+79500861146",
        "password1": "dnqxfewfewf",
        "password2": "dnqxfewfewf"
    },
)


class TestUrls(TestCase):
    def test_urls_of_class_view(self):
        for key, value in CLASS_VIEW.items():
            url = reverse(key)
            self.assertEquals(resolve(url).func.view_class, value)

    def test_urls_of_funct_view(self):
        for key, value in FUNC_VIEW.items():
            url = reverse(key)
            self.assertEquals(resolve(url).func, value)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.sign_up = reverse("login")

    def test_project_list_GET(self):
        for url, template in TEMPLATES.items():
            response = self.client.get(reverse(url))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, template)

    def test_project_POST_add_new_user(self):
        for user in USERS:
            response = self.client.post(self.sign_up, data=user)
            self.assertEquals(response.status_code, 200)


class TestValidationForms(TestCase):

    def test_user_creation_form(self):
        for data in DATA_FOR_USER_CREATION_FORM:
            form = UserCreate(data=data)
            self.assertTrue(form.is_valid())
