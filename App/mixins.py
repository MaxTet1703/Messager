from .models import Users, Message


class CompanionMixin:
    @property
    def get_companion(self):
        return Users.objects.exclude(pk=self.request.user.pk).only("pk", 
                                                                   "first_name",
                                                                   "last_name",
                                                                   "profile_image")


class MessagesMixin:
    @property
    def get_messages(self):
        return Message.objects.all().select_related("user").only("text", "user").order_by("created")
            
