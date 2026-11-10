from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.title

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default="IFOKONBALE")
    cover = models.ImageField(upload_to='covers/')
    audio = models.FileField(upload_to='songs/')
    release_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.title} - {self.artist}"