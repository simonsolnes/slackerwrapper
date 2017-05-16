#!/usr/local/bin/python3
import slackerwrapper

slack = slackerwrapper.SlackerWrapper()

if slack.test_api(): print("api test: OK")
else: print("api test: NOT OK!!!!")

print("users:")
users = slack.get_users()
for user in users: print("\t" + user)

print("channels:")
channels = slack.get_channels()
for channel in channels: print("\t" + channel)

slack.fetch_history(channels, 5)

for channel in channels:
    print("channel history for " + channel)
    for message in slack.get_history(channel):
        print("\t" + message["name"] + ":\t" + message["text"])

slack.send_message("testing", "test from python: testing unicode: æøååß∂ƒ©˙")
