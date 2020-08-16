import socket
import time
import urllib
import urllib.request
import urllib.error
import datetime
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

KFR_Guesses = False
# {"username": "test", "guess": "1:06:25"}
KFR_Guesses_List = []

wr_category = "lvdowokp" # Portal Out of Bounds
wr_string = "The WR for Portal Out of Bounds is "


def get_kfr_winners(time):
    KFR_Guesses_List.pop(len(KFR_Guesses_List) - 1)
    winner_array = []

    for x in KFR_Guesses_List:
        if time in x["guess"]:
            winner_array.append(x["username"])

    if len(winner_array) > 0:
        result = "Winners: "
        for x in winner_array:
            result += str(x) + " "
        return result
    else:
        return "No Winners"


with open("commands.json") as cmd:
    commands = json.loads(cmd.read())


def time_format(sec):
    return str(datetime.timedelta(seconds=int(sec)))


def send_message(text):
    s.send(bytes("PRIVMSG #" + CHAN + " :" + text + "\r\n", "UTF-8"))
    time.sleep(1)


def get_time(url):
    try:
        data = json.loads(urllib.request.urlopen(url).read())
        wr_time = time_format(data["data"]["runs"][0]["run"]["times"]["primary_t"])
        wr_user = data["data"]["players"]["data"][0]["names"]["international"]
        return wr_string + wr_time + " by " + str(wr_user)
    except LookupError or urllib.error.URLError:
        return wr_string + "Error"


def get_category():
    try:
        category = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/categories/" + wr_category + "?embed=game").read())
    except urllib.error.URLError:
        return "Error"

    global wr_string
    wr_string = "The WR for " + str(category["data"]["game"]["data"]["names"]["international"]) + " " + str(category["data"]["name"]) + " is "
    return get_time(category["data"]["links"][5]["uri"] + "?top=1&embed=players")


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

        if KFR_Guesses:
            KFR_Guesses_List.append({"username": str(username), "guess": message})

        # print(username + ": " + message)
        if message.startswith("!multi"):
            names = message.split()[1:]
            if username == "aminibeast" and len(names) > 0:
                multi_url = "https://beta.multitwitch.net/aminibeast"
                if names[0] != "reset":
                    for x in names:
                        multi_url += "/" + str(x)

                send_message("@aMinibeast -> command updated successfully")

            else:
                send_message(multi_url)

        elif message.startswith("!wr"):
            send_message(get_category())

        elif message.startswith("!setwr") and username == "aminibeast":
            try:
                wr_category = str(message.split()[1])
                send_message("Updated successfully")
            except LookupError:
                send_message("Please run the command with a category ID")

        elif message.startswith("!g") and username == "aminibeast":
            if message.startswith("!gs"):
                if not KFR_Guesses:
                    KFR_Guesses = True
                else:
                    send_message("@aMinibeast -> KFR_Guesses is already enabled")
            elif message.startswith("!gr") and KFR_Guesses is True:
                try:
                    send_message(get_kfr_winners(message.split()[1]))
                    KFR_Guesses_List = []
                except LookupError:
                    send_message("@aMinibeast -> No time given")

            elif message.startswith("!gf") and KFR_Guesses is True:
                try:
                    send_message(get_kfr_winners(message.split()[1]))
                    KFR_Guesses = False
                    KFR_Guesses_List = []
                except LookupError:
                    send_message("@aMinibeast -> No time given")

            elif message.startswith("!gquit") and KFR_Guesses is True:
                KFR_Guesses = False
                KFR_Guesses_List = []

            else:
                send_message("@aMinibeast -> gs to start race, gr to reset, gf to finish, gquit to end")

        elif message.startswith("!update"):
            with open("commands.json") as cmd:
                commands = json.loads(cmd.read())
                send_message("@aMinibeast -> successfully read commands file")

        else:
            for x in commands["data"]:
                if message.startswith(x["name"]):
                    send_message(x["text"])
                    break
