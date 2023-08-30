from django.contrib import admin
from .models import Chat, ChatUser, AIModel, ChatMessage

admin.site.register(Chat)
admin.site.register(ChatUser)
admin.site.register(AIModel)
admin.site.register(ChatMessage)

# Register your models here.
