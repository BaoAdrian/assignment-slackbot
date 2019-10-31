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

## List
```
list
list-all
list-completed
list-todo
```

## Add
```
add [assignment] [due-date]
```

Example:
```
add Project 5 - The Traveling Salesman 11/07
```

## Remove
```
remove [assignment]
```

Example:
```
remove Project 5 - The Traveling Salesman
```

## Complete
```
complete [assignment]
```

Example:
```
complete Project 5 - The Traveling Salesman
```

## Update
WIP