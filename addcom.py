import json

name = input("Command Name (WITH PREFIX): ")
text = input("Text: ")

with open("commands.json") as cmd:
    commands = json.loads(cmd.read())
    cmd.close()

commands["data"].append({"name": name, "text": text})

with open("commands.json", "w+") as cmd:
    cmd.write(json.dumps(commands))
    print("\nSuccessfully written command " + name + " to file (!update)")
    quit()
