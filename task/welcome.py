import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1358606087183532203
        self.image_url = "https://cdn.discordapp.com/attachments/1102406059722801184/1358889095790596287/C00E1126-4A6F-4184-BCBB-0912DF08F119.png?ex=67f57b97&is=67f42a17&hm=da39665dcf918afc591e6910e3132a557d9cea78608e252a6c83eca7ac0c1354&"

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        channel = guild.get_channel(self.welcome_channel_id)

        if channel:
            embed = discord.Embed(
                title="𓈒𖥔˚｡˖ 𝐁𝐢𝐞𝐧𝐯𝐞𝐧𝐮𝐞 𝐝𝐚𝐧𝐬 𝐍𝐎𝐂𝐓Æ ˖ ࣪⭑",
                description=(
                    "Une étoile de plus vient d’apparaître... bienvenue chez toi. 🌙\n"
                    "→ Choisis ta langue pour entrer doucement dans l’univers.\n\n"
                    "A new star has appeared... welcome home. 🌟\n"
                    "→ Please choose your language to gently enter the universe."
                ),
                color=discord.Color.from_str("#C9B6D9")
            )
            embed.set_image(url=self.image_url)
            embed.set_footer(text="NOCTÆ Bot — Système d’accueil")

            await channel.send(
    content=(
        f"🌸・**Bienvenue {member.mention}**\n"
        f"🌸・**Welcome {member.mention}**\n\n"
        f"✨ Tu es le **{guild.member_count}ᵉ** membre à rejoindre notre univers.\n"
        f"✨ You are the **{guild.member_count}ᵗʰ** soul joining our universe."
    ),
    embed=embed
)

        # Message privé
        try:
            dm_embed = discord.Embed(
                title="𓈒𖥔˚｡˖ 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐝𝐞 𝐛𝐢𝐞𝐧𝐯𝐞𝐧𝐮𝐞 ˖ ࣪⭑",
                description=(
                    "𓈒𖥔˚｡˖ **𝐌𝐞𝐫𝐜𝐢 𝐝’𝐚𝐯𝐨𝐢𝐫 𝐫𝐞𝐣𝐨𝐢𝐧𝐭 𝐍𝐎𝐂𝐓Æ** ˖ ࣪⭑\n"
                    "Merci d’avoir poussé la porte de notre univers.\n"
                    "Si tu parles français, rejoins aussi notre serveur communautaire ici **tout âge**:\n"
                    "→ https://discord.gg/6hdNFvjXYb\n\n"
                    "𓈒𖥔˚｡˖ **𝐓𝐡𝐚𝐧𝐤𝐬 𝐟𝐨𝐫 𝐣𝐨𝐢𝐧𝐢𝐧𝐠 𝐍𝐎𝐂𝐓Æ** ˖ ࣪⭑\n"
                    "If you're more comfortable in French, feel free to join our cozy FR **all-ages** community:\n"
                    "→ https://discord.gg/6hdNFvjXYb\n\n"
                    "À bientôt entre les étoiles ✦"
                ),
                color=discord.Color.from_str("#C9B6D9")
            )
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            # MP désactivés — on ne fait rien
            pass

async def setup(bot):
    await bot.add_cog(Welcome(bot))
