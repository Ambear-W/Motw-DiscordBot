import hikari
import lightbulb
import firebase_admin
from firebase_admin import credentials
from config import *

#make sure you activate the evn/virtual enviroment to test: venv & then run the python code py botSetUp.py

#Note, every time you make changes, close the bot in the terminal and then restart it.  It will then have your changes.

#basic auto-sharding bot implementation, uses the token to connect to your bot
#don't share this (aka AMBER MAKE SURE YOU REMOVE IT BEFORE YOU PUT IT ON GITHUB SINCE IT'S PUBLIC)
bot = lightbulb.BotApp(
    token = token_config, 
    default_enabled_guilds = (default_enabled_guilds_config)
)

#calls to the config file for the info to get into our Firebase.  We do not want to share this info because other users could access the data base
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

#The below is an example of an eventlistener!  eventlistners are similar to functions, expect they are listening to something!
#  the code that will run when ever the event is triggered, which is every time a message is sent/created in the channel
#   it will print what was sent in the channel in the terminal/console
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

#There are groups and sub commands as well, they are very similar to the previous commands - but there are differences
@bot.command
@lightbulb.command('group', 'This is a group')
#this command is going to have subcommands and will be grouped toogether
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def my_group(ctx):
    #do nothing just go on!
    #why? --> group commands cannot be run with just slash commands
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
