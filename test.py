#!/usr/local/bin/python3
import slackerwrapper
from colorstring import ColorString
import time
import threading

# print(str(type(time())))

slack = slackerwrapper.SlackerWrapper(dbmode = True)

if slack.test_api(): print("api test:", ColorString("OK", "green"))
else: print("api test:", ColorString("NOT OK", "red"))

slack.fetch()

print("users:")
for user in slack.get_users():
    print("\t" + user)

print("channels:")
for channel in slack.get_channels():
    print("\t" + channel)

slack.fetch_history(["potatobuffer", "general"], 5)

print("channel history for potatobuffer")
for message in slack.get_channel_history("potatobuffer"):
    print("\t" + message["name"] + ":\t" + message["text"])

print("im history for general")
for message in slack.get_channel_history("general"):
    print("\t" + message["name"] + ":\t" + message["text"])


slack.send_message("testing", "test from python: testing unicode: æøååß∂ƒ©˙")
