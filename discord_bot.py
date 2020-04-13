import discord
import json
import urllib
import urllib.request
import urllib.error
import datetime
import sys

prefix = "!"

errorEmbed = discord.Embed(title="Error", type='rich')


def time_format(sec):
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


async def smo_queue():
    try:
        data = json.loads(urllib.request.urlopen(
            "https://www.speedrun.com/api/v1/runs?game=76r55vd8&status=new&direction=asc&orderby=date&embed=players,category.variables").read())
    except urllib.error.URLError:
        return errorEmbed

    embed = discord.Embed(title="Super Mario Odyssey", url="https://www.speedrun.com/smo", type='rich',
                          color=discord.Color.blurple(), timestamp=datetime.datetime.now())

    embed.set_thumbnail(url="https://www.speedrun.com/themes/smo/cover-256.png")

    embed.set_author(
        name="speedrun.com",
        url="https://speedrun.com",
        icon_url=client.user.avatar_url)

    i = 0

    while i <= 10 and i < len(data["data"]):
        try:
            embed.add_field(name=(data["data"][i]["category"]["data"]["name"]),
                            value="[" + time_format(data["data"][i]["times"]["primary_t"]) + "](" + data["data"][i][
                                "weblink"] + ") by " + data["data"][i]["players"]["data"][0]["names"]["international"])
        except LookupError:
            embed.add_field(
                name=(data["data"][i]["category"]["data"]["name"]),
                value="[" + time_format(data["data"][i]["times"]["primary_t"]) + "](" + data["data"][i][
                    "weblink"])
        i += 1

    return embed


async def smoce_queue():
    try:
        data = json.loads(urllib.request.urlopen(
            "https://www.speedrun.com/api/v1/runs?game=m1mxxw46&status=new&direction=asc&orderby=date&embed=players,category.variables").read())
    except urllib.error.URLError:
        return errorEmbed

    embed = discord.Embed(title="Super Mario Odyssey Category Extensions", url="https://www.speedrun.com/smoce",
                          type='rich', color=discord.Color.blurple(), timestamp=datetime.datetime.now())

    embed.set_thumbnail(url="https://www.speedrun.com/themes/smoce/cover-256.png")

    embed.set_author(
        name="speedrun.com",
        url="https://speedrun.com",
        icon_url=client.user.avatar_url)

    i = 0

    while i <= 10 and i < len(data["data"]):
        try:
            embed.add_field(
                name=(data["data"][i]["category"]["data"]["name"]),
                value="[" + time_format(data["data"][i]["times"]["primary_t"]) + "](" + data["data"][i][
                    "weblink"] + ") by " + data["data"][i]["players"]["data"][0]["names"]["international"])
        except LookupError:
            embed.add_field(
                name=(data["data"][i]["category"]["data"]["name"]),
                value="[" + time_format(data["data"][i]["times"]["primary_t"]) + "](" + data["data"][i][
                    "weblink"])
        i += 1

    return embed


async def run_count():
    try:
        data = json.loads(urllib.request.urlopen(
            "https://www.speedrun.com/api/v1/runs?game=76r55vd8&status=new&direction=asc&orderby=date&max=200").read())
    except urllib.error.URLError:
        return errorEmbed

    checked_users = []
    message = ""

    for x in data["data"]:
        if x["players"][0]["id"] in checked_users:
            continue

        try:
            main_data = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/runs?game=76r55vd8&status=new&user=" + x["players"][0]["id"]).read())
            ce_data = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/runs?game=m1mxxw46&status=new&user=" + x["players"][0]["id"]).read())
        except urllib.error.URLError or LookupError:
            message += "Error occurred with " + str(x["players"][0]["id"]) + " user ID\n"
            continue

        main_count = len(main_data["data"])
        ce_count = len(ce_data["data"])
        message += str(x["players"][0]["id"]) + " = " + str(main_count) + " + " + str(ce_count) + "\n"
        checked_users.append(x["players"][0]["id"])
    return message


async def user_queue(user):
    try:
        initData = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/users?lookup=" + str(user)).read())["data"][0]
    except urllib.error.URLError:
        return errorEmbed
    except LookupError:
        try:
            tempData = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/users/" + str(user)).read())
        except urllib.error.URLError or LookupError:
            return errorEmbed
        return await user_queue(tempData["data"]["names"]["international"])

    try:
        queueData = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/runs?user=" + str(initData["id"])
                                                      + "&status=new&embed=players,category.variables").read())
    except urllib.error.URLError:
        return errorEmbed

    embed = discord.Embed(title=str(initData["names"]["international"]), url=str(initData["weblink"]), type='rich',
                          color=discord.Color.blurple(), timestamp=datetime.datetime.now())

    embed.set_author(
        name="speedrun.com",
        url="https://speedrun.com",
        icon_url=client.user.avatar_url)

    i = 0
    while len(embed) < 6000 and i < len(queueData["data"]):
        if (queueData["data"][i]["game"] != "76r55vd8") and (queueData["data"][i]["game"] != "m1mxxw46"):
            i += 1
            continue
        embed.add_field(name=(queueData["data"][i]["category"]["data"]["name"]),
                        value="[" + time_format(queueData["data"][i]["times"]["primary_t"]) + "](" + queueData["data"][i][
                            "weblink"] + ")")

        i += 1
    return embed


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        # print('Message from {0.author}: {0.content}'.format(message))
        if message.content.startswith(prefix + "load"):
            if message.channel.id != 689140446546755680:
                return

            await message.channel.send(await run_count())

        if message.content.startswith(prefix + "queue"):
            if message.channel.id != 689140446546755680:
                return
            try:
                data = (message.content.split())[1]

                userembed = await user_queue(data)
                await message.channel.send("<@" + str(message.author.id) + "> ", embed=userembed)
            except LookupError:
                mainembed = await smo_queue()
                await message.channel.send("<@" + str(message.author.id) + "> ", embed=mainembed)
                ceembed = await smoce_queue()
                await message.channel.send(embed=ceembed)

        if message.content.startswith(prefix + "role"):
            member = message.author
            role = discord.utils.find(lambda r: r.id == 650547547743715378, message.guild.roles)
            if role in member.roles:
                await member.remove_roles(role)
                await message.channel.send(
                    content="<@" + str(member.id) + ">, you will no longer receive stream notifications",
                    delete_after=3
                )
                await message.delete(delay=1)
            else:
                await member.add_roles(role)
                await message.channel.send(
                    content="<@" + str(member.id) + ">, you will now receive stream notifications",
                    delete_after=3
                )
                await message.delete(delay=1)


client = MyClient()
client.run(str(sys.argv[1]))  # Token run through argument
