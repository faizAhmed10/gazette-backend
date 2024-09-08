from rest_framework import serializers
from api.models import *
from api.serializers.userSerializer import *
from api.serializers.articleSerializer import *

class CommentSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at', 'article', 'parent', 'replies']

    def get_replies(self, obj):
        # Return only direct replies to this comment
        replies = obj.replies.all()
        if replies.exists():
            return CommentSerializer(replies, many=True).data
        return []  # Return an empty list if no replies

