#imports libs
import discord
from discord import channel, player
from discord.colour import Color
from discord.ext import commands
from discord.utils import get
import asyncio
from helpers import *
from time import strftime,gmtime,sleep
import os
import json
import random
import logging
bot = commands.Bot(command_prefix=">>")
bot.remove_command('help')
timern = strftime("%H:%M:%S", gmtime())
logging.basicConfig(filename='./Resources/Gamblebot.log', filemode='w', level=logging.INFO)
#COMMAND FUNCTIONS------------------------#
logging.info(f"[{timern}]Booting...")
print(f"[{timern}]Booting...")
print("Logs saved at |./Resources/Gamblebot.log|")
@bot.event
async def on_ready():
    timern = strftime("%H:%M:%S", gmtime())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Casino games'))
    print(f"[{timern}]Gamble bot ready!")
    logging.info(f"[{timern}]Gamble bot ready!")


@bot.event
async def on_command_error(ctx,error):
    timern = strftime("%H:%M:%S", gmtime())
    logging.info(f"[{timern}]Command cooldown for {ctx.author.name}")
    if isinstance(error,commands.CommandOnCooldown):
        msg = "please try again in {:.2f}s".format(error.retry_after)
        cdn = discord.Embed(title='Cooldown',color = discord.Color.red())
        cdn.add_field(name = "This command is on cool down",value=msg)
        cdn.set_thumbnail(url = ctx.author.avatar_url)
        await ctx.send(embed = cdn)
        

@bot.command(name="bankinfo")
async def balance(ctx):
    timern = strftime("%H:%M:%S", gmtime())
    logging.info(f"[{timern}]{ctx.author.name} requested their bank details")
    await open_bank(ctx.author)
    user = ctx.author
    users = await get_bank_info()
    
    wall_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    balem = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.green())
    balem.add_field(name = ":moneybag:Wallet Balance: ",value=wall_amt)
    balem.add_field(name = ":bank:Bank Balance: ",value=bank_amt)
    balem.set_thumbnail(url = ctx.author.avatar_url)
    await ctx.send(embed = balem)

@bot.command()
async def rules(ctx):
    timern = strftime("%H:%M:%S", gmtime())
    logging.info(f"[{timern}]{ctx.author.name} requested the rules")
    await ctx.send(':one:Blackjack games have a bet cap of 100000')
    sleep(1)
    await ctx.send(':two:Roulette has a bet cap of 100000000')
    sleep(1)
    await ctx.send(':three:If you have no money do "!beg" to get a random ammount of money')
    sleep(1)
    await ctx.send(':four:To purchase a role you must have banked the money')
    sleep(1)


@bot.command()
async def vip(ctx):
    timern = strftime("%H:%M:%S", gmtime())
    member = ctx.message.author
    await open_bank(ctx.author)
    user = ctx.author
    users = await get_bank_info()
    bal = await update_bank(ctx.author)
    bank_amt = users[str(user.id)]["bank"]
    if bal[1]<10000:
        logging.info(f"[{timern}]{ctx.author.name} Requested VIP with insufficient funds")
        toopoor = discord.Embed(title = "Insufficient funds", color = discord.Color.red())
        toopoor.set_thumbnail(url = ctx.author.avatar_url)
        toopoor.add_field(name = "Cost:",value=":moneybag:10000")
        toopoor.add_field(name = "You have:",value=f" {bank_amt}")
        await ctx.send(embed = toopoor)

        return
    if bal[1]<0:
        await ctx.send(f"{ctx.author.name} Amount must be positive!")
        return
    logging.info(f"[{timern}]{ctx.author.name} Purchased VIP")
    await update_bank(ctx.author,-10000,"bank")
    purchased = discord.Embed(title = f"{ctx.author.name} Purchased VIP", color = discord.Color.purple())
    purchased.set_thumbnail(url = ctx.author.avatar_url)
    purchased.add_field(name = "Cost:",value=":moneybag:10000")
    await ctx.send(embed = purchased)
    await member.add_roles(discord.utils.get(member.guild.roles, name="Casino VIP"))


@bot.command()
async def millionaire(ctx):
    timern = strftime("%H:%M:%S", gmtime())
    member = ctx.message.author
    await open_bank(ctx.author)
    user = ctx.author
    users = await get_bank_info()
    bal = await update_bank(ctx.author)
    bank_amt = users[str(user.id)]["bank"]
    if bal[1]<1000000:
        logging.info(f"[{timern}]{ctx.author.name} Requested Millionaire with insufficient funds")
        toopoor = discord.Embed(title = "Insufficient funds", color = discord.Color.red())
        toopoor.set_thumbnail(url = ctx.author.avatar_url)
        toopoor.add_field(name = "Cost:",value=":moneybag:1000000")
        toopoor.add_field(name = "You have:",value=f" {bank_amt}")
        await ctx.send(embed = toopoor)

        return
    if bal[1]<0:
        await ctx.send(f"{ctx.author.name} Amount must be positive!")
        return
    logging.info(f"[{timern}]{ctx.author.name} Purchased Millionaire")
    await update_bank(ctx.author,-10000,"bank")
    purchased = discord.Embed(title = f"{ctx.author.name} Purchased Millionaire", color = discord.Color.purple())
    purchased.set_thumbnail(url = ctx.author.avatar_url)
    purchased.add_field(name = "Cost:",value=":moneybag:1000000")
    await ctx.send(embed = purchased)
    await member.add_roles(discord.utils.get(member.guild.roles, name="Millionaire"))


@bot.command(aliases = ["bank"])
async def deposit(ctx,amount = None):
    timern = strftime("%H:%M:%S", gmtime())
    await open_bank(ctx.author)
    if amount == None:
        logging.info(f"[{timern}]{ctx.author.name} Attempted bank with no amount")
        noamn = discord.Embed(title = f"{ctx.author.name} | Unable to bank", color = discord.Color.red())
        noamn.set_thumbnail(url = ctx.author.avatar_url)
        noamn.add_field(name = "ERROR",value="Please enter valid amount")
        await ctx.send(embed = noamn)

        return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount >bal[0]:
        logging.info(f"[{timern}]{ctx.author.name} Attempted Bank with insufficient amount")
        toolow = discord.Embed(title = f"{ctx.author.name} | Unable to bank", color = discord.Color.red())
        toolow.set_thumbnail(url = ctx.author.avatar_url)
        toolow.add_field(name = "ERROR",value="You do not have enough")
        await ctx.send(embed = toolow)

        return
    if amount<0:
        logging.info(f"[{timern}]{ctx.author.name} Attempted bank with negative amount")
        toolittle = discord.Embed(title = f"{ctx.author.name} | Unable to bank", color = discord.Color.red())
        toolittle.set_thumbnail(url = ctx.author.avatar_url)
        toolittle.add_field(name = "ERROR",value="amount must be positive")
        await ctx.send(embed = toolittle)

        return
    else:
        logging.info(f"[{timern}]{ctx.author.name} Banked {amount}")
        await update_bank(ctx.author,amount,"bank")
        await update_bank(ctx.author,-1*amount,"wallet")
        banked = discord.Embed(title = f"{ctx.author.name}| Deposit", color = discord.Color.green())
        banked.set_thumbnail(url = ctx.author.avatar_url)
        banked.add_field(name = "SUCCESS",value=f"{amount} Has been deposited into your bank!")
        await ctx.send(embed = banked)


@bot.command(aliases = ["wallet"])
async def withdraw(ctx,amount = None):
    timern = strftime("%H:%M:%S", gmtime())
    await open_bank(ctx.author)
    if amount == None:
        logging.info(f"[{timern}]{ctx.author.name} Attempted withdraw with no amount")
        noamn = discord.Embed(title = f"{ctx.author.name} | Unable to withdraw", color = discord.Color.red())
        noamn.set_thumbnail(url = ctx.author.avatar_url)
        noamn.add_field(name = "ERROR",value="Please enter valid amount")
        await ctx.send(embed = noamn)

        return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount>bal[1]:
        logging.info(f"[{timern}]{ctx.author.name} Attempted withdraw with insufficient amount")
        toolow = discord.Embed(title = f"{ctx.author.name} | Unable to withdraw", color = discord.Color.red())
        toolow.set_thumbnail(url = ctx.author.avatar_url)
        toolow.add_field(name = "ERROR",value="You do not have enough")
        await ctx.send(embed = toolow)

        return
    if amount<0:
        logging.info(f"[{timern}]{ctx.author.name} Attempted withdraw with negative amount")
        toolittle = discord.Embed(title = f"{ctx.author.name} | Unable to withdraw", color = discord.Color.red())
        toolittle.set_thumbnail(url = ctx.author.avatar_url)
        toolittle.add_field(name = "ERROR",value="amount must be positive")
        await ctx.send(embed = toolittle)

        return
    else:
        logging.info(f"[{timern}]{ctx.author.name} Withdrew {amount}")
        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount,"bank")
        banked = discord.Embed(title = f"{ctx.author.name}| Withdraw", color = discord.Color.green())
        banked.set_thumbnail(url = ctx.author.avatar_url)
        banked.add_field(name = "SUCCESS",value=f"{amount} Has been withdrawn from your bank!")
        await ctx.send(embed = banked)


@bot.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def beg(ctx):
    timern = strftime("%H:%M:%S", gmtime())
    user = ctx.author
    await open_bank(user)
    users = await get_bank_info()
    bal = await update_bank(ctx.author)
    if bal[1]>= 1000 or bal[0]>= 500:
        logging.info(f"[{timern}]{ctx.author.name} Tried to beg was too rich")
        rich = discord.Embed(title = "Beg", color = discord.Color.red())
        rich.set_thumbnail(url = ctx.author.avatar_url)
        rich.add_field(name = "Beg failed",value="You are too rich to beg")
        await ctx.send(embed = rich)

        return

    earnings = random.randrange(101)
    res = discord.Embed(title = "Beg", color = discord.Color.green())
    res.set_thumbnail(url = ctx.author.avatar_url)
    res.add_field(name = "Beg succeeded",value=f"You gained {earnings} Tokens")
    await ctx.send(embed = res)
    logging.info(f"[{timern}]{ctx.author.name} Begged and gained {earnings}")
    users[str(user.id)]["wallet"] += earnings
    with open("./UserData/Banks.json","w") as f:
        json.dump(users,f)


@bot.command(aliases = ["Gift"])
async def send(ctx,member:discord.Member,amount = None):
    timern = strftime("%H:%M:%S", gmtime())
    await open_bank(ctx.author)
    await open_bank(member)
    if amount == None:
        logging.info(f"[{timern}]{ctx.author.name} Tried to gift with invalid amount")
        noamn = discord.Embed(title = f"{ctx.author.name} | Unable to send", color = discord.Color.red())
        noamn.set_thumbnail(url = ctx.author.avatar_url)
        noamn.add_field(name = "ERROR",value="Please enter valid amount")
        await ctx.send(embed = noamn)

        return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount>bal[1]:
        logging.info(f"[{timern}]{ctx.author.name} Tried to gift more than they own")
        toolow = discord.Embed(title = f"{ctx.author.name} | Unable to send", color = discord.Color.red())
        toolow.set_thumbnail(url = ctx.author.avatar_url)
        toolow.add_field(name = "ERROR",value="You do not have enough")
        await ctx.send(embed = toolow)

        return
    if amount<0:
        logging.info(f"[{timern}]{ctx.author.name} Tried to gift negative amount")
        toolittle = discord.Embed(title = f"{ctx.author.name} | Unable to send", color = discord.Color.red())
        toolittle.set_thumbnail(url = ctx.author.avatar_url)
        toolittle.add_field(name = "ERROR",value="amount must be positive")
        await ctx.send(embed = toolittle)

        return
    else:
        logging.info(f"[{timern}]{ctx.author.name} Sent {amount} to {member}")
        await update_bank(ctx.author,-1*amount,"bank")
        await update_bank(member,amount,"bank")
        sent = discord.Embed(title = f"{ctx.author.name}| Deposit", color = discord.Color.green())
        sent.set_thumbnail(url = ctx.author.avatar_url)
        sent.add_field(name = "SUCCESS",value=f"{amount} Has been sent to {member}!")
        await ctx.send(embed = sent)


@bot.command(aliases=["roulette","r"])
async def game1(ctx,amount = 0,number=None):
    timern = strftime("%H:%M:%S", gmtime())
    numbers = [1,2,3,4,5,6,7,8,9,10]
    users = await get_bank_info()
    bal = await update_bank(ctx.author)
    user = ctx.author
    if number == None:
        logging.info(f"[{timern}]{ctx.author.name} attempted roulette no number picked")
        nonum = discord.Embed(title = "Roulette", color = discord.Color.red())
        nonum.set_thumbnail(url = ctx.author.avatar_url)
        nonum.add_field(name = "ERROR",value="Please enter a number to bet on")
        await ctx.send(embed = nonum)

        return
    roulettenumb = random.randint(0,10)
    number = int(number)
    if amount>= 100000000:
        logging.info(f"[{timern}]{ctx.author.name} attempted roulette insufficient amount")
        toohi = discord.Embed(title = "Roulette", color = discord.Color.red())
        toohi.set_thumbnail(url = ctx.author.avatar_url)
        toohi.add_field(name = "ERROR",value="Max bet is 100000000")
        await ctx.send(embed = toohi)

        return
    if amount>bal[0]:
        logging.info(f"[{timern}]{ctx.author.name} attempted roulette insufficient amount")
        toolow = discord.Embed(title = "Roulette", color = discord.Color.red())
        toolow.set_thumbnail(url = ctx.author.avatar_url)
        toolow.add_field(name = "ERROR",value="You do not have enough")
        await ctx.send(embed = toolow)
        return
    if number not in numbers:
        logging.info(f"[{timern}]{ctx.author.name} attempted roulette invalid number")
        badnum = discord.Embed(title = "Roulette", color = discord.Color.red())
        badnum.set_thumbnail(url = ctx.author.avatar_url)
        badnum.add_field(name = "ERROR",value="Number must be 1-10")
        await ctx.send(embed = badnum)
        return
    if number == roulettenumb:
        result = amount * 2
        logging.info(f"[{timern}]{ctx.author.name} Rouletted and won {result}")
        users[str(user.id)]["wallet"] += result
        with open("./UserData/Banks.json","w") as f:
            json.dump(users,f)
        won = discord.Embed(title = "Roulette", color = discord.Color.green())
        won.set_thumbnail(url = ctx.author.avatar_url)
        won.add_field(name = "You won",value=f"{result} Has been won!")
        won.add_field(name = "Number was:",value=f"{roulettenumb} Well done")
        await ctx.send(embed = won)
        print(f"{user} rouletted and the number was",roulettenumb)
        
    else:
        logging.info(f"[{timern}]{ctx.author.name} Rouletted on {number} and lost {amount}| Number:{roulettenumb}")
        lost = discord.Embed(title = "Roulette", color = discord.Color.red())
        lost.set_thumbnail(url = ctx.author.avatar_url)
        lost.add_field(name = "You lost",value=f"You lost {amount} unlucky")
        lost.add_field(name = "Number was:",value=f"{roulettenumb}")
        await ctx.send(embed = lost)
        users[str(user.id)]["wallet"] -= amount
        with open("./UserData/Banks.json","w") as f:
            json.dump(users,f)
        print(f"{user} rouletted and the number was",roulettenumb)


@bot.command(aliases=["Jackpot","j","jackpot"])
async def game2(ctx):
    timern = strftime("%H:%M:%S", gmtime())
    user = ctx.author
    users = await get_bank_info()
    bal = await update_bank(user)
    emotes = ['Discord','Blockheadbandit','Terminal','Boogie']
    if bal[0] < 25:
        logging.info(f"[{timern}]{ctx.author.name} Attempted jackpot | Insufficient funds")
        insuf = discord.Embed(title = "Jackpot", color= discord.Color.red())
        insuf.set_thumbnail(url = ctx.author.avatar_url)
        insuf.add_field(name = "ERROR",value="You cannot afford Jackpot")
        await ctx.send(embed = insuf)
        return
    j1 = emotes[random.randint(0,3)]
    j2 = emotes[random.randint(0,3)]
    j3 = emotes[random.randint(0,3)]
    if j1 == 'Discord' and j2 == 'Discord' and j3 == 'Discord':
        reward = 100
        emote = '<:Discord:830812916361986080>'
        logging.info(f"[{timern}]{ctx.author.name} Jackpotted and won {reward}")
        win1 = discord.Embed(title = "Jackpot", color= discord.Color.green())
        win1.set_thumbnail(url = ctx.author.avatar_url)
        win1.add_field(name = "Slots:",value=f"| {emote} | {emote} | {emote} |")
        win1.add_field(name="You win", value=f"You have won {reward}")
        await ctx.send(embed = win1)
        users[str(user.id)]["wallet"] += reward
        with open("./UserData/Banks.json","w") as f:
            json.dump(users,f)
        print(f"{user} jackpotted and won {reward}")
    if j1 == 'Blockheadbandit' and j2 == 'Blockheadbandit' and j3 == 'Blockheadbandit':
        emote = '<:Blockheadbandit:816329848754274336>'
        reward = 500
        logging.info(f"[{timern}]{ctx.author.name} Jackpotted and won {reward}")
        win2 = discord.Embed(title = "Jackpot", color= discord.Color.green())
        win2.set_thumbnail(url = ctx.author.avatar_url)
        win2.add_field(name = "Slots:",value=f"| :{emote}: | :{emote}: | :{emote}: |")
        win2.add_field(name="You win", value=f"You have won {reward}")
        await ctx.send(embed = win2)
        users[str(user.id)]["wallet"] += reward
        with open("./UserData/Banks.json","w") as f:
            json.dump(users,f)
        print(f"{user} jackpotted and won {reward}")
    if j1 == 'Terminal' and j2 == 'Terminal' and j3 == 'Terminal':
        emote = '<a:Terminal:816329926067093564>'
        reward = 200
        logging.info(f"[{timern}]{ctx.author.name} Jackpotted and won {reward}")
        win3 = discord.Embed(title = "Jackpot", color= discord.Color.green())
        win3.set_thumbnail(url = ctx.author.avatar_url)
        win3.add_field(name = "Slots:",value=f"| :{emote}: | :{emote}: | :{emote}: |")
        win3.add_field(name="You win", value=f"You have won {reward}")
        await ctx.send(embed = win3)
        users[str(user.id)]["wallet"] += reward
        with open("./UserData/Banks.json","w") as f:
            json.dump(users,f)
        print(f"{user} jackpotted and won {reward}")
    if j1 == 'Boogie' and j2 == 'Boogie' and j3 == 'Boogie':
        emote = '<a:Boogie:816329999434252309>'
        reward = 1000
        logging.info(f"[{timern}]{ctx.author.name} Jackpotted and won {reward}")
        win4 = discord.Embed(title = "Jackpot", color= discord.Color.green())
        win4.set_thumbnail(url = ctx.author.avatar_url)
        win4.add_field(name = "Slots:",value=f"| :{emote}: | :{emote}: | :{emote}: |")
        win4.add_field(name="You win", value=f"You have won {reward}")
        await ctx.send(embed = win4)
        users[str(user.id)]["wallet"] += reward
        with open("./UserData/Banks.json","w") as f:
            json.dump(users,f)
        print(f"{user} jackpotted and won {reward}")
    else:
        logging.info(f"[{timern}]{ctx.author.name} Jackpotted and lost")
        if j1 == "Discord":
            emote1 = '<:Discord:830812916361986080>'
        if j1 == "Blockheadbandit":
            emote1 = '<:Blockheadbandit:816329848754274336>'
        if j1 == "Terminal":
            emote1 = '<a:Terminal:816329926067093564>'
        if j1 == "Boogie":
            emote1 = '<a:Boogie:816329999434252309>'
        if j2 == "Discord":
            emote2 = '<:Discord:830812916361986080>'
        if j2 == "Blockheadbandit":
            emote2 = '<:Blockheadbandit:816329848754274336>'
        if j2 == "Terminal":
            emote2 = '<a:Terminal:816329926067093564>'
        if j2 == "Boogie":
            emote2 = '<a:Boogie:816329999434252309>'
        if j3 == "Discord":
            emote3 = '<:Discord:830812916361986080>'
        if j3 == "Blockheadbandit":
            emote3 = '<:Blockheadbandit:816329848754274336>'
        if j3 == "Terminal":
            emote3 = '<a:Terminal:816329926067093564>'
        if j3 == "Boogie":
            emote3 = '<a:Boogie:816329999434252309>'
        lose = discord.Embed(title = "Jackpot", color= discord.Color.red())
        lose.set_thumbnail(url = ctx.author.avatar_url)
        lose.add_field(name = "Slots:",value=f"| {emote1} | {emote2} | {emote3} |")
        lose.add_field(name="You lose", value=f"You have lost")
        await ctx.send(embed = lose) 
        users[str(user.id)]["wallet"] -= 25
        with open("./UserData/Banks.json","w") as f:
            json.dump(users,f)
        print(f"{user} jackpotted and lost")
        return

@bot.command(name="?")
async def helper(ctx):
    logging.info(f"[{timern}]{ctx.author.name} Called help command")
    helpem = discord.Embed(title = "Help",description="Commands:", color = discord.Color.green())
    helpem.add_field(name = ">>r <amount> <0-10> / !roulette <amount> <0-10>",value="This starts a roulette you can use !r !roulette followed by an amount and a number 0-10")
    helpem.add_field(name = ">>bankinfo",value="This shows you your current bank and wallet info")
    helpem.add_field(name = ">>bank <amount>",value="This banks the amount into your bank")
    helpem.add_field(name = ">>withdraw <amount>",value="This withdraws the amount into your bank")
    helpem.add_field(name = ">>send <member> <amount>",value="This sends the amount to another user")
    helpem.add_field(name = ">>VIP ",value="This purchases VIP role for 10000")
    helpem.add_field(name = ">>Millionaire ",value="This purchases Millionaire role for 1000000")
    helpem.add_field(name = ">>beg ",value="This gives you a random amount of money it is capped at 500 in wallet or 1000")
    await ctx.send(embed = helpem)
    
#------------------------------------------------------------#
if __name__ == "__main__":
    filemain = open("./Resources/clientkey.txt","r")
    key = filemain.readline()
    bot.run(key)