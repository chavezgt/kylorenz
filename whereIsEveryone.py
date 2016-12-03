from telegram.ext import Updater
from telegram import InlineKeyboardButton
from telegram.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.forcereply import ForceReply
from telegram.ext import CommandHandler, MessageHandler, Filters
import requests
from threading import Timer

baseUrl = 'https://maps.googleapis.com/maps/api/staticmap'
updater = Updater(token='320338185:AAE2toXmrb-EKXPFNW_EoJoJ5CGY3tUzi0A')
key = 'AIzaSyBC9KPbyRovhnqIHhhLm460aphgzi65kxk'

force_reply = ForceReply(
        force_reply=True,
        selective = True
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
            reply_to_message_id=update.message.message_id,
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
        if locObj["id"] not  in [obj["id"] for obj in locationArray]:
            locationArray.append(locObj)
        else:
            upD =[ obj for obj in locationArray if obj["id"] == locObj["id"]][0]
            upD["latitude"] = locObj["latitude"]
            upD["longitude"] = locObj["longitude"]
            
    print("added " + str(locObj))
    #ADD ERROR MANAGEMENT in case it doesn't work

def calculateCentrum():
       maxY = max([obj["longitude"] for obj in locationArray] )
       minY = min([obj["longitude"] for obj in locationArray] )
       maxX = max([obj["latitude"] for obj in locationArray] )
       minX = min([obj["latitude"] for obj in locationArray] )
       centerY = (maxY + minY )/2
       centerX = (maxX + minX )/2
       return [centerX, centerY]


def constructUrl():
    url = baseUrl + '?'
    url += 'size=1024x1024&'
    center = calculateCentrum()
    url += 'center='
    url += str(center[0])
    url += ','
    url += str(center[1])
    url += '&'
    url += 'key=' + key
    url += '&'
    #label name
    #add all the longs and lats for each location object
    for obj in locationArray:
        url += 'markers=color:blue%7Clabel:'
        url += str(obj["userName"])[0].upper()
        url += '%7C'
        url += str(obj["latitude"])
        url += ','
        url += str(obj["longitude"])
        url += '&'
        

    return url

def giveLocs(bot,update):
    url=constructUrl()
    print(url)
    bot.sendPhoto(chat_id=update.message.chat_id,
            photo=url)
    print(str(locationArray))



def gatherLoc(bot,chatId):
    global gathering 
    gathering = True
    global locationArray 
    locationArray= []
    #t = Timer(30.0, giveLocs, [bot,chatId])
    #t.start()

start_handler = CommandHandler('start', start)
loc_handler = CommandHandler('me', askLoc)
locadd_handler = MessageHandler(Filters.location, getLoc)
makemap_handler = CommandHandler('now',giveLocs)

dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(loc_handler)
dispatcher.add_handler(locadd_handler)
dispatcher.add_handler(makemap_handler)


updater.start_polling()
