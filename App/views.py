from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models.query import Prefetch
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user
from django.views import View

from .forms import PlacesFrom, UserLogin, UserCreate
from .models import Users, Chats, Places, Message
from .mixins import CompanionMixin, MessagesMixin



# Create your views here.


class Login(View):
    template_name = "login.html"

    def login(self, request):
        form = UserLogin(self.request.POST)
        if form.is_valid():
            number = form.cleaned_data.get("number")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=number, password=password)
            print(type(user))
            if user:
                login(self.request, user)
                print(type(user))
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
        new_chat = Chats.objects.create()
        new_chat.participants.add(friend, self.request.user)
        new_chat.save()
        return JsonResponse({'status': 'ok'}, status=200)


class ChatsView(CompanionMixin, LoginRequiredMixin, View):
    template_name = "chats.html"

    def get(self, request):
        chats = Chats.objects.filter(participants__pk__in=(self.request.user.pk,)). \
            prefetch_related(Prefetch("participants", queryset=self.get_companion), 
                             Prefetch("messages", queryset=Message.objects.order_by("-pk")))
        context = {
            "query": chats
        }
        return render(request, self.template_name, context)


class DialogView(MessagesMixin, CompanionMixin, LoginRequiredMixin, DetailView):
    model = Chats
    template_name = "dialog.html"
    context_object_name = "dialog"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        return Chats.objects.prefetch_related(Prefetch("participants", queryset=self.get_companion),
                                              Prefetch("messages", queryset=self.get_messages)).get(
                                                        pk=self.kwargs['id'])


class NewslineView(LoginRequiredMixin, FormView, ListView):
    template_name = 'newsline.html'
    form_class = PlacesFrom
    model = Places
    context_object_name = "reviews"

    def get_queryset(self):
        return Places.objects.filter(user_id=self.request.user).select_related("user_id").only("pk", "name",
                                                                     "comment", "user_id",
                                                                    "user_id__profile_image")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def form_valid(self, form: PlacesFrom):
        new_entry = form.save(commit=False)
        new_entry.user_id = self.request.user
        new_entry.save()
        return JsonResponse({"mes": "Готово"}, status=200)

    def form_invalid(self, form: PlacesFrom):
        return JsonResponse({
            "mes": "Заполните данные полностью"
            }, status=400)


class ProfilePageView(LoginRequiredMixin, DetailView):
    template_name = "profile_page.html"
    pk_url_kwarg = 'id'
    context_object_name = "user"

    def get_object(self):
        return Users.objects.filter(pk=self.kwargs.get("user_id")).annotate(message_count=Count("user"),
                                                                    chats_count=Count("chats"),
                                                                    posts_count=Count("places"))[0]
    

def getting_user(request):
    user = get_user(request)
    print(user.id)
    return JsonResponse({"id": user.id})


@cache_page(60*20)
def about_us(request):
    return render(request, "about_us.html", {"is_about": True})


def logout_user(request):
    logout(request)
    return redirect('login')



