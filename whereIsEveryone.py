from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.forcereply import ForceReply

# Global variables
baseUrl = 'https://maps.googleapis.com/maps/api/staticmap'
key = 'AIzaSyBC9KPbyRovhnqIHhhLm460aphgzi65kxk'

locationArray = []

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
        text="Ok, I'll need to gather all of your locations, if you want"
        + " to participate, send me the command /me")
    gatherLoc(bot,update.message.chat_id)

def askLoc(bot, update):
    user = update.message.from_user.first_name
    
    bot.sendMessage(chat_id=update.message.chat_id, 
        reply_markup=ForceReply(force_reply=True, selective = True),
        reply_to_message_id=update.message.message_id,
        text="Send me your location, " + user)

def getLoc(bot, update):
    userName = update.message.from_user.first_name
    userId  = update.message.from_user.id
    longitude = update.message.location.longitude
    latitude  = update.message.location.latitude

    addLocToArr(userId, userName, longitude, latitude)

def addLocToArr(userId, userName, longitude, latitude):
    global locationAarray
    
    locObj = {
        "id" : userId,
        "userName": userName,
        "longitude" : longitude,
        "latitude"  : latitude
    }

    upD = [obj for obj in locationArray if obj["id"] == locObj["id"]]
        
    if len(upD) == 0:
        locationArray.append(locObj)
        print("Added " + locObj["username"]
            + " at location " + str(locObj["longitude"])
            + ", " + str(locObj["latitude"]))
    else:
        upD[0]["latitude"] = locObj["latitude"]
        upD[0]["longitude"] = locObj["longitude"]
        print("Updated location of " + upD[0]["userName"]
            + " to " + str(upD[0]["latitude"])
            + ", " + str(upD[0]["longitude"]))
            
    # TODO: Add error management in case it doesn't work

def calculateCentrum():
    maxY = max([obj["longitude"] for obj in locationArray])
    minY = min([obj["longitude"] for obj in locationArray])
    maxX = max([obj["latitude"] for obj in locationArray])
    minX = min([obj["latitude"] for obj in locationArray])
    centerY = (maxY + minY) / 2
    centerX = (maxX + minX) / 2
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

    # Add all the longs and lats for each location object
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
    bot.sendPhoto(chat_id=update.message.chat_id, photo=url)

def gatherLoc(bot,chatId):
    global locationArray
    locationArray = []

def main():
    updater = Updater(token='320338185:AAE2toXmrb-EKXPFNW_EoJoJ5CGY3tUzi0A')

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

if __name__ == "__main__":
    main()
