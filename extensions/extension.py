import hikari
import lightbulb
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#this is an extension, aka a different way to put your commands to better organize them
#name the plug in
test_plugin = lightbulb.Plugin("TestPlugin")

#set up the command
@test_plugin.command()
@lightbulb.command('hewwo', 'hewwo?')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    member = ctx.user
    memberName = ctx.member.display_name
    memberID = ctx.member.id
    data = {member, memberName}
    await ctx.respond(f'Hello!!!!! {member} or {memberName} or {memberID}')


#load in the extension
def load(bot):
    bot.add_plugin(test_plugin)

def unload(bot):
    bot.remove_plugin(test_plugin)   