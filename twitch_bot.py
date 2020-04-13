import socket
import time
import urllib
import urllib.request
import urllib.error
import json
import sys

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "aminibOt"
PASS = str(sys.argv[1])  # OAuth run through argument
CHAN = "aminibeast"

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + CHAN + " \r\n", "UTF-8"))

multi_url = "https://beta.multitwitch.net/aminibeast"


def time_format(sec):
    sec = int(sec)
    mins = sec // 60
    sec = sec % 60
    sec = round(sec, 3)
    hours = mins // 60
    mins = mins % 60

    if sec < 10:
        sec = str(0) + str(sec)

    if mins < 10:
        mins = str(0) + str(mins)

    if hours < 10:
        hours = str(0) + str(hours)

    return "{0}:{1}:{2}".format(hours, mins, sec)


def send_message(text):
    s.send(bytes("PRIVMSG #" + CHAN + " :" + text + "\r\n", "UTF-8"))
    time.sleep(1)


def get_time(url):
    try:
        data = json.loads(urllib.request.urlopen(url).read())
        return time_format(data["data"]["runs"][0]["run"]["times"]["primary_t"])
    except LookupError or urllib.error.URLError:
        return "Error"


while True:
    line = str(s.recv(1024))
    if "End of /NAMES list" in line:
        break

while True:
    for line in str(s.recv(1024)).split('\\r\\n'):
        parts = line.split(':')
        if len(parts) < 3:
            continue

        if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
            message = parts[2][:len(parts[2])]
        else:
            message = ""

        usernamesplit = parts[1].split("!")
        username = usernamesplit[0]

        # print(username + ": " + message)
        if message == "!test":
            send_message("ping pong the bot is alive")

        if message.startswith("!multi"):
            names = message.split()[1:]
            if username == "aminibeast" and len(names) > 0:
                multi_url = "https://beta.multitwitch.net/aminibeast"
                if names[0] != "reset":
                    for x in names:
                        multi_url += "/" + str(x)

                send_message("@aMinibeast command updated successfully")

            else:
                send_message(multi_url)

        if message.startswith("!wr"):
            text = ""

            try:
                date = "&date=" + str(message.split()[1])
            except LookupError:
                date = ""
            text += "Any%: " + get_time(
                "https://www.speedrun.com/api/v1/leaderboards/76r55vd8/category/w20w1lzd?top=1&var-68km3w4l=zqoyz021" + date)
            text += ", Any% 2P: " + get_time(
                "https://www.speedrun.com/api/v1/leaderboards/76r55vd8/category/w20w1lzd?top=1&var-68km3w4l=013vz03l" + date)
            text += ", World Peace: " + get_time(
                "https://www.speedrun.com/api/v1/leaderboards/76r55vd8/category/vdooo3yd?top=1" + date)
            text += ", Dark Side: " + get_time(
                "https://www.speedrun.com/api/v1/leaderboards/76r55vd8/category/wdmw4e42?top=1" + date)
            text += ", Darker Side: " + get_time(
                "https://www.speedrun.com/api/v1/leaderboards/76r55vd8/category/vdooqjod?top=1" + date)
            text += ", All Moons: " + get_time(
                "https://www.speedrun.com/api/v1/leaderboards/76r55vd8/category/wk6719ed?top=1" + date)
            text += ", 100%: " + get_time(
                "https://www.speedrun.com/api/v1/leaderboards/76r55vd8/category/n2y5jwek?top=1" + date)

            send_message(text)
