import socket
import sys
import urllib.request
import json
import urllib.error
import datetime

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "aminibOt"
PASS = str(sys.argv[1])  # OAuth run through argument
CHAN = "source28"

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + CHAN + " \r\n", "UTF-8"))


def time_format(sec):
    return str(datetime.timedelta(seconds=int(sec)))


def send_message(text):
    s.send(bytes("PRIVMSG #" + CHAN + " :" + text + "\r\n", "UTF-8"))


while True:
    line = str(s.recv(1024))
    if "End of /NAMES list" in line:
        break

while True:
    for line in str(s.recv(1024)).split('\\r\\n'):
        if "PING" in line:
            s.send(bytes("PONG :tmi.twitch.tv\r\n", "UTF-8"))

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
        if username.startswith("manofsteel"):
            send_message("/ban " + str(username))

        elif message.startswith("!kill") and (username == "aminibeast" or username == "source28"):
            quit()

        elif message.startswith("!user"):
            try:
                user = message.split()[1]
            except LookupError:
                send_message("No username was added in the request")
                continue

            try:
                src_name = json.loads(urllib.request.urlopen("http://speedrun.com/api/v1/users?lookup=" + str(user)).read())
            except urllib.error.URLError:
                send_message("SRC is down. Failed user search request")
                continue

            try:
                src_pbs = src_name["data"][0]["links"][3]["uri"]
            except LookupError:
                send_message("Invalid username")
                continue

            try:
                src_pbs = json.loads(urllib.request.urlopen(src_pbs).read())
            except urllib.error.URLError:
                send_message("SRC is down. Failed personal best request")
                continue

            pbs = []
            result = ""
            # SMO 76r55vd8
            # Any w20w1lzd
            # World Peace vdooo3yd
            # Dark Side wdmw4e42
            # Darker Side vdooqjod
            # All Moons wk6719ed
            # 100 n2y5jwek
            for x in src_pbs["data"]:
                if x["run"]["game"] == "76r55vd8" and x["run"]["level"] is None:
                    if x["run"]["category"] == "w20w1lzd" and x["run"]["values"]["68km3w4l"] != "zqoyz021":
                        continue

                    placement = x["place"]
                    if placement == 1:
                        placement = "WR"

                    pbs.append({"category": x["run"]["category"], "time": time_format(x["run"]["times"]["primary_t"]), "place": placement})

            for x in pbs:
                if x["category"] == "w20w1lzd":
                    result += "Any%: " + x["time"] + " (" + str(x["place"]) + "), "

            for x in pbs:
                if x["category"] == "vdooo3yd":
                    result += "World Peace: " + x["time"] + " (" + str(x["place"]) + "), "

            for x in pbs:
                if x["category"] == "wdmw4e42":
                    result += "Dark Side: " + x["time"] + " (" + str(x["place"]) + "), "

            for x in pbs:
                if x["category"] == "vdooqjod":
                    result += "Darker Side: " + x["time"] + " (" + str(x["place"]) + "), "

            for x in pbs:
                if x["category"] == "wk6719ed":
                    result += "All Moons: " + x["time"] + " (" + str(x["place"]) + "), "

            for x in pbs:
                if x["category"] == "n2y5jwek":
                    result += "100%: " + x["time"] + " (" + str(x["place"]) + "), "

            send_message(user + ": " + result[:-2])