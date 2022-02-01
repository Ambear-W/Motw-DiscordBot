import hikari
import lightbulb
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from config import *

#Make sure you activate the evn/virtual enviroment to test: .\env\Scripts\activate or .\\env\Scripts\activate
#To start hikari: py botSetUp.py
#Note, every time you make changes, close the bot in the terminal and then restart it.  It will then have your changes.

#basic auto-sharding bot implementation - I made a config.py file to make data safer
bot = lightbulb.BotApp(
    token = token_config, 
    default_enabled_guilds = (default_enabled_guilds_config)
)
#sets up our connection with Google Firebase - this will be were we store player's information!

cred = credentials.Certificate(firebaseStuff)
firebase_admin.initialize_app(cred)

db = firestore.client()

bot.load_extensions("extensions.extension")

#db.collection('PlayerMoves').add({'MoveName' : 'move descripition'})

#The below is an example of an eventlistener!
#  the code that will run when triggered - reading the message sent in chat and printing it in ther terminal (I commented it out to save time)
#@bot.listen(hikari.GuildMessageCreateEvent)
#async def print_message(event):
    #print(event.content)

#These are the commands!  These are the things that your bot will do! (EX: !ping the bot will replay with Pong!)
@bot.command
#name of command, description of command
@lightbulb.command('ping', 'Says pong!')
#this is a slash command - when creating slash commands (type / in discord chanell), 
#TAKE NOTICE- discord takes some time regristing the commands, its easiest to copy the id of your server and add them to the token link.
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond('Pong!')

#There are groups and subcommands - aka you can group similar commands together
@bot.command
@lightbulb.command('group', 'This is a group')
#this command is going to have subcommands and will be grouped toogether 
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def my_group(ctx):
    #why pass? --> group commands cannot be ran
    pass

#we want the subcommands to be a child of the group we made
@my_group.child
@lightbulb.command('subcommand', 'This is a subcommand')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond('I am a subcommand!')
@my_group.child
@lightbulb.command('subcommand27', 'This is a subcommand')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand27(ctx):
    await ctx.respond('I am a subcommand! BUT 27!')

#we can add options to our commands but adding decorations! 
@bot.command
#here we add the options - you dont have to do type but it'll automatically make it a string
#the options HAVE to be ABOVE the lightbulb.command and UNDER bot.command
@lightbulb.option('num2', 'The second number', type=int)
@lightbulb.option('num1', 'The first number', type=int)
@lightbulb.command('add', 'Add two numbers together')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx):
    await ctx.respond(ctx.options.num1 + ctx.options.num2)

#how to write something to the database
@bot.command
@lightbulb.command('newcharacter', "Make a character here")
@lightbulb.implements(lightbulb.SlashCommand)
async def test(ctx: lightbulb.Context) -> None:
    member = ctx.user
    memberName = ctx.member.display_name
    memberID = ctx.member.id
    data = {'name' : member, "username" : memberName}
    db.collection('User').add({'UserId' : memberID , 'UserName' : memberName})
    await ctx.respond("Hello!  Let's see if it's in the database!")


#THE BASIC HUNTER MOVES
@bot.command()
@lightbulb.command('hunterbasicmoves', 'What moves a hunter can make')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def hunterBasicMoves(ctx):
    pass

@hunterBasicMoves.child
@lightbulb.command('kick-some-ass', 'When you get into a fight and kick some ass, roll +Tough.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandKickSomeAss(ctx):
    kickAss = (db.collection('HunterMoves').document('HunterBasicMoves').collection('KickSomeAss').document('description').get()).to_dict()
    description = kickAss['description']
    on7Plus = kickAss['on7Plus'].replace("\\n", '\n')
    on10Plus = kickAss['on10Plus'].replace("\\n", '\n')
    on12Plus = kickAss['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + on12Plus)

@hunterBasicMoves.child
@lightbulb.command('act-under-pressure', 'When you act under pressure, roll +Cool.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    underPressure = (db.collection('HunterMoves').document('HunterBasicMoves').collection('ActUnderPressure').document('description').get()).to_dict()
    description = underPressure['description']
    on7Plus = underPressure['on7Plus'].replace("\\n", '\n')
    on10Plus = underPressure['on10Plus'].replace("\\n", '\n')
    on12Plus = underPressure['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + on12Plus)

bot.run()
