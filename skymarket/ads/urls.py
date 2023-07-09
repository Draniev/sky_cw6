from ads.views import AdViewSet, CurUserListView, CommentViewSet
from django.urls import include, path
from rest_framework import routers

# TODO настройка роутов для модели

router = routers.SimpleRouter()
router.register('', AdViewSet)
# router.register('<int:ad_pk>/comments', CommentViewSet)

urlpatterns = [
    path('me/', CurUserListView.as_view()),
    path('<int:ad_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:ad_pk>/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'update'})),
]

urlpatterns += router.urls
