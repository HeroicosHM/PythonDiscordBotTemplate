import discord
from discord.ext import commands
import datetime

"""Cog | Error Handler

This cog handles all errors for the bot, preventing
the runtime from crashing or forcing bot exit.

NOTE: All commands are restricted to server use only by default,
remove the `@commands.guild_only()` line before any command that
should also be able to be used in a DM.
"""
class Errors(commands.Cog, name = "Error Handling"):
    """
    Commands relating to bot error handling.
    """
    def __init__(self, bot):
        self.bot = bot
        print("Loaded Error Cog.")

    @commands.guild_only()
    @commands.command(name = "broken", aliases = ['borked'], help = "Used to report when the bot has stopped working.", brief = "")
    async def err_report(self, ctx):
        """Command | Report Broken Bot

        This command is used to report when the bot is broken or stopped working,
        it prints some useful information to the console and attempts to
        ping the owner of the bot.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        app = await self.bot.application_info()
        embed = discord.Embed(
            title = "I'm broken!",
            description = f"Come fix me {app.owner.mention}!",
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
        await ctx.send(content = app.owner.mention, embed = embed)

        print(f"{self.bot.WARN} {self.bot.TIMELOG()} Recieved 'broken' command:")
        failed_com = ctx.message.content.split(' ')
        if len(failed_com) > 1:
            print(f"{' ' * 35} Command: {failed_com[0]} | Args: {' '.join(failed_com[1:])}")
        else:
            print(f"{' ' * 35} Command: {failed_com[0]}")
        print(f"{' ' * 35} Author: {ctx.author} | ID: {ctx.author.id}")
        print(f"{' ' * 35} Channel: {ctx.channel} | ID: {ctx.channel.id}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Listener | Command Error Handler

        Take in command specific errors and return response to user
        based on error.

        If the error is not in the list of directly handled errors,
        reply with the command error, and send a log of the error to
        the log channel.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()
        if isinstance(error, commands.CommandNotFound):
            print(f"{self.bot.WARN} {self.bot.TIMELOG()} Command Not Found:")
            failed_com = ctx.message.content.split(' ')
            if len(failed_com) > 1:
                print(f"{' ' * 35} Command: {failed_com[0]} | Args: {' '.join(failed_com[1:])}")
            else:
                print(f"{' ' * 35} Command: {failed_com[0]}")
            print(f"{' ' * 35} Author: {ctx.author} | ID: {ctx.author.id}")
            print(f"{' ' * 35} Channel: {ctx.channel} | ID: {ctx.channel.id}")

            embed = discord.Embed(
                title = "Command not found.",
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

            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
            embed.timestamp = self.bot.embed_ts()
            await self.bot.log_channel.send(embed = embed)

        elif isinstance(error, commands.BadArgument) and "Member" in str(error) and "not found" in str(error):
            print(f"{self.bot.ERR} {self.bot.TIMELOG()} Member Not Found:")
            failed_com = ctx.message.content.split(' ')
            if len(failed_com) > 1:
                print(f"{' ' * 35} Command: {failed_com[0]} | Args: {' '.join(failed_com[1:])}")
            else:
                print(f"{' ' * 35} Command: {failed_com[0]}")
            print(f"{' ' * 35} Author: {ctx.author} | ID: {ctx.author.id}")
            print(f"{' ' * 35} Channel: {ctx.channel} | ID: {ctx.channel.id}")

            embed = discord.Embed(
                title = "Member not found.",
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

            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
            embed.timestamp = self.bot.embed_ts()
            await self.bot.log_channel.send(embed = embed)

        elif isinstance(error, commands.CheckFailure):
            print(f"{self.bot.WARN} {self.bot.TIMELOG()} User attempted to use command without permission:")
            failed_com = ctx.message.content.split(' ')
            if len(failed_com) > 1:
                print(f"{' ' * 35} Command: {failed_com[0]} | Args: {' '.join(failed_com[1:])}")
            else:
                print(f"{' ' * 35} Command: {failed_com[0]}")
            print(f"{' ' * 35} Author: {ctx.author} | ID: {ctx.author.id}")
            print(f"{' ' * 35} Channel: {ctx.channel} | ID: {ctx.channel.id}")

            embed = discord.Embed(
                title = "Permission Denied",
                description = f"I'm sorry {ctx.author.name}, I'm afraid I can't to that.",
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

            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
            embed.timestamp = self.bot.embed_ts()
            await self.bot.log_channel.send(embed = embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            error = str(error).split(" ")
            error[0] = '`' + error[0] + '`'
            error = " ".join(error)

            print(f"{self.bot.ERR} {self.bot.TIMELOG()} Missing required parameter:")
            print(f"{' ' * 35} Error: {error}")
            failed_com = ctx.message.content.split(' ')
            if len(failed_com) > 1:
                print(f"{' ' * 35} Command: {failed_com[0]} | Args: {' '.join(failed_com[1:])}")
            else:
                print(f"{' ' * 35} Command: {failed_com[0]}")
            print(f"{' ' * 35} Author: {ctx.author} | ID: {ctx.author.id}")
            print(f"{' ' * 35} Channel: {ctx.channel} | ID: {ctx.channel.id}")

            embed = discord.Embed(
                title = "Missing Required Parameter",
                description = error.split(' ')[0],
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

            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
            embed.timestamp = self.bot.embed_ts()
            await self.bot.log_channel.send(embed = embed)

        else:
            embed = discord.Embed(
                title = "Command Failed",
                description = str(error),
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

            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
            embed.timestamp = self.bot.embed_ts()
            await self.bot.log_channel.send(embed = embed)

            await err_report(ctx)
            print(f"{self.bot.ERR} {self.bot.TIMELOG()} {error}")

    @commands.Cog.listener()
    async def on_error(self, error):
        """Listener | Global Error Handler

        The generalized handler for all errors taht happen in the bot,
        preventing suspension of runtime should something go wrong.
        """
        print(f"{self.bot.ERR} {self.bot.TIMELOG()} {error}")

def setup(bot):
    """Setup

    The function called by Discord.py when adding another file in a multi-file project.
    """
    bot.add_cog(Errors(bot))
