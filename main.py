# bot.py
import os
import asyncio
import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import Bot

# from dotenv import load_dotenv
# load_dotenv()
# TOKEN = os.getenv("TOKEN")

bot = Bot('$')
@bot.event
async def on_ready():
    print('- online -')


MasterDict = {}


def get_nickname(id):
    global bot
    return bot.get_user(id).name

class Paper:
    def __init__(self, name, link):
        self.name, self.link = name, link
        return self

class Speaker:
    def __init__(self, id, name, paper, date):
        ### IF DATE IS A DATE (AND NOT TBA), USE PYTHON DATE FORMAT #####
        self.id, self.name = id, name
        self.papers = [(paper, date)]
        return self

    def update(self):
        self.name = get_nickname(self.id)

    def update(self, date):
        self.date = date

    def add_paper(self, paper, date):
        self.papers.append((paper,date))

    def represent(self):
        self.update()
        string = f"presentations made by {name}:\n"
        for i in self.papers:
            string += f"\n \" {self.papers[i][0].name} \" , {self.papers[i][1]} \n {self.papers[i][0].link} \n"
            # paper, name, \n link
        return self.papers




@bot.command(name="uap", help="user add presentation: add a new presentation to a member!\nformat: uap @user paper_name date link")
async def uap(ctx):
    ### USERID HAS TO BE GOTTEN FROM CTX.MESSAGE.MENTIONS ####
    username = bot.get_user(userid).name
    msg = ctx.split()
    _, _, paper_name, date, paper_link = msg

    if userid in MasterDict.keys():
        MasterDict[userid] = MasterDict[userid].add_paper(Paper(paper_name, paper_link), date)
    else:
        MasterDict[userid] = Speaker(userid, username, Paper(paper_name, paper_link), date)

@bot.command(name="change_date", help="change date of presentation for a user! \nformat: change_date @user paper_name date")
async def change_date(ctx):
    #### FIND USERID FROM CTX.MESSAGE.MENTIONS ####
    msg = ctx.split()
    _, _, paper_name, date, paper_link = msg
    #### HERE SPEAKER.UDPATE_TIME SHOULD BE CALLED ####

##--- Unnecessary stuff ---##

@bot.command(name="religion")
async def religion(ctx):
    await ctx.send('All hail the great highness, the untouchable one, his hotness himself, the unspeakable Hugo!')
