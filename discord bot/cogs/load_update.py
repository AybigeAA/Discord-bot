#cog for updating the users.xlsx database with a file that has the same headings as the users.xlsx file
import discord
from discord.ext import commands
import pandas as pd
import os
#this class loads the data 
class LoadUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_users_data()  # Load user data upon cog initialization

    def load_users_from_excel(self, file_path="data/users.xlsx"):
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            return df
        else:
            return pd.DataFrame()

    def load_users_data(self):
        file_path = os.path.join("data", "users.xlsx")
        self.users_data = self.load_users_from_excel(file_path)


    @commands.command(name='update')
    async def update_users_file(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("Please attach a file")
            return
        
        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.xlsx'):
            await ctx.send("Please load an excel (.xlsx) file ")
            return

        temp_file_path = "data/temp_users.xlsx"
        await attachment.save(temp_file_path)

        # Load existing and new files
        existing_df = self.load_users_from_excel(os.path.join("data", "users.xlsx"))
        new_df = pd.read_excel(temp_file_path)

        # Concatenate files
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)

        # Save combined file
        combined_df.to_excel(os.path.join("data", "users.xlsx"), index=False)

        # Update self.users_data
        self.users_data = combined_df

        # Remove temporary file
        os.remove(temp_file_path)

        await ctx.send("Data from excel file updated successfully")

async def setup(bot):
    await bot.add_cog(LoadUpdate(bot))





