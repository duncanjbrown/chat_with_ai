import logging
import os
import re
import llm
from .models import Chat, AIModel, ChatUser, ChatMessage

from slack_bolt import App

logger = logging.getLogger(__name__)

llm_model = llm.get_model("gpt-3.5-turbo")
llm_model.key = os.getenv('OPENAI_API_KEY')

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # disable eagerly verifying the given SLACK_BOT_TOKEN value
    token_verification_enabled=False,
)

try:
    model = AIModel.objects.get(name="gpt3.5-turbo")
except AIModel.DoesNotExist:
    print("You don't have the gpt3.5-turbo model in your ai_models table yet. We need it so we can associate your chats with the model. Create it following the instructions in the readme.")
    exit()

chat = Chat(ai_model=model)

@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    # get user_id and find or create a local user
    slack_user_id = event["user"]
    try:
        user = ChatUser.objects.get(slack_user_id=slack_user_id)
    except ChatUser.DoesNotExist:
        user = ChatUser(slack_user_id=slack_user_id)

    slack_user = app.client.users_info(
        user=slack_user_id
    )
    user.name = slack_user["user"]["real_name"]
    user.save()

    # we could be cleverer about this and not repeat every time
    chat.user = user
    chat.save()

    text = event['text']

    # this will not do well with mentions in the middle of the string
    cleaned_text = re.sub(r'<[^>]+>', '', text).strip()

    ChatMessage(text=cleaned_text, message_type="user",chat=chat).save()

    response = llm_model.prompt(cleaned_text)

    ChatMessage(text=response.text(), message_type="assistant", chat=chat).save()

    logger.info(event)
    say(f"<@{event['user']}>\n\n*{cleaned_text}*.\n\n_{response.text()}_")
