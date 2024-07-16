#cog for banning users for 2 years, blacklist.xlsx must be loaded while using the !ban command. file must include Discord Username and Ban Time headings as a table.
import discord
from discord.ext import commands, tasks
import pandas as pd
from datetime import datetime, timedelta
import os

class BanUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blacklist_file = 'blacklist.xlsx'
        
        # Ensure blacklist.xlsx exists
        if not os.path.isfile(self.blacklist_file):
            df = pd.DataFrame(columns=['Discord Username', 'Ban Time'])
            df.to_excel(self.blacklist_file, index=False)
        
        self.unban_task.start()

    def cog_unload(self):
        self.unban_task.cancel()

    @commands.command(name='ban')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("PLease load an excel file")
            return
        
        attachment = ctx.message.attachments[0]
        file_path = f"./{attachment.filename}"
        await attachment.save(file_path)
        
        # Read the Excel file
        try:
            user_df = pd.read_excel(file_path)
        except Exception as e:
            await ctx.send("File not read, load a valid file")
            os.remove(file_path)
            return
        
        # Check if the required column is in the uploaded file
        if 'Discord Username' not in user_df.columns:
            await ctx.send(" 'Discord Username' heading cannot be found in the excel file")
            os.remove(file_path)
            return
        
        # Load or create the blacklist
        blacklist_df = pd.read_excel(self.blacklist_file)
        
        now = datetime.now()
        usernames_to_ban = user_df['Discord Username'].tolist()
        
        banned_users = []
        
        for username in usernames_to_ban:
            member = discord.utils.get(ctx.guild.members, name=username)
            if member:
                await ctx.guild.ban(member, reason="Banned via bot")
                banned_users.append({'Discord Username': username, 'Ban Time': now})
        
        # Update the blacklist
        if not banned_users:
            await ctx.send("User cannot be found")
            os.remove(file_path)
            return
        
        new_blacklist_df = pd.DataFrame(banned_users)
        blacklist_df = pd.concat([blacklist_df, new_blacklist_df], ignore_index=True)
        blacklist_df.to_excel(self.blacklist_file, index=False)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        await ctx.send(f"{len(banned_users)} is banned and added to blacklist.xlsx ")

    @tasks.loop(hours=24)  # Check every 24 hours
    async def unban_task(self):
        now = datetime.now()
        blacklist_df = pd.read_excel(self.blacklist_file)
        two_years_ago = now - timedelta(days=2*365)
        
        to_unban = blacklist_df[blacklist_df['Ban Time'] < two_years_ago]
        
        for username in to_unban['Discord Username']:
            user = discord.utils.get(await self.bot.guilds[0].bans(), name=username)
            if user:
                await self.bot.guilds[0].unban(user.user, reason="Ban time over")
        
        # Remove unbanned users from blacklist
        blacklist_df = blacklist_df[blacklist_df['Ban Time'] >= two_years_ago]
        blacklist_df.to_excel(self.blacklist_file, index=False)

    @unban_task.before_loop
    async def before_unban_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(BanUsers(bot))
