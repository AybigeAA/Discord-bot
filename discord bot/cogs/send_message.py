#cog for sending messages to users' mails'
import os
import discord
import base64
import pandas as pd
from io import BytesIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from discord.ext import commands
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import asyncio
from io import BytesIO

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

class SendMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sendMessage')
    async def send_message(self, ctx, *, message_content: str):
        if not ctx.message.attachments:
            await ctx.send("Please add an excel file with the e-mails")
            return

        # read the attached excel file 
        attachment = ctx.message.attachments[0]
        file_bytes = await attachment.read()
        
        try:
            df = pd.read_excel(BytesIO(file_bytes))
        except Exception as e:
            await ctx.send("file cannot be read, please load a valid excel file")
            return
        
        if 'Email' not in df.columns or 'Name' not in df.columns:
            await ctx.send(" 'Email' and 'Name' cloumns cannot be found in the file")
            return
        
        for _, row in df.iterrows():
            email = row['Email']
            name = row['Name']
            
            personalized_message = f"Hello {name}!🎓,\n\n{message_content}"
            self.send_email(email, personalized_message)
            await asyncio.sleep(5)

        await ctx.send(f"Message is sent to {len(df)}")

    def send_email(self, to_email, message):
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        msg = MIMEMultipart()
        msg['From'] = ""  # sender e-mail
        msg['To'] = to_email
        msg['Subject'] = "sour mail's subject"

        msg.attach(MIMEText(message, 'plain'))

        try:
            raw_message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
            message = service.users().messages().send(userId="me", body=raw_message).execute()
            print(f"e-mail is sent to {to_email}  Message ID: {message['id']}")
        except Exception as e:
            print(f"e-mail couldn't be sent to {to_email}  {e}")
            

async def setup(bot):
    await bot.add_cog(SendMessage(bot))


