import discord, asyncio, discord, random
from discord import app_commands
import bot_func

TOKEN = <discord bot TOKEN>

class aclinet(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}")
        while True:
            content, who = await bot_func.check_task()
            print(content, who)
            channel = client.get_channel(<指定頻道ID>)
            await channel.send(f'<@{who}> {content} ')
        

client = aclinet()
tree = app_commands.CommandTree(client)

@tree.command(name = "task", description = "鬧鐘(time格式為24小時制, HH:MM)" )
async def self(interaction: discord.Integration, mm:int, dd:int, time:str, desc:str):
    if ":" in time:
        if mm <=24 and dd <=59:
            bot_func.task(mm, dd, time, desc, interaction.user.id, interaction.user)
            await interaction.response.send_message(f"鬧鐘已定在{mm}/{dd}, {time}, 內容: {desc}")
        else:
            await interaction.response.send_message("你什麼時候看過時間會大於25或60的<:n_:1006744546186629242>")
    else:
        await interaction.response.send_message("time要打':'")

@tree.command(name = "吃啥", description = "就是吃啥:D" )
async def self(interaction: discord.Integration):
    food = bot_func.read_food()
    rd = random.randint(0, len(food)-1)
    await interaction.response.send_message(food[rd])

@tree.command(name = "addfood", description = "增加food清單" )
async def self(interaction: discord.Integration, food:str):
    food = bot_func.write_food(food)
    rd = random.randint(1, 3)
    msg = "k" * rd
    await interaction.response.send_message(f"{msg} <:nice:1006743132169310208>")

@tree.command(name = "rmfood", description = "刪除food清單" )
async def self(interaction: discord.Integration, food:str):
    food = bot_func.rm_food(food)
    await interaction.response.send_message(f"好 <:rushicry:1006744501928337498>")

@tree.command(name = "foodlist", description = "列出food清單" )
async def self(interaction: discord.Integration):
    food = bot_func.read_food()
    msg = ''
    for i in food:
        msg += i + "\n"
    await interaction.response.send_message(msg)

@tree.command(name = "tasklist", description = "列出鬧鐘任務清單" )
async def self(interaction: discord.Integration):
    msg = bot_func.tasklist()
    await interaction.response.send_message(msg)

client.run(TOKEN)