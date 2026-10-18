from django.db import models
from myapp.models import Account

class Profile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    username = models.CharField(max_length=50,unique=True)
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    bio = models.TextField(blank=True)
    def __str__(self):
        return self.username

class Avatar(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='avatars')
    image = models.ImageField(upload_to='avatars/')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.profile.username