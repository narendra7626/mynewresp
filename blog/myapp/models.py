from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title
class UserProfile(models.Model):
    user=models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
    gender=models.CharField(max_length=100)
    image=models.ImageField(upload_to='profile_pics')

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='post_pics')
    detail=models.TextField()
    create_date=models.DateTimeField(default=timezone.now)
    publish_date=models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.publish_date=timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approve_comments=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=264)
    title=models.TextField()
    create_date=models.DateTimeField(default=timezone.now)
    approve_comments=models.BooleanField(default=False)

    def approve(self):
        self.approve_comments=True
        self.save()




