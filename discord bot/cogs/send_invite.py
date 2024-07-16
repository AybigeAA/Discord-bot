#cog for sending dc invite links to mail's of the users. Links can be used for once
import discord
import pandas as pd
from io import BytesIO
from discord.ext import commands
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import asyncio


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

def send_invite_to_email(email, invite_link, full_name, base_message):
    try:
        sender_email = ""  # Replace with your email
        subject = "message's subject"
        message_text = f"hey  {full_name}!👋🏻\n\n{base_message}\n\nDiscord invite link {invite_link}"

        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        message = create_message(sender_email, email, subject, message_text)
        send_message(service, "me", message)
    except Exception as e:
        print(f"Error sending email: {e}")

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(f'An error occurred: {error}')

class SendInvite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sendInvite(self, ctx, *, base_message: str):
        try:
            if not ctx.message.attachments:
                await ctx.send("Please load an excel file")
                return

            attachment = ctx.message.attachments[0]
            if not attachment.filename.endswith('.xlsx'):
                await ctx.send("Please load an excel (.xlsx) file ")
                return
            
            file_content = await attachment.read()
            excel_data = pd.read_excel(BytesIO(file_content))
            
            if 'Email' not in excel_data.columns or 'Name' not in excel_data.columns or 'Surname' not in excel_data.columns:
                await ctx.send(" 'Email', 'Name' or 'Surname' cloumns cannot be found in the excel file")
                return
            
            for row in excel_data.iterrows():
                email = row['Email']
                full_name = f"{row['Name']} {row['Surname']}"
                invite_link = await self.create_invite(ctx)
                if not invite_link:
                    await ctx.send("Invite link cannot be created")
                    return
                send_invite_to_email(email, invite_link, full_name, base_message)
                await ctx.send(f"e-mail is sent to {email} ")
                await asyncio.sleep(3)
        except Exception as e:
            await ctx.send(f"Error occured: {e}")
            print(f"error in sendInvite command: {e}")
            import traceback
            traceback.print_exc()

    async def create_invite(self, ctx):
        try:
            guild = ctx.guild
            if not guild:
                print("Server not found")
                return None
            channel = guild.text_channels[0]
            invite = await channel.create_invite(max_uses=1, unique=True)
            return invite.url
        except Exception as e:
            print(f"Invite not created error: {e}")
            return None

async def setup(bot):
    await bot.add_cog(SendInvite(bot))
