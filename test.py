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

print("channel history for testing")
slack.fetch_channel_history("testing", 3)
for message in slack.get_channel_history("testing"):
    print("\t" + message["name"] + ":\t" + message["text"])

print("im history for potatobuffer")
slack.fetch_channel_history("potatobuffer", 5)
for message in slack.get_channel_history("potatobuffer"):
    print("\t" + message["name"] + ":\t" + message["text"])


slack.send_message("testing", "test from python: testing unicode: æøååß∂ƒ©˙")
