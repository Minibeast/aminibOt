import socket
import time
import sys

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "aminibOt"
PASS = str(sys.argv[1])  # OAuth run through argument
CHANNELS = ["source28", "sailo93", "cjya2016", "l1ghtrc"]

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
for x in CHANNELS:
    s.send(bytes("JOIN #" + str(x) + " \r\n", "UTF-8"))


def send_message(text):
    for x in CHANNELS:
        s.send(bytes("PRIVMSG #" + str(x) + " :" + text + "\r\n", "UTF-8"))


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

        elif message.startswith("!kill") and username == "aminibeast":
            quit()

        elif message.startswith("!test") and (username in CHANNELS or username == "aminibeast"):
            send_message("ping")
