# Tu peux choisir cette fonctionnalité ou encore celle dans task/autoannonce.py ou les deux!
# You can choose this one or the one in task/autoannonce.py or both!
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

ANNOUNCE_ROLE_ID = 1358630855542706395
EMBED_COLOR = discord.Color.from_str("#DCCEF2")  # Pale mauve

class Annonce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="annonce")
    @commands.has_permissions(administrator=True)
    async def annonce_prefix(self, ctx, *, message: str):
        await ctx.message.delete()
        await self.send_announcement(ctx.channel, message)

    @annonce_prefix.error
    async def annonce_prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Tu dois être **administrateur** pour utiliser cette commande.", delete_after=10)

    @app_commands.command(name="annonce", description="Envoyer une annonce jolie + mention.")
    @app_commands.checks.has_permissions(administrator=True)
    async def annonce_slash(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)
        await self.send_announcement(interaction.channel, message)
        await interaction.followup.send("✅ Annonce envoyée !", ephemeral=True)

    @annonce_slash.error
    async def annonce_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                "🚫 Tu dois être **administrateur** pour utiliser cette commande.",
                ephemeral=True
            )

    async def send_announcement(self, channel, message: str):
        role_mention = f"<@&{ANNOUNCE_ROLE_ID}>"

        embed = discord.Embed(
            title="✦ 𝑵𝑶𝑪𝑻Æ • 𝐀𝐍𝐍𝐎𝐍𝐂𝐄 | 𝐀𝐍𝐍𝐎𝐔𝐍𝐂𝐄𝐌𝐄𝐍𝐓",
            description=message,
            color=EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="NOCTÆ Bot • Système d’annonce")

        await channel.send(content=role_mention, embed=embed)

async def setup(bot):
    await bot.add_cog(Annonce(bot))
