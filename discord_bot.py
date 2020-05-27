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
    return str(datetime.timedelta(seconds=int(sec)))


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


async def world_records():
    records = {"data": []}
    try:
        main_records = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/games/76r55vd8/records?miscellaneous=no&scope=full-game&top=1&max=200").read())
        ce_records = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/games/m1mxxw46/records?miscellaneous=no&scope=full-game&top=1&max=200").read())
    except urllib.error.URLError:
        return errorEmbed

    for x in main_records["data"]:
        try:
            records["data"].append({"category": x["category"], "time": x["runs"][0]["run"]["times"]["primary_t"]})
        except LookupError:
            continue

    for x in ce_records["data"]:
        # Fetches Pending requests
        # (can be imported to work with min caps; harder to predict results with min caps [2 sub-cats])
        if x["category"] == "9d84we7k":
            pending_records = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/variables/rn14rmpn").read())
            records["data"].append({"category": "Pending", "data": []})
            for i in pending_records["data"]["values"]["values"]:
                pending_cat_lb = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/leaderboards/m1mxxw46/category/9d84we7k?top=1&var-rn14rmpn=" + str(i)).read())
                records["data"][len(records["data"]) - 1]["data"].append({"category": str(i), "time": pending_cat_lb["data"]["runs"][0]["run"]["times"]["primary_t"], "label": pending_records["data"]["values"]["values"][i]["label"]})
            continue

        try:
            records["data"].append({"category": x["category"], "time": x["runs"][0]["run"]["times"]["primary_t"]})
        except LookupError:
            continue
    try:
        main_queue = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/runs?game=76r55vd8&status=new&direction=asc&orderby=date&embed=players,category.variables&max=200").read())
        ce_queue = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/runs?game=m1mxxw46&status=new&direction=asc&orderby=date&embed=players,category.variables&max=200").read())
    except urllib.error.URLError:
        return errorEmbed

    embed = discord.Embed(title="World Records", url="https://www.speedrun.com/smo", type='rich', timestamp=datetime.datetime.now(), color=discord.Color.blurple())

    embed.set_thumbnail(url="https://www.speedrun.com/themes/smo/cover-256.png")

    embed.set_author(
        name="speedrun.com",
        url="https://speedrun.com",
        icon_url=client.user.avatar_url)

    for x in main_queue["data"]:
        for i in records["data"]:
            if x["category"]["data"]["id"] == i["category"]:
                if x["times"]["primary_t"] < i["time"]:
                    if len(embed) > 5800:
                        break
                    try:
                        embed.add_field(name=(x["category"]["data"]["name"]),
                                        value="[" + time_format(x["times"]["primary_t"]) + "](" + x["weblink"] + ") by " + x["players"]["data"][0]["names"]["international"])
                    except LookupError:
                        embed.add_field(
                            name=(x["category"]["data"]["name"]),
                            value="[" + time_format(x["times"]["primary_t"]) + "](" + x[
                                "weblink"])

    for x in ce_queue["data"]:
        if "rn14rmpn" in x["values"]:
            for i in records["data"][len(records["data"]) - 1]["data"]:
                if x["values"]["rn14rmpn"] == i["category"]:
                    if x["times"]["primary_t"] < i["time"]:
                        if len(embed) > 5800:
                            break
                        try:
                            embed.add_field(name=("Pending - " + i["label"]),
                                            value="[" + time_format(x["times"]["primary_t"]) + "](" + x[
                                                "weblink"] + ") by " + x["players"]["data"][0]["names"][
                                                      "international"])
                        except LookupError:
                            embed.add_field(
                                name=("Pending - " + i["label"]),
                                value="[" + time_format(x["times"]["primary_t"]) + "](" + x[
                                    "weblink"])

        for i in records["data"]:
            if x["category"]["data"]["id"] == i["category"]:
                if x["times"]["primary_t"] < i["time"]:
                    if len(embed) > 5800:
                        break
                    try:
                        embed.add_field(name=(x["category"]["data"]["name"]),
                                        value="[" + time_format(x["times"]["primary_t"]) + "](" + x[
                                            "weblink"] + ") by " + x["players"]["data"][0]["names"]["international"])
                    except LookupError:
                        embed.add_field(
                            name=(x["category"]["data"]["name"]),
                            value="[" + time_format(x["times"]["primary_t"]) + "](" + x[
                                "weblink"])
    return embed


class MyClient(discord.Client):
    async def on_ready(self):
        status = discord.Game(name="github.com/Minibeast/aminibot")
        await client.change_presence(status=discord.Status.dnd, activity=status)
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        # print('Message from {0.author}: {0.content}'.format(message))
        if message.content.startswith(prefix + "records"):
            if message.channel.id != 689140446546755680 and message.channel.id != 439215885572505602:
                return

            await message.channel.send(embed=await world_records())

        if message.content.startswith(prefix + "queue"):
            if message.channel.id != 689140446546755680 and message.channel.id != 439215885572505602:
                return
            try:
                data = (message.content.split())[1]

                try:
                    data.encode("ascii")
                except UnicodeEncodeError:
                    await message.channel.send("<@" + str(message.author.id) + ">, Only ascii characters are valid. "
                                                                               "Please type the username without "
                                                                               "accents (ex: Orolmë becomes Orolme)")

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
