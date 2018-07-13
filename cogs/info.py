"""
    MAT's Bot: An open-source, general purpose Discord bot written in Python.
    Copyright (C) 2018  NinjaSnail1080  (Discord User: @NinjaSnail1080#8581)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mat import __version__, find_color
from discord.ext import commands
import discord

import datetime

class Info:
    """Information"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """Info about me"""

        app = await self.bot.application_info()

        embed = discord.Embed(
            title=str(self.bot.user), description=app.description + "\n\n**User/Client ID**: " +
            str(app.id), color=find_color(ctx, ctx.channel.guild))
        embed.set_thumbnail(url=app.icon_url)
        embed.add_field(name="Version", value=__version__)
        embed.add_field(name="Author", value=app.owner)
        embed.add_field(name="Server Count", value=len(self.bot.guilds))
        embed.add_field(name="Language", value="Python 3.6.4")
        embed.add_field(name="Library", value="discord.py (rewrite)")
        embed.add_field(name="License", value="GPL v3.0")
        embed.add_field(name="Github Repo", value="https://github.com/NinjaSnail1080/MATs-Bot",
                        inline=False)
        embed.set_footer(text="Dedicated to WooMAT1417#1142")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """Info about the server"""

        await ctx.channel.trigger_typing()
        s = ctx.channel.guild

        on_members = []
        for m in s.members:
            if m.status != discord.Status.offline:
                on_members.append(m)

        bots = []
        for m in s.members:
            if m.bot:
                bots.append(m)

        anim_emojis = []
        for e in s.emojis:
            if e.animated:
                anim_emojis.append(e)

        embed = discord.Embed(
            title=s.name, description="Server ID: " + str(s.id), color=find_color(
                ctx, ctx.channel.guild))
        embed.set_thumbnail(url=s.icon_url)
        embed.add_field(
            name="Members", value="%d (Online: %d)" % (s.member_count, len(on_members)))
        embed.add_field(name="Roles", value=len(s.roles))
        embed.add_field(name="Text Channels", value=len(s.text_channels))
        embed.add_field(name="Voice Channels", value=len(s.voice_channels))
        embed.add_field(name="Categories", value=len(s.categories))
        if anim_emojis:
            embed.add_field(
                name="Custom Emojis", value="%d (Animated: %d)" % (
                    len(s.emojis), len(anim_emojis)))
        else:
            embed.add_field(name="Custom Emojis", value=len(s.emojis))
        embed.add_field(name="Bots", value=len(bots))
        embed.add_field(name="Region", value=str(s.region).upper())
        embed.add_field(
            name="Verification Level", value=str(s.verification_level).capitalize())
        embed.add_field(
            name="Explicit Content Filter", value=str(s.explicit_content_filter).title())
        if s.afk_channel is not None:
            if s.afk_timeout // 60 == 1:
                minute_s = " minute"
            else:
                minute_s = " minutes"
            embed.add_field(
                name="AFK Channel", value=s.afk_channel.mention + " after " + str(
                    s.afk_timeout // 60) + minute_s)
        else:
            embed.add_field(name="AFK Channel", value="No AFK channel")
        embed.add_field(
            name="Server Created", value=s.created_at.strftime("%b %-d, %Y"))
        if s.features:
            embed.add_field(
                name="Server Features", value="`" + "`, `".join(s.features) + "`", inline=False)
        embed.add_field(
            name="Server Owner", value=s.owner.mention + " (User ID: " + str(s.owner_id) + ")",
            inline=False)

        delta = datetime.datetime.utcnow() - s.created_at

        y = int(delta.total_seconds()) // 31557600  #* Number of seconds in 365.25 days
        mo = int(delta.total_seconds()) // 2592000 % 12  #* Number of seconds in 30 days
        d = int(delta.total_seconds()) // 86400 % 30  #* Number of seconds in 1 day
        h = int(delta.total_seconds()) // 3600 % 24  #* Number of seconds in 1 hour
        mi = int(delta.total_seconds()) // 60 % 60
        se = int(delta.total_seconds()) % 60
        #! Do not change "int(delta.totalseconds())" to "delta.seconds"
        #! For reasons I don't fully understand, it doesn't work

        if y == 1:
            year_s = " year"
        else:
            year_s = " years"
        if mo == 1:
            month_s = " month"
        else:
            month_s = " months"
        if d == 1:
            day_s = " day"
        else:
            day_s = " days"
        if h == 1:
            hour_s = " hour"
        else:
            hour_s = " hours"
        if mi == 1:
            minute_s = " minute"
        else:
            minute_s = " minutes"
        if se == 1:
            second_s = " second"
        else:
            second_s = " seconds"

        footer = []
        if y != 0:
            footer.append(str(y) + year_s + ", ")
        if mo != 0:
            footer.append(str(mo) + month_s + ", ")
        if d != 0:
            footer.append(str(d) + day_s + ", ")
        if h != 0:
            footer.append(str(h) + hour_s + ", ")
        if mi != 0:
            footer.append(str(mi) + minute_s + ", ")
        footer.append("and " + str(se) + second_s + ".")

        embed.set_footer(text=s.name + " has been around for roughly " + "".join(footer))

        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, user=None):
        """Info about a user. By default it'll show your user info, but you can specify a different member of your server.
        Format like this: `<prefix> userinfo (OPTIONAL)<@mention user or user's id>`
        """
        await ctx.channel.trigger_typing()
        if user is None:
            m = ctx.author
        else:
            if not ctx.message.mentions:
                for member in ctx.message.mentions:
                    m = member
                    break
            else:
                m = ctx.channel.guild.get_member(int(user))
                if m is None:
                    await ctx.send("Huh, something went wrong. You're supposed to format the "
                                   "message like this: `<prefix> userinfo (OPTIONAL)<@mention "
                                   "user or user's id>` If you did format it correctly then "
                                   "the user id you put is probably invalid, or it was for "
                                   "someone who isn't in this server.\n\nJust so that this "
                                   "command doesn't go to waste, here's *your* user info:")
                    m = ctx.author

        roles = []
        for r in m.roles:
            if r.name != "@everyone":
                roles.append("`" + r.name + "`")
        roles = roles[::-1]

        if m.activity is not None:
            if m.activity.type == discord.ActivityType.listening:
                t = "Listening to"
                a = m.activity.title
            elif m.activity.type == discord.ActivityType.streaming:
                t = "Streaming"
                a = m.activity.name
            elif m.activity.type == discord.ActivityType.watching:
                t = "Watching"
                a = m.activity.name
            else:
                t = "Playing"
                a = m.activity.name
        else:
            t = "Playing"
            a = "Nothing"

        embed = discord.Embed(
            title=str(m), description="User ID: " + str(m.id), color=find_color(
                ctx, ctx.channel.guild))
        embed.set_thumbnail(url=m.avatar_url)

        embed.add_field(name="Display Name", value=m.display_name)
        embed.add_field(name="Status", value=str(m.status).title())
        embed.add_field(name="Color", value=str(m.color))
        embed.add_field(name=t, value=a)
        embed.add_field(name="Top Role", value=m.top_role)
        embed.add_field(name="Joined Server", value=m.joined_at.strftime("%b %-d, %Y"))
        if m.bot:
            embed.add_field(name="Bot?", value="Yes")
        else:
            embed.add_field(name="Bot?", value="No")
        embed.add_field(name="Joined Discord", value=m.created_at.strftime("%b %-d, %Y"))
        if roles:
            embed.add_field(
                name="Roles (" + str(len(roles)) + ")", value=", ".join(roles), inline=False)
        else:
            embed.add_field(name="Roles", value="`No roles`")

        delta = datetime.datetime.utcnow() - m.created_at

        y = int(delta.total_seconds()) // 31557600  #* Number of seconds in 356.25 days
        mo = int(delta.total_seconds()) // 2592000 % 12  #* Number of seconds in 30 days
        d = int(delta.total_seconds()) // 86400 % 30  #* Number of seconds in 1 day
        h = int(delta.total_seconds()) // 3600 % 24  #* Number of seconds in 1 hour
        mi = int(delta.total_seconds()) // 60 % 60
        se = int(delta.total_seconds()) % 60
        #! Do not change "int(delta.totalseconds())" to "delta.seconds"
        #! For reasons I don't fully understand, it doesn't work

        if y == 1:
            year_s = " year"
        else:
            year_s = " years"
        if mo == 1:
            month_s = " month"
        else:
            month_s = " months"
        if d == 1:
            day_s = " day"
        else:
            day_s = " days"
        if h == 1:
            hour_s = " hour"
        else:
            hour_s = " hours"
        if mi == 1:
            minute_s = " minute"
        else:
            minute_s = " minutes"
        if se == 1:
            second_s = " second"
        else:
            second_s = " seconds"

        footer = []
        if y != 0:
            footer.append(str(y) + year_s + ", ")
        if mo != 0:
            footer.append(str(mo) + month_s + ", ")
        if d != 0:
            footer.append(str(d) + day_s + ", ")
        if h != 0:
            footer.append(str(h) + hour_s + ", ")
        if mi != 0:
            footer.append(str(mi) + minute_s + ", ")
        footer.append("and " + str(se) + second_s + ".")

        embed.set_footer(
            text=m.name + " has been on Discord for roughly " + "".join(footer))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
