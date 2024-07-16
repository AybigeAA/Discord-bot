#cog for adding roles, uses data from the already provided users.xlsx file
import discord
from discord.ext import commands

class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addRole')
    async def add_role_to_new_users(self, ctx):

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
                await ctx.send(f"{user['Discord Username']} cannot be found")
                continue

            roles = user['Roles'].split(',')
            for role_name in roles:
                role = discord.utils.get(ctx.guild.roles, name=role_name.strip())
                if role and role not in member.roles:
                    await member.add_roles(role)
                    await ctx.send(f"new roles are added to{ user['Discord Username']} ")
                elif not role:
                    await ctx.send(f"role {role_name.strip()} cannot be found ")

async def setup(bot):
    await bot.add_cog(AddRole(bot))
