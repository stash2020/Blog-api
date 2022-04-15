from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.shortcuts import reverse

User = get_user_model()

# Create your models here.
class Post(models.Model):    
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)    
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    '''
    def get_api_url(self):
        try:
            return reverse("posts_api:post_detail", kwargs={"post_id": self.post_id})
        except:
            None
    '''

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter(parent=instance)
        return qs
    
    @property
    def likes(self):
        instance = self
        qs = Like.objects.filter(parent=instance)
        return qs
    


class Comment(models.Model):   
    comment_id = models.IntegerField(default=1) 
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class Like(models.Model):
    like_id = models.IntegerField(default=1) 
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
