# Assignment Slack Bot
This is a simple Slackbot is meant to help organize your weekly schedule with handy notifications for upcoming assignments/exams!

[Supports the following commands:](#supported-commands)
- [help](#help)
- [list](#list)
- [add](#add)
- [remove](#remove)
- [complete](#complete)
- [update](#update)

# Getting Started
If you wish to run/install this Slackbot, you will need to have installed `python` and optionally `virtualenv`
```
$ brew install python3
$ brew install postgresql
$ pip3 install virtualenv
```

Next, clone this repo and optionally activate/enter the `virtualenv`
```
$ virtualenv bot
$ source bot/bin/activate
```

Install python dependencies using `pip`
```
(bot) $ pip install -r requirements.txt
```

Run the bot (WIP)
```
(assignment-bot) $ python3 assignment_bot.py
```

# Supported Commands
## Help
Lists the help menu detailing the acceptable commands

## List
Lists the given assignments, filtered by provided commmand:
1. `list` OR `list-all`
   - Lists ALL assignments, _completed or not_, in a formatted table
2. `list-completed`
   - Only lists assignments marked/entered as _completed_
3. `list-todo`
   - Only lists assignments that are still _pending_
```
list
list-all
list-completed
list-todo
```

## Add
Adds a given assignment to the database with a corresponding due date
```
add [assignment] [due-date]
```

Example:
```
add Project 5 - The Traveling Salesman 11/07
```

## Remove
Removes an assignment from the database
```
remove [assignment]
```

Example:
```
remove Project 5 - The Traveling Salesman
```

## Complete
Marks a given assignment as completed (updating the `completed` columm to _TRUE_)
```
complete [assignment]
```

Example:
```
complete Project 5 - The Traveling Salesman
```

## Update
Updates a given assignment, updating a specific field for the corresponding assignment
WIP