from django.db import models
from django.core.exceptions import ValidationError
from myapp.models import Account

class Chat(models.Model):
    user_1 = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='chats_as_user_1')
    user_2 = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='chats_as_user_2')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_1', 'user_2'],
                name='unique_chat_pair'
            ),
            models.CheckConstraint(
                condition=~models.Q(user_1=models.F('user_2')),
                name='different_chat_users'
            )
        ]
    def save(self, *args, **kwargs):
        if self.user_1_id == self.user_2_id:
            raise ValidationError("You cannot create a chat with yourself.")
        if self.user_1_id > self.user_2_id:
            self.user_1_id, self.user_2_id = self.user_2_id, self.user_1_id
        chat_exists = Chat.objects.filter(user_1_id=self.user_1_id,user_2_id=self.user_2_id).exclude(pk=self.pk).exists()
        if chat_exists:
            raise ValidationError("This chat already exists.")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user_1} - {self.user_2}"

class Message(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message {self.id}"