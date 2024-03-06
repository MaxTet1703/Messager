from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import *


# Create your views here.


class Login(View):
    template_name = "login.html"

    def login(self, request):
        form = UserLogin(self.request.POST)
        if form.is_valid():
            number = form.cleaned_data.get("number")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=number, password=password)
            if user:
                login(self.request, user)
                return JsonResponse({"type_form": "login", "status": 200}, status=200)
        return JsonResponse({"type_form": "login", "status": 400}, status=400)

    def sign_up(self, request):
        form = UserCreate(self.request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse({"type_form": "sign-up", "status": 200}, status=200)
        return JsonResponse(data={"type_form": "sign-up", "errors": form.errors.get_json_data(), "status": 400},
                            status=400)

    methods = {
        "login": login,
        "sign-up": sign_up
    }

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('main')
        context = dict()
        context["form_login"] = UserLogin()
        context["form_sign_up"] = UserCreate()
        context["title"] = "Вход в систему"
        return render(request, self.template_name, context)

    def post(self, request):
        return self.methods[self.request.POST.get("message")](self, request)


class HomePage(View):
    template_name = 'homepage.html'

    def get(self, request):
        print(f"Что за хрень {reverse('main')}")
        return render(self.request, self.template_name)


def about_us(request):
    return render(request, "about_us.html")


def logout_user(request):
    logout(request)
    return redirect('login')
