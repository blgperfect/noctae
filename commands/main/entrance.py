import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime

class LanguageRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="langue")
    @commands.has_permissions(administrator=True)
    async def langue_prefix(self, ctx):
        await self.send_language_embed(ctx)

    @app_commands.command(name="langue", description="Affiche les boutons pour choisir la langue.")
    @app_commands.checks.has_permissions(administrator=True)
    async def langue_slash(self, interaction: discord.Interaction):
        await self.send_language_embed(interaction)

    async def send_language_embed(self, ctx_or_inter):
        embed = discord.Embed(
            title="𓈒𖥔˚｡˖ 𝐁𝐈𝐄𝐍𝐕𝐄𝐍𝐔𝐄 𝐃𝐀𝐍𝐒 𝐍𝐎𝐂𝐓Æ ˖ ࣪⭑",
            description=(
                "Welcome to NOCTÆ, a soft & aesthetic place for celestial souls.\n\n"
                "Merci de choisir ta langue pour accéder aux règles et au serveur. 🌙\n"
                "Please choose your language to see the rules & access the server. ✨"
            ),
            color=discord.Color.from_str("#BDA3FF"),
            timestamp=datetime.utcnow()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102406059722801184/1358867848071614696/raw.png?ex=67f567cd&is=67f4164d&hm=4c41cfcc9692b25e39830acbc646bdeb7713a5f9f1a58cd4940c7ce945b8eb13&")
        embed.set_footer(text="NOCTÆ System | Rôles linguistiques")

        view = LanguageButtonView()
        if isinstance(ctx_or_inter, commands.Context):
            await ctx_or_inter.send(embed=embed, view=view)
        else:
            await ctx_or_inter.response.send_message(embed=embed, view=view)

class LanguageButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.rules_channel_id = 1358605942106755092

    async def toggle_role_and_notify(self, interaction: discord.Interaction, role_id: int, lang: str):
        role = interaction.guild.get_role(role_id)
        rules_channel = interaction.guild.get_channel(self.rules_channel_id)
        mention = rules_channel.mention if rules_channel else "le salon des règles"

        if not role:
            await interaction.response.send_message("❌ Rôle introuvable.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)

            messages = {
                "Français": "❌ Rôle **Français** retiré.\nTu n'as plus accès au serveur.\nMerci de rechoisir ta langue.",
                "English": "❌ **English** role removed.\nYou no longer have access to the server.\nPlease choose your language again.",
                "Both": (
                    "❌ Rôle **Les deux** retiré.\nTu n'as plus accès au serveur.\nMerci de rechoisir ta langue.\n\n"
                    "❌ **Both** role removed.\nYou no longer have access to the server.\nPlease choose your language again."
                )
            }

            await interaction.response.send_message(messages[lang], ephemeral=True)
        else:
            await interaction.user.add_roles(role)

            messages = {
                "Français": f"✅ Rôle **Français** attribué.\nMerci de lire attentivement {mention} 🇫🇷",
                "English": f"✅ **English** role given.\nPlease read the rules in {mention} 🇬🇧",
                "Both": f"✅ Rôle **Les deux** donné.\nMerci de lire {mention} en 🇫🇷 et 🇬🇧"
            }

            await interaction.response.send_message(messages[lang], ephemeral=True)

    @discord.ui.button(label="🇫🇷 Français", style=discord.ButtonStyle.primary, custom_id="lang_fr")
    async def fr_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role_and_notify(interaction, 1358619683984511006, "Français")

    @discord.ui.button(label="🇬🇧 English", style=discord.ButtonStyle.success, custom_id="lang_en")
    async def en_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role_and_notify(interaction, 1358619777140133949, "English")

    @discord.ui.button(label="🌐 Les deux / Both", style=discord.ButtonStyle.secondary, custom_id="lang_both")
    async def both_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role_and_notify(interaction, 1358619857922556034, "Both")

async def setup(bot):
    await bot.add_cog(LanguageRole(bot))
