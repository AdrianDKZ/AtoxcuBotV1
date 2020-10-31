import tweepy, time, json, random
import credentials

#####################
##### FUNCTIONS #####
#####################

###### FILES ######

def read_json(path):
    with open(path) as json_data:
        return json.load(json_data)

def write_json(path,data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file)

##### GET INFO #####

def getDMMentions(message):
    return message.message_create.get('message_data').get('entities').get('user_mentions')

def getSender(message):
    return message.message_create.get('sender_id')

##### TIME ACTIONS #####

##### Check if counters and files must be restarted
def checkTime(senders,victims):
    files={'senders':senders,'victims':victims}
    for key in counters:
        if counters[key] < sleepTime['total']:
            counters[key] = waitTime[key]
            files[key]={}
    return files['senders'],files['victims']

##### Sleep and rest time to counters
def sleep(sleepTime_):
    for key in counters:
        counters[key]-=sleepTime_
    time.sleep(sleepTime_)

##### ACTIONS #####

##### Error message if victim cannot receive tweet
def errorMsg(sender,victim):
    try:
        apiDM.send_direct_message(sender,"Me temo que no es posible enviar un tweet al usuario @"+victim+" debido a que recibió un tweet nuestro hace poco. Perdona las molestias. \n¡Un saludo!")
    except tweepy.TweepError as ex:
            print(ex,sender,victim)

##### Check if sender has made more petitions than allowed
def overPetitions(sender):
    if allSenders[sender][0]>=5:
        if allSenders[sender][1] is False:
            apiDM.send_direct_message(sender,"Lo siento, has superado el máximo de 5 peticiones por día.")
            allSenders[sender][1]=True
        return True
    return False

##### Check victim, +1 sender, tweet, DM and error DM
def atoxcu(sender,victim):
    allSenders[sender][0]+=1
    if victim in allVictims:
        errorMsg(sender,victim)
    else:
        allVictims[victim]=sender
        try:
            tweet = apiTW[random.randint(0,1)].update_status("¡Muy buenas, @"+victim+"! Alguien me ha pedido que le haga el favor de mandarte a tomar por culo.")
            apiDM.send_direct_message(sender,"¡Tweet enviado a @"+victim+"!\n"+"https://twitter.com/user/status/" + str(tweet.id))
        except tweepy.TweepError as ex:
            print(ex,sender,victim)
            if ex.args[0][0]['code']==187:
                errorMsg(sender,victim)

#######################
##### GLOBAL INFO #####
#######################

##### DIRECT MESSAGES AUTH #####
authDM=tweepy.OAuthHandler(credentials.DM_ApiKey,credentials.DM_ApiSecret)
authDM.set_access_token(credentials.DM_AccessToken,credentials.DM_AccessSecret)
apiDM=tweepy.API(authDM)

##### TWEETS 1 AUTH #####
authTW1=tweepy.OAuthHandler(credentials.TW1_ApiKey,credentials.TW1_ApiSecret)
authTW1.set_access_token(credentials.TW1_AccessToken,credentials.TW1_AccessSecret)
apiTW1=tweepy.API(authTW1)

##### TWEET 2 AUTH #####
authTW2=tweepy.OAuthHandler(credentials.TW2_ApiKey,credentials.TW2_ApiSecret)
authTW2.set_access_token(credentials.TW2_AccessToken,credentials.TW2_AccessSecret)
apiTW2=tweepy.API(authTW2)

##### LIST WITH BOTH TWEET AUTHS #####
apiTW=[apiTW1,apiTW2]


##### GLOBAL VARIABLES #####
me=apiDM.me().id_str
waitTime={'senders':86400,'victims':604800}
counters={'senders':86400,'victims':604800}
sleepTime={'total':90,'tweet':420}
# Get status at every execution
write_json("status.json",apiDM.rate_limit_status())

################
##### MAIN #####
################

def main():

    global allSenders
    global allVictims
    allSenders=read_json("senders.json")
    allVictims=read_json("victims.json")

    DMList=apiDM.list_direct_messages(50)
    #DMList.reverse()

    for DM in DMList:

        sender=getSender(DM)
        DMMentions=getDMMentions(DM)

        ##### MAIN CHECKINGS #####
        ##### Pass following DM if no mentions or i am the sender
        if len(DMMentions)<1 or sender==me:
            continue
        ##### If sender exists in file, check if over petitions. Otherwise, initialize it.
        if sender in allSenders:
            if overPetitions(sender) is True:
                apiDM.destroy_direct_message(DM.id)
                continue
        else:
            allSenders[sender]=[0,False]

        ##### LOOP ALL USERS MENTIONED #####
        for user in DMMentions:
            victim=user.get('screen_name')
            atoxcu(sender,victim)
            #### Sleep after tweet
            sleep(sleepTime['tweet'])
            ##### Leave loop if over mentions
            if overPetitions(sender) is True:
                break
        ##### Sleep if last mention of message
        apiDM.destroy_direct_message(DM.id)

    ##### COUNTERS CHECKING #####
    files=checkTime(allSenders,allVictims)

    ##### WRITE FILES #####
    write_json("senders.json",files[0])
    write_json("victims.json",files[1])

    sleep(sleepTime['total'])

while True:
    main()
