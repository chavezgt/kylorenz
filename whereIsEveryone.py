from telegram.ext import Updater
from telegram import InlineKeyboardButton
from telegram.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.forcereply import ForceReply
from telegram.ext import CommandHandler, MessageHandler, Filters
from threading import Timer


updater = Updater(token='320338185:AAE2toXmrb-EKXPFNW_EoJoJ5CGY3tUzi0A')

force_reply = ForceReply(
        force_reply=True
        )
gathering = False
locationArray = []

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
            text="Ok, I'll need to gather all of your locations, if you want"
            +"to participate, send me the command /me")
    gatherLoc(bot,update.message.chat_id)

def askLoc(bot, update):
    user = update.message.from_user.first_name
    
    bot.sendMessage(chat_id=update.message.chat_id, 
            reply_markup=force_reply,
            text="Send me your location, " + user)

def getLoc(bot, update):
            userName = update.message.from_user.first_name
            userId  = update.message.from_user.id
            longitude = update.message.location.longitude 
            latitude  = update.message.location.latitude 
            addLocToArr(userId, userName, longitude, latitude)

def addLocToArr(userId, userName, longitude, latitude):
    global gathering
    global locationAarray
    locObj = {"id" : userId,
              "userName": userName,
              "longitude" : longitude,
              "latitude"  : latitude}
    if(gathering):
        locationArray.append(locObj)
    print("added " + str(locObj))
    #ADD ERROR MANAGEMENT in case it doesn't work


def giveLocs(bot,chatId):
    bot.sendMessage(chat_id=chatId,
            text=str(locationArray))
    print(str(locationArray))



def gatherLoc(bot,chatId):
    global gathering 
    gathering = True
    global locationArray 
    locationArray= []
    t = Timer(30.0, giveLocs, [bot,chatId])
    t.start()








start_handler = CommandHandler('start', start)
loc_handler = CommandHandler('me', askLoc)
locadd_handler = MessageHandler(Filters.location, getLoc)

dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(loc_handler)
dispatcher.add_handler(locadd_handler)


updater.start_polling()
