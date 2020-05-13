import discord
from discord.ext import commands
import datetime

"""Class | Custom Help Command

Contains all of the features for a custom help message depending on certain
values set when defining a command in the first place.
"""
class TheHelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        """Help | General Bot

        Uncomment the commented lines to make it so that bot help messages
        can only be sent in channels that start with the word "bot".

        NOTE: Will be paginated at a later date.
        """
        #if self.context.channel.name.startswith('bot'):
        embed = discord.Embed(
            title = "Command Help",
            description = "A listing of all available commands sorted by grouping.\nTo learn more about specific commands, use `{0.clean_prefix}help <command>`".format(self),
            color = self.context.bot.embed_color
        )
        for cog in mapping.keys():
            if cog:
                command_list = await self.filter_commands(mapping[cog], sort = True)
                if len(command_list) > 0:
                    embed.add_field(
                        name = cog.qualified_name,
                        value = "{0.description}\nCommands:\n".format(cog) + ", ".join("`{1.qualified_name}`".format(self, command) for command in command_list),
                        inline = False
                    )
        embed.set_footer(
            text = self.context.bot.footer,
            icon_url = self.context.bot.footer_image,
        )
        if self.context.bot.show_command_author:
            embed.set_author(
                name = self.context.message.author.name,
                icon_url = self.context.message.author.avatar_url
            )
        await self.get_destination().send(embed = embed)
        #else:
        #    embed = discord.Embed(
        #        description = "Help commands can only be used in bot channels.",
        #        color = self.context.bot.embed_color
        #    )
        #    await self.get_destination().send(embed = embed)

    async def send_cog_help(self, cog):
        """Help | Cog Specific

        Sends help for all commands contained within a cog, by
        cog name.

        Uncomment the commented lines to make it so that bot help messages
        can only be sent in channels that start with the word "bot".
        """
        #if self.context.channel.name.startswith('bot'):
        embed = discord.Embed(
            title = cog.qualified_name + " Help",
            description = "{0.description}\n".format(cog) + "To learn more about specific commands, use `{0.clean_prefix}help <command>`".format(self),
            color = self.context.bot.embed_color
        )
        embed.add_field(
            name = "Commands",
            value = "\n".join("`{1.qualified_name}`".format(self, command) for command in cog.walk_commands() if not command.hidden),
            inline = False
        )
        embed.set_footer(
            text = self.context.bot.footer,
            icon_url = self.context.bot.footer_image,
        )
        if self.context.bot.show_command_author:
            embed.set_author(
                name = self.context.message.author.name,
                icon_url = self.context.message.author.avatar_url
            )
        await self.get_destination().send(embed = embed)
        #else:
        #    embed = discord.Embed(
        #        description = "Help commands can only be used in bot channels.",
        #        color = random.choice(self.context.bot.embed_colors)
        #    )
        #    await self.get_destination().send(embed = embed)

    async def send_group_help(self, group):
        """Help | Grouped Commands

        Sends help message for all commands grouped in a parent command.

        Uncomment the commented lines to make it so that bot help messages
        can only be sent in channels that start with the word "bot".
        """
        #if self.context.channel.name.startswith('bot'):
        command_list = group.walk_commands()
        command_activation = []
        command_example = []
        for command in command_list:
            if "`" + command.qualified_name + " " + command.signature + "` - {}".format(command.help) not in command_activation and not command.hidden:
                command_activation.append("`" + command.qualified_name + " " + command.signature + "` - {}".format(command.help))
                if command.brief:
                    command_example.append("`" + self.clean_prefix + command.qualified_name + " " + command.brief + "`")
                else:
                    command_example.append("`" + self.clean_prefix + command.qualified_name + "`")

        embed = discord.Embed(
            title = "{} Help".format(group.qualified_name.capitalize()),
            description = "{0.help}\n\nFor more information on each command, use `{1.clean_prefix}help [command]`.".format(group, self),
            color = self.context.bot.embed_color
        )
        if group.aliases:
            embed.add_field(
                name = "Aliases",
                value = ", ".join('`{}`'.format(alias) for alias in group.aliases),
                inline = False
            )
        embed.add_field(
            name = "Commands",
            value = "\n".join(command_activation),
            inline = False
        )
        embed.add_field(
            name = "Examples",
            value = "\n".join(command_example)
        )
        embed.set_footer(
            text = self.context.bot.footer,
            icon_url = self.context.bot.footer_image,
        )
        if self.context.bot.show_command_author:
            embed.set_author(
                name = self.context.message.author.name,
                icon_url = self.context.message.author.avatar_url
            )
        await self.get_destination().send(embed = embed)
        #else:
        #    embed = discord.Embed(
        #        description = "Help commands can only be used in bot channels.",
        #        color = random.choice(self.context.bot.embed_colors)
        #    )
        #    await self.get_destination().send(embed = embed)

    async def send_command_help(self, command):
        """Help | Command Specific

        Send help for a specific given single command.

        Uncomment the commented lines to make it so that bot help messages
        can only be sent in channels that start with the word "bot".
        """
        #if self.context.channel.name.startswith('bot'):
        embed = discord.Embed(
            title = "'{0}' Help".format(command.name.capitalize()),
            description = "{0.help}".format(command),
            color = self.context.bot.embed_color
        )
        if command.aliases:
            embed.add_field(
                name = "Aliases",
                value = ", ".join('`{}`'.format(alias) for alias in command.aliases),
                inline = False
            )
        embed.add_field(
            name = "Usage",
            value = "`" + self.clean_prefix + command.qualified_name + " " + command.signature + "`",
            inline = False
        )
        if command.brief:
            embed.add_field(
                name = "Example",
                value = "`" + self.clean_prefix + command.qualified_name + " " + command.brief + "`",
                inline = False
            )
        else:
            embed.add_field(
                name = "Example",
                value = "`" + self.clean_prefix + command.qualified_name + "`",
                inline = False
            )
        embed.set_footer(
            text = self.context.bot.footer,
            icon_url = self.context.bot.footer_image,
        )
        if self.context.bot.show_command_author:
            embed.set_author(
                name = self.context.message.author.name,
                icon_url = self.context.message.author.avatar_url
            )
        await self.get_destination().send(embed = embed)
        #else:
        #    embed = discord.Embed(
        #        description = "Help commands can only be used in bot channels.",
        #        color = random.choice(self.context.bot.embed_colors)
        #    )
        #    await self.get_destination().send(embed = embed)

"""Cog | Class Loader

Loads the custom help command class above.
"""
class LoadHelp(commands.Cog, name = "Help"):
    """
    Lists all available commands, sorted by the Cog they are in.
    """
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = TheHelpCommand()
        bot.help_command.cog = self
        print(f"{bot.OK} {bot.TIMELOG()} Loaded Help Cog.")

def setup(bot):
    """Setup

    The function called by Discord.py when adding another file in a multi-file project.
    """
    bot.add_cog(LoadHelp(bot))
