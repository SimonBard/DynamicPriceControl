import requests
import os
from dotenv import load_dotenv

class Telegram():
    
    def message_personA(self, message):
        TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') 
        chat_id = os.getenv('TELEGRAM_personA_chat_id')
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        if TOKEN is not None:
            requests.get(url).json()  # this sends the message

    def message_personB(self, message):
        TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') 
        chat_id = os.getenv('TELEGRAM_personB_chat_id')

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        if TOKEN is not None:
            requests.get(url).json() # this sends the message

    def message_all(self, message):
        self.message_personA(message)
        self.message_personB(message)

def main():
    inst = Telegram()
    inst.message_all('My first message')


if __name__ == "__main__":
    main()