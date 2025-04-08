import os
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Select
from datetime import datetime
from dotenv import load_dotenv
import motor.motor_asyncio

# === ENV + Mongo
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client_mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client_mongo[DATABASE_NAME]
tickets_col = db["tickets"]

# === CONSTS
TICKET_CATS = {
    "fr": 1358611466835464364,
    "en": 1358611520753238198
}
TICKET_PANEL = {
    "fr": 1358611177852375241,
    "en": 1358611219711397988
}
TICKET_LOGS = 1359275755539796138
URGENT_ROLE_ID = 1358619011470065804
ALLOWED_ROLES_FR = [1358619683984511006, 1358619857922556034]
ALLOWED_ROLES_EN = [1358619777140133949, 1358619857922556034]
class TicketView(View):
    def __init__(self, lang: str):
        super().__init__(timeout=None)
        self.lang = lang
        self.add_item(TicketTypeSelect(lang))
        self.add_item(ApplicationSelect(lang))

class TicketTypeSelect(Select):
    def __init__(self, lang: str):
        options = [
            discord.SelectOption(label="Signalement", value="signalement"),
            discord.SelectOption(label="Urgence", value="urgence"),
            discord.SelectOption(label="Partenariat", value="partenariat"),
        ]
        super().__init__(placeholder="Sélectionne une raison..." if lang == "fr" else "Choose a reason...",
                         min_values=1, max_values=1, options=options)
        self.lang = lang

    async def callback(self, interaction: discord.Interaction):
        await create_ticket(interaction, self.values[0], self.lang)

class ApplicationSelect(Select):
    def __init__(self, lang: str):
        options = [
            discord.SelectOption(label="Administration", value="administration"),
            discord.SelectOption(label="Modérateur", value="moderateur"),
            discord.SelectOption(label="Animateur", value="animateur"),
            discord.SelectOption(label="Surveillant", value="surveillant"),
            discord.SelectOption(label="Partner Manager", value="partner_manager"),
        ]
        super().__init__(placeholder="Postuler en tant que..." if lang == "fr" else "Apply for role...",
                         min_values=1, max_values=1, options=options)
        self.lang = lang

    async def callback(self, interaction: discord.Interaction):
        await create_ticket(interaction, self.values[0], self.lang)
async def create_ticket(interaction: discord.Interaction, reason: str, lang: str):
    guild = interaction.guild
    user = interaction.user

    # Vérifie les rôles autorisés
    allowed_roles = ALLOWED_ROLES_FR if lang == "fr" else ALLOWED_ROLES_EN
    if not any(role.id in allowed_roles for role in user.roles):
        await interaction.response.send_message(
            "❌ Tu n'as pas la permission d'ouvrir un ticket." if lang == "fr" else "❌ You cannot open a ticket.",
            ephemeral=True
        )
        return

    # Anti double ticket
    existing = await tickets_col.find_one({"user_id": user.id, "status": "open"})
    if existing:
        await interaction.response.send_message(
            "❌ Tu as déjà un ticket ouvert." if lang == "fr" else "❌ You already have an open ticket.",
            ephemeral=True
        )
        return

    # Création du salon
    category = guild.get_channel(TICKET_CATS[lang])
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True
        )
    }
    ticket_name = f"ticket-{user.name}".lower()
    channel = await guild.create_text_channel(ticket_name, category=category, overwrites=overwrites)

    # Enregistrement en base
    await tickets_col.insert_one({
        "_id": channel.id,
        "user_id": user.id,
        "type": reason,
        "status": "open",
        "lang": lang,
        "created_at": datetime.utcnow()
    })

    # Message d’accueil dans le ticket
    await channel.send(content=f"{user.mention}")
    await channel.send(embed=generate_ticket_embed(reason, lang, user))

    await interaction.response.send_message(
        f"✅ Ticket ouvert : {channel.mention}", ephemeral=True
    )

def generate_ticket_embed(reason: str, lang: str, user: discord.Member):
    embed = discord.Embed(color=discord.Color.blurple(), timestamp=datetime.utcnow())
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)

    messages = {
        "signalement": {
            "fr": "Merci d'expliquer ta situation et d'envoyer tout message ou preuve pertinent pour les admins.",
            "en": "Please explain your situation and provide any message or evidence that may help staff."
        },
        "urgence": {
            "fr": f"Merci d'expliquer cette urgence. <@&{URGENT_ROLE_ID}> a été alerté.",
            "en": f"Please describe your urgent situation. <@&{URGENT_ROLE_ID}> has been notified."
        },
        "partenariat": {
            "fr": "Merci de nous soumettre ton lien de serveur ainsi qu’une description claire.",
            "en": "Please provide your server link and a clear description of your partnership offer."
        },
        "administration": {
            "fr": "Merci de nous donner ton expérience, ton horaire et ce que tu peux apporter.",
            "en": "Please share your experience, schedule, and what you can bring to the server."
        }
    }

    default_app_msg = {
        "fr": "Merci de nous donner ton expérience, ton horaire et ce que tu peux apporter.",
        "en": "Please share your experience, schedule, and what you can bring to the server."
    }

    # Type de ticket
    text = messages.get(reason, default_app_msg)[lang]
    title = f"🎫 Ticket - {reason.title()}"
    embed.title = title
    embed.description = text
    return embed
import io

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === Afficher le menu ticket
    @commands.command(name="ticketpanel")
    @commands.has_permissions(manage_channels=True)
    async def ticket_panel(self, ctx):
        if ctx.channel.id == TICKET_PANEL["fr"]:
            lang = "fr"
        elif ctx.channel.id == TICKET_PANEL["en"]:
            lang = "en"
        else:
            await ctx.send("❌ Cette commande doit être utilisée dans un salon ticket dédié (FR ou EN).", delete_after=10)
            return

        embed = discord.Embed(
            title="🎟️ Système de ticket" if lang == "fr" else "🎟️ Ticket System",
            description="Merci de sélectionner la raison de ton ticket." if lang == "fr" else "Please select the reason for your ticket.",
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed, view=TicketView(lang))


    # === Claim le ticket
    @commands.command(name="claim")
    @commands.has_permissions(manage_messages=True)
    async def claim_ticket(self, ctx):
        data = await tickets_col.find_one({"_id": ctx.channel.id, "status": "open"})
        if not data:
            return await ctx.send("❌ Ce salon n’est pas un ticket actif.")
        
        user = ctx.guild.get_member(data["user_id"])
        if not user:
            return await ctx.send("Utilisateur introuvable.")

        lang = data["lang"]
        msg = {
            "fr": f"{ctx.author.mention} a réclamé le ticket, il s'occupe de toi maintenant.",
            "en": f"{ctx.author.mention} claimed this ticket, they will help you now."
        }
        await ctx.send(f"{user.mention}\n{msg[lang]}")

        await tickets_col.update_one({"_id": ctx.channel.id}, {"$set": {"claimed_by": ctx.author.id}})

    # === Fermer le ticket
    @commands.command(name="close")
    @commands.has_permissions(manage_channels=True)
    async def close_ticket(self, ctx):
        data = await tickets_col.find_one({"_id": ctx.channel.id, "status": "open"})
        if not data:
            return await ctx.send("❌ Ce salon n’est pas un ticket actif.")

        # Transcript
        messages = []
        async for msg in ctx.channel.history(limit=None, oldest_first=True):
            timestamp = msg.created_at.strftime('%Y-%m-%d %H:%M')
            messages.append(f"[{timestamp}] {msg.author.name}: {msg.content}")

        transcript = "\n".join(messages)
        transcript_file = discord.File(io.StringIO(transcript), filename=f"transcript-{ctx.channel.name}.txt")

        log_channel = ctx.guild.get_channel(TICKET_LOGS)
        await log_channel.send(
            f"📁 Ticket fermé : {ctx.channel.name}",
            file=transcript_file
        )

        await tickets_col.update_one({"_id": ctx.channel.id}, {"$set": {"status": "closed", "closed_at": datetime.utcnow()}})
        await ctx.send("Fermeture du ticket...")

        await ctx.channel.delete()

    # === Auto fermeture si user quitte
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        open_ticket = await tickets_col.find_one({"user_id": member.id, "status": "open"})
        if not open_ticket:
            return
        guild = self.bot.get_guild(member.guild.id)
        channel = guild.get_channel(open_ticket["_id"])
        if channel:
            try:
                messages = []
                async for msg in channel.history(limit=None, oldest_first=True):
                    timestamp = msg.created_at.strftime('%Y-%m-%d %H:%M')
                    messages.append(f"[{timestamp}] {msg.author.name}: {msg.content}")
                transcript = "\n".join(messages)
                transcript_file = discord.File(io.StringIO(transcript), filename=f"transcript-{channel.name}.txt")

                log_channel = guild.get_channel(TICKET_LOGS)
                await log_channel.send(
                    f"📁 Ticket auto-fermé (départ utilisateur) : {channel.name}",
                    file=transcript_file
                )
            except:
                pass
            await tickets_col.update_one({"_id": channel.id}, {"$set": {"status": "closed", "closed_at": datetime.utcnow()}})
            await channel.delete()

# === Setup
async def setup(bot: commands.Bot):
    await bot.add_cog(TicketSystem(bot))
