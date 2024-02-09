from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import *


# Create your views here.


class Login(View):
    template_name = "login.html"

    def login(self):
        form = UserLogin(self.request.POST)
        if form.is_valid():
            number = form.cleaned_data.get("number")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request, number=number, password=password)
            if user:
                login(self.request, user)
                return JsonResponse({"type_form": "login", "status": 200}, status=200)

        return JsonResponse({"type_form": "login", "status": 400}, status=200)

    def sign_up(self):
        form = UserCreate(self.request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"type_form": "sign-up", "status": 200}, status=200)
        return JsonResponse({"type_form": "sign-up", "errors": form.errors.get_json_data(),  "status": 400}, status=200)

    methods = {
        "login": login,
        "sign-up": sign_up
    }

    def get(self, request):
        context = dict()
        context["form_login"] = UserLogin()
        context["form_sign_up"] = UserCreate()
        context["title"] = "Вход в систему"
        return render(request, self.template_name, context)

    def post(self, request):
        return self.methods[self.request.POST.get("message")](self)


def about_us(request):
    return render(request, "about_us.html")
