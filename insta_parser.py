import time
from instagrapi import Client


class InstaParser:
    def __init__(self, bot_username, bot_password, username, log):
        self.bot_username = bot_username
        self.bot_password = bot_password
        self.username = username
        self.log = log
        self.user_id = ''
        self.followers_dict = {}
        self.followers_count = 0
        self.cl = Client()
        self.stop = False

    def login(self):
        self.log("Вход в аккаунт...")
        login_result = self.cl.login(self.bot_username, self.bot_password)
        if login_result:
            self.log("Успешно!")
            self.stop = False
            self.user_id = self.cl.user_id_from_username(self.username)
            self.followers_dict, self.followers_count = self.get_followers()

    def find_new_followers(self):
        self.send_message(f"Процесс обработки {self.username} запущен...")
        while not self.stop:
            print('timeout')
            time.sleep(60)
            print('start')
            followers_count_new = self.cl.user_info(self.user_id, use_cache=False).follower_count
            if self.followers_count != followers_count_new and followers_count_new > self.followers_count:
                self.send_message("Изменилось кол-во подписчиков, получение логинов...")
                time.sleep(120)
                followers_dict_new, followers_count_new = self.get_followers()
                new_followers = []
                for f_id in followers_dict_new:
                    if f_id not in self.followers_dict:
                        new_followers.append(self.cl.username_from_user_id(f_id))
                self.followers_dict = followers_dict_new
                self.followers_count = followers_count_new
                new_followers_string = ', '.join([str(f) for f in new_followers])
                self.send_message(
                    f'Подписался(лись): {new_followers_string}. Итого {followers_count_new} подписчика(ов).')
        else:
            self.send_message("Процесс обработки остановлен.")

    def get_followers(self):
        followers = self.cl.user_followers(self.user_id, use_cache=False).keys()
        return followers, len(followers)

    def send_message(self, message):
        self.log(message)
        print(message)

    def stop_parser(self):
        self.stop = True
