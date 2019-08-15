from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseRedirect

from groups.models import Group

from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.

class Post(models.Model):
    user=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    message=models.TextField()
    message_html=models.TextField(editable=False)
    group=models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.CASCADE)
    image = models.ImageField(blank=True,upload_to="posts",null=True)
    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username,
                                                'pk':self.pk})

    class Meta:
        ordering=['-created_at']
        unique_together=['user','message']

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    comment_writer=models.ForeignKey(User,related_name='wrote',on_delete=models.CASCADE,blank=True,null=True)
    text=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.post.user.username,'pk':self.post.pk})
    def __str__(self):
        return self.text
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
    class Meta:
        ordering=['-created_at']
