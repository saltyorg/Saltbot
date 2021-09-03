import logging
import re
import discord

lookups = {
    "{author}": lambda m: m.author,
    "{author.mention}": lambda m: m.author.mention
}

class SaltBot(discord.Client):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggers = config['triggers']
        self.commands = config['commands']
        self.prefix = config['command_prefix']
        self.logger = logging.getLogger('saltbot')
        logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)

    async def on_ready(self):
        self.logger.info(f'We have logged in as {self.user}')

    @staticmethod
    def replace_template(response, message):
        matches = re.findall(r'(\{.*?\})', response)

        for match in matches:
            response = response.replace(match, lookups.get(match, lambda f: f)(message))
        return response

    async def parse_trigger(self, message):
        for trigger in self.triggers:
            if trigger.lower() in message.content.lower():
                await message.channel.send(self.replace_template(self.triggers[trigger], message))
                return
        

    async def on_message(self, message):
        is_bot = message.author.bot
        is_webhook = bool(message.webhook_id)
        if is_bot or is_webhook:
            return
        match = re.match(f'{re.escape(self.prefix)}' + f'({"|".join([k.lower() for k in self.commands.keys()])})', message.content.lower())
        
        if not match:
            return await self.parse_trigger(message)
        
        response = self.replace_template(self.commands[match[0].replace(self.prefix, '')], message)

        await message.channel.send(response)
        self.logger.info('Sent message to ' + str(message.channel))

    async def update_commands(self, commands=None, triggers=None, prefix=None):
        if commands:
            self.commands = commands
        if triggers:
            self.triggers = triggers
        if prefix and prefix != self.prefix:
            self.prefix = prefix
    