from .models import Users, Message
from django.contrib.auth.mixins import LoginRequiredMixin
import vk_api


class CompanionMixin:
    @property
    def get_companion(self):
        return Users.objects.exclude(pk=self.request.user.pk).only("pk", "first_name", "last_name", "profile_image")


class MessagesMixin:
    @property
    def get_messages(self):
        return Message.objects.all().select_related("user").only("text", "user").order_by("created")


class GetDataFromVKAPIMixin(LoginRequiredMixin):

    def get_photo_image(self):
        extra_data = self.request.user.social_auth.all().first()
        if extra_data:
            access_token = extra_data.extra_data["access_token"]
            api = vk_api.VkApi(token=access_token).get_api()
            photo_url = api.users.get(user_ids=extra_data.uid, fields='photo_max_orig')[0]['photo_max_orig']
            return {"vkurl_photo": photo_url}
        return None
            
