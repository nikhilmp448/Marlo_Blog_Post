
from django.db import models
from users.models import Account

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    file = models.FileField(upload_to='blog_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_count = models.PositiveIntegerField(default=0)

class UserFeedback(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comments = models.TextField(default=None,blank=True,null=True)
    aprooval = models.BooleanField(default=False)

class Vote(models.Model):
    post=models.ForeignKey(BlogPost,related_name='votes',on_delete=models.CASCADE)
    up_vote_by = models.ForeignKey(Account,related_name='up_vote_user',on_delete=models.CASCADE,default=None,blank=True,null=True)
    down_vote_by=models.ForeignKey(Account,related_name='down_vote_user',on_delete=models.CASCADE,default=None,blank=True,null=True)
    def __str__(self):
        return self.post.content
