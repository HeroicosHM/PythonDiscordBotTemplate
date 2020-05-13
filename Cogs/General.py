import discord
from discord.ext import commands
import datetime
from math import trunc

"""Cog | General Commands

This Cog contains a list of commands that almost every program
should utilize.

NOTE: All commands are restricted to server use only by default,
remove the `@commands.guild_only()` line before any command that
should also be able to be used in a DM.
"""
class General(commands.Cog, name = "General"):
    """
    A general set of commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print(f"{bot.OK} {bot.TIMELOG()} Loaded General Cog.")

    @commands.guild_only()
    @commands.command(name = "prefix", help = "Changes the command prefix for the bot.", brief = "?")
    async def prefix(self, ctx, prefix: str):
        old = self.bot.prefix
        self.bot.config['Prefix'] = prefix
        with open('./Config.yml', 'w') as file:
            self.bot.yaml.dump(self.bot.config, file)

        self.bot.prefix = prefix
        if self.bot.show_game_status:
            game = discord.Game(name = self.bot.game_to_show.format(prefix = self.bot.prefix))
            await self.bot.change_presence(activity = game)

        embed = discord.Embed(
            title = "Prefix Updated",
            description = f"New Prefix: `{self.bot.prefix}`",
            color = self.bot.embed_color,
            timestamp = self.bot.embed_ts()
        )
        embed.add_field(
            name = "New",
            value = f"{self.bot.prefix}command"
        )
        embed.add_field(
            name = "Old",
            value = f"{old}command"
        )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer,
            icon_url = self.bot.footer_image
        )
        await ctx.send(embed = embed)
        embed.set_author(
            name = ctx.author.name,
            icon_url = ctx.author.avatar_url
        )
        await self.bot.log_channel.send(embed = embed)

    @commands.guild_only()
    @commands.command(name = "restart", help = "Restarts the bot.", brief = "")
    async def restart(self, ctx):
        """Command | Restarts the bot.

        Sends a message to the log channel, adds a reaction to the message, then
        attempts to gracefully disconnect from Discord.

        Either a Batch or Shell script (depending on operating system) will then
        re-activate the bot, which allows the bot to take in file updates on the fly.
        """

        embed = discord.Embed(
            title = self.bot.restarting_message.format(username = self.bot.user.name),
            color = self.bot.embed_color,
            timestamp = self.bot.embed_ts()
        )
        embed.set_footer(
            text = self.bot.footer,
            icon_url = self.bot.footer_image
        )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        await self.bot.log_channel.send(embed = embed)

        await ctx.message.add_reaction('✅')
        await self.bot.close()

    @commands.guild_only()
    @commands.command(name='uptime', help = 'Returns the amount of time the bot has been online.')
    async def uptime(self, ctx, test):
        """Command | Get Bot Uptime

        As the name implies... this returns the amount of time the
        bot has been online, given that the `bot.start_time` value
        was set in `main.py` in the `on_ready` function.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        seconds = trunc((datetime.datetime.now(datetime.timezone.utc) - self.bot.start_time).total_seconds())
        hours = trunc(seconds / 3600)
        seconds = trunc(seconds - (hours * 3600))
        minutes = trunc(seconds / 60)
        seconds = trunc(seconds - (minutes * 60))

        embed = discord.Embed(
            title = f":alarm_clock: {self.bot.user.name} Uptime",
            description = f"{hours} Hours\n{minutes} Minutes\n{seconds} Seconds",
            color = self.bot.embed_color,
            timestamp = self.bot.embed_ts()
        )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer,
            icon_url = self.bot.footer_image
        )
        await ctx.send(embed = embed)

    @commands.guild_only()
    @commands.command(name='ping', aliases=['pong'], help = 'Gets the current latency of the bot.')
    async def ping(self, ctx):
        """Command | Get Bot Ping

        Returns two values, the ping of the Discord bot to the API,
        and the ping time it takes from when the original message is sent
        to when the bot successfully posts its response.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        embed = discord.Embed(
            title = ":ping_pong: Pong!",
            description = "Calculating ping time...",
            color = self.bot.embed_color,
        )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer,
            icon_url = self.bot.footer_image
        )
        m = await ctx.send(embed = embed)

        embed = discord.Embed(
            title = ":ping_pong: Pong!",
            description = "Message latency is {} ms\nDiscord API Latency is {} ms".format(
                trunc((m.created_at - ctx.message.created_at).total_seconds() * 1000),
                trunc(self.bot.latency * 1000)
            ),
            color = self.bot.embed_color
        )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer,
            icon_url = self.bot.footer_image
        )
        await m.edit(embed = embed)

    @commands.guild_only()
    @commands.command(name='invite', help = 'Returns the server invite link.', brief = "")
    async def invite(self, ctx):
        """Command | Get Server Invite

        Returns a static invite link which is set in the Config.yml file.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        embed = discord.Embed(
            title = "Invite Link",
            description = f"{self.bot.invite_link}",
            color = self.bot.embed_color
        )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer,
            icon_url = self.bot.footer_image
        )
        await ctx.send(embed = embed)

def setup(bot):
    """Setup

    The function called by Discord.py when adding another file in a multi-file project.
    """
    bot.add_cog(General(bot))
