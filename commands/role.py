import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime

# 🎨 Couleur + image
COLOR = discord.Color.from_str("#C9B6D9")
IMAGE_URL = "https://cdn.discordapp.com/attachments/1102406059722801184/1358641522396102727/88404701-6A3B-462A-B81A-507325387F6B.png?ex=67f53dc5&is=67f3ec45&hm=2444b63ea252bc0ce9850708a3d2c6d6e0f7a48dc1c141186143a925f09e3340&"

# === DICTIONNAIRES DE RÔLES ===
COLOR_ROLES = {
    "⭑ Eclipse Violet": 1358635151000862756,
    "⭑ Lilac Dream": 1358634767570043062,
    "⭑ Moon Blue": 1358634867071520828,
    "⭑ Mint Aura": 1358635052925452501,
    "⭑ Peach Glow": 1358634962173300856,
    "⭑ Blush Pink": 1358634665963159865,
}

VIBE_ROLES = {
    "⭑ Soft Core": 1358623769178013706,
    "⭑ Dark Romance": 1358624086061875410,
    "⭑ Chaos Babe": 1358624203493998613,
    "⭑ Dreamer": 1358624297354133504,
    "⭑ Celestial Soul": 1358624431311949944,
    "⭑ Lover": 1358624521229172866,
    "⭑ Night Owl": 1358624655585579090,
}

DM_ROLES = {
    "✉️ Open DMs": 1358626277426204703,
    "🔒 Closed DMs": 1358626386524246107,
    "✦ Ask before DM": 1358626530674212981,
}

ABOUT_ROLES = {
    "☁️ Fille / Girl": 1358629690017058868,
    "☁️ Garçon / Men": 1358629858686795796,
    "☁️ Non-binaire / Non-binary": 1358629990752587969,
    "☁️ Secret": 1358630119845138554,
}

PING_ROLES = {
    "⨳ Server update": 1358630855542706395,
    "⨳ Events": 1358630993761796266,
    "⨳ welcome in": 1358631151992045608,
    "⨳ bump": 1358631180420907119,
    "⨳ Giveaways": 1358631224960090128,
    "⨳ New Partner": 1358631851543236780,
    "⨳ Dead chat": 1358631911471190189,
}

NSFW_ROLES = {
    "⟡ Sub": 1358632531221676195,
    "⟡ Dom": 1358632627170578562,
    "⟡ Switch": 1358632836252434512,
    "⟡ Brat": 1358632944201105610,
    "⟡ Pet / Kitten / Little": 1358633082361741353,
    "⟡ Caregiver / Daddy / Mommy": 1358633195955818698,
    "✦ Soft Only": 1358633371965722770,
    "✦ Hard / Rough ok": 1358633520913846382,
    "✦ Kinks open": 1358633616929980646,
    "✦ BDSM curious": 1358633718675280043,
}

# === CLASSES DE BOUTONS ===

class ExclusiveButton(Button):
    def __init__(self, label, role_id, all_ids):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.role_id = role_id
        self.all_ids = all_ids

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        selected = guild.get_role(self.role_id)

        removed = []
        for rid in self.all_ids:
            r = guild.get_role(rid)
            if r in member.roles and r != selected:
                await member.remove_roles(r)
                removed.append(r.name)

        if selected in member.roles:
            await member.remove_roles(selected)
            msg = f"❌ **{selected.name}** retiré.\n❌ **{selected.name}** removed."
        else:
            await member.add_roles(selected)
            msg = f"✅ **{selected.name}** attribué !\n✅ **{selected.name}** given!"

        await interaction.response.send_message(msg, ephemeral=True)

class MultiRoleButton(Button):
    def __init__(self, label, role_id):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        role = interaction.guild.get_role(self.role_id)

        if role in member.roles:
            await member.remove_roles(role)
            msg = f"❌ **{role.name}** retiré.\n❌ **{role.name}** removed."
        else:
            await member.add_roles(role)
            msg = f"✅ **{role.name}** attribué !\n✅ **{role.name}** given!"

        await interaction.response.send_message(msg, ephemeral=True)

# === VUES DE RÔLES ===

class ColorRolesView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for name, role_id in COLOR_ROLES.items():
            self.add_item(ExclusiveButton(name, role_id, list(COLOR_ROLES.values())))

class ExclusiveRoleView(View):
    def __init__(self, role_dict):
        super().__init__(timeout=None)
        role_ids = list(role_dict.values())
        for name, role_id in role_dict.items():
            self.add_item(ExclusiveButton(name, role_id, role_ids))

class MultiRoleView(View):
    def __init__(self, role_dict):
        super().__init__(timeout=None)
        for name, role_id in role_dict.items():
            self.add_item(MultiRoleButton(name, role_id))

# === VUE PRINCIPALE ===

class MainRoleView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="༄ Color Roles ༄", style=discord.ButtonStyle.primary)
    async def color_roles(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🎨 Couleurs...", view=ColorRolesView(), ephemeral=True)

    @discord.ui.button(label="⭑ VIBES ⭑", style=discord.ButtonStyle.primary)
    async def vibe_roles(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🎭 Vibes...", view=MultiRoleView(VIBE_ROLES), ephemeral=True)

    @discord.ui.button(label="𓈒𖥔˚｡˖ DM STATUS ˖ ࣪⭑", style=discord.ButtonStyle.primary)
    async def dm_status(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("✉️ DM Status...", view=ExclusiveRoleView(DM_ROLES), ephemeral=True)

    @discord.ui.button(label="𓈒𖥔˚｡˖ About / À propos ˖", style=discord.ButtonStyle.primary)
    async def about_roles(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("☁️ À propos...", view=ExclusiveRoleView(ABOUT_ROLES), ephemeral=True)

    @discord.ui.button(label="⨳ PING ⨳", style=discord.ButtonStyle.primary)
    async def ping_roles(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔔 Ping...", view=MultiRoleView(PING_ROLES), ephemeral=True)

    @discord.ui.button(label="⟡ NSFW Roles ⟡", style=discord.ButtonStyle.danger)
    async def nsfw_roles(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔞 NSFW...", view=MultiRoleView(NSFW_ROLES), ephemeral=True)

# === COG PRINCIPAL AVEC LA STRUCTURE REQUISE ===

class RoleSetupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rolesetup")
    @commands.has_permissions(administrator=True)
    async def rolesetup_prefix(self, ctx):
        await self.send_roles_embed(ctx)

    @app_commands.command(name="rolesetup", description="Envoie le panneau de sélection des rôles.")
    @app_commands.checks.has_permissions(administrator=True)
    async def rolesetup_slash(self, interaction: discord.Interaction):
        await self.send_roles_embed(interaction)

    async def send_roles_embed(self, ctx_or_inter):
        embed = discord.Embed(
            title="𓈒𖥔˚｡˖ 𝐑𝐎𝐋𝐄𝐒 𝐈𝐍𝐓𝐄𝐑𝐀𝐂𝐓𝐈𝐅𝐒 ˖ ࣪⭑",
            description="**Choisis tes rôles ci-dessous.**\n**Select your roles below.**",
            color=COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=IMAGE_URL)
        embed.set_footer(text="NOCTÆ Role System")

        view = MainRoleView()
        if isinstance(ctx_or_inter, commands.Context):
            await ctx_or_inter.send(embed=embed, view=view)
        else:
            await ctx_or_inter.response.send_message(embed=embed, view=view)

# === EXTENSION ===

async def setup(bot):
    await bot.add_cog(RoleSetupCommand(bot))
