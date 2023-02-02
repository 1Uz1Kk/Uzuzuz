# IMPORT #
import asyncio
import random
import json

# OS #
import os
os.chdir("C:\\Users\\igorp\\PycharmProjects\\Uzbot")

# DISCORD IMPORT #
import discord
from discord.ext import commands
from discord import app_commands

# DISCORD INTENTS
intents = discord.Intents.all()
client = commands.Bot(command_prefix="=", help_command=None, intents=intents)
TOKEN = "MTA2NTc0MzE5MzM2NDI1NDgwMQ.GGLkeb.uVTKV0xNQt3aD1aQ4VzRXIv2NfAayx_5HBu5vk"

# DISCORD BASICS #
@client.event
async def on_ready():
    print("Uz Bot Is Successfully Online!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} Commands")
    except Exception as e:
        print(e)
    client.loop.create_task(status_task())
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game("Gambling With Zycxes"))
        await asyncio.sleep(3)
        await client.change_presence(activity=discord.Game("Gambling With Uz1Kk"))
        await asyncio.sleep(3)

# --------------------------------------------------- COMMANDS ---------------------------------------------------

# BEG #
@client.command()
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(101)
    await ctx.send(f"Someone Gave You {earnings} Coins")

    users[str(user.id)]["wallet"] += earnings
    with open("bank.json", "w") as f:
        json.dump(users, f)

# BALANCE ( SLASH COMMAND ) #
@client.tree.command(name="balance")
async def balance(interaction: discord.Interaction):
    await open_account(interaction.user)
    user = interaction.user
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title= f"{interaction.user.name}'s Balance", color = discord.Color.red())
    em.add_field(name = "Wallet:", value= wallet_amt)
    em.add_field(name = "Bank:", value= bank_amt)
    await interaction.response.send_message(embed = em)

# BALANCE #
@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title= f"{ctx.author.name}'s Balance", color = discord.Color.red())
    em.add_field(name = "Wallet:", value= wallet_amt)
    em.add_field(name = "Bank:", value= bank_amt)
    await ctx.send(embed = em)


@client.tree.command(name="roulette")
@app_commands.describe(amount="How Much Coins Do You Want To Gamble?")
async def roulette(interaction: discord.Interaction, amount: int):
    await open_account(interaction.user)
    user = interaction.user
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    a1 = 1
    while a1 == 1:
        if wallet_amt <= amount:
            await interaction.response.send_message(f"You Don't Have Enough Coins In Your Wallet")
            a1 = 0
        else:
            a1 = 0

        wallet_amt -= amount

        a2 = random.randint(1, 6)
        a3 = wallet_amt + (amount*(7-1))
        if a2 == 1:
            amount *= 6
            wallet_amt += (amount*7)
        elif a1 != 1:
            amount *= 0

        if a2 == 1:
            await interaction.response.send_message(f"You Have Won {a3} Coins, Due To The Ball Landing On The Number {a2}")
        else:
            await interaction.response.send_message(f"You Have Lost Your Coins, Due To The Ball Landing On The Number {a2}")







@client.tree.command(name="spin")
@app_commands.describe(amount="How Much Coins Do You Want To Gamble?")
async def spin(interaction: discord.Interaction, amount: int):
    x1 = random.randint(1, 20)
    if x1 == 1:
        amount *= 5
        x2 = f"The Wheel Has Landed On {x1}, You Have Won With A 5x Multiplier And Have Received {amount} Coins"
    elif x1 == 2 or x1 == 3:
        amount *= 3
        x2 = f"The Wheel Has Landed On {x1}, You Have Won With A 3x Multiplier And Have Received {amount} Coins"
    elif x1 == 4 or x1 == 5 or x1 == 6 or x1 == 7 or x1 == 8 or x1 == 9 or x1 == 10:
        amount *= 2
        x2 = f"The Wheel Has Landed On {x1}, You Have Won With A 2x Multiplier And Have Received {amount} Coins"
    else:
        x2 = f"The Wheel Has Landed On {x1}, You Have Lost {amount} Coins"
    await interaction.response.send_message(f"{x2}")


@client.tree.command(name="coinflip")
@app_commands.describe(side="Heads Or Tails?")
@app_commands.describe(amount="How Much Coins Do You Want To Gamble?")
@app_commands.choices(side=[
        discord.app_commands.Choice(name="Heads", value=1),
        discord.app_commands.Choice(name="Tails", value=2),
])
async def coinflip(interaction: discord.Interaction, side: discord.app_commands.Choice[int], amount: int):
    h2 = 1
    while h2 == 1:
        h1 = random.randint(1, 2)
        if h1 == 1:
            h3 = "Heads"
            h2 = 0
        elif h1 == 2:
            h3 = "Tails"
            h2 = 0
    if h3 == f"{side.name}":
        amount *= 2
        await interaction.response.send_message(f"It Has Landed On {h3}, You Have Doubled Your Coins To {amount}")
    elif h3 != f"{side.name}":
        amount *= 0
        await interaction.response.send_message(f"It Landed On {h3}, You Lost Your Coins")


@client.tree.command(name="duels")
@app_commands.describe(people="How Much People To Join The Duel?")
@app_commands.describe(amount="How Much Coins Do You Want To Gamble?")
async def duels(interaction : discord.Interaction, people: int, amount: int):
    q1 = 1
    q2 = 1
    q3 = 1
    while q2 == 1:
        q4 = random.randint(1, people)
        if q4 == 1:
            amount *= people
            q3 = 1
            q2 = 0
        else:
            q3 = 0
            q2 = 0
    if q3 == 0:
        await interaction.response.send_message(f"The Number {q4} Has Been Picked, You Have Lost {amount} Coins")
    else:
        await interaction.response.send_message(f"The Number {q4} Has Been Picked, You Have Won With A Multiplier Of {people}x, You Have Received {amount} Coins")


@client.tree.command(name="towers")
@app_commands.describe(corner="What Corner Do You Want To Pick Of The Tower?")
@app_commands.describe(amount="How Much Coins Do You Want To Gamble?")
@app_commands.choices(corner=[
    discord.app_commands.Choice(name="Left", value=1),
    discord.app_commands.Choice(name="Middle", value=2),
    discord.app_commands.Choice(name="Right", value=3),
])
async def towers(interaction: discord.Interaction, corner: discord.app_commands.Choice[int], amount: int):
    f1 = 1
    f2 = 1
    while f1 == 1:
        f3 = random.randint(1, 3)
        if f3 == 1:
            f2 += 0.5
            amount *= 1.5
            f1 = 0
        elif f3 == 2:
            f2 += 0.5
            amount *= 1.5
            f1 = 0
        else:
            f2 = 0
            amount *= 1
            f1 = 0
    if f2 == 1.5:
        await interaction.response.send_message(f"You Have Picked A Tower Without A Bomb, You Have Won With A {f2}x Multiplier And Have Received {amount} Coins")
    else:
        await interaction.response.send_message(f"You Have Picked A Tower With A Bomb, You Have Lost Your {amount} Coins")


@client.tree.command(name="commands")
@app_commands.describe(command="What Command Do You Want To Know About?")
@app_commands.choices(command=[
    discord.app_commands.Choice(name="/spin", value=1),
    discord.app_commands.Choice(name="/roulette", value=2),
    discord.app_commands.Choice(name="/coinflip", value=3)
])
async def commands(interaction: discord.Interaction, command: discord.app_commands.Choice[int]):
    if f"{command.name}" == "/spin":
        await interaction.response.send_message(f"A Wheel With 20 Numbers Is Spun, It Will Land On A Random Number!\n"
                                                f"- If It Lands On **1** You Get 5x Your Coins -\n"
                                                f"- If It Lands On **2-3** You Get 3x Your Coins -\n"
                                                f"- If It Lands On **4-10** You Get 2x Your Coins -\n"
                                                f"- If It Lands On **11-20** You Get None Of Your Coins -\n")
    elif f"{command.name}" == "/roulette":
        await interaction.response.send_message(f"A Ball Is Dropped Into A Dome With 6 Holes!\n"
                                                f": The Ball Will Drop Into A Random One :\n"
                                                f"- If It Lands In The First One, You Get 6x Of Your Coins -\n"
                                                f"- If It Lands Into Any Other Hole, You Get None Of Your Coins -\n")
    elif f"{command.name}" == "/coinflip":
        await interaction.response.send_message(f"A Coin Is Flipped And It Lands On Heads Or Tails!\n"
                                                f"- You Pick A Side, If You Picked The Side The Coin Landed On -\n"
                                                f"- YOU WIN 2x -")

#--------------------------------------------------- FUNCTIONS ---------------------------------------------------

#OPEN_ACCOUNT
async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True

#GET_BANK_DATA
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users


client.run(TOKEN)