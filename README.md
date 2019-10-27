# Assignment Slack Bot
This is a simple Slackbot is meant to help organize your weekly schedule with handy notifications for upcoming assignments/exams!

Supports the following commands: (WIP)
- help
- add
- remove
- complete
- update

# Getting Started
If you wish to run/install this Slackbot, you will need to have installed `python` and optionally `virtualenv`
```
$ brew install python3
$ brew install postgresql
$ pip3 install virtualenv
```

Next, close this repo and optionally enter activate the `virtualenv`
```
$ virtualenv assignment-bot
$ source assignment-bot/bin/activate
```

Install python dependencies using `pip`
```
(assignment-bot) $ pip install -r requirements.txt
```

Run the bot (WIP)
```
(assignment-bot) $ python3 assignment_bot.py
```