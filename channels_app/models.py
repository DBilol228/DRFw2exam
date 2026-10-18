from django.db import models
from myapp.models import Account
from django.utils.text import slugify

class Channel(models.Model):
    TYPE_CHOICES = [
        ("public","Public"),
        ("private","Private"),
    ]
    owner = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='channels')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20,choices=TYPE_CHOICES,default='public')
    slug = models.SlugField(max_length=200,unique=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.title)
            slug = original_slug
            number = 1
            while Channel.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{number}"
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class Following(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='channel_followings')
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE,related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','channel')
    def __str__(self):
        return f"{self.user} - {self.channel}"

class Post(models.Model):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.title