from rest_framework.compat import requests
from ads.models import Ad, Comment
from rest_framework import serializers
from users.models import User
from users.serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ModelField(model_field=User, write_only=True,
                                    default=serializers.CurrentUserDefault())
    author_id = serializers.IntegerField(required=False)
    author_first_name = serializers.CharField(
        source='author.first_name', required=False)
    author_last_name = serializers.CharField(
        source='author.last_name', required=False)
    author_image = serializers.ImageField(
        source='author.image', required=False)
    ad_id = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    author = serializers.ModelField(model_field=User, write_only=True,
                                    default=serializers.CurrentUserDefault())
    # created_at = serializers.DateTimeField(write_only=True, default=)

    class Meta:
        model = Ad
        fields = ['pk', 'image', 'title', 'price',
                  'description', 'author']


class AdDetailSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer()
    author_id = serializers.IntegerField()
    author_first_name = serializers.CharField(source='author.first_name')
    author_last_name = serializers.CharField(source='author.last_name')
    phone = serializers.CharField(source='author.phone')

    pk = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Ad
        # fields = '__all__'
        fields = ['pk', 'image', 'description', 'title',
                  'price', 'created_at', 'author_id',
                  'author_first_name', 'author_last_name', 'phone']
