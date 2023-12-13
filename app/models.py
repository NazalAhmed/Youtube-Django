from django.db import models

from django.contrib.auth.models import User

class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subscribers = models.ManyToManyField(User, related_name='subscribed_channels', blank=True)
    profile_picture = models.ImageField(upload_to='images/', default='images/default_pfp.png')

    def __str__(self):
        return self.name

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    upload_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='images/')

    view = models.ManyToManyField(User, related_name='video_view', blank=True)
    likes = models.ManyToManyField(User, related_name='video_like', blank=True)
    dislikes = models.ManyToManyField(User, related_name='video_dislike', blank=True)

    def number_of_views(self):
        return self.view.count()

    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.user.username} : {self.video.title}"