from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Users)

admin.site.register(Chats)
admin.site.register(Message)
admin.site.register(Places)