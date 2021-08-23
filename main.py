# bot.py
import os
import asyncio
import discord
from random import choice
from discord import File
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
# from dotenv import load_dotenv
# load_dotenv()
# TOKEN = os.getenv("TOKEN")

bot = Bot('$')
@bot.event
async def on_ready():
    print('- online -')


MasterDict = {}

class TBA:
    def __init__(self):
        pass
    def strftime(self, nothing):
        return "tba"
    def __repr__(self):
        return "tba"

def get_date(date):
    if date == "TBA" or date == "tba":
        return TBA()
    else:
        L = date.split("/")
        if len(L) != 2:
            return False
        else:
            year = datetime.datetime.now().year
            return datetime.datetime(year, L[1], L[0])

def get_nickname(id):
    global bot
    return bot.get_user(id).name

class Paper:
    def __init__(self, name, link):
        self.name, self.link = name, link
        return self

class Speaker:
    def __init__(self, id, name, paper, date):
        self.id, self.name = id, name
        self.papers = [(paper, date)]
        return self

    def name(self):
        self.update()
        return self.name

    def update(self):
        self.name = get_nickname(self.id)

    def update_time(self, paper, date):
        index = [i for i in range(len(self.papers)) if self.papers[i][0].name == paper][0]
        self.papers[index][1] = date
        return self

    def cancel_presentation(self, paper, date):
        index =  [i for i in range(len(self.papers)) if self.papers[i][0].name == paper and self.papers[i][1] == date][0]
        del self.papers[index]
        return self

    def add_paper(self, paper, date):
        self.papers.append((paper,date))
        return self

    def represent(self):
        self.update()
        string = f"presentations made by {name}:\n"
        for i in self.papers:
            string += f"""\n \" {self.papers[i][0].name} \" , {self.papers[i][1].strftime("%x")} \n {self.papers[i][0].link} \n"""
            # paper, date, \n link
        return string


##--- Manage Speakers ---##

@bot.command(name="uap", help="user add presentation: add a new presentation to a member!\nformat: !uap @user paper_name date link")
async def uap(ctx):
    global MasterDict

    try:
        userid = ctx.message.mentions[0].id
    except IndexError:
        ctx.send(f"No user mentioned! Expected format: !uap @user paper_name date link")
        ctx.message.add_reaction(":x:")
        return

    username = bot.get_user(userid).name
    msg = ctx.split()
    try:
        _, _, paper_name, date_raw, paper_link = msg
    except ValueError:
        ctx.send(f"Message not understood! Expected format: !uap @user paper_name date link")
        ctx.message.add_reaction(":x:")
        return

    date = get_date(date_raw)
    if not date:
        ctx.send(f"Wrong date format! Expected format: day/month ; e.g.: 420/69 \ngotten: {date_raw}")
        ctx.message.add_reaction(":x:")
        return

    elif userid in MasterDict.keys():
        MasterDict[userid] = MasterDict[userid].add_paper(Paper(paper_name, paper_link), date)
    else:
        print("Hi naomi pls tell me if this message appears")
        MasterDict[userid] = Speaker(userid, username, Paper(paper_name, paper_link), date)
        print("If this one also does (but it still doesnt work) its bad")

    ctx.message.add_reaction(":white_check_mark:")



@bot.command(name="change_date", help="change date of presentation for a user! \nformat: !change_date @user paper_name date (format: day/month)")
async def change_date(ctx):
    global MasterDict

    try:
        userid = ctx.message.mentions[0].id
    except IndexError:
        ctx.send(f"No user mentioned! Expected format: !change_date @user paper_name date")
        ctx.message.add_reaction(":x:")
        return

    msg = ctx.split()
    try:
        _, _, paper_name, date_raw = msg
    except ValueError:
        ctx.send(f"Message not understood! Expected format: !change_date @user paper_name date")
        ctx.message.add_reaction(":x:")
        return

    date = get_date(date_raw)
    if not date:
        ctx.send(f"Wrong date format! Expected format: day/month ; e.g.: 420/69 \ngotten: {date_raw}")
        ctx.message.add_reaction(":x:")
        return
    MasterDict[userid] = MasterDict[userid].update_time(paper_name, date)
    ctx.message.add_reaction(":white_check_mark:")



@bot.command(name="cap", help="cancel presentation for a user! \nformat: !cap @user paper_name date (format: day/month)")
async def cap(ctx):
    global MasterDict

    try:
        userid = ctx.message.mentions[0].id
    except IndexError:
        ctx.send(f"No user mentioned! Expected format: !cap @user paper_name date")
        ctx.message.add_reaction(":x:")
        return

    msg = ctx.split()
    try:
        _, _, paper_name, date_raw = msg
    except ValueError:
        ctx.send(f"Message not understood! Expected format: !cap @user paper_name date")
        ctx.message.add_reaction(":x:")
        return

    date = get_date(date_raw)
    if not date:
        ctx.send(f"Wrong date format! Expected format: day/month ; e.g.: 420/69 \ngotten: {date_raw}")
        ctx.message.add_reaction(":x:")
        return
    MasterDict[userid] = MasterDict[userid].cancel_presentation(paper_name, date)
    ctx.message.add_reaction(":white_check_mark:")

##--- print out info ---##

@bot.command(name="history", help="give out a list of papers the given person is an expert on! \nformat: !history @user")
async def history(ctx):
    global MasterDict
    userid = ctx.message.mentions[0].id
    await ctx.send(MasterDict[userid].represent())

@bot.command(name="papers", help="give out a list of papers that have already been held in the past or are scheduled for soon!")
async def papers(ctx):
    global MasterDict
    string = f"papers prepared in the past:\n"
    for speaker in MasterDict.values():
        for paper in speaker.papers:
            string += f"\n \" {paper[0].name} \" \nheld by {speaker.name()} on {paper[1]} \n{paper[0].link} \n"
    await ctx.send(string)

##--- Unnecessary stuff ---##

@bot.command(name="religion")
async def religion(ctx):
    await ctx.send('All hail the great highness, the untouchable one, his hotness himself, the unspeakable Hugo!')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot: return
    if message.content.lower() == "hello":
        msg = choice([f"Wazzup, {message.author.name}", f"Yo {message.author.name}, whats poppin'!", f"All good under the hood?",f"Hey {message.author.name}, how are you today?"])
        await message.channel.send(msg)
