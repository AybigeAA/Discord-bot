# Discord-bot
A discord bot for sending invitation links and messages, adding roles and nicknames.
- "!sendInvite your message" is used for sending discord server invitations to people. You need to add an excel file with Email, Name and Surname headers.
- "!sendMessage your message" is used for sending messages. You need to add an excel file with Email and Name headers.
- "!addNick" adds name and surname as server nickname. Gets data from the alreadt provided users.xlsx file.
- "!addRole" adds role to users. Gets data from the alreadt provided users.xlsx file.
- "!ban" bans users for 2 years also unbans them when 2 years is up.
- "!update" updates the users.xlsx with the provided data. The file that you add to this command must be configured as the users.xlsx.
- "!show name surname" shows the info of the user provided.
- If shows an error about e-mail and password, it is probably because of the credentials.json or token.json file. Make sure that they are coorect.
