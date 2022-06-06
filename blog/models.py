from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.author} : {self.content}'
    
    def get_absolute_url(self):
        return reverse('blog-home')
