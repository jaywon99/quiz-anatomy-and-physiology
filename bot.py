# -*- coding: utf-8 -*-

import discord
import sys
import os
import random

client = discord.Client()

QUESTIONS = [["Q1", "A1"],
             ["Q2", "A2"]]

# refer https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
@client.event
async def on_ready():
    # https://discordpy.readthedocs.io/en/latest/api.html#user
    # node.js client.user.tag == client.user.name + '#' + client.user.discriminator
    print("Logged in as %s" % (client.user.name + '#' + client.user.discriminator))

# refer https://discordpy.readthedocs.io/en/latest/api.html#discord.on_member_join
@client.event
async def on_member_join(member):
    '''
    node.js code is
    // Send the message to a designated channel on a server:
    const channel = member.guild.channels.find(ch => ch.name === 'member-log');
    // Do nothing if the channel wasn't found on this server
    if (!channel) return;
    // Send the message, mentioning the member
    channel.send(`Welcome to the server, ${member}`);
    '''
    # find channel
    channel = next(channel for channel in member.guild.channels if channel.name == 'member-log')
    if not channel:
        return
    # await client.send_message(channel, 'Welcome to the server, %s' % (member.name))
    await channel.send('Welcome to the server, %s' % (member.name))
    pass

label = None

# refer https://discordpy.readthedocs.io/en/latest/api.html#discord.on_message
@client.event
async def on_message(message):
    # DEFINE global var label in module
    global label

    # check this message came from bot - then skip!
    if message.author.bot:
        return
    cmd_param = message.content.split(" ", 1)
    cmd = cmd_param[0]
    param = None
    if len(cmd_param) > 1:
        param = cmd_param[1]

    if cmd == '!question':
        # DO question
        label = random.randrange(0, len(QUESTIONS))
        await message.channel.send(QUESTIONS[label][0])
        return

    if cmd == '!a':
        # DO answer
        if label == None:
            return await message.channel.send("No Question.")

        if param == QUESTIONS[label][1]:
            return await message.channel.send('Correct')
        else:
            return await message.channel.send('Incorrect. The answer is %s.' % QUESTIONS[label][1])
        return

    return

#run the program!
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    TOKEN = os.getenv('TOKEN')

    # logs into channel    
    try:
        print("START discord quiz bot!!")
        client.run(TOKEN)
    except:        
        client.close()

