from django.db import models
from myapp.models import Account

class Group(models.Model):
    title = models.CharField(max_length=150)
    owner = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='owned_groups')
    avatar = models.ImageField(upload_to='group_avatars/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class GroupMember(models.Model):
    ROLE_CHOICES = [
        ("owner","Owner"),
        ("admin","Admin"),
        ("member","Member")
        ]
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='members')
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='group_memberships')
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('group', 'user')
    def __str__(self):
        return f"{self.user} - {self.group}"

class GroupMessage(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='messages')
    author = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='group_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Group message {self.id}'