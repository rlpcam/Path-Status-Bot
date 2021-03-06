"""
Path.net Status Bot
Author: Rubik#7711
Version: 1.0
"""

import discord, os, requests, json, asyncio, re, time, datetime
from discord.ext.commands import Bot
from discord.ext import commands
import config
intents = discord.Intents.default()
bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents)
bot.remove_command("help")

### config ###
Channel_ID = 965017038517067886
Bot_Activity_Refresh = 210 # seconds
Incidents_Refresh = 210
Maintenance_Refresh = 210
Embed_Thumbnail = 'https://i.imgur.com/naud7XH.png'

### notifications ###
Should_Ping = True
ROLE_ID = 247436279686365184 # @Network Alerts ping

@bot.event
async def on_ready():
    bot.loop.create_task(bot_activity())
    bot.loop.create_task(incidents())
    bot.loop.create_task(maintenance())
    print("Logged in as Dingus")

async def bot_activity():
    while True:
        r = requests.get('https://status.path.net/api/v2/summary.json')
        json_data = json.loads(r.text)
        status = json_data['status']['description']
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'status.path.net'))
        await asyncio.sleep(Bot_Activity_Refresh)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{status}'))
        await asyncio.sleep(Bot_Activity_Refresh)

def GetMessageID(method,incidentID):
    Found = False
    with open(f'{method}.txt', 'r') as r:
        lines = r.readlines()
        for line in lines:
            if incidentID in line:
                Found = line.split("=")[1].strip()
                break
            else:
                Found = False
                
        return Found 
   
async def incidents():
    while True:
        r = requests.get('https://status.path.net/api/v2/incidents.json')
        json_data = json.loads(r.text)
        incidentID = json_data['incidents'][0]['id']
        Impact = json_data['incidents'][0]['impact']
        Title = json_data['incidents'][0]['name']
        Status = json_data['incidents'][0]['status']
        LastUpdate = json_data['incidents'][0]['updated_at']
        Desc = json_data['incidents'][0]['incident_updates'][0]['body']
        channel = bot.get_channel(Channel_ID)

        if Status == "resolved":
            color = 0xdadee6
        elif Impact == "critical":
            color = 0xce422b
        elif Impact == "major":
            color = 0xe57e21
        elif Impact == "minor":
            color = 0xe5c61e
        else:
            color = 0x596074

        with open('incidents.txt', 'a+') as f:
            if not GetMessageID('incidents',incidentID):         
                embed = discord.Embed(
                    title=f'Incident Report: {Title}',
                    description= Desc,
                    color=color,
                    url=f"https://status.path.net/incidents/{incidentID}",
                )
                embed.set_thumbnail(
                    url=Embed_Thumbnail
                )
                embed.add_field(
                    name="Status:",
                    value=Status.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="Impact:",
                    value=Impact.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="Updated:",
                    value=LastUpdate,
                    inline=True
                )
                embed.set_footer(
                    text=f"ID: {incidentID}"
                )
                if Should_Ping:
                    await channel.send(f'<@&{ROLE_ID}> a new incident has been reported: {Title} ')
                embed_message = await channel.send(embed=embed)
                f.write(f"{incidentID}={embed_message.id} \n")
                await asyncio.sleep(Incidents_Refresh)
            else:             
                embed = discord.Embed(
                    title=f'Incident Report: {Title}',
                    description= Desc,
                    color=color,
                    url=f"https://status.path.net/incidents/{incidentID}",
                )
                embed.set_thumbnail(
                    url=Embed_Thumbnail
                )
                embed.add_field(
                    name="Status:",
                    value=Status.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="Impact:",
                    value=Impact.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="Updated:",
                    value=LastUpdate,
                    inline=True
                )
                embed.set_footer(
                    text=f"ID: {incidentID}"
                )
                msg = await channel.fetch_message(GetMessageID('incidents',incidentID))
                await msg.edit(embed=embed)

                await asyncio.sleep(Incidents_Refresh)

async def maintenance():
    while True:
        r = requests.get('https://status.path.net/api/v2/scheduled-maintenances.json')
        json_data = json.loads(r.text)
        incidentID = json_data['scheduled_maintenances'][0]['id']
        Impact = json_data['scheduled_maintenances'][0]['impact']
        Title = json_data['scheduled_maintenances'][0]['name']
        Status = json_data['scheduled_maintenances'][0]['status']
        LastUpdate = json_data['scheduled_maintenances'][0]['updated_at']
        Desc = json_data['scheduled_maintenances'][0]['incident_updates'][0]['body']
        channel = bot.get_channel(Channel_ID)

        with open('maintenance.txt', 'a+') as f:
            if not GetMessageID('maintenance',incidentID):         
                embed = discord.Embed(
                    title=Title,
                    description= Desc,
                    color=0x3598db,
                    url=f"https://status.path.net/incidents/{incidentID}",
                )
                embed.set_thumbnail(
                    url=Embed_Thumbnail
                )
                embed.add_field(
                    name="Status:",
                    value=Status.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="Impact:",
                    value=Impact.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="Updated:",
                    value=LastUpdate,
                    inline=True
                )
                embed.set_footer(
                    text=f"ID: {incidentID}"
                )
                if Should_Ping:
                    await channel.send(f'<@&{ROLE_ID}> {Title} ')
                embed_message = await channel.send(embed=embed)
                f.write(f"{incidentID}={embed_message.id} \n")
                await asyncio.sleep(Maintenance_Refresh)
            else:             
                embed = discord.Embed(
                    title=Title,
                    description= Desc,
                    color=0x3598db,
                    url=f"https://status.path.net/incidents/{incidentID}",
                )
                embed.set_thumbnail(
                    url=Embed_Thumbnail
                )
                embed.add_field(
                    name="Status:",
                    value=Status.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="Impact:",
                    value=Impact.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="Updated:",
                    value=LastUpdate,
                    inline=True
                )
                embed.set_footer(
                    text=f"ID: {incidentID}"
                )
                msg = await channel.fetch_message(GetMessageID('maintenance',incidentID))
                await msg.edit(embed=embed)
                await asyncio.sleep(Maintenance_Refresh)

bot.run(config.TOKEN)
