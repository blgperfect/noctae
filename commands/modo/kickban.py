#avec log / with logs
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

LOG_CHANNEL_ID = 1358606855307268176  # Salon de logs

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === Commande Kick (Prefix)
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_prefix(self, ctx, member: discord.Member, *, reason: str = "Aucune raison / No reason provided"):
        await self.process_kick(ctx, member, reason)

    # === Commande Kick (Slash)
    @app_commands.command(name="kick", description="Expulser un membre (FR/EN Kick)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison / No reason provided"):
        await self.process_kick(interaction, member, reason)

    # === Commande Ban (Prefix)
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_prefix(self, ctx, member: discord.Member, *, reason: str = "Aucune raison / No reason provided"):
        await self.process_ban(ctx, member, reason)

    # === Commande Ban (Slash)
    @app_commands.command(name="ban", description="Bannir un membre (FR/EN Ban)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison / No reason provided"):
        await self.process_ban(interaction, member, reason)

    # === Fonction KICK
    async def process_kick(self, context, member: discord.Member, reason: str):
        author = context.user if isinstance(context, discord.Interaction) else context.author
        guild = context.guild

        # 🔒 Protection hiérarchie
        if member.top_role >= author.top_role:
            msg = (
                "❌ Tu ne peux pas expulser ce membre, son rôle est égal ou supérieur au tien.\n"
                "You can't kick this member — their role is equal or higher than yours."
            )
            if isinstance(context, discord.Interaction):
                await context.response.send_message(msg, ephemeral=True)
            else:
                await context.send(msg, delete_after=10)
            return

        # ✉️ DM bilingue
        try:
            await member.send(
                f"**Bonjour {member.name},**\n"
                f"Tu as été **expulsé (kick)** du serveur **{guild.name}**.\n"
                f"**Raison :** {reason}\n\n"
                f"---\n"
                f"**Hello {member.name},**\n"
                f"You have been **kicked** from **{guild.name}**.\n"
                f"**Reason :** {reason}"
            )
        except discord.Forbidden:
            pass  # DM fermé

        await member.kick(reason=reason)

        embed = discord.Embed(
            title="🚪 Membre Expulsé / Member Kicked",
            description=f"{member.mention} (`{member}`) a été expulsé.",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="👮 Par / By", value=author.mention, inline=True)
        embed.add_field(name="📄 Raison / Reason", value=reason, inline=False)

        log_channel = guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

        if isinstance(context, discord.Interaction):
            await context.response.send_message(f"{member} a été expulsé ✅", ephemeral=True)
        else:
            await context.send(f"{member.mention} a été expulsé ✅")

    # === Fonction BAN
    async def process_ban(self, context, member: discord.Member, reason: str):
        author = context.user if isinstance(context, discord.Interaction) else context.author
        guild = context.guild

        # 🔒 Protection hiérarchie
        if member.top_role >= author.top_role:
            msg = (
                "❌ Tu ne peux pas bannir ce membre, son rôle est égal ou supérieur au tien.\n"
                "You can't ban this member — their role is equal or higher than yours."
            )
            if isinstance(context, discord.Interaction):
                await context.response.send_message(msg, ephemeral=True)
            else:
                await context.send(msg, delete_after=10)
            return

        # ✉️ DM bilingue
        try:
            await member.send(
                f"**Bonjour {member.name},**\n"
                f"Tu as été **banni** du serveur **{guild.name}**.\n"
                f"**Raison :** {reason}\n\n"
                f"---\n"
                f"**Hello {member.name},**\n"
                f"You have been **banned** from **{guild.name}**.\n"
                f"**Reason :** {reason}"
            )
        except discord.Forbidden:
            pass  # DM fermé

        await member.ban(reason=reason)

        embed = discord.Embed(
            title="🔨 Membre Banni / Member Banned",
            description=f"{member.mention} (`{member}`) a été banni.",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="👮 Par / By", value=author.mention, inline=True)
        embed.add_field(name="📄 Raison / Reason", value=reason, inline=False)

        log_channel = guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

        if isinstance(context, discord.Interaction):
            await context.response.send_message(f"{member} a été banni ✅", ephemeral=True)
        else:
            await context.send(f"{member.mention} a été banni ✅")

# === Setup
async def setup(bot):
    await bot.add_cog(Moderation(bot))
