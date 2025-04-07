import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime

class RulesView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🇫🇷 Français", style=discord.ButtonStyle.primary, custom_id="rules_fr")
    async def fr_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="˖ ࣪⭑ 𓈒𖥔˚｡˖ 𝐑𝐄̀𝐆𝐋𝐄𝐌𝐄𝐍𝐓 ˖ ࣪⭑",
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="1. ⭑ Respect & bienveillance", value="Aucun propos haineux, moqueur ou toxique ne sera toléré.", inline=False)
        embed.add_field(name="2. ⭑ Consentement avant tout", value="Aucun contenu NSFW ou privé sans accord clair et explicite.", inline=False)
        embed.add_field(name="3. ⭑ Pas de spam ni de pub", value="Pas de promos sauvages, de chaînes ou de DMs non sollicités.", inline=False)
        embed.add_field(name="4. ⭑ Aucun mineur n’est autorisé", value="Le serveur est strictement réservé aux personnes majeures (18+).", inline=False)
        embed.add_field(name="5. ⭑ Le staff veille avec calme", value="En cas de souci, viens en parler. Le staff a le dernier mot.", inline=False)
        embed.set_footer(text="˚₊‧୨୧ Merci de respecter l’énergie douce, safe & sincère de NOCTÆ.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🇬🇧 English", style=discord.ButtonStyle.success, custom_id="rules_en")
    async def en_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="˖ ࣪⭑ 𓈒𖥔˚｡˖ 𝐑𝐔𝐋𝐄𝐒 ˖ ࣪⭑",
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="1. ⭑ Respect & kindness", value="Toxicity, hate or mocking behavior won’t be tolerated.", inline=False)
        embed.add_field(name="2. ⭑ Consent is sacred", value="No NSFW or private content without clear permission.", inline=False)
        embed.add_field(name="3. ⭑ No spam or self-promo", value="No mass DMs, no advertising unless allowed by staff.", inline=False)
        embed.add_field(name="4. ⭑ No minors allowed", value="This server is strictly 18+. If you’re underage, you must leave.", inline=False)
        embed.add_field(name="5. ⭑ Staff holds final word", value="If there’s an issue, talk to us. We’re here, calm & fair.", inline=False)
        embed.set_footer(text="˚₊‧୨୧ Please honor NOCTÆ’s safe, soft and respectful energy.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class RulesCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="regles")
    @commands.has_permissions(administrator=True)
    async def regles_prefix(self, ctx):
        await self.send_rules_embed(ctx)

    @app_commands.command(name="regles", description="Envoie le message de sélection des règles avec boutons.")
    @app_commands.checks.has_permissions(administrator=True)
    async def regles_slash(self, interaction: discord.Interaction):
        await self.send_rules_embed(interaction)

    async def send_rules_embed(self, ctx_or_inter):
        embed = discord.Embed(
            title="˚₊‧୨୧ 𝐑𝐄̀𝐆𝐋𝐄𝐌𝐄𝐍𝐓𝐒 / 𝐑𝐔𝐋𝐄𝐒 ୨୧‧₊˚",
            description="Veuillez choisir votre langue pour consulter le règlement.\nPlease choose your language to view the rules.",
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102406059722801184/1358881058866598101/raw.png?ex=67f5741b&is=67f4229b&hm=3dea3f419687690cc39ffe923748431125eda43b370650e50a723baffce43736&")
        embed.set_footer(text="NOCTÆ Server | Choix de langue")

        view = RulesView()
        if isinstance(ctx_or_inter, commands.Context):
            await ctx_or_inter.send(embed=embed, view=view)
        else:
            await ctx_or_inter.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(RulesCommand(bot))
