#cog to see the info of a user
import discord
from discord.ext import commands
import pandas as pd

class ShowUserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_data = pd.read_excel('data/users.xlsx')  # Assuming user data is stored in an Excel file

    @commands.command(name='show')
    async def show(self, ctx, *, full_name: str):
        # Split the full name into parts and handle case and whitespace
        name_parts = full_name.strip().split()
        if len(name_parts) < 2:
            await ctx.send("Please provide both a first name and a surname.")
            return

        name = ' '.join(name_parts[:-1])
        surname = name_parts[-1]

        # Filter the user data to find the matching entries
        matching_users = self.user_data[(self.user_data['Name'].str.strip().str.lower() == name.lower()) &
                                        (self.user_data['Surname'].str.strip().str.lower() == surname.lower())]

        print("Filtered users:")
        print(matching_users)

        if matching_users.empty:
            await ctx.send("No users found with the given name and surname.")
        else:
            for row in matching_users.iterrows():
                user_info = (
                    f"Name: {row['Name']}\n"
                    f"Surname: {row['Surname']}\n"
                    f"Email: {row['Email']}\n"
                    f"Discord Username: {row['Discord Username']}\n"
                    f"Phone Number: {row['Phone Num']}\n"
                    f"Roles: {row['Roles']}\n"
                )
                await ctx.send(f"```{user_info}```")

async def setup(bot):
    await bot.add_cog(ShowUserInfo(bot))
