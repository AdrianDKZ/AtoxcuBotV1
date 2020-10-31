# AtoxcuBotV1
Current version of the Twitter bot @AtoxcuBot

In addition to the main Python file this program will need of:

**Credentials.py**:
It will store the credentials of the Twitter app.

**Victims.json**
A dict that will store as key the user who recently received a tweet and the ID of the user who requested it.
It will be restarted after a week.
> {"victim": id_sender}

**Senders.json**
A dict that will store the user who has recently request for a tweet as key and, as value, a list with the number of tweets he has sent and a boolean to indicate if he has already pass the limit.
It will be restarded once a day.
> {"sender": [x,False]}
