from rest_framework.viewsets import (ReadOnlyModelViewSet,
                                     ModelViewSet, GenericViewSet)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from posts.models import Group, Post
from .serializers import (GroupSerializer, PostSerializer,
                          FollowSerializer, CommentSerializer)
from .permissions import IsAuthorOrReadOnly


class GroupViewSet(ReadOnlyModelViewSet):
    """Вьюсет для обработки групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


class PostViewSet(ModelViewSet):
    """Вьюсет для обработки постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(CreateModelMixin,
                    ListModelMixin,
                    GenericViewSet
                    ):
    """Вьюсет для обработки подписок."""
    serializer_class = FollowSerializer
    filter_backends = [SearchFilter]
    search_fields = ('user__username', 'following__username')
    permission_classes = (
        IsAuthenticated,
        IsAuthorOrReadOnly,
    )
    filter_backends = 
        SearchFilter,
    )
    search_fields = (
        'following__username',
    )
    pagination_class = None

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(
            author=self.request.user,
            post=post)
