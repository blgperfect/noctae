import discord
from discord.ext import commands
from discord import app_commands

class NSFWTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prefix : !nsfw-enable
    @commands.command(name="nsfw-enable")
    @commands.has_permissions(administrator=True)
    async def nsfw_prefix(self, ctx):
        await ctx.channel.edit(nsfw=True)
        await ctx.send("✅ Ce salon est maintenant un salon **NSFW (18+)**.")

    # Slash : /nsfw-enable
    @app_commands.command(name="nsfw-enable", description="Activer le mode NSFW dans ce salon (18+)")
    @app_commands.checks.has_permissions(administrator=True)
    async def nsfw_slash(self, interaction: discord.Interaction):
        await interaction.channel.edit(nsfw=True)
        await interaction.response.send_message("✅ Ce salon est maintenant un salon **NSFW (18+)**.", ephemeral=True)

    # Gestion erreurs permissions
    @nsfw_prefix.error
    async def nsfw_prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Tu dois être administrateur pour utiliser cette commande.")

    @nsfw_slash.error
    async def nsfw_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("❌ Tu dois être administrateur pour utiliser cette commande.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(NSFWTools(bot))
