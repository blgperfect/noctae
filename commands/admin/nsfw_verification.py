import os
import locale
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

from dotenv import load_dotenv
import motor.motor_asyncio

# === Configuration locale FR
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except Exception:
    pass

# === ENV & Mongo
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
client_mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client_mongo[DATABASE_NAME]

# === CONSTANTES (à adapter à ton serveur)
ROLE_PLUS18       = 1358622354321965248
ROLE_ZONE_ROUGE   = 1358622493019082943
ROLE_JAIL         = 1358930694776295667
ROLE_VERIFIED     = 1358622597285285938
ROLE_NOTIFICATION = 1358619011470065804

CHANNEL_RULES_ID  = 1358611957015646288
CHANNEL_VERIFY_ID = 1358929674696392965
TEMP_CAT_ID       = 1358933384390508744

# === VUE BOUTONS DE LANGUE
class NSFWRulesView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="𓈒𖥔˚｡˖ NSFW Vérification (Français)", style=discord.ButtonStyle.primary, custom_id="nsfwrules:fr")
    async def fr_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="𓈒𖥔˚｡˖ 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍 𝐍𝐒𝐅𝐖 ˖ ࣪⭑",
            description=(
                "Bienvenue dans l’espace de vérification NSFW de NOCTÆ.\n"
                "Pour accéder aux salons NSFW, merci de lire attentivement ce qui suit.\n\n"
                "୨୧ ‧₊✧ 𝐂𝐨𝐧𝐝𝐢𝐭𝐢𝐨𝐧𝐬 :\n"
                "・Tu dois avoir **18 ans ou plus**.\n"
                "・Aucune fausse déclaration ne sera tolérée.\n"
                "・L'équipe se réserve le droit de refuser l'accès en cas de doute.\n"
                "・Ton âge ne sera pas affiché publiquement.\n\n"
                "✧ ˚₊ 𝐐𝐮𝐞 𝐟𝐚𝐮𝐭-𝐢𝐥 𝐟𝐚𝐢𝐫𝐞 ?\n"
                "▸ Envoie simplement ton âge ici (exemple : `18`)\n\n"
                "⤷ Un membre du staff t’attribuera le rôle `+18` s’il valide ta demande.\n"
                "⤷ Ensuite, tu auras accès à l’espace NSFW.\n\n"
                "✧ ˚₊ 𝐀𝐯𝐞𝐫𝐭𝐢𝐬𝐬𝐞𝐦𝐞𝐧𝐭 :\n"
                "Le non-respect des règles NSFW entraînera une exclusion immédiate.\n"
                "Le **respect, le consentement et la confidentialité** sont obligatoires."
            ),
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="𓈒𖥔˚｡˖ NSFW Verification (English)", style=discord.ButtonStyle.success, custom_id="nsfwrules:en")
    async def en_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="𓈒𖥔˚｡˖ NSFW 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍 ˖ ࣪⭑",
            description=(
                "Welcome to NOCTÆ's NSFW verification space.\n"
                "To access the NSFW channels, please read carefully.\n\n"
                "୨୧ ‧₊✧ 𝐂𝐨𝐧𝐝𝐢𝐭𝐢𝐨𝐧𝐬 :\n"
                "・You must be **18 years old or older**.\n"
                "・Any false declaration will result in an immediate ban.\n"
                "・Staff reserves the right to deny access if there is any doubt.\n"
                "・Your age will not be displayed publicly.\n\n"
                "✧ ˚₊ 𝐖𝐡𝐚𝐭 𝐬𝐡𝐨𝐮𝐥𝐝 𝐲𝐨𝐮 𝐝𝐨 ?\n"
                "▸ Just send your age here (example: `18`)\n\n"
                "⤷ A staff member will assign you the `+18` role once approved.\n"
                "⤷ Then you’ll gain access to the NSFW space.\n\n"
                "✧ ˚₊ 𝐖𝐚𝐫𝐧𝐢𝐧𝐠 :\n"
                "**Respect, consent, and confidentiality** are strictly required."
            ),
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# === VUE POUR BOUTON DE VÉRIFICATION
class JailVerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vérifier / Verify", style=discord.ButtonStyle.success, custom_id="jail:verify")
    async def verify_btn(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="Voici comment te vérifier / How to Verify",
            description=(
                "**FR :** Prends une photo nette de toi avec une feuille contenant la date, le nom du serveur (NOCTÆ) et ton pseudo.\n"
                "En cas de doute, une photo de ta carte d'identité pourra être demandée (visage + date de naissance visibles uniquement).\n\n"
                "**EN :** Take a clear photo of yourself holding a paper with today's date, server name (NOCTÆ), and your username.\n"
                "If suspicious, we may ask for your ID (only birthdate and face visible).\n\n"
                "→ Ensuite, tape `verify` dans ce salon."
            ),
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )
        await interaction.response.send_message(embed=embed)

# === COG PRINCIPAL
class NSFWCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Slash & Prefix Command pour envoyer règles
    @commands.command(name="nsfwrules")
    @commands.has_permissions(administrator=True)
    async def nsfw_prefix(self, ctx):
        await ctx.send(embed=self.get_lang_embed(), view=NSFWRulesView())

    @app_commands.command(name="nsfwrules", description="Afficher les règles NSFW avec choix de langue.")
    @app_commands.checks.has_permissions(administrator=True)
    async def nsfw_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.get_lang_embed(), view=NSFWRulesView())

    def get_lang_embed(self):
        return discord.Embed(
            title="Veuillez choisir votre langue / Please choose your language",
            description="**Please choose your language for the NSFW rules.**",
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content = message.content.strip()
        if message.channel.id == CHANNEL_RULES_ID:
            if content.isdigit():
                age = int(content)
                guild = message.guild
                if age >= 18:
                    try:
                        await message.author.add_roles(
                            guild.get_role(ROLE_PLUS18),
                            guild.get_role(ROLE_ZONE_ROUGE)
                        )
                        await message.channel.send(f"{message.author.mention} → **Vérification réussie ! Accès NSFW accordé.**")
                    except Exception as e:
                        await message.channel.send(f"Erreur lors de l'attribution des rôles : {e}")
                else:
                    try:
                        await message.author.edit(roles=[guild.get_role(ROLE_JAIL)])
                        verify_chan = guild.get_channel(CHANNEL_VERIFY_ID)
                        embed = discord.Embed(
                            title="VÉRIFICATION NSFW / NSFW VERIFICATION",
                            description=(
                                f"**FR :** Tu as indiqué avoir moins de 18 ans.\n"
                                f"**EN :** You stated you're under 18."
                            ),
                            color=discord.Color.from_str("#C9B6D9"),
                            timestamp=datetime.utcnow()
                        )
                        await verify_chan.send(content=f"{message.author.mention} <@{ROLE_NOTIFICATION}>", embed=embed)
                        await message.channel.send("Merci d’appuyer sur le bouton ci-dessous pour voir comment te vérifier.", view=JailVerifyView())
                    except Exception as e:
                        await message.channel.send(f"Erreur lors de la mise en Jail : {e}")
                await message.delete()
            else:
                await message.delete()

        elif message.channel.id == CHANNEL_VERIFY_ID:
            if content.lower() == "verify":
                if any(r.id == ROLE_JAIL for r in message.author.roles):
                    temp_cat = message.guild.get_channel(TEMP_CAT_ID)
                    temp = await message.guild.create_text_channel(f"jail-{message.author.name}", category=temp_cat)
                    await message.channel.send(f"{message.author.mention} → Salon temporaire créé : {temp.mention}")
                await message.delete()
            else:
                await message.delete()

    @commands.command(name="verify")
    @commands.has_permissions(administrator=True)
    async def admin_verify(self, ctx, member: discord.Member):
        if not ctx.channel.name.startswith("jail-"):
            await ctx.send("❌ Utilise cette commande dans un salon `jail-`.")
            return
        try:
            await member.add_roles(
                ctx.guild.get_role(ROLE_PLUS18),
                ctx.guild.get_role(ROLE_ZONE_ROUGE),
                ctx.guild.get_role(ROLE_VERIFIED)
            )
            if ROLE_JAIL in [r.id for r in member.roles]:
                await member.remove_roles(ctx.guild.get_role(ROLE_JAIL))
            notif_embed = discord.Embed(
                title="Nouvelle vérification Jail / New Jail Verification",
                description="Les admins seront avec toi sous peu.\nAdmins will be with you shortly.",
                color=discord.Color.from_str("#C9B6D9"),
                timestamp=datetime.utcnow()
            )
            await ctx.guild.get_channel(CHANNEL_VERIFY_ID).send(
                content=f"{member.mention} <@{ROLE_NOTIFICATION}>", embed=notif_embed
            )
            await ctx.channel.delete()
        except Exception as e:
            await ctx.send(f"Erreur : {e}")

# Setup du COG
async def setup(bot):
    await bot.add_cog(NSFWCommand(bot))
