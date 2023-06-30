from django.conf import settings
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=200, validators=[
                             MinLengthValidator(5)])
    price = models.FloatField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Comment(models.Model):
    text = models.CharField(max_length=1000, validators=[
                            MinLengthValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.ad_id} - {self.author}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
