import discord
from discord.ext import commands
from datetime import datetime

BOOST_CHANNEL_ID = 1358599335109202175
BOOST_IMAGE = "https://cdn.discordapp.com/attachments/1102406059722801184/1358641520151887872/FFD47160-2DCE-4657-BF67-99C72E0EE9A9.png?ex=67f53dc4&is=67f3ec44&hm=f3caac4733a89444f8d991dfd06a21b83443cc89ed9fabffae5c9b308b68cb90&"
EMBED_COLOR = discord.Color.from_str("#DCCEF2")  # doux violet

class BoostMerci(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🎉 Quand quelqu’un boost
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since != after.premium_since and after.premium_since is not None:
            await self.send_boost_message(after)

    # 💻 Commande de test pour admins
    @commands.command(name="testboost")
    @commands.has_permissions(administrator=True)
    async def testboost(self, ctx):
        await self.send_boost_message(ctx.author)
        await ctx.message.delete()

    async def send_boost_message(self, booster: discord.Member):
        channel = booster.guild.get_channel(BOOST_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="˖ ࣪⭑ 𝐍𝐎𝐔𝐕𝐄𝐀𝐔 𝐁𝐎𝐎𝐒𝐓 ˖ ࣪⭑",
            description=(
                f"🌸 Merci {booster.mention} d’avoir illuminé NOCTÆ avec un boost magique !\n"
                f"Une étoile de plus dans notre univers... 💖\n"
                f"> ✦ Tu rends cet espace encore plus doux et spécial.\n\n"
                f"˚₊‧୨୧ Grâce à toi, la lune brille un peu plus fort ce soir."
            ),
            color=EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=BOOST_IMAGE)
        embed.set_footer(text="NOCTÆ • Cœur scintillant boosté")

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BoostMerci(bot))
