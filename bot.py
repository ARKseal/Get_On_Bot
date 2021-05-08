import asyncio as _asyncio
import os as _os

from discord.ext.commands import Bot as _Bot
from dotenv import load_dotenv as _load_dotenv

from Firebase_Connector import Firebase_Connector
from Json_Handler import Json_Handler
from Task_List import Tasklist


async def _spammer(ctx, count: int, response: str):
    for _ in range(count):
        await ctx.send(response)
        await _asyncio.sleep(1)

_load_dotenv()

_TOKEN = _os.getenv('DISCORD_TOKEN')
_BOTOWNER = _os.getenv('BOT_OWNER')

print(_os.getenv('DATABASE_URL'))
_DATABASE_URL = _os.getenv('DATABASE_URL')
_GOOGLE_APPLICATION_CREDENTIALS = _os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

FIREBASE = Firebase_Connector(_GOOGLE_APPLICATION_CREDENTIALS, _DATABASE_URL, 'data.json')
TASK = Tasklist()
VALUES = Json_Handler()

_code_website = "https://github.com/ARKseal/Get_On_Bot"

_bot = _Bot(command_prefix='?')

@_bot.event
async def on_ready():
    print("Online!")
    global VALUES

    for guild in _bot.guilds:
        print(str(guild.id))
        if str(guild.id) not in VALUES.getData():
            VALUES[str(guild.id)] = {
                'spam': ['max count', 40],
                'stop': [],
                'code': [],
                'change': []
            }

@_bot.event
async def on_guild_join(guild):
    VALUES[str(guild.id)] = {
        'spam': ['max count', 40],
        'stop': [],
        'code': [],
        'change': []
    }

"""@_bot.event
async def on_message(message):
    if message.author == _bot.user:
        return
    if message.author"""

@_bot.command(name='spam', help='Spam something!')
async def _spam(ctx, count: int, *people_and_message):
    global TASK
    guild = ctx.guild
    print(ctx.author)
    max_count = VALUES[str(guild.id)]['spam'][1]
    if count > max_count: count = max_count
    people = []
    msg = []
    for a in people_and_message:
        if a.startswith('<') and a.endswith('>'):
            people.append(a)
        else:
            msg.append(a)
    if not msg: msg = ["I", "think", "you", "need", "to", "do", "something"]
    response = ((' '.join(people) + ' - ') if people else '') + ' '.join(msg)

    TASK.add(guild, _asyncio.create_task(_spammer(ctx, count, response)))


@_bot.command(name='stop', help='Stop spamming the current spam command!')
async def _stop(ctx):
    global TASK
    TASK.stop(ctx.guild)

@_bot.command(name='code', help='Get the link to my code!')
async def _code(ctx):
    await ctx.send('See my code at {} under Get_On_Bot!'.format(_code_website))

@_bot.command(name='change', help='Change an important value!')
async def _change(ctx, command: str, value: int):
    global VALUES

    guild = ctx.guild
    print(str(ctx.author))
    print(str(guild.owner))
    if (not ctx.message.author.guild_permissions.administrator) and str(ctx.author) != _BOTOWNER:
        await ctx.send("Sorry, you do not have the permission to change command values")
        return

    command = command.lower()
    if command in VALUES[str(guild.id)]:
        if VALUES[str(guild.id)][command]:
            old_val = VALUES[str(guild.id)][command][:]
            VALUES[str(guild.id)][command][1] = value
            await ctx.send("The value '{o[0]}' in the command '{c}' changed from '{o[1]}' to '{v}'".format(o=old_val,c=command,v=value))
            FIREBASE.sendData()
        else:
            await ctx.send("There are no changeable values in the command '{}'".format(command))
    else:
        await ctx.send("Sorry, I do not have the command '{}'".format(command))

_bot.run(_TOKEN)