"""Python Library Imports

Discord libraries for, well... Discord.

Datetime... do I really need to explain?

Ruamel.Yaml to allow comments to remain in YAML files when reading/writing them.

OS for file system and environment variable stuff.

Resources.Data for repetitive data file management, found in ./Resources/Data.py

Colorama for fancy colored logging.
"""

import discord
from discord.ext import commands
import datetime
from ruamel.yaml import YAML
import os
from Resources.Data import save_data, load_data
from colorama import init, Fore
init()

# load Config and Permissions file.
yaml = YAML()
with open("./Config.yml", 'r') as file:
    config = yaml.load(file)

bot_permissions = {}
with open("./Permissions.yml", 'r') as file:
    permissions = yaml.load(file)
    # Raw permission input is formatted to have role IDs in place.
    roles = dict(permissions['Roles'])
    for key in permissions.keys():
        if not key in (None, 'Roles'):
            bot_permissions[key] = []
            for permission in permissions[key]:
                bot_permissions[key].append(permission.format(**roles))

def get_prefix(client, message):
    """Prefix | Dynamic Prefix Manager

    Allows for dynamically changing prefix by reading from
    config actively.

    'prefix' command can update the bot prefix in this way.
    """
    with open("./Config.yml", 'r') as file:
        config = yaml.load(file)
    prefix = config['Prefix']
    return prefix

# Create the 'bot' instance, using the fucntion above for getting the prefix.
bot = commands.Bot(command_prefix=get_prefix, description="Heroicos_HM's Custom Bot", case_insensitive = True)

# Remove the help command to leave room for implementing a custom one.
bot.remove_command('help')

"""Setup | Bot Config

Loading Config and Permission variables into bot attributes.

See 'Config.yml' and 'Permissions.yml' for specifics on each setting.
"""
# Main Settings
bot.TOKEN              = os.getenv(config['Token Env Var'])
bot.prefix             = config['Prefix']
bot.online_message     = config['Online Message']
bot.restarting_message = config['Restarting Message']
bot.data_file          = os.path.abspath(config['Data File'])
bot.show_game_status   = config['Game Status']['Active']
bot.game_to_show       = config['Game Status']['Game']
bot.log_channel_id     = config['Log Channel']
bot.invite_link        = config['Server Invite']
bot.permissions        = permissions
bot.config             = config
bot.yaml               = yaml

# Embed Options
bot.embed_color = discord.Color.from_rgb(
    config['Embed Settings']['Color']['r'],
    config['Embed Settings']['Color']['g'],
    config['Embed Settings']['Color']['b']
)
bot.footer =              config['Embed Settings']['Footer']['Text']
bot.footer_image =        config['Embed Settings']['Footer']['Icon URL']
bot.delete_commands =     config['Embed Settings']['Delete Commands']
bot.show_command_author = config['Embed Settings']['Show Author']
bot.embed_ts =            lambda: datetime.datetime.now(datetime.timezone.utc)

# Logging Variables
bot.OK = f"{Fore.GREEN}[OK]{Fore.RESET}  "
bot.WARN = f"{Fore.YELLOW}[WARN]{Fore.RESET}"
bot.ERR = f"{Fore.RED}[ERR]{Fore.RESET} "
bot.TIMELOG = lambda: datetime.datetime.now().strftime('[%m/%d/%Y | %I:%M:%S %p]')

"""Setup | Initial Data Loading/Prep

Check if the data file exists, if it does, load it, if not, create it.

If the data file exists but has not data, give it a new empty data object.
"""
if os.path.exists(bot.data_file):
    with open(bot.data_file, 'r') as file:
        content = file.read()
        if len(content) == 0:
            bot.data = {}
            save_data(bot.data_file, bot.data)
        else:
            bot.data = load_data(bot.data_file)
else:
    bot.data = {}
    save_data(bot.data_file, bot.data)

# List of extension files to load.
extensions = [
    'Cogs.Errors',
    'Cogs.General',
    'Cogs.Help'
]

print(f"{bot.OK} {bot.TIMELOG()} Connecting to Discord...")

@bot.event
async def on_ready():
    """Listener | On Discord Connection

    Triggered when the bot successfully connects with Discord.

    Sets up the remaining initial configuration for the bot and loads all Cogs.
    """
    # Load the extension files listed above.
    for extension in extensions:
        bot.load_extension(extension)

    print(f"{bot.OK} {bot.TIMELOG()} Logged in as {bot.user} and connected to Discord! (ID: {bot.user.id})")

    # Set the playing status of the bot to what is set in the config.
    if bot.show_game_status:
        game = discord.Game(name = bot.game_to_show.format(prefix = bot.prefix))
        await bot.change_presence(activity = game)

    # Create online message template.
    embed = discord.Embed(
        title = bot.online_message.format(username = bot.user.name),
        color = bot.embed_color,
        timestamp = bot.embed_ts()
    )
    embed.set_footer(
        text = bot.footer,
        icon_url = bot.footer_image
    )
    # Set the log channel object to a bot variable for later use.
    bot.log_channel = bot.get_channel(bot.log_channel_id)
    await bot.log_channel.send(embed = embed)

    # Set the bot start time for use in the uptime command.
    bot.start_time = bot.embed_ts()

@bot.check
async def command_permissions(ctx):
    """Check | Global Permission Manager

    This is attached to all commands.

    When a comand is used this function will use the permissions imported
    from Permissions.yml to verify that a user is/is not allowed
    to use a command.
    """
    # Administrators are always allowed to use the command.
    if ctx.author.guild_permissions.administrator:
        return True
    else:
        # Finding permission name scheme of a command.
        name = ctx.command.name
        if ctx.command.parent:
            command = ctx.command
            parent_exists = True
            while parent_exists == True:
                name = ctx.command.parent.name + '-' + name
                command = ctx.command.parent
                if not command.parent:
                    parent_exists = False

        """Checking command permissions

        For each role ID listed for a command, check if the user has that role id.

        If they do, allow command usage, otherwise, proceed to checking next role on the list.

        If the user does not have any of the roles, deny the command usage.
        """
        if name in ctx.bot.permissions.keys():
            for permission in ctx.bot.permissions[name]:
                try:
                    role = ctx.guild.get_role(int(permission))
                    if role in ctx.author.roles:
                        return True
                except Exception as e:
                    print(e)
            return False
        else:
            return True

try:
    bot.run(bot.TOKEN, bot = True, reconnect = True)
except discord.LoginFailure:
    print(f"{bot.ERR} {bot.TIMELOG()} Invalid TOKEN Variable: {bot.TOKEN}")
    input("Press enter to continue.")
