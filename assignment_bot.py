import os
import time
import re
import json
from slackclient import SlackClient

# Read data from secrets directory
data = {}
with open("secrets/tokens.json", "r") as f:
    data = json.load(f)

# instantiate Slack client
slack_client = SlackClient(data["BOT_USER_ACCESS_TOKEN"])

# bots's user ID in Slack: value is assigned after the bot starts up
bot_id = None
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "add [assignment] [due date]"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id:
                print("here")
                print("{} > {}".format(message, event["channel"]))
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    # Default response is help text for the user
    default_response = "Hmmm, I didn't quite catch that. Try *{}*.".format(EXAMPLE_COMMAND)
    response = None
    if command.startswith("help"):
        response = "How may I help?"
    elif command.startswith("add"):
        # Parse the command
        parts = command.split(" ")
        assignment = parts[1]
        due_date = parts[2]
        response = "Adding `{}` which is due on `{}`".format(assignment, due_date)
    elif command.startswith("complete"):
        parts = command.split(" ")
        assignment = parts[1]
        response = "Marking `{}` as completed! Great Job!".format(assignment)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            print("{} : {}".format(command, channel))
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")