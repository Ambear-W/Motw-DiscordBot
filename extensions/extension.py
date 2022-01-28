import hikari
import lightbulb

#this is an extension, aka a different way to put your commands to better organize them
#name the plug in
test_plugin = lightbulb.Plugin("TestPlugin")

#set up the command
@test_plugin.command()
@lightbulb.command('hello', 'Says hello back!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    target = ctx.user
    target2 = ctx.member.display_name
    await ctx.respond(f'Hello!!!!! {target} and {target2} and {target3}')

#load in the extension
def load(bot):
    bot.add_plugin(test_plugin)

def unload(bot):
    bot.remove_plugin(test_plugin)    