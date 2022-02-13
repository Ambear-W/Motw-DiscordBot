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
    description = kickAss['description'].replace("\\n", '\n')
    on7Plus = kickAss['on7Plus'].replace("\\n", '\n')
    on10Plus = kickAss['on10Plus'].replace("\\n", '\n')
    on12Plus = kickAss['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + on12Plus)

@hunterBasicMoves.child
@lightbulb.command('act-under-pressure', 'When you act under pressure, roll +Cool.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    underPressure = (db.collection('HunterMoves').document('HunterBasicMoves').collection('ActUnderPressure').document('description').get()).to_dict()
    description = underPressure['description'].replace("\\n", '\n')
    on7Plus = underPressure['on7Plus'].replace("\\n", '\n')
    on10Plus = underPressure['on10Plus'].replace("\\n", '\n')
    on12Plus = underPressure['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + on12Plus)

@hunterBasicMoves.child
@lightbulb.command('help-out', 'When you help another hunter, roll +Cool.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    helpOut = (db.collection('HunterMoves').document('HunterBasicMoves').collection('HelpOut').document('description').get()).to_dict()
    description = helpOut['description'].replace("\\n", '\n')
    on7Plus = helpOut['on7Plus'].replace("\\n", '\n')
    on10Plus = helpOut['on10Plus'].replace("\\n", '\n')
    on12Plus = helpOut['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + on12Plus)

@hunterBasicMoves.child
@lightbulb.command('investigate-a-mystery', 'When you investigate a mystery, roll +Sharp.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    investigateMystery = (db.collection('HunterMoves').document('HunterBasicMoves').collection('InvestigateAMystery').document('description').get()).to_dict()
    description = investigateMystery['description'].replace("\\n", '\n')
    holds = investigateMystery['holds'].replace("\\n", '\n')
    on7Plus = investigateMystery['on7Plus'].replace("\\n", '\n')
    on10Plus = investigateMystery['on10Plus'].replace("\\n", '\n')
    on12Plus = investigateMystery['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + holds + '\n \n' + on12Plus)

@hunterBasicMoves.child
@lightbulb.command('manipulate-someone', 'Once you have given them a reason, tell them what you want them to do and roll +Charm')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    investigateMysteryDescription = (db.collection('HunterMoves').document('HunterBasicMoves').collection('ManipulateSomeone').document('description').get()).to_dict()
    description = investigateMysteryDescription['description'].replace("\\n", '\n')

    investigateMysteryNormal = (db.collection('HunterMoves').document('HunterBasicMoves').collection('ManipulateSomeone').document('normalPerson').get()).to_dict()
    on7PlusNormal = investigateMysteryNormal['on7Plus'].replace("\\n", '\n')
    on10PlusNormal = investigateMysteryNormal['on10Plus'].replace("\\n", '\n')
    on12PlusNormal = investigateMysteryNormal['on12Plus'].replace("\\n", '\n')
    descriptionNormal = investigateMysteryNormal['description'].replace("\\n", '\n')

    investigateMysteryHunter = (db.collection('HunterMoves').document('HunterBasicMoves').collection('ManipulateSomeone').document('hunterPerson').get()).to_dict()
    on7PlusHunter = investigateMysteryHunter['on7Plus'].replace("\\n", '\n')
    on10PlusHunter = investigateMysteryHunter['on10Plus'].replace("\\n", '\n')
    on12PlusHunter = investigateMysteryHunter['on12Plus'].replace("\\n", '\n')
    descriptionHunter = investigateMysteryHunter['description'].replace("\\n", '\n')
    onMiss = investigateMysteryHunter['onMiss'].replace("\\n", '\n')
    
    await ctx.respond(
        description + 
        '\n \n' + '**' + descriptionNormal + '**' + '\n - ' + on10PlusNormal + '\n - ' + on7PlusNormal + '\n - ' + on12PlusNormal +
        '\n \n' + '**' + descriptionHunter + '**' + '\n - ' + on10PlusHunter + '\n - ' + on7PlusHunter + '\n - ' + onMiss + '\n -' + on12PlusHunter       
    )

@hunterBasicMoves.child
@lightbulb.command('protect-someone', 'When you prevent harm to another character, roll +Tough')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    protectSomeone = (db.collection('HunterMoves').document('HunterBasicMoves').collection('ProtectSomeone').document('description').get()).to_dict()
    description = protectSomeone['description'].replace("\\n", '\n')
    on7Plus = protectSomeone['on7Plus'].replace("\\n", '\n')
    on10Plus = protectSomeone['on10Plus'].replace("\\n", '\n')
    on12Plus = protectSomeone['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + on12Plus)

@hunterBasicMoves.child
@lightbulb.command('read-a-bad-situation', 'When you look around and read a bad situation, roll +Sharp.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    readSituation = (db.collection('HunterMoves').document('HunterBasicMoves').collection('ReadABadSituation').document('description').get()).to_dict()
    description = readSituation['description'].replace("\\n", '\n')
    holds = readSituation['holds'].replace("\\n", '\n')
    on7Plus = readSituation['on7Plus'].replace("\\n", '\n')
    on10Plus = readSituation['on10Plus'].replace("\\n", '\n')
    on12Plus = readSituation['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + holds + '\n \n' + on12Plus)

@hunterBasicMoves.child
@lightbulb.command('use-magic', 'When you look around and read a bad situation, roll +Sharp.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    useMagic = (db.collection('HunterMoves').document('HunterBasicMoves').collection('UseMagic').document('description').get()).to_dict()
    description = useMagic['description'].replace("\\n", '\n')
    effects = useMagic['effects'].replace("\\n", '\n')
    glitches = useMagic['glitches'].replace("\\n", '\n')
    keeperMaySay = useMagic['keeperMaySay'].replace("\\n", '\n')
    on7Plus = useMagic['on7Plus'].replace("\\n", '\n')
    on10Plus = useMagic['on10Plus'].replace("\\n", '\n')
    on12Plus = useMagic['on12Plus'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + on7Plus + '\n \n' + on10Plus + '\n \n' + on12Plus + '\n \n' + effects + '\n \n' + glitches + '\n \n' + keeperMaySay)

@hunterBasicMoves.child
@lightbulb.command('big-magic', 'When you look around and read a bad situation, roll +Sharp.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommandActUnderPressure(ctx):
    bigMagic = (db.collection('HunterMoves').document('HunterBasicMoves').collection('BigMagic').document('description').get()).to_dict()
    description = bigMagic['description'].replace("\\n", '\n')
    keeperMayRequire = bigMagic['keeperMayRequire'].replace("\\n", '\n')
    await ctx.respond(description + '\n \n' + keeperMayRequire)

bot.run()
