from rest_framework import routers
from django.urls import include, path

from .views import (PostViewSet,
                    CommentViewSet,
                    GroupViewSet,
                    FollowViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('follow', FollowViewSet, basename='follow')

v1_patterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
