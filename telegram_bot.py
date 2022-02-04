import telebot
import time
from insta_parser import InstaParser
from config import BotSettings, BotReplyText

bot = telebot.TeleBot(BotSettings.BOT_TOKEN.value)


class TeleInstaBot:
    def __init__(self, chat_id, ibot_username, ibot_password, username):
        self.bot = bot
        self.chat_id = chat_id
        self.ibot_username = ibot_username
        self.ibot_password = ibot_password
        self.username = username
        self.log = lambda text: bot.send_message(self.chat_id, text)
        self.insta_parser = InstaParser(self.ibot_username, self.ibot_password, self.username, self.log)

    def main(self):
        try:
            self.stop_parser()
            self.insta_parser.login()
            self.insta_parser.find_new_followers()
        except KeyboardInterrupt:
            print("\nStopping...")
        except Exception as err:
            self.log('Error: ' + str(err))
            print(err)
            self.restart()

    def stop_parser(self):
        self.insta_parser.stop_parser()

    def restart(self):
        self.log('Try to restart...')
        self.stop_parser()
        sleep(300)
        self.log('Timeout 5 min for re-login...')
        main()


tele_insta_bot = None


@bot.message_handler(commands=['start'])
def start(message):
    get_data(message)


@bot.message_handler(commands=['stop'])
def stop(message):
    if tele_insta_bot:
        tele_insta_bot.stop_parser()
        bot.send_message(message.chat.id, 'Stopped.')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, BotReplyText.REPLY_HELP_TEXT.value)


def get_data(message):
    bot.send_message(message.chat.id, "Введите имя аккаунта для логина")
    bot.register_next_step_handler(message, get_username)


def get_username(message):
    if not message_is_command(message):
        bot.send_message(message.from_user.id, "Введите пароль для логина")
        bot.register_next_step_handler(message, get_pass, username=message.text)


def get_pass(message, username):
    if not message_is_command(message):
        bot.send_message(message.from_user.id, "Введите имя аккаунта, информацию с которого собирать")
        bot.register_next_step_handler(message, get_to_download, username, password=message.text)


def get_to_download(message, username, password):
    if not message_is_command(message):
        global tele_insta_bot
        tele_insta_bot = TeleInstaBot(chat_id=message.chat.id,
                                      ibot_username=username,
                                      ibot_password=password,
                                      username=message.text)
        tele_insta_bot.main()


def message_is_command(message):
    if message.text == '/start':
        stop(message)
        start(message)
        return True
    elif message.text == '/stop':
        stop(message)
        return True
    elif message.text == '/help':
        return False
    else:
        return False


bot.polling(none_stop=True, interval=0)
