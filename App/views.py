from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import Prefetch
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.views.generic.list import ListView
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import *
from .models import *
from .mixins import CompanionMixin, MessagesMixin
from .serializers import PlacesSerializer


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
        context = {
            "form_login": UserLogin(),
            "form_sign_up": UserCreate(),
            "title": "Вход в систему"
        }
        return render(request, self.template_name, context)

    def post(self, request):
        return self.methods[self.request.POST.get("message")](self, request)


class HomePage(LoginRequiredMixin, View):
    template_name = 'homepage.html'

    def get(self, request):
        return render(self.request, self.template_name)

    def post(self, request):
        friend = Users.objects.get(pk=request.POST.get('pk'))
        new_chat = Chats.objects.create().participants(friend, self.request.user)
        new_chat.save()
        return JsonResponse({'status': 'ok'}, status=200)


class ChatsView(CompanionMixin, LoginRequiredMixin, View):
    template_name = "chats.html"

    def get(self, request):
        chats = Chats.objects.filter(participants__pk__in=(self.request.user.pk,)). \
            prefetch_related(Prefetch("participants",
                                      queryset=self.get_companion))
        print(self.args)
        return render(request, self.template_name, {"query": chats})


class DialogView(MessagesMixin, CompanionMixin, LoginRequiredMixin, DetailView):
    model = Chats
    template_name = "dialog.html"
    context_object_name = "dialog"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        return Chats.objects.prefetch_related(Prefetch("participants", queryset=self.get_companion),
                                              Prefetch("messages", queryset=self.get_messages)).get(
            pk=self.kwargs['id'])



class NewslineView(FormView, ListView):
    template_name = 'newsline.html'
    form_class = PlacesFrom
    model = Places
    context_object_name = "reviews"

    def get_queryset(self):
        return Places.objects.filter(
            user_id=self.request.user).select_related("user_id").only("pk", "name",
                                                                     "comment", "user_id",
                                                                    "user_id__profile_image")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["use_map"] = True
        return context

    def form_valid(self, form: PlacesFrom):
        new_entry = form.save()
        new_entry.user_id = self.request.user
        new_entry.save()
        return JsonResponse(form.cleaned_data, status=200)

    def form_invalid(self, form: PlacesFrom):
        return JsonResponse({
            "mes": "Заполните данные полностью"
            }, status=400)

@api_view(["GET"])
def get_reviews(request):
    queryset = Places.objects.all().only("pk", "longitude", 'latitude')
    serializer = PlacesSerializer(queryset, many=True)
    return Response(serializer.data)

def getting_user(request):
    user = get_user(request)
    print(user.id)
    return JsonResponse({"id": user.id})


def about_us(request):
    return render(request, "about_us.html", {"is_about": True})


def logout_user(request):
    logout(request)
    return redirect('login')



