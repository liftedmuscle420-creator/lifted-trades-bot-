"""
Lifted Trades Discord bot.
- Welcomes new members with a branded embed + DM
- Auto-assigns the free member role
- Slash commands: /model /risk /psychology /links

Setup: see README.md
"""

import os

import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_TOKEN"]
WELCOME_CHANNEL_ID = int(os.environ.get("WELCOME_CHANNEL_ID", "0") or 0)
FREE_ROLE_NAME = os.environ.get("FREE_ROLE_NAME", "Free Member")
GUILD_ID = os.environ.get("GUILD_ID")  # optional: instant slash-command sync
# Channel IDs used in the welcome message — set these to your real channels
CH_FREE_PLAYS_ID = os.environ.get("CH_FREE_PLAYS_ID", "")
CH_COURSE_ID = os.environ.get("CH_COURSE_ID", "")
CH_UPGRADE_ID = os.environ.get("CH_UPGRADE_ID", "")


def _ch(channel_id: str, fallback: str) -> str:
    """Render a clickable channel mention, or a fallback name if no ID is set."""
    return f"<#{channel_id}>" if channel_id else f"#{fallback}"

BRAND_GREEN = 0x39FF14
BRAND_PURPLE = 0xA855F7

intents = discord.Intents.default()
intents.members = True  # privileged: enable "Server Members Intent" in the portal

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    if GUILD_ID:
        await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
    else:
        await bot.tree.sync()
    print(f"Online as {bot.user} 🦅")


@bot.event
async def on_member_join(member: discord.Member):
    # 1. Auto-role
    role = discord.utils.get(member.guild.roles, name=FREE_ROLE_NAME)
    if role:
        try:
            await member.add_roles(role, reason="Lifted Trades auto-role")
        except discord.Forbidden:
            print(f"Missing permission to assign role in {member.guild.name}")

    # 2. Public welcome (styled like the Honey Drip greetings bot)
    if WELCOME_CHANNEL_ID:
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            free_plays = _ch(CH_FREE_PLAYS_ID, "free-plays")
            course = _ch(CH_COURSE_ID, "start-here")
            upgrade = _ch(CH_UPGRADE_ID, "upgrade-to-premium")
            embed = discord.Embed(
                title="🦅 Welcome to Lifted Trades 🦅",
                description=(
                    f"Good to have you, {member.mention}.\n\n"
                    "Take a minute to look around. Check out "
                    f"{free_plays} for free breakdowns and watchlists, and visit "
                    f"{course} to learn the Eagle Eye Model. "
                    "The paid tiers are where we move different — "
                    "daily game plans, live sessions, direct access, the inner circle.\n\n"
                    f"When you want in, head to {upgrade}.\n\n"
                    "**Lifted Trades**\n"
                    "DISCIPLINE BUILDS FREEDOM."
                ),
                color=BRAND_GREEN,
            )
            embed.set_footer(text="Lifted Trades • Risk management and psychology first")
            await channel.send(content=member.mention, embed=embed)

    # 3. DM welcome (best effort — fails if user has DMs closed)
    try:
        await member.send(
            "Welcome to **Lifted Trades** 🦅\n\n"
            "Quick start: read #start-here, introduce yourself in #introductions, "
            "and run `/model` to learn the Eagle Eye Model.\n\n"
            "Discipline builds freedom."
        )
    except discord.Forbidden:
        pass


@bot.tree.command(name="model", description="The Eagle Eye Model — how we trade")
async def model_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🦅 The Eagle Eye Model",
        description=(
            "**LOCATION → RAID → SHIFT → 1M OB + FVG → EXECUTE**\n\n"
            "1. **Location** — find a clean higher-timeframe Fair Value Gap.\n"
            "2. **Level** — if an Order Block sits with the HTF FVG, that's the level. "
            "If not, find the meaningful swing inside the FVG (swing low for longs, swing high for shorts).\n"
            "3. **Raid** — wait for price to take that liquidity. The raid means interest, NOT entry.\n"
            "4. **Shift** — drop to the 1M and confirm a Change in State of Delivery with displacement.\n"
            "5. **Execute** — the 1M OB + 1M FVG around the shift is the entry zone. Target opposing liquidity.\n\n"
            "⛔ **Hard rule: no raid / no shift / no 1M OB + FVG = NO TRADE.**\n"
            "Define invalidation and target BEFORE execution."
        ),
        color=BRAND_GREEN,
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="risk", description="Risk management rules")
async def risk_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛡️ Risk Management",
        description=(
            "• Risk a small fixed % per trade — survive first, profit second.\n"
            "• Define your invalidation BEFORE you enter. No invalidation = no trade.\n"
            "• Cap daily loss. Hit the cap → screens off, no exceptions.\n"
            "• Position size comes from the stop, never from conviction.\n"
            "• One model, one plan. Revenge trading is account suicide."
        ),
        color=BRAND_PURPLE,
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="psychology", description="Trading psychology reminders")
async def psychology_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🧠 Psychology",
        description=(
            "• Patience pays more than any strategy.\n"
            "• Fewer trades, better trades.\n"
            "• Journal every trade — review weekly.\n"
            "• You don't need to be right, you need to be disciplined.\n"
            "• Discipline today, freedom tomorrow."
        ),
        color=BRAND_PURPLE,
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="links", description="Important Lifted Trades links")
async def links_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔗 Links",
        description=(
            "📸 Instagram: https://instagram.com/liftedtrader\n"
            "💬 (Add your Whop / mentorship links here)"
        ),
        color=BRAND_GREEN,
    )
    await interaction.response.send_message(embed=embed)


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Set the DISCORD_TOKEN environment variable. See README.md.")
    bot.run(TOKEN)
