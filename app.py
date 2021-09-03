import asyncio
import json

from quart import Quart, render_template, request
from discordbot.discordbot import SaltBot


app = Quart(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods=['GET'])
async def home():
    return await render_template('index.html.jinja')


@app.route('/api/config', methods=['GET'])
async def conf():
    context = {
        'command_prefix': config.get('command_prefix', '?'),
        'commands': config.get('commands', []),
        'triggers': config.get('triggers', [])
    }
    return context


@app.route('/api/update', methods=['POST'])
async def update():
    body = await request.get_json()

    newconf = transform_config(body)

    await discordbot.update_commands(commands=newconf['commands'], triggers=newconf['triggers'], prefix=newconf['command_prefix'])
    update_config(body)
    return {'success': 'ok'}


def update_config(conf):
    token = config.get('token')
    conf['token'] = token
    with open('./config.json', 'w') as f:
        f.write(json.dumps(conf, indent=2))


def transform_config(config):

    config = dict(config)

    def _convert(d):
        trigger = d.get('trigger', '')
        response = d.get('response', '')
        return (trigger, response)

    commands = config.get('commands', [])

    config['commands'] = dict([_convert(c) for c in commands])
    triggers = config.get('triggers', [])
    config['triggers'] = dict([_convert(c) for c in triggers])
    return config


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    config = json.load(open('./config.json', 'r'))
    discordbot = SaltBot(transform_config(config))

    loop.create_task(discordbot.start(config.get('token', '')))
    app.run(loop=loop)
