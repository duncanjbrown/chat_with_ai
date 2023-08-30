# Chat with AI

Local-only interface for chatting with AIs and recording the responses.

## Installation

```
python -m venv .venv
. ./.venv/bin/activate
pip install -r requirements-dev.txt
```

You will need to run django migrations before starting the server

```
python manage.py migrate
```

Start django:

`python manage.py startapp`

## Running the Slack bot

Running this app in development requires [ngrok](https://ngrok.com/).

Copy .env.example to .env and populate.

- Create a slack app via the UI and collect SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET: https://api.slack.com/start/building/bolt-python
- Run ngrok and place the URL of your tunnel in NGROK_HOST in the .env file

