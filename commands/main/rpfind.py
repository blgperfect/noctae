import discord
from discord.ext import commands
from discord import app_commands

FR_CHANNEL_ID = 1358635318126842074
EN_CHANNEL_ID = 1358635253148684361
COMMAND_REDIRECT_ID = 1358610101237321789
EMBED_COLOR = discord.Color.from_str("#C9B6D9")

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
            label="Description de la recherche / RP description",
            placeholder="Décris ce que tu cherches / Describe what you're looking for",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )

        self.add_item(self.type_rp)
        self.add_item(self.desc)

    async def on_submit(self, interaction: discord.Interaction):
        is_fr = self.language == "fr"
        channel_id = FR_CHANNEL_ID if is_fr else EN_CHANNEL_ID
        channel = interaction.client.get_channel(channel_id)

        header = f"{interaction.user.mention} cherche un RP..." if is_fr else f"{interaction.user.mention} is looking for RP..."
        notice = (
            "⚠️ **Merci de respecter les membres.**\n"
            "Ne répondez **que si vous correspondez réellement** à la recherche.\n"
            "Tout comportement déplacé entraînera une sanction."
            if is_fr else
            "⚠️ **Please respect all members.**\n"
            "Only reply if you genuinely match the request.\n"
            "Any inappropriate behavior will lead to sanctions."
        )
        title = "💜 Recherche RP" if is_fr else "💜 RP Search"
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
        embed.set_footer(text=f"{'Envoyé' if is_fr else 'Posted'} par {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await channel.send(content=header, embed=embed)
        await interaction.response.send_message("✅ Annonce envoyée / Post published successfully!", ephemeral=True)

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

class RPFind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rp-find")
    async def rp_find_prefix(self, ctx: commands.Context):
        await ctx.send("📩 Choisis ta langue / Choose your language to post your RP request:", view=LangSelectView())

    @app_commands.command(name="rp-find", description="Trouver un RP / Find a RP partner")
    async def rp_find_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message("📩 Choisis ta langue / Choose your language to post your RP request:", view=LangSelectView(), ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id in [FR_CHANNEL_ID, EN_CHANNEL_ID]:
            try:
                await message.delete()
                if message.channel.id == FR_CHANNEL_ID:
                    msg = (
                        f"{message.author.mention} tu ne peux pas écrire ici.\n"
                        f"Utilise la commande `/rp-find` ou `!rp-find` dans <#{COMMAND_REDIRECT_ID}>."
                    )
                else:
                    msg = (
                        f"{message.author.mention} you can't write here.\n"
                        f"Use `/rp-find` or `!rp-find` in <#{COMMAND_REDIRECT_ID}>."
                    )
                await message.channel.send(msg, delete_after=10)
            except:
                pass

async def setup(bot):
    await bot.add_cog(RPFind(bot))
