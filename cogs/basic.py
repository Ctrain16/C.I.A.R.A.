from asyncio.windows_events import NULL
import discord
from discord.ext import commands
from discord.utils import get

default_role : discord.Role = NULL

class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Events
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await ctx.send('Error: Role was not found')
            print('Error: Basic -> role was not found\n')


    @commands.Cog.listener()
    async def on_member_join(self, member):
        global default_role
        guild = member.guild

        if guild.system_channel is not None:
            await guild.system_channel.send('Welcome {0.mention}, to {1.name}!'.format(member, guild))
            print(f'Basic: {member} joined {guild.name}\n')
        
        if default_role != NULL:
            await member.add_roles(default_role)
            print(f'Basic: {member} was given the {default_role.name} role.\n')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            await guild.system_channel.send('{0.mention} has left {1.name}.... :('.format(member, guild))
            print(f'Basic: {member} has left {guild.name}\n')


    #Commands
    @commands.command(description='Evaluates a math equation', aliases=['c','calc','math'])
    async def compute(self,ctx,*,equation):
        await ctx.send(f'{eval(equation)} = {equation}')
        print(f'Basic: computed the following equation : {equation}\n')


    @commands.command(description='Retrieves latency of bot')
    async def ping(self,ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'{latency}ms')
        print(f'Basic: Ping = {latency}\n')


    @commands.command(description='Sets default role to assign to new members', aliases=['set default role','setDefRole','sdr'])
    async def role(self,ctx,role : discord.Role):
        global default_role
        default_role = role
        await ctx.send(f'Default role set to: {default_role.mention}')
        print(f'Basic: Default role was set to {default_role.name}\n')

    
def setup(bot):
    bot.add_cog(Basic(bot))
