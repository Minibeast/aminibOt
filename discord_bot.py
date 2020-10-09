import discord
import json
import urllib
import urllib.request
import urllib.error
import datetime
import sys

PREFIX = "!"
QUEUE_CHANNELS = [689140446546755680, 439215885572505602]
SERVER = 630534093813317662
ROLE_ID = 650547547743715378


REACT_SERVER = 640640211981959181 # Discount Bois
REACT_CHANNEL = 756194739098877992 # good-messages

REACT2_SERVER = 686725610449797135 # Krusty Krab
REACT2_CHANNEL = 763944837002821662 # Pins

"""
REACT2_SERVER = 339790925029048321 # Ian's Testing Server
REACT2_CHANNEL = 763947145848946718 # code-testing-2
"""

HANDLED_STARBOARD = []

errorEmbed = discord.Embed(title="Error", type='rich')


def time_format(sec):
    return str(datetime.timedelta(seconds=int(sec)))


async def smo_queue(date=""):
    if date is None:
        try:
            data = json.loads(urllib.request.urlopen(
                "https://www.speedrun.com/api/v1/runs?game=76r55vd8&status=new&direction=asc&orderby=date&embed=players,category.variables").read())
        except urllib.error.URLError:
            return errorEmbed

    else:
        try:
            data = json.loads(urllib.request.urlopen(
                "https://www.speedrun.com/api/v1/runs?game=76r55vd8&status=new&direction=asc&orderby=date&embed=players,category.variables&max=200").read())
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
    x = 0

    while x <= 10 and i < len(data["data"]):
        if len(date) == 0 or (len(date) > 0 and data["data"][i]["date"] == str(date)):
            try:
                embed.add_field(name=(data["data"][i]["category"]["data"]["name"]),
                                value="[" + time_format(data["data"][i]["times"]["primary_t"]) + "](" + data["data"][i][
                                    "weblink"] + ") by " + data["data"][i]["players"]["data"][0]["names"]["international"])
            except LookupError:
                embed.add_field(
                    name=(data["data"][i]["category"]["data"]["name"]),
                    value="[" + time_format(data["data"][i]["times"]["primary_t"]) + "](" + data["data"][i][
                        "weblink"])
            x += 1
        i += 1

    return embed


async def smoce_queue(date=""):
    if date is None:
        try:
            data = json.loads(urllib.request.urlopen(
                "https://www.speedrun.com/api/v1/runs?game=m1mxxw46&status=new&direction=asc&orderby=date&embed=players,category.variables").read())
        except urllib.error.URLError:
            return errorEmbed

    else:
        try:
            data = json.loads(urllib.request.urlopen(
                "https://www.speedrun.com/api/v1/runs?game=m1mxxw46&status=new&direction=asc&orderby=date&embed=players,category.variables&max=200").read())
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
    x = 0

    while x <= 10 and i < len(data["data"]):
        if len(date) == 0 or (len(date) > 0 and data["data"][i]["date"] == str(date)):
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
            x += 1
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


async def user_queue(user, search_index=0):
    try:
        initData = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/users?lookup=" + str(user)).read())
        user_info = initData["data"][search_index]
    except urllib.error.URLError:
        return errorEmbed
    except LookupError:
        try:
            tempData = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/users/" + str(user)).read())
            user_info = tempData["data"]
        except urllib.error.URLError or LookupError:
            return errorEmbed

    try:
        queueData = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/runs?user=" + str(user_info["id"])
                                                      + "&status=new&embed=players,category.variables").read())
    except urllib.error.URLError:
        return errorEmbed

    embed = discord.Embed(title=str(user_info["names"]["international"]), url=str(user_info["weblink"]), type='rich',
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

    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if message.guild.id == REACT_SERVER:
            if reaction.emoji != "🥴":
                return

            if message.channel.id == REACT_CHANNEL:
                return

            if reaction.count == 3 and message.id not in HANDLED_STARBOARD:
                webhook_channel = discord.utils.find(lambda c: c.id == REACT_CHANNEL, message.channel.guild.channels)
                try:
                    webhook = await webhook_channel.webhooks()
                    webhook = webhook[0]
                except discord.errors.Forbidden and LookupError:
                    return

                files = []
                embeds = message.embeds
                embeds.append(discord.Embed(description="[Jump](" + message.jump_url + ")"))

                for x in message.attachments:
                    files.append(await x.to_file())

                await webhook.send(content=message.content, username=message.author.name,
                                   avatar_url=message.author.avatar_url, files=files, embeds=embeds)
                HANDLED_STARBOARD.append(message.id)
        elif message.guild.id == REACT2_SERVER:
            if reaction.emoji != "📌":
                return

            if message.channel.id == REACT2_CHANNEL:
                return

            if message.id not in HANDLED_STARBOARD:
                webhook_channel = discord.utils.find(lambda c: c.id == REACT2_CHANNEL, message.channel.guild.channels)
                try:
                    webhook = await webhook_channel.webhooks()
                    webhook = webhook[0]
                except discord.errors.Forbidden and LookupError:
                    return

                files = []
                embeds = message.embeds
                embeds.append(discord.Embed(description="[Jump](" + message.jump_url + ")"))

                for x in message.attachments:
                    files.append(await x.to_file())

                await webhook.send(content=message.content, username=message.author.name,
                                   avatar_url=message.author.avatar_url, files=files, embeds=embeds)
                HANDLED_STARBOARD.append(message.id)

    async def on_message(self, message):
        if message.author == client.user:
            return

        # print('Message from {0.author}: {0.content}'.format(message))
        if message.content.startswith(PREFIX + "records"):
            if message.channel.id not in QUEUE_CHANNELS:
                return

            await message.channel.send(embed=await world_records())

        elif message.content.startswith(PREFIX + "queuedate"):
            if message.channel.id not in QUEUE_CHANNELS:
                return
            try:
                date = message.content.split()[1]
                date = int(date)
            except LookupError:
                await message.channel.send("<@" + str(message.author.id) + ">, No number given")
                return
            except ValueError:
                await message.channel.send("<@" + str(message.author.id) + ">, Not a valid number")
                return

            formatted_date = datetime.datetime.now() - datetime.timedelta(days=date)
            formatted_date = formatted_date.strftime("%Y-%m-%d")
            await message.channel.send("<@" + str(message.author.id) + "> ", embed=await smo_queue(date=formatted_date))
            await message.channel.send(embed=await smoce_queue(date=formatted_date))

        elif message.content.startswith(PREFIX + "queue"):
            if message.channel.id not in QUEUE_CHANNELS:
                return
            try:
                data = message.content.split()
                if len(data) > 2:
                    index = data[2]
                else:
                    index = 0

                try:
                    data[1].encode("ascii")
                except UnicodeEncodeError:
                    await message.channel.send("<@" + str(message.author.id) + ">, Only ascii characters are valid. "
                                                                               "Please type the username without "
                                                                               "accents (ex: Orolmë becomes Orolme)")
                    return

                await message.channel.send("<@" + str(message.author.id) + "> ", embed=await user_queue(data[1], search_index=int(index)))
            except LookupError:
                await message.channel.send("<@" + str(message.author.id) + "> ", embed=await smo_queue())
                await message.channel.send(embed=await smoce_queue())

        elif message.content.startswith(PREFIX + "role"):
            if message.guild.id != SERVER:
                return

            member = message.author
            role = discord.utils.find(lambda r: r.id == ROLE_ID, message.guild.roles)
            if role in member.roles:
                await member.remove_roles(role)
                await message.channel.send(
                    content="<@" + str(member.id) + ">, you will no longer receive stream notifications",
                    delete_after=3
                )
                await message.delete()
            else:
                await member.add_roles(role)
                await message.channel.send(
                    content="<@" + str(member.id) + ">, you will now receive stream notifications",
                    delete_after=3
                )
                await message.delete()

        elif message.content.startswith(PREFIX + "starboardadd") and message.author.id == 258002965833449472:
            try:
                id = message.content.split()[1]
            except LookupError:
                return

            if message.guild.id == REACT_SERVER:
                starboard_msg = await message.channel.fetch_message(id)

                if starboard_msg.id not in HANDLED_STARBOARD:
                    webhook_channel = discord.utils.find(lambda c: c.id == REACT_CHANNEL,
                                                         message.channel.guild.channels)
                    try:
                        webhook = await webhook_channel.webhooks()
                        webhook = webhook[0]
                    except discord.errors.Forbidden and LookupError:
                        return

                    files = []
                    embeds = starboard_msg.embeds
                    embeds.append(discord.Embed(description="[Jump](" + starboard_msg.jump_url + ")"))

                    for x in starboard_msg.attachments:
                        files.append(await x.to_file())

                    await webhook.send(content=starboard_msg.content, username=starboard_msg.author.name,
                                       avatar_url=starboard_msg.author.avatar_url, files=files, embeds=embeds)
                    HANDLED_STARBOARD.append(starboard_msg.id)

            elif message.guild.id == REACT2_SERVER:
                starboard_msg = await message.channel.fetch_message(id)

                if starboard_msg.id not in HANDLED_STARBOARD:
                    webhook_channel = discord.utils.find(lambda c: c.id == REACT2_CHANNEL,
                                                         message.channel.guild.channels)
                    try:
                        webhook = await webhook_channel.webhooks()
                        webhook = webhook[0]
                    except discord.errors.Forbidden and LookupError:
                        return

                    files = []
                    embeds = starboard_msg.embeds
                    embeds.append(discord.Embed(description="[Jump](" + starboard_msg.jump_url + ")"))

                    for x in starboard_msg.attachments:
                        files.append(await x.to_file())

                    await webhook.send(content=starboard_msg.content, username=starboard_msg.author.name,
                                       avatar_url=starboard_msg.author.avatar_url, files=files, embeds=embeds)
                    HANDLED_STARBOARD.append(starboard_msg.id)


client = MyClient()
client.run(str(sys.argv[1]))  # Token run through argument
