import os
import locale
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

from dotenv import load_dotenv
import motor.motor_asyncio

# === Locale FR
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except Exception:
    pass

# === ENV + Mongo
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
client_mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client_mongo[DATABASE_NAME]

# === IDs (à adapter)
ROLE_PLUS18       = 1358622354321965248
ROLE_ZONE_ROUGE   = 1358622493019082943
ROLE_JAIL         = 1358930694776295667
ROLE_VERIFIED     = 1358622597285285938
ROLE_NOTIFICATION = 1358619011470065804

CHANNEL_RULES_ID  = 1358611957015646288
CHANNEL_VERIFY_ID = 1358929674696392965
TEMP_CAT_ID       = 1358933384390508744

# === Vue des règles (boutons langue)
class NSFWRulesView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="𓈒𖥔˚｡˖ NSFW Vérification (Français)", style=discord.ButtonStyle.primary, custom_id="nsfwrules:fr")
    async def fr_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="𓈒𖥔˚｡˖ 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍 𝐍𝐒𝐅𝐖 ˖ ࣪⭑",
            description=(
                "Bienvenue dans l’espace de vérification NSFW de NOCTÆ.\n\n"
                "୨୧ ‧₊✧ 𝐂𝐨𝐧𝐝𝐢𝐭𝐢𝐨𝐧𝐬 :\n"
                "・Tu dois avoir **18 ans ou plus**.\n"
                "・Aucune fausse déclaration ne sera tolérée.\n"
                "・L'équipe peut refuser l'accès si doute.\n"
                "・Ton âge reste privé.\n\n"
                "✧ ˚₊ 𝐐𝐮𝐞 𝐟𝐚𝐮𝐭-𝐢𝐥 𝐟𝐚𝐢𝐫𝐞 ?\n"
                "▸ Envoie juste ton âge (ex: `18`)\n"
                "⤷ Le staff t’attribuera l’accès NSFW."
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
                "Welcome to NOCTÆ's NSFW verification space.\n\n"
                "୨୧ ‧₊✧ Conditions:\n"
                "・You must be **18 or older**.\n"
                "・No false claims allowed.\n"
                "・Staff may deny access if unsure.\n"
                "・Your age stays private.\n\n"
                "✧ ˚₊ What to do?\n"
                "▸ Just type your age (e.g., `18`)\n"
                "⤷ Staff will give NSFW access."
            ),
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# === Vue vérification (mineur)
class JailVerifyView(View):
    def __init__(self, user_id: int):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="Vérifier / Verify", style=discord.ButtonStyle.success, custom_id="jail:verify")
    async def verify_btn(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce bouton n'est pas pour toi.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Voici comment te vérifier / How to Verify",
            description=(
                "**FR :** Prends une photo nette avec :\n"
                "• Ton visage visible\n"
                "• Une feuille avec la **date**, le **serveur** et ton **pseudo**\n"
                "→ Si doute, une photo d'ID peut être demandée.\n\n"
                "**EN :** Take a clear photo showing:\n"
                "• Your face\n"
                "• A paper with **today’s date**, **server name**, and **username**\n"
                "→ If suspicious, we may ask for ID.\n\n"
                "**Tape `verify` dans ce salon** pour créer ton espace."
            ),
            color=discord.Color.from_str("#C9B6D9"),
            timestamp=datetime.utcnow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
# === COG Principal
class NSFWCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nsfwrules")
    @commands.has_permissions(administrator=True)
    async def nsfw_prefix(self, ctx):
        await ctx.send(embed=self.get_lang_embed(), view=NSFWRulesView())

    @app_commands.command(name="nsfwrules", description="Afficher les règles NSFW")
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
        guild = message.guild

        if message.channel.id == CHANNEL_RULES_ID:
            if content.isdigit():
                age = int(content)
                if age >= 18:
                    try:
                        await message.author.add_roles(
                            guild.get_role(ROLE_PLUS18),
                            guild.get_role(ROLE_ZONE_ROUGE)
                        )
                        await message.channel.send(
                            f"{message.author.mention} → **Vérification réussie !** ✅",
                            delete_after=10
                        )
                    except Exception as e:
                        await message.channel.send(f"Erreur : {e}", delete_after=10)
                else:
                    try:
                        # 🔒 Sauvegarde des rôles actuels (hors @everyone)
                        old_roles = [role.id for role in message.author.roles if role != guild.default_role]
                        await db.user_roles.update_one(
                            {"_id": message.author.id},
                            {"$set": {"roles": old_roles}},
                            upsert=True
                        )

                        # 🔒 Attribution du rôle jail
                        jail = guild.get_role(ROLE_JAIL)
                        await message.author.edit(roles=[jail])

                        # 🔔 Embed + ping dans salon de vérif
                        embed = discord.Embed(
                            title="VÉRIFICATION NSFW / NSFW VERIFICATION",
                            description=(
                                f"**FR :** Salut {message.author.mention}, tu as moins de 18 ans.\n"
                                f"**EN :** Hi {message.author.mention}, you are under 18."
                            ),
                            color=discord.Color.from_str("#C9B6D9"),
                            timestamp=datetime.utcnow()
                        )
                        verify_chan = guild.get_channel(CHANNEL_VERIFY_ID)
                        await verify_chan.send(
                            content=f"{message.author.mention}",
                            embed=embed,
                            view=JailVerifyView(user_id=message.author.id)
                        )
                    except Exception as e:
                        await message.channel.send(f"Erreur jail : {e}", delete_after=10)
                await message.delete()
            else:
                await message.delete()

        elif message.channel.id == CHANNEL_VERIFY_ID:
            if content.lower() == "verify":
                if any(r.id == ROLE_JAIL for r in message.author.roles):
                    cat = guild.get_channel(TEMP_CAT_ID)
                    temp = await guild.create_text_channel(f"jail-{message.author.name}", category=cat)
                    embed = discord.Embed(
                        title="Espace privé créé / Private Room Created",
                        description="Un membre de l'équipe va te vérifier sous peu.\nAn admin will verify you shortly.",
                        color=discord.Color.from_str("#C9B6D9"),
                        timestamp=datetime.utcnow()
                    )
                    await temp.send(content=f"{message.author.mention} <@&{ROLE_NOTIFICATION}>", embed=embed)
                    await message.channel.send(
                        f"{message.author.mention} → Salon privé créé : {temp.mention}",
                        delete_after=10
                    )
                await message.delete()
            else:
                await message.delete()

    @commands.command(name="verify")
    @commands.has_permissions(administrator=True)
    async def verify_user(self, ctx, member: discord.Member):
        if not ctx.channel.name.startswith("jail-"):
            await ctx.send("❌ Utilise cette commande dans un salon `jail-...`.", delete_after=10)
            return
        try:
            # 🔁 Récupération des anciens rôles depuis MongoDB
            data = await db.user_roles.find_one({"_id": member.id})
            if data and "roles" in data:
                previous_roles = [
                    ctx.guild.get_role(rid)
                    for rid in data["roles"]
                    if rid != ROLE_JAIL and ctx.guild.get_role(rid)
                ]
            else:
                previous_roles = []

            # ✅ Ajout des rôles NSFW + restaurés
            await member.edit(roles=previous_roles + [
                ctx.guild.get_role(ROLE_PLUS18),
                ctx.guild.get_role(ROLE_ZONE_ROUGE),
                ctx.guild.get_role(ROLE_VERIFIED)
            ])

            # 🔄 Suppression du rôle jail
            await member.remove_roles(ctx.guild.get_role(ROLE_JAIL))

            # 📢 Message embed dans salon général de vérif
            embed = discord.Embed(
                title="Nouvelle vérification Jail / New Jail Verification",
                description="Les admins seront avec toi sous peu.\nAdmins will be with you shortly.",
                color=discord.Color.from_str("#C9B6D9"),
                timestamp=datetime.utcnow()
            )
            await ctx.guild.get_channel(CHANNEL_VERIFY_ID).send(
                content=f"{member.mention} <@&{ROLE_NOTIFICATION}>", embed=embed
            )

            await ctx.send(f"{member.mention} a été vérifié ✅", delete_after=10)
            await ctx.channel.delete()

            # 🧹 Nettoyage MongoDB
            await db.user_roles.delete_one({"_id": member.id})

        except Exception as e:
            await ctx.send(f"❌ Erreur : {e}", delete_after=15)
 
# === Setup
async def setup(bot):
    await bot.add_cog(NSFWCommand(bot))
