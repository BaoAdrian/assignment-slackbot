from random import randint
import os, re, time, json, psycopg2
import slack

acceptable_greetings = [
    "hi",
    "hello",
    "hey",
    "howdy",
    "hi there",
]

greetings_quotes = [
    "Greetings!",
    "Hello human!",
    "How may I be of assistance?",
    "Howdy!",
    "Hi there!",
    "Oh good, I have someone to talk to now!",
    "What assignments can I process for you today?",
    "Sup?",
    "I've been alone for so long! Don't leave!"
]

do_assignment_quotes = [
    "Get on it!",
    "Chop Chop!!",
    "Better get started",
    "Don't procrastinate on this one...",
    "Plenty of time!"
]

invalid_quotes = [
    "Hmmm, I don't understand...",
    "NOPE! CAN'T DO THAT!",
    "According to my calculations, that input is invalid!",
    "It appears you do not abide by the rules of THE BOT",
    "Come again?",
    "Nah...",
    "That ain't it chief"
]

# Read data from secrets directory
data = {}
with open("secrets/secrets.json", "r") as f:
    data = json.load(f)

# Connect to database
try:
    conn = psycopg2.connect(user=data["DB_USER"],
                            password=data["DB_PASS"],
                            host=data["DB_HOST"],
                            port="5432",
                            database=data["DB_NAME"])
    cursor = conn.cursor()
except (Exception, psycopg2.Error) as error:
    print("Unanble to connect to database!")
    exit(1)

def parse_direct_mention(message_text):
    """
    Parses message_text String to extract channel and command strings

    @param message_text String value input by user on Slack
    @return (command, channel) tuple extracted from parameter text
    """
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command):
    # Default response is help text for the user
    default_response = "Hmmm, I didn't quite catch that. Try one of these: \n{}".format(generate_help_menu())
    response = None
    if command in acceptable_greetings:
        response = greetings_quotes[randint(0, len(greetings_quotes)-1)]
    elif command.startswith("help"):
        # Display help menu
        response = generate_help_menu()
    elif command.startswith("list"): 
        command = '-'.join(command.split(" ")) # format command
        if command == "list-all" or command == "list":
            psql = "SELECT * FROM assignments ORDER BY due ASC;"
            response = get_assignments(psql, "entered")
        elif command == "list-completed":
            psql = "SELECT * FROM assignments WHERE completed=TRUE ORDER BY due ASC;"
            response = get_assignments(psql, "completed")
        elif command == "list-todo" or command == "list-pending":
            psql = "SELECT * FROM assignments WHERE completed=FALSE ORDER BY due ASC;"
            response = get_assignments(psql, "pending")
        else:
            response = invalid_quotes[randint(0, len(invalid_quotes)-1)]
    elif command.startswith("add"):
        # Add assignment to database
        response = add_assignment(command.split(" "))
    elif command.startswith("complete"):
        assignment = ' '.join(command.split(" ")[1:])
        response = complete_assignment(assignment)
    elif command.startswith("remove") or command.startswith("delete"):
        assignment = ' '.join(command.split(" ")[1:])
        response = remove_assignment(assignment)
    elif command.startswith("update"):
        pass
    else:
        response = invalid_quotes[randint(0, len(invalid_quotes)-1)]

    return response or default_response

def generate_help_menu():
    return """
```
Usage:
$ [command] [assignment] [options]

Commands:
'help': Presents user with help menu
'list' or 'list-all': Lists all assignments 
'list-completed': Lists all completed assignments
'list-todo': Lists all pending assignments
'add' : Adds an assignment to database, defaulting as incomplete
    > add Project 2 10/24
'remove': Removes an assignment from database
    > remove Project 2
'complete': Marks assignment as complete
    > complete Project 2
'update': Updates fields of a specific assignment
    > update Project 2 due-date=10/31

Options:
due: Date when assignment is due in the format MM/DD (e.g. 09/28)
```
"""

def get_assignments(psql, tag):
    response = "Here is your list of `{}` assignments!\n```\n".format(tag)
    cursor.execute(psql)
    res = cursor.fetchall()
    if not res:
        return "No `{}` assignments found!".format(tag)
    max_len = max([len(row[1]) for row in res])
    response += ".{}.{}.{}.\n".format("-"*(max_len+5), "-"*10, "-"*7)
    response += "|{}|{}|{}|\n".format("Name".center(max_len + 5), "Due Date".center(10), "Done?".center(7))
    response += "|{}|{}|{}|\n".format("-"*(max_len+5), "-"*10, "-"*7)
    for row in res:
        date_str = "{}/{}".format(row[2].month, row[2].day)
        response += "|{}|{}|{}|\n".format(str(" " + row[1]).ljust(max_len + 5), str(" " + date_str).ljust(10), "Yes".center(7) if row[3] else "".ljust(7))
    response += "'{}'{}'{}'\n".format("-"*(max_len+5), "-"*10, "-"*7)
    response += "```"
    return response

def add_assignment(parts):
    assignment = ' '.join(parts[1:-1])
    dd_parts = parts[-1].split('/')
    due_date_str = "2019-{}-{}".format(dd_parts[0], dd_parts[1])
    psql = """
    INSERT INTO assignments (name, due, completed) 
        VALUES ('{}', '{}', false);""".format(assignment, due_date_str)
    cursor.execute(psql)
    conn.commit()
    response = "Added `{}` with a due date of `{}`! {}".format(assignment, due_date_str, do_assignment_quotes[randint(0, len(do_assignment_quotes)-1)])
    return response

def complete_assignment(assignment):
    # First check to make sure assignment exists
    psql = "SELECT * FROM assignments WHERE name='{}';".format(assignment)
    cursor.execute(psql)
    res = cursor.fetchall()
    if len(res) == 0 :
        return "Hmmm, couldn't find `{}`! Try another assignment.".format(assignment)
    elif len(res) > 1:
        return "Looks like you have multiple entries for `{}`. Please remove one!".format(assignment)
    
    psql = "UPDATE assignments SET completed=TRUE WHERE name='{}';".format(assignment)
    cursor.execute(psql)
    conn.commit()
    return "Marking `{}` as completed! Great Job!".format(assignment) 

def remove_assignment(assignment):
    psql = "SELECT * FROM assignments WHERE name='{}';".format(assignment)
    cursor.execute(psql)
    res = cursor.fetchall()
    if len(res) == 0 :
        return "Hmmm, couldn't find `{}`! Try another assignment.".format(assignment)
    
    psql = "DELETE FROM assignments WHERE name='{}';".format(assignment)
    cursor.execute(psql)
    conn.commit()
    return "Successfully removed `{}` from you assignments!".format(assignment)

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']

    user_id, command = parse_direct_mention(data["text"])

    # Authenticatae bot_id
    bot_id = web_client.api_call("auth.test")["user_id"]
    if bot_id == user_id:
        response = handle_command(command)

        # rtm_client = payload['rtm_client']
        web_client.chat_postMessage(
            channel=data["channel"],
            text=response
        )

if __name__ == "__main__":
    print("Starting Bot...")
    rtm_client = slack.RTMClient(token=data["BOT_USER_ACCESS_TOKEN"])
    rtm_client.start()
