from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import Prefetch
from django.views import View

from .forms import *
from .models import *


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


class HomePage(LoginRequiredMixin, View):
    template_name = 'homepage.html'

    def get(self, request):
        return render(self.request, self.template_name)

    def post(self, request):
        friend = Users.objects.get(pk=request.POST.get('pk'))
        new_chat = Chats.objects.create()
        new_chat.participants.add(friend, self.request.user)
        new_chat.save()
        return JsonResponse({'status': 'ok'}, status=200)


class ChatsView(LoginRequiredMixin, View):
    template_name = "chats.html"

    def get(self, request):
        chats = Chats.objects.filter(participants__pk__in=(self.request.user.pk,)). \
            prefetch_related(Prefetch("participants",
                                      queryset=Users.objects.exclude(pk=self.request.user.pk).only("first_name",
                                                                                                   "last_name",
                                                                                                   "profile_image")))

        return render(request, self.template_name, {"query": chats})


def message(request):
    return HttpResponse(request)


def about_us(request):
    return render(request, "about_us.html")


def logout_user(request):
    logout(request)
    return redirect('login')
