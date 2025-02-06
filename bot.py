import discord
from discord import app_commands
from discord.utils import get
import os
import responses    
from discord.ext import commands
import asyncio
async def send_message(message,user_message,is_private):
    try:
        response,needDelete = responses.handle_response(user_message,message.author)

        if not needDelete and response != None: 
            await message.author.send(response) if is_private else await message.channel.send(response)
        elif response != None and message.reference != None:
            repliedMessage = await message.channel.fetch_message(message.reference.message_id)
            await message.delete()
            await repliedMessage.reply(response, mention_author=True)
            
        elif response != None:
            await message.delete()
            new_message = await message.channel.send(response)
            reaction = '⬆️'
            await new_message.add_reaction(reaction)
            await message.channel.create_thread(name=f"{message.author.nick}", message=new_message)
    except Exception as e:
        print(e)
        

def run_discord_bot():

    
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        tree.copy_global_to(guild=discord.Object(id=1050941726283534438))
        tree.copy_global_to(guild=discord.Object(id=780881088486703124))

        await tree.sync(guild=discord.Object(id=1050941726283534438))
        await tree.sync(guild=discord.Object(id=780881088486703124))

        await client.change_presence(activity=discord.Streaming(name='CSA', url='https://www.twitch.tv/tenz'))
        
        print("Ready!")


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        if len(message.attachments) > 0 and user_message == "":
            
            return
        else:
            await send_message(message,user_message,is_private=False)



    tree = app_commands.CommandTree(client)

    @tree.command(name = "tiktok", description = "Use this command for any Tiktok ideas that don't have links") 
    async def send(interaction: discord.Interaction, idea: str):
        await interaction.response.send_message(idea, suppress_embeds=True)
        message = await interaction.original_response()
        await message.create_thread(name = f"{interaction.user.mention}: {idea}")
        reaction = '⬆️'
        await message.add_reaction(reaction)




    client.run(os.environ['TOKEN'])
