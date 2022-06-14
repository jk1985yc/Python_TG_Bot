import logging, configparser, telegram

# Load data from config.ini file
config=configparser.ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger=logging.getLogger(__name__)

# To dict
CHAT_ID=dict(config.items('CHAT_ID'))

class TG:
    def __init__(self, content=None, id=None, file=None):
        self.bot = telegram.Bot(token=config.get('TELEGRAM','ACCESS_TOKEN'))
        self.id = id
        self.content=content
        self.file=file

    def send_message(self):
        self.bot.sendMessage(chat_id=self.id, text=self.content)

    def send_message_all(self):
        for id in CHAT_ID.values():
            self.bot.sendMessage(chat_id = id, text=self.content)

    def send_img_file(self):
        self.bot.sendPhoto(chat_id=self.id, caption=self.content, photo=open( self.file, 'rb'))

    def send_img_file_all(self):
        for id in CHAT_ID.values():
            self.bot.sendPhoto(chat_id=id, caption=self.content, photo=open( self.file, 'rb'))
