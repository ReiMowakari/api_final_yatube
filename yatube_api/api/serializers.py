from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Post."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Group."""

    class Meta:
        model = Group
        fields = (
            'id', 'title', 'slug', 'description'
        )


class FollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Follow."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Подписка на автора ранее уже была оформлена!')
            ),
        )

    def validate_following(self, value):
        """Запрещающий метод для подписки на самого себя."""
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'К сожалению, подписаться на самого себя нельзя!')
        return value
