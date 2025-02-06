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
            await message.channel.create_thread(name=f"{message.author.nick}: {user_message}", message=new_message)
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

        await client.change_presence(activity=discord.Streaming(name='CSA', url='https://www.twitch.tv/uwaterloocsa'))
        
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
        await interaction.response.send_message(f"{interaction.user.mention}: {idea}", suppress_embeds=True)
        message = await interaction.original_response()
        await message.create_thread(name = f"{interaction.user.nick}: {idea}")
        reaction = '⬆️'
        await message.add_reaction(reaction)

    @client.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return  # Ignore bot reactions

        specific_emoji = '<:shanade:1337156702851694632>' # Emoji to watch for
        if str(reaction.emoji) == specific_emoji and (str(user.id) == "735967869367746562" or str(user.id) == "96435974011105280"):
            message = reaction.message
            print(message)

            # # Check if the message already has a thread
            active_threads = await message.channel.active_threads()

            # Check if a thread exists for this message
            existing_thread = next((thread for thread in active_threads if thread.starter_message_id == message.id), None)

            if existing_thread:
                # Create a string of mentions from raw_mentions
                mentions = ' '.join(f"{user_id.mention}" for user_id in reaction.message.mentions)

                # Send the message with all mentions at the beginning
                await existing_thread.send(f"{mentions}! {user.mention} has approved of your idea! Please plan a filming + relevant people needed.")


    client.run(os.environ['TOKEN'])
