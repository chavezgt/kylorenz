# All print statements for debugging purposes only
# This file should probably be renamed

import requests
import lbot

INITIAL_ID = 263969345
LONG_POLLING_TIMEOUT = 60
ADDRESS = ''
MAX_UPDATES = 10
BOT_USERNAME = 'KleinLuisBot'
NEW_MEMBER_MESSAGE = 'Hi. I\'m a bot that makes fun of Luis. Send the command /luis and I\'ll make fun of him.'

class Message:
    # Minimum necessary parameters are text and chat_id
    def __init__ (self, text, chat_id):
      self.text = text
      self.chat_id = chat_id
      self.dict = {'text': self.text, 'chat_id': self.chat_id}
    
    # Getter for the dictionary
    def toDict(self):
      return self.dict

    # Add an extra key val pair
    def addKeyPair(self, key, val):
      self.dict[key] = val

class LuisBot:
  def run(self):
    # For initialization
    self.last_id = -100

    # Forever
    while True:
      incoming_updates = self.getUpdates()
      
      for update in incoming_updates:
        self.processUpdate(update)
  
  def processUpdate(self, update):
    keys = update.keys()

    if 'update_id' not in keys:
      # This isn't a proper update object
      return

    update_id = update['update_id']
    print('Update with id ' + str(update_id) + ' recieved')

    # Check if this update contains a message
    if 'message' in keys:
      print(' Update contains a message')
      self.processMessage(update['message'])

    self.last_id = update_id

  def processMessage(self, message):
    keys = message.keys()

    if 'chat' in keys:
      chat = message['chat']
      
      if 'id' in chat.keys():
        chat_id = chat['id']
        
        if 'text' in keys:
          text = message['text']
        
          print('  Message is a text message: ' + message['text'])
        
          if text == '/luis':
            print('   Text contains a valid command: ' + text + '. Sending response...')
            sendMessage(Message(lbot.getLuisWord(), chat_id))

        elif 'new_chat_member' in keys:
          if 'username' in message['new_chat_member']:
            if message['new_chat_member']['username'] == BOT_USERNAME:
              sendMessage(Message(NEW_MEMBER_MESSAGE, chat_id))


  def getUpdates(self):
    arguments = {'offset': self.last_id + 1, 'limit': MAX_UPDATES, 'timeout': LONG_POLLING_TIMEOUT}

    # 1.5 * LONG_POLLING_TIMEOUT so that the respone
    # from the server has time to reach us
    json_response = sendReq('getUpdates', arguments, 1.5 * LONG_POLLING_TIMEOUT)

    if 'ok' in json_response.keys():
      if json_response['ok'] is True:
        if 'result' in json_response.keys():
          return json_response['result']

    return None

def sendMessage(message):
  arguments = message.toDict()
  arguments['parse_mode'] = 'HTML'

  json_response = sendReq('sendMessage', arguments)
  
  if 'ok' in json_response.keys():
    if json_response['ok'] is True:
      print('   Response sent successfully: ' + message.text)

# This method is outside of the class for now,
# since it's a generic request to the Telegram Bot API
# The response is converted to a JSON object because
# all Telegram Bot API responses are in JSON format
def sendReq(command, arguments, timeout=None):
  while True:
    try:
      return requests.get(ADDRESS + command, params=arguments, timeout=timeout).json()
    except requests.exceptions.RequestException:
      pass
