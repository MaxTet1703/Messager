from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
import vk_api


def check(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        if not user.profile_image.url or user.profile_image.url.endswith('default_image/default.jpg'):
            extra_data = user.social_auth.all().first()
            access_token = extra_data.extra_data["access_token"]
            api = vk_api.VkApi(token=access_token).get_api()
            photo_url = api.users.get(user_ids=extra_data.uid, fields='photo_max_orig')[0]['photo_max_orig']
            print(f'АУ БЛЯТЬ{photo_url}')
            img_temp = NamedTemporaryFile(delete=False)
            img_temp.write(urlopen(photo_url).read())
            img_temp.flush()
            user.profile_image.save(f"image_{user.pk}.jpg", File(img_temp))
            user.save()
        