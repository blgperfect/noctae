# task/boost_thanks.py
import discord
from discord.ext import commands
from datetime import datetime

BOOST_CHANNEL_ID = 1358599335109202175
BOOST_IMAGE = "https://cdn.discordapp.com/attachments/1102406059722801184/1358641520151887872/FFD47160-2DCE-4657-BF67-99C72E0EE9A9.png"
EMBED_COLOR = discord.Color.from_str("#DCCEF2")

class BoostAutoTask(commands.Cog, name="BoostAutoTask"):
    def __init__(self, bot):
        self.bot = bot
        print("[INIT] BoostAutoTask instancié")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        print(f"[DEBUG] Vérif boost pour {after.display_name}")
        if before.premium_since != after.premium_since and after.premium_since is not None:
            print(f"[✅] {after.display_name} a boosté !")
            await self.send_boost_message(after)

    async def send_boost_message(self, booster: discord.Member):
        channel = booster.guild.get_channel(BOOST_CHANNEL_ID)
        if not channel:
            print(f"[⚠️] Channel introuvable : {BOOST_CHANNEL_ID}")
            return

        embed = discord.Embed(
            title="˖ ࣪⭑ 𝐁𝐎𝐎𝐒𝐓 𝐌𝐄𝐑𝐂𝐈 / 𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 ˖ ࣪⭑",
            description=(
                f"🌸 Merci {booster.mention} d’avoir boosté NOCTÆ !\n"
                f"→ Ton énergie rend notre univers encore plus magique 💖\n"
                f"✦ Grâce à toi, la lune brille un peu plus fort ce soir...\n\n"
                f"🌸 Thank you {booster.mention} for boosting NOCTÆ!\n"
                f"→ Your energy makes our universe even more magical 💖\n"
                f"✦ Thanks to you, the moon shines a little brighter tonight..."
            ),
            color=EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=BOOST_IMAGE)
        embed.set_footer(text="NOCTÆ • Boost détecté automatiquement")

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BoostAutoTask(bot))
    print("✅ BoostAutoTask bien enregistré comme cog.")
