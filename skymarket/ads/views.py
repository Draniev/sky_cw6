from ads.models import Ad, Comment
from ads.permissions import IsOwner, ReadOnly
from ads.serializers import AdDetailSerializer, AdSerializer, CommentSerializer
from rest_framework import pagination, status, viewsets
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


class AdPagination(pagination.PageNumberPagination):
    pass


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [ReadOnly | IsOwner | IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AdDetailSerializer(instance)
        return Response(serializer.data)


class CurUserListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        self.queryset = Ad.objects.filter(author__exact=request.user)
        return super().get(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ReadOnly | IsOwner | IsAdminUser]

    # ok
    def list(self, request, ad_pk=None):
        queryset = Comment.objects.filter(ad_id__exact=ad_pk)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # ok
    def retrieve(self, request, ad_pk=None, pk=None):
        queryset = Comment.objects.filter(ad_id__exact=ad_pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    # ok
    def create(self, request, ad_pk=None):
        data = request.data
        # data['ad'] = get_object_or_404(Ad.objects.all(), pk=ad_pk)
        data['ad'] = ad_pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # ok
    def update(self, request, pk=None, ad_pk=None, **kwargs):
        queryset = Comment.objects.filter(ad_id__exact=ad_pk)
        # return super().update(self, request, **kwargs)
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # ok
    def destroy(self, request, pk=None, ad_pk=None):
        queryset = Comment.objects.filter(ad_id__exact=ad_pk)
        instance = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
