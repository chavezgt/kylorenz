from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.forcereply import ForceReply

import key_extractor

class FriendLocationBot:
    def __init__(self, telegramToken, googleKey):
        self.baseUrl = 'https://maps.googleapis.com/maps/api/staticmap'
        self.key = googleKey

        self.minLongitude = 13.082634
        self.maxLongitude = 13.766688
        self.minLatitude = 52.337776
        self.maxLatitude = 52.676643

        self.locationArray = []

        start_handler = CommandHandler('start', self.start)
        loc_handler = CommandHandler('me', self.askLoc)
        makemap_handler = CommandHandler('now', self.giveLocs)
        locadd_handler = MessageHandler(Filters.location, self.getLoc)

        self.updater = Updater(token=telegramToken)
        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(loc_handler)
        dispatcher.add_handler(locadd_handler)
        dispatcher.add_handler(makemap_handler)

    def run(self):
        self.updater.start_polling()

    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id,
            text="Ok, I'll need to gather all of your locations, if you want"
            + " to participate, send me the command /me")
        locationArray = []

    def askLoc(self, bot, update):
        user = update.message.from_user.first_name
        
        bot.sendMessage(chat_id=update.message.chat_id, 
            reply_markup=ForceReply(force_reply=True, selective = True),
            reply_to_message_id=update.message.message_id,
            text="Send me your location, " + user)

    def getLoc(self, bot, update):
        userName = update.message.from_user.first_name
        userId  = update.message.from_user.id
        longitude = update.message.location.longitude
        latitude  = update.message.location.latitude

        if (longitude < self.minLongitude or longitude > self.maxLongitude
            or latitude < self.minLatitude or latitude > self.maxLatitude):
            text = "I didn't add the location you provided because it is outside of Berlin."
            text += " Please give me a location in Berlin"

            bot.sendMessage(chat_id=update.message.chat_id, 
                reply_to_message_id=update.message.message_id,
                text=text)

            return

        locObj = {
            "id" : userId,
            "userName": userName,
            "longitude" : longitude,
            "latitude"  : latitude
        }

        upD = [obj for obj in self.locationArray if obj["id"] == locObj["id"]]
            
        if len(upD) == 0:
            self.locationArray.append(locObj)
            
            text = "Added " + locObj["userName"]
            text += " at location " + str(locObj["longitude"])
            text += ", " + str(locObj["latitude"])
        else:
            upD[0]["latitude"] = locObj["latitude"]
            upD[0]["longitude"] = locObj["longitude"]
 
            text = "Updated location of " + upD[0]["userName"]
            text += " to " + str(upD[0]["latitude"])
            text += ", " + str(upD[0]["longitude"])

        bot.sendMessage(chat_id=update.message.chat_id, text=text)

    def giveLocs(self, bot, update):
        url = self.constructUrl()
        bot.sendPhoto(chat_id=update.message.chat_id, photo=url)

    def constructUrl(self):
        url = self.baseUrl + '?'
        url += 'size=1024x1024&'
        center = self.calculateCenter()
        url += 'center='
        url += str(center[0])
        url += ','
        url += str(center[1])
        url += '&'
        url += 'key=' + self.key
        url += '&'

        # Add all the longs and lats for each location object
        for obj in self.locationArray:
            url += 'markers=color:blue%7Clabel:'
            url += str(obj["userName"])[0].upper()
            url += '%7C'
            url += str(obj["latitude"])
            url += ','
            url += str(obj["longitude"])
            url += '&'

        return url

    def calculateCenter(self):
        maxY = max([obj["longitude"] for obj in self.locationArray])
        minY = min([obj["longitude"] for obj in self.locationArray])
        maxX = max([obj["latitude"] for obj in self.locationArray])
        minX = min([obj["latitude"] for obj in self.locationArray])
        centerY = (maxY + minY) / 2
        centerX = (maxX + minX) / 2
        return (centerX, centerY)

if __name__ == "__main__":
    flb = FriendLocationBot(key_extractor.getKey("telegram"),
        key_extractor.getKey("google"))
    flb.run()
