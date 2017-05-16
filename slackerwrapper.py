from slacker import Slacker
import json
import threading
import queue
import http.client


class SlackerWrapper():
    def __init__(self):
        try:
            with open('token', 'r') as f: token = f.readline().strip()
        except: raise Exception("Document 'token' needs to exist")

        self.slacker = Slacker(token)
        self.ch_his = {}
        self.fetch()

    def has_internet(self):
        conn = http.client.HTTPConnection("www.google.com", timeout=5)
        try:
            conn.request("HEAD", "/")
            return True
        except: return False
        finally: conn.close()

    def test_api(self):
        if not self.has_internet(): raise Exception("no internet")
        data = self.slacker.api.test().body
        if not data or not "ok" in data:
            raise Exception("test did not work")
            return False
        else: return True

    def fetch(self):
        if not self.has_internet(): raise Exception("no internet")
        data_queue = queue.Queue()
        threads = []
        threads.append(threading.Thread(target = data_queue.put, args = [self.slacker.users.list().body]))
        threads.append(threading.Thread(target = data_queue.put, args = [self.slacker.channels.list().body]))
        threads.append(threading.Thread(target = data_queue.put, args = [self.slacker.im.list().body]))
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        
        self.users = []
        self.users_name = {}
        self.channels = []
        self.channels_id = {}
        self.ims = []

        while not data_queue.empty():
            data = data_queue.get()
            if not "ok" in data or not data["ok"]:
                raise Exception("cannot fetch")

            if "channels" in data:
                for channel in data["channels"]:
                    if "name" in channel and "id" in channel:
                        self.channels_id[channel["name"]] = channel["id"]
                        self.channels.append(channel["name"])
            if "ims" in data:
                for im in data["ims"]:
                    if im["user"] in self.users_name:
                        self.channels_id[self.users_name[im["user"]]] = im["id"]
                        self.ims.append(self.users_name[im["user"]])
                        self.channels.append(self.users_name[im["user"]])
            if "members" in data:
                for user in data["members"]:
                    if "name" in user and "id" in user:
                        self.users_name[user["id"]] = user["name"]
                        self.users.append(user["name"])

    def fetch_history(self, channels, count):
        if not self.has_internet(): raise Exception("no internet")
        data_queue = queue.Queue()
        threads = []
        for channel in channels:
            if channel not in self.channels:
                raise Exception("not a channel")
                
            if channel in self.ims:
                threads.append(threading.Thread(target = data_queue.put, 
                    args = [{"channel" : channel,
                    "data" : self.slacker.im.history(channel = self.channels_id[channel], count = count).body}]))
            elif channel in self.channels:
                threads.append(threading.Thread(target = data_queue.put, 
                    args = [{"channel" : channel,
                    "data" : self.slacker.channels.history(channel = self.channels_id[channel], count = count).body}]))
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        while not data_queue.empty():
            data = data_queue.get()
            channel = data["channel"]
            data = data["data"]
            if not "ok" in data or not data["ok"]: raise Exception("cannot fetch history")
            self.ch_his[channel] = []
            if "messages" in data:
                for message in data["messages"][::-1]:
                    if "user" in message and "text" in message:
                        self.ch_his[channel].append({"name": self.users_name[message["user"]] , "text" : message["text"]})


    def send_message(self, channel, text):
        if not self.has_internet(): raise Exception("no internet")
        if channel not in self.channels: raise Exception("not a channel")
        self.channels_id[channel]
        data = self.slacker.chat.post_message( channel = channel, text = text, as_user = True, link_names = True, unfurl_links = False, unfurl_media = False).body
        if not data["ok"]: raise Exception("cannot send message")

    def get_users(self):
        return self.users

    def get_channels(self):
        return self.channels

    def get_channel_history(self, channel):
        return self.ch_his[channel]
