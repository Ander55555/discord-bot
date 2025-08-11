import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix='/', intents=intents)

MODERATOR_ID = 1229958159662186621
reports = []  # In-memory report log

def is_mod():
    async def predicate(ctx):
        return ctx.author.id == MODERATOR_ID
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def report(ctx):
    try:
        await ctx.author.send("👋 Who would you like to report? Include their username and reason.")

        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        msg = await bot.wait_for('message', check=check, timeout=120)
        reports.append((ctx.author.name, msg.content))
        mod = await bot.fetch_user(MODERATOR_ID)
        await mod.send(f"🚨 Report from {ctx.author}:\n{msg.content}")
        await ctx.author.send("✅ Your report has been sent.")
    except discord.Forbidden:
        await ctx.send("🚫 I couldn't DM you. Please enable DMs from server members.")
    except asyncio.TimeoutError:
        await ctx.author.send("⏰ You took too long. Try again with `/report`.")

@bot.command()
async def challenge_suggestion(ctx):
    try:
        await ctx.author.send("👋 Hi! What challenge would you like to suggest and say how much xp the challenge is worth.")

        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        msg = await bot.wait_for('message', check=check, timeout=120)
        mod = await bot.fetch_user(MODERATOR_ID)
        await mod.send(f"🚨 Challenge suggestion from {ctx.author}:\n{msg.content}")
        await ctx.author.send("✅ Thanks! Your challenge suggestion has been sent to the moderators.")
    except discord.Forbidden:
        await ctx.send("🚫 I couldn't DM you. Please enable DMs from server members.")
    except asyncio.TimeoutError:
        await ctx.author.send("⏰ You took too long to respond. Try again with `/challenge_suggestion`.")

@bot.command()
@is_mod()
async def viewreports(ctx):
    if not reports:
        await ctx.send("📭 No reports available.")
    else:
        for i, (user, content) in enumerate(reports, 1):
            await ctx.send(f"**#{i}** from **{user}**:\n{content}")

@bot.command()
@is_mod()
async def clearreports(ctx):
    reports.clear()
    await ctx.send("🧹 All reports have been cleared.")


@bot.command()
@is_mod()
async def reportlog(ctx):
    mod = await bot.fetch_user(MODERATOR_ID)
    if not reports:
        await mod.send("📭 No reports logged.")
    else:
        log = "\n\n".join([f"{i+1}. {user}: {content}" for i, (user, content) in enumerate(reports)])
        await mod.send(f"📜 Full Report Log:\n{log}")

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="📜 Command List", color=discord.Color.blue())
    embed.add_field(name="/report", value="DMs you to submit a report to mods", inline=False)
    embed.add_field(name="/challenge_suggestion", value="DMs you to submit a challenge suggestion", inline=False)
    embed.add_field(name="/commands", value="Show this command list", inline=False)

    # Mod-only commands
    if ctx.author.id == MODERATOR_ID:
        embed.add_field(name="🔒 Mod Commands", value="(Visible only to mods)", inline=False)
        embed.add_field(name="/viewreports", value="View all submitted reports", inline=True)
        embed.add_field(name="/clearreports", value="Clear all reports", inline=True)
        embed.add_field(name="/reportlog", value="Send full report log to mod", inline=True)

    await ctx.send(embed=embed)
bot.run('MTQwMjgwOTUzODQxMDk3NTM0Mg.GTAJEY.vi1MHSKyD2OHOqqUAMCIp4-ISlkAzXtLr5tmOg')
