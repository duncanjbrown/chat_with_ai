from django.db import models


class ChatUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slack_user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class AIModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # we will represent costs in integers representing 1/10,000th of a cent
    # because floating point numbers can be imprecise.
    name = models.CharField(max_length=255)
    input_token_cost = models.IntegerField()
    completion_token_cost = models.IntegerField()

    class Meta:
        verbose_name = "AI model"

class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)


class ChatMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()

    # better with an enum: user/system/assistant, but not sure how this generalises to other models yet
    message_type = models.CharField(max_length=255)
