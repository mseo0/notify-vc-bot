import os
import discord
import json
from keep_alive import keep_alive
from discord.ext import commands
from discord import app_commands

client = discord.Client(command_prefix="-", intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

notify_list = []
notify_list_file = "notify_list.json"
# voice_channel = ctx.author.voice.channel

# Load notify list from JSON file
def load_notify_list():
    global notify_list
    if os.path.exists(notify_list_file):
        with open(notify_list_file, "r") as file:
            notify_list = json.load(file)

# Save notify list to JSON file
def save_notify_list():
    with open(notify_list_file, "w") as file:
        json.dump(notify_list, file)

def get_notify_list_names():
    names = []
    for user_id, user_name in notify_list:
        names.append(user_name)
    return names

@client.event
async def on_ready():
  print("Zane bot is online!")
  print(client.user)
  await client.change_presence(status=discord.Status.idle, activity=discord.Activity(
  type=discord.ActivityType.watching,
  name='Zane'
  ))#end of presense change
  
  await tree.sync(guild=discord.Object(id=710158480560095325))


#contantly checks vc
@client.event
async def on_voice_state_update(member, before, after):
  guild_id = 710158480560095325  # Replace with your desired guild ID
  if member.guild.id != guild_id:
    return

  if before.channel is None and after.channel is not None:
     # User joined a voice channel
    for user_id in notify_list:
      user = client.get_user(user_id)
      if user:
        await user.send(f"{member.display_name} has joined a voice channel!")


#first command notify
@tree.command(name="notify", description="Get notified whenever someone joins the VC!", guild=discord.Object(id=710158480560095325))
async def send_dm(interaction):
  user_id = int(interaction.user.id)
  if user_id in notify_list:
    await interaction.response.send_message("You are currently on the notify list!", ephemeral=True)
  else:
    notify_list.append(user_id)
    save_notify_list()
    await interaction.response.send_message("You will be notified when someone joins the voice channel!", ephemeral=True)


    
#second command stopnotify
@tree.command(name = "stopnotify", description = "Stop getting notified whenever someone joins the VC.", guild=discord.Object(id=710158480560095325))
async def second_command(interaction):
  global notify_list  # Add this line to indicate that we are modifying the global notify_list variable
  user_id = int(interaction.user.id)
  if user_id in [entry[0] for entry in notify_list]:
    notify_list = [entry for entry in notify_list if entry[0] != user_id]
    save_notify_list()  # Save the updated notify list to JSON file
    await interaction.response.send_message("You will no longer be notified when someone joins a voice channel!", ephemeral=True)
  else:
    await interaction.response.send_message("You are not currently on the notify list!", ephemeral=True)

#third command ban Timmy
@tree.command(name = "ban-timmy", description = "Ban Timothy!",guild=discord.Object(id=710158480560095325))
async def ban(interaction):
    member = interaction.target
    reason = "Banned Timothy"
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.name} has been banned!")

#print out the list of names
@tree.command(name = "notifylist", description = "Print the list of people on the notify list", guild=discord.Object(id=1114740568233345064))
async def print_notify(interaction):
  load_notify_list()  # Load notify list when the bot is ready

    # Print the names of the people on the notify list
  names = get_notify_list_names()
  if names:
    print("People on the notify list:")
    for name in names:
      print(name)
  else:
    print("Notify list is empty.")
      
#checks for ni:D
@client.event
async def on_ni(message):
  if message.author.bot:
    return
    
  if message.content.lower() == "ni":
    await message.channel.send_message("gger")

#logs in console messages sent to the bot
@client.event
async def on_message(message):
  if message.author.bot:
    return 
    
  author = message.author
  print(f"{author.name} said: " + message.content + '\n')
  

keep_alive()
client.run(os.environ['DISCORD_BOT_SECRET'])