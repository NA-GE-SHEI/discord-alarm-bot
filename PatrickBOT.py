import discord, time, datetime, asyncio, re, discord, random, sys, logging, os, openai, calendar, typing
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from discord import app_commands
from discord.ui import Button, View
import BotFunc

load_dotenv(r"./.env", override=True)
TOKEN = os.getenv("DiscordBotToken")
openai.api_key = os.getenv("ChatGPTToken")

log_path = r"./patrick_hehe.log"
log = logging.getLogger()
handlers = RotatingFileHandler(log_path, "a", 1024*1024*5, 3, "utf-8")
log.addHandler(handlers)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s[%(levelname)s]%(funcName)s: %(message)s")
handlers.setFormatter(formatter)

class aclinet(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default(), timeout=60.0)
        self.value = None
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            logging.info(f"We have logged in as {self.user}")
        while True:
            content, who, where = await BotFunc.check_task()
            channel = client.get_channel(where)
            try:
                await channel.send(f'{who} {content} ')
                logging.info(f"Successfuly alarm task, from {who}")
            except Exception as e:
                logging.error(f"任務失敗, 來自 '{where}' 頻道\n請確認機器人權限")
                logging.error(e)
        

client = aclinet()
tree = app_commands.CommandTree(client)

@tree.command(name = "alarm", description = "鬧鐘(time格式為24小時制, HH:MM)")
async def self(interaction: discord.Integration, mm:int, dd:int, time:str, desc:str, who:str = "default"):
    if who == "default":
        who = f"<@{interaction.user.id}>"
    class hourErr(BaseException):
        msg = "他媽你看過哪個小時會超過24的???"
    class minErr(BaseException):
        msg = "他媽你看過哪個分鐘會超過60的???"
    toDay = datetime.datetime.now()
    nowYear = toDay.year
    try:
        checkDay = calendar.monthrange(nowYear, mm)[1]
        if dd > checkDay or not str(dd).isdigit() or dd <=0:
            raise
        if ":" in time:
            if int(time.split(":")[0]) >=24:
                raise hourErr
            if int(time.split(":")[1]) >=60:
                raise minErr
            BotFunc.task(mm, dd, time, desc, who, interaction.user,
                            interaction.guild.id, interaction.guild, interaction.guild.system_channel.id)
            await interaction.response.send_message(f"鬧鐘已定在{mm}/{dd}, {time}, 內容: {desc}")
            logging.info(f"來自'{interaction.user}'已成功設定鬧鐘")
        else:
            await interaction.response.send_message("time要打':'")
            logging.warning(f"時間設定格式錯誤")
    except hourErr as e:
        await interaction.response.send_message(e.msg)
        logging.warning(f"時間設定錯誤")
    except minErr as e:
        await interaction.response.send_message(e.msg)
        logging.warning(f"時間設定錯誤")
    except:
        await interaction.response.send_message(f"不是, 你確定{mm}月有{dd}號這天 <:n_:1006744546186629242>")
        logging.warning(f"時間設定錯誤")        

@tree.command(name = "吃啥", description = "就是吃啥:D" )
async def self(interaction: discord.Integration):
    food = BotFunc.read_food()
    rd = random.randint(0, len(food)-1)
    try:
        await interaction.response.send_message(food[rd])
        logging.info(f"來自 '{interaction.user}' 完成 '吃啥'")
    except Exception as e:
        logging.error(f"來自 '{interaction.user}' 失敗 '吃啥'")
        logging.error(e)

@tree.command(name = "addfood", description = "增加food清單" )
async def self(interaction: discord.Integration, food:str):
    food = BotFunc.write_food(food)
    rd = random.randint(1, 3)
    msg = "o"+"k" * rd
    try:
        await interaction.response.send_message(f"{msg} <:nice:1006743132169310208>")
        logging.info(f"來自 '{interaction.user}' 完成 'addfood'")
    except Exception as e:
        logging.error(f"來自 '{interaction.user}' 失敗 'addfood'")
        logging.error(e)

@tree.command(name = "rmfood", description = "刪除food清單" )
async def self(interaction: discord.Integration, food:str):
    food = BotFunc.rm_food(food)
    try:
        await interaction.response.send_message(f"好 <:rushicry:1006744501928337498>")
        logging.info(f"來自 '{interaction.user}' 完成 'rmfood'")
    except Exception as e:
        logging.error(f"來自 '{interaction.user}' 失敗 'rmfood'")
        logging.error(e)

@tree.command(name = "foodlist", description = "列出food清單" )
async def self(interaction: discord.Integration):
    food = BotFunc.read_food()
    msg = ''
    for i in food:
        msg += i + "\n"
    try:
        await interaction.response.send_message(msg)
        logging.info(f"來自 '{interaction.user}' 完成 'foodlist'")
    except Exception as e:
        logging.error(f"來自 '{interaction.user}' 失敗 'foodlist'")
        logging.error(e)

@tree.command(name = "alarmlist", description = "列出鬧鐘任務清單" )
async def self(interaction: discord.Integration):
    msg = BotFunc.tasklist(interaction.guild.id)
    try:
        await interaction.response.send_message(msg)
        logging.info(f"來自 '{interaction.user}' 完成 'alarmlist'")
    except Exception as e:
        logging.error(f"來自 '{interaction.user}' 失敗 'alarmlist'")
        logging.error(e)

@tree.command(name = "set_alarm_channel", description = "設定提醒頻道ID, 沒設就是系統訊息頻道" )
async def self(interaction: discord.Integration, id:str):
    BotFunc.set_channel(interaction.guild, interaction.guild.id, id)
    try:
        await interaction.response.send_message(f"好 <:nice:1006743132169310208>")
        logging.info(f"來自 '{interaction.user}' 完成 'set_alarm_channel'")
    except Exception as e:
        logging.error(f"來自 '{interaction.user}' 失敗 'set_alarm_channel'")
        logging.error(e)

@tree.command(name = "說", description = "派大星說" )
async def self(interaction: discord.Integration, echo:str):
    channel = client.get_channel(interaction.channel.id)
    await interaction.response.send_message(echo, ephemeral=True)
    try:
        await channel.send(f"{echo}")
        logging.info(f"來自 '{interaction.user}' 完成 '說'")
        logging.debug(f"{interaction.user}({interaction.user.id})說: {echo}")
    except Exception as e:
        logging.error(f"來自 '{interaction.user}' 失敗 '說'")
        logging.error(e)

@tree.command(name = "請問", description = "就打你想問的" )
async def self(interaction: discord.Integration, content:str):
    print("Content:", content)
    try:
        await interaction.response.defer()
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=content,
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = completion.choices[0].text
        if len(response) <= 0:
            raise Exception
        print("Response:", str(response))
        await interaction.followup.send(response, ephemeral=True)
    except Exception as e:
        print("Error:", e)
        response = "uhhhh.......Something error. Please retry again later."
        await interaction.followup.send(response, ephemeral=True)

@tree.command(name = "ping", description = "就ping" )
async def self(interaction: discord.Integration):
    await interaction.response.send_message(f'Pong! {round(client.latency * 1000, 2)}ms.')

@tree.command(name = "rmalarm", description = "使用alarmlist後, 最後面(#?)為任務編號")
async def self(interaction: discord.Integration, delete:str):
    try:
        result = BotFunc.rmalarm(delete, interaction.user.id)
        await interaction.response.send_message(f"{result}")
    except:
        await interaction.response.send_message(f"失敗了 <:saddog:845948423130578984>")
        
# @tree.command(name = "test", description = "測試還要解釋?" )
# async def self(interaction: discord.Integration):
#     channel = client.get_channel(972505788016889957)
#     try:
#         accept_decline = await channel.send(f'test')
#         await accept_decline.add_reaction('\u2611')
#         client.wait_for()
#         print(accept_decline)
#         a = accept_decline.reactions
#         print(a)
#     except Exception as e:
#         print(e)

client.run(TOKEN)