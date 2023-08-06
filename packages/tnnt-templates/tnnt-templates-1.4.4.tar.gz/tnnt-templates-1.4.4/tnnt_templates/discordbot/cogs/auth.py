"""
"Auth" cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

import logging

from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands

from django.conf import settings

from aadiscordbot.app_settings import get_site_url, get_admins

from allianceauth.services.modules.discord.models import DiscordUser
from allianceauth.eveonline.evelinks.eveimageserver import (
    alliance_logo_url,
    corporation_logo_url,
)

logger = logging.getLogger(__name__)


class Auth(commands.Cog):
    """
    A Collection of Authentication Tools for Alliance Auth
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def auth(self, ctx):
        """
        Returns a link to the AllianceAuth Install
        Used by many other Bots and is a common command that users will attempt to run.
        """

        await ctx.trigger_typing()

        embed = Embed(title="Alliance Auth")

        try:
            if settings.TNNT_TEMPLATE_ENTITY_ID == 1:
                embed.set_thumbnail(url=get_site_url + "static/icons/allianceauth.png")
            else:
                if settings.TNNT_TEMPLATE_ENTITY_TYPE == "alliance":
                    embed.set_thumbnail(
                        url=alliance_logo_url(settings.TNNT_TEMPLATE_ENTITY_ID, 256)
                    )
                elif settings.TNNT_TEMPLATE_ENTITY_TYPE == "corporation":
                    embed.set_thumbnail(
                        url=corporation_logo_url(settings.TNNT_TEMPLATE_ENTITY_ID, 256)
                    )
        except AttributeError:
            pass

        embed.colour = Color.blue()

        embed.description = (
            "All authentication functions for this Discord "
            "server are handled through our Alliance Auth instance."
        )

        url = get_site_url()

        embed.add_field(
            name="Auth Link",
            value="[{auth_url}]({auth_url})".format(auth_url=url),
            inline=False,
        )

        return await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def orphans(self, ctx):
        """
        Returns a list of users on this server, who are not known to AA
        """

        if ctx.message.author.id not in get_admins():
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.trigger_typing()
        await ctx.send("Searching for Orphaned Discord Users")
        await ctx.trigger_typing()

        payload = "The following Users cannot be located in Alliance Auth\n"

        member_list = ctx.message.guild.members

        for member in member_list:
            discord_member_id = member.id
            discord_member_is_bot = member.bot

            try:
                discord_member_exists = DiscordUser.objects.get(uid=discord_member_id)
            except DiscordUser.DoesNotExist as exception:
                logger.error(exception)
                discord_member_exists = False

            if discord_member_exists is not False:
                # nothing to do, the user exists. Move on with ur life dude.
                pass

            elif discord_member_is_bot is True:
                # lets also ignore bots here
                pass
            else:
                # Dump the payload if it gets too big
                if len(payload) > 1000:
                    try:
                        await ctx.send(payload)

                        payload = (
                            "The following Users cannot be located in Alliance Auth\n"
                        )
                    except Exception as e:
                        logger.error(e)

                # keep building the payload
                payload = payload + member.mention + "\n"

        try:
            await ctx.send(payload)
        except Exception as e:
            logger.error(e)
            # await ctx.send(payload[0:1999])
            # await ctx.send("Maximum Discord message length reached")


def setup(bot):
    """
    setup the cog
    :param bot:
    """

    bot.add_cog(Auth(bot))
