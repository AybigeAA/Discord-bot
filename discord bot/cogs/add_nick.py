#cog for adding nicknames as name and surname, uses data from the already provided users.xlsx file
import discord
from discord.ext import commands

class AddNick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addNick')
    async def add_nick_to_users(self, ctx):
        load_users_cog = self.bot.get_cog('LoadUpload')
        if not load_users_cog:
            await ctx.send("LoadUpload cog not found.")
            return

        users_data = load_users_cog.users_data
        if users_data.empty:
            await ctx.send("User data is empty or not loaded.")
            return

        for  user in users_data.iterrows():
            member = ctx.guild.get_member_named(user['Discord Username'])
            if not member:
                await ctx.send(f"{user['Discord Username']} is not found")
                continue

            name = user['Name']
            surname = user['Surname']
            if not member.nick or member.nick != f"{name} {surname}":
                try:
                    await member.edit(nick=f"{name} {surname}")
                    
                except discord.Forbidden:
                    await ctx.send(f"{member.name}'s nickname cannot be updated : insufficient permision")
                except discord.HTTPException as e:
                    await ctx.send(f"{member.name}'s nickname cannot be updated : {e}")


async def setup(bot):
    await bot.add_cog(AddNick(bot))
