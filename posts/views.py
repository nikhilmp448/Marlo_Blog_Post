from .models import BlogPost,Vote,UserFeedback
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from .serializers import BlogSerializer,VoteSerializer,CommentSerializer
from rest_framework import viewsets,serializers,permissions
from.permission import IsAdminUser,hasSelfVotedOrReadOnly,IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404


class BlogList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'posts.html'

    def get(self, request):
        queryset = BlogPost.objects.all()
        return Response({'posts': queryset})

class PostDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_details.html'

    def get(self, request, pk):
        queryset = BlogPost.objects.get(id = pk)
        serializer = BlogSerializer(queryset,many=False)
        BlogPost.objects.filter(id = pk).update(read_count = F('read_count')+1)
        print(queryset.image)
        return Response({'serializer': serializer, 'post': queryset})


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminUser]


class VoteViewSet(viewsets.ModelViewSet):
    queryset=Vote.objects.all()
    serializer_class=VoteSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,hasSelfVotedOrReadOnly]
    def perform_create(self, serializer):
        post_instance=get_object_or_404(BlogPost,pk=self.request.data['post'])

        #if user likes the post
        if self.request.data['vote']:
            already_up_voted=Vote.objects.filter(post=post_instance,up_vote_by=self.request.user).exists()
            if already_up_voted:
                raise serializers.ValidationError({"message":"You have already liked this post"})
            else:
                if_downvoted =Vote.objects.filter(post=post_instance,down_vote_by=self.request.user).first()
                if (if_downvoted):
                    if_downvoted.delete()
                serializer.save(up_vote_by=self.request.user,post=post_instance)
        #if dislikes
        else:
            already_down_voted=Vote.objects.filter(post=post_instance,down_vote_by=self.request.user).exists()
            if already_down_voted:
                raise serializers.ValidationError({"message":"You have already disliked this post"})
            else:
                if_upvoted =Vote.objects.filter(post=post_instance,up_vote_by=self.request.user).first()
                if (if_upvoted):
                    if_upvoted.delete()
                serializer.save(down_vote_by=self.request.user,post=post_instance)


class CommentViewSet(viewsets.ModelViewSet):
    """Comments"""
    queryset = UserFeedback.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
