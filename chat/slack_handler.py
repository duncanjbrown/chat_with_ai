import logging
import os
import re
import llm

from slack_bolt import App

logger = logging.getLogger(__name__)

model = llm.get_model("gpt-3.5-turbo")
model.key = os.getenv('OPENAI_API_KEY')

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # disable eagerly verifying the given SLACK_BOT_TOKEN value
    token_verification_enabled=False,
)


@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    text = event['text']

    # this will not do well with mentions in the middle of the string
    cleaned_text = re.sub(r'<[^>]+>', '', text).strip()

    response = model.prompt(cleaned_text)

    logger.info(event)
    say(f"<@{event['user']}>\n\n*{cleaned_text}*.\n\n_{response.text()}_")
