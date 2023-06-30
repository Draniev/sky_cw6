from ads.models import Ad, Comment
from django.contrib import admin

# TODO здесь можно подкючить ваши модели к стандартной джанго-админке
admin.site.register(Ad)
admin.site.register(Comment)
