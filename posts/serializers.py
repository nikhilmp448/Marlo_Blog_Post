from rest_framework import serializers
from .models import BlogPost,Vote,UserFeedback


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author','created_at','read_count','likes','dislikes']

class VoteSerializer(serializers.ModelSerializer):
    up_vote_by = serializers.ReadOnlyField(source='up_vote_by.email')
    down_vote_by=serializers.ReadOnlyField(source='down_vote_by.email')
    class Meta:
        model = Vote
        fields = ['id','post','up_vote_by','down_vote_by']

class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = UserFeedback
        fields = ['id', 'comment','commented_by','post']