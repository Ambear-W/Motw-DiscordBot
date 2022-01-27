import hikari
import lightbulb
import firebase_admin
from firebase_admin import credentials
from config import *

#Make sure you activate the evn/virtual enviroment to test: venv & then run the python code py botSetUp.py
#Note, every time you make changes, close the bot in the terminal and then restart it.  It will then have your changes.

#basic auto-sharding bot implementation - I made a config.py file to make data safer
bot = lightbulb.BotApp(
    token = token_config, 
    default_enabled_guilds = (default_enabled_guilds_config)
)
#sets up our connection with Google Firebase - this will be were we store player's inform
# ation!
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

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

bot.run()
