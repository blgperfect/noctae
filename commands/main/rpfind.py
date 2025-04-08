import discord
from discord.ext import commands
from discord import app_commands

# Salon IDs
FR_CHANNEL_ID = 1358635318126842074
EN_CHANNEL_ID = 1358635253148684361
EMBED_COLOR = discord.Color.from_str("#C9B6D9")

# === MODAL POUR RP ===
class RPModal(discord.ui.Modal, title="Recherche RP / RP Search"):
    def __init__(self, language: str):
        super().__init__()
        self.language = language

        self.type_rp = discord.ui.TextInput(
            label="Type de RP (sub, dom, love, etc.)",
            placeholder="Ex: brat, dom...",
            max_length=20
        )
        self.desc = discord.ui.TextInput(
            label="Description de la recherche",
            placeholder="Décris ce que tu cherches (max 1000 caractères)",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )

        self.add_item(self.type_rp)
        self.add_item(self.desc)

    async def on_submit(self, interaction: discord.Interaction):
        lang = self.language
        channel_id = FR_CHANNEL_ID if lang == "fr" else EN_CHANNEL_ID
        channel = interaction.client.get_channel(channel_id)

        if lang == "fr":
            header = f"{interaction.user.mention} cherche un RP..."
            notice = (
                "⚠️ **Merci de respecter les membres.**\n"
                "Ne répondez **que si vous correspondez réellement** à la recherche.\n"
                "Tout comportement déplacé entraînera une sanction."
            )
            title = "💜 Recherche RP"
            type_label = "Type"
            desc_label = "Description"
        else:
            header = f"{interaction.user.mention} is looking for RP..."
            notice = (
                "⚠️ **Please respect all members.**\n"
                "Only reply if you genuinely match the request.\n"
                "Any inappropriate behavior will lead to sanctions."
            )
            title = "💜 RP Search"
            type_label = "Type"
            desc_label = "Description"

        embed = discord.Embed(
            title=title,
            description=(
                f"{notice}\n\n"
                f"**{type_label} :** {self.type_rp.value.capitalize()}\n"
                f"**{desc_label} :**\n{self.desc.value}"
            ),
            color=EMBED_COLOR
        )
        embed.set_footer(text=f"Envoyé par {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await channel.send(content=header, embed=embed)
        await interaction.response.send_message("✅ Ton annonce a été publiée avec succès !", ephemeral=True)

# === VUE POUR LANGUE ===
class LangSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.select(
        placeholder="Choisis ta langue / Choose your language",
        options=[
            discord.SelectOption(label="Français", value="fr", emoji="🇫🇷"),
            discord.SelectOption(label="English", value="en", emoji="🇬🇧"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(RPModal(language=select.values[0]))

# === COG PRINCIPAL ===
class RPFind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rp-find")
    async def rp_find_prefix(self, ctx: commands.Context):
        await ctx.send("📩 Choisis ta langue pour publier ton annonce RP :", view=LangSelectView())

    @app_commands.command(name="rp-find", description="Trouver un RP (FR/EN)")
    async def rp_find_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message("📩 Choisis ta langue pour publier ton annonce RP :", view=LangSelectView(), ephemeral=True)

# === SETUP ===
async def setup(bot):
    await bot.add_cog(RPFind(bot))
