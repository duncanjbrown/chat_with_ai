from django.db import models


class ChatUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slack_user_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class AIModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # we will represent costs in integers representing a suitable fraction of a cent
    # because floating point numbers can be imprecise
    input_token_cost = models.IntegerField()
    completion_token_cost = models.IntegerField()


class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)


class ChatMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)

    ai_model = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()

    # better with an enum: user/system/assistant, but not sure how this generalises to other models yet
    message_type = models.CharField(max_length=255)
