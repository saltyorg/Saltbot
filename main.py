import discord
import json

config = json.load(open("config.json"))

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    is_bot = message.author.bot
    is_webhook = bool(message.webhook_id)

    if (not is_bot) or (not is_webhook):
        if message.content.startswith(config["command_prefix"]):
            for command in config["commands"]:
                if command["command"] in message.content:
                    command_output = command["response"]
                    if "{author}" in command["response"]:
                        command_output = command_output.replace("{author}", message.author.name)
                    if "{author.mention}" in command["response"]:
                        command_output = command_output.replace("{author.mention}", message.author.mention)
                    await message.channel.send(command_output)
        else:
            for response in config["responses"]:
                if response["trigger"] in message.content:
                    response_output = response["response"]
                    if "{author}" in response["response"]:
                        response_output = response_output.replace("{author}", message.author.name)
                    if "{author.mention}" in response["response"]:
                        response_output = response_output.replace("{author.mention}", message.author.mention)
                    await message.channel.send(response_output)


client.run(config["token"])
