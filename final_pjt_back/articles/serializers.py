from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    is_author = serializers.SerializerMethodField()  # 추가

    class Meta:
        model = Comment
        fields = ('id', 'content', 'username', 'created_at', 'updated_at', 'is_author')
        read_only_fields = ('user',)

    def get_is_author(self, obj):  # 추가
        user = self.context['request'].user
        return obj.user == user


class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()  # 추가

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'username', 'comments', 
                'like_count', 'is_liked', 'is_author', 'created_at', 'updated_at')
        read_only_fields = ('user', 'likes')

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all() if user.is_authenticated else False

    def get_is_author(self, obj):  # 추가
        user = self.context['request'].user
        return obj.user == user
