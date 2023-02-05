from dotenv import load_dotenv
load_dotenv()

import nextcord
from nextcord.ext import commands
import os

from cogs import music, ibm_site, node_listener
from server import srv

cogs = [music, ibm_site, node_listener]

intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix="&", case_insensitive=True, intents=intents, enable_debug_events=True)
bot.remove_command("help")
for cog in cogs:
    cog.setup(bot)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        srv[str(guild.id)] = {
            "ctx": None,
            'queue': [],
            'player': None,
            "last_message": None,
            "loop": False,
            'thread': None,
            'time': 0,
            'pause': False,
            'skipping': False,
        }

    activity = nextcord.Game(name="some music!", type=3)
    await bot.change_presence(activity=activity)
    print(f'{bot.user} joined the game')


def start():
    token = os.getenv("BOT_TOKEN")
    bot.run(token)


if __name__ == '__main__':
    start()