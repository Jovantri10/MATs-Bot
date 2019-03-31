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

from utils import find_color, get_data

from discord.ext import commands
import discord

import asyncio
import re
import os
import random

sigma_responses = ["Woah, who is that other bot? She looks g-g-gorgeous...", "D-D-Does s-s-she "
                   "have a boyf-f-friend?\nAsking for a friend!", "What a beautiful voice..."]
#* MAT has a huge crush on SigmaBot (https://github.com/NeonLights10/Sigma-Kizuna).
#* Whenever she says something, MAT will send one of the above responses.


class Triggers(commands.Cog):
    """Trigger words that the bot will respond to"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.guild is not None:
            if "triggers_disabled" in get_data("server")[str(message.guild.id)]:
                if str(message.channel.id) in get_data("server")[str(message.guild.id)]["triggers_disabled"]:
                    return

        if message.author.id == 281807963147075584:
            #* This is the user ID of SigmaBot, who is the love interest for MAT
            return await message.channel.send(random.choice(sigma_responses))

        if message.guild is not None:
            if random.random() < (10 / message.guild.member_count) / 100:
                return await message.channel.send(file=discord.File(
                    os.path.join("assets", f"{random.choice(['autism.jpg', 'crater.png'])}")))

        if re.search("pinged", message.content, re.IGNORECASE):
            embed = discord.Embed(color=find_color(message))
            embed.set_image(url="https://i.imgur.com/LelDalN.gif")
            return await message.channel.send(content="Pinged?", embed=embed)

        elif (re.search("think", message.content, re.IGNORECASE) or
                  re.search("thonk", message.content, re.IGNORECASE) or
                      re.search("thunk", message.content, re.IGNORECASE) or
                          re.search("thenk", message.content, re.IGNORECASE) or
                              re.search("hmm", message.content, re.IGNORECASE)):
            return await message.add_reaction(":thonk:468520122848509962")

        elif message.content.lower() == "k":
            return await message.channel.send(
                message.author.mention + " This is an auto-response. The person you are trying "
                "to reach has no idea what \"k\" is meant to represent. They assume you wanted "
                "to type \"ok\" but could not expand the energy to type two whole letters since "
                "you were stabbed. The police have been notified.")

        elif ("can't believe" in message.content.lower() or
                  "can't fucking believe" in message.content.lower() or
                      "cant believe" in message.content.lower() or
                          "cant fucking believe" in message.content.lower()):
            return await message.channel.send("You better believe it, scrub")

        elif message.content.lower() == "jesus":
            return await message.channel.send("Christ")

        elif message.content.lower() == "good bot" or message.content.lower() == "best bot":
            async for m in message.channel.history(limit=4):
                if m.author == self.bot.user:
                    await message.channel.send("Why thank you, human!")
                    break
            return

        elif re.search("thank you", message.content, re.IGNORECASE) or re.search(
            "thanks", message.content, re.IGNORECASE):
            async for m in message.channel.history(limit=4):
                if m.author == self.bot.user:
                    await message.channel.send("You're welcome!")
                    break
            return

        elif message.content.lower() == "f" or re.search(
            "press f", message.content, re.IGNORECASE):
            return await message.channel.send("F")

        elif message.content.lower() == "first":
            await message.channel.send("second")
            await message.channel.trigger_typing()
            await asyncio.sleep(1)
            await message.channel.send("third")
            await message.channel.trigger_typing()
            await asyncio.sleep(1)
            return await message.channel.send("∞th")

        elif message.content.lower() == "ping":
            return await message.channel.send("pong")

        elif re.search("no u", message.content, re.IGNORECASE):
            return await message.channel.send("no u")

        elif (re.search("kill myself", message.content, re.IGNORECASE) or
                  re.search("live anymore", message.content, re.IGNORECASE) or
                      re.search("end it all", message.content, re.IGNORECASE) or
                          re.search("all to stop", message.content, re.IGNORECASE) or
                              re.search("commit suicide", message.content, re.IGNORECASE) or
                                  re.search("want to die", message.content, re.IGNORECASE)):
            embed = discord.Embed(
                title="There is help.", description="[Click here to see the suicide "
                "prevention hotlines and other resources for the country you live in]"
                "(https://13reasonswhy.info/)\nIf you call, they'll be able to help you, "
                "I promise.", color=find_color(message))
            return await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Triggers(bot))
