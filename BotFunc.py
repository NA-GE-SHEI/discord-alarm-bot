import sqlite3, time, asyncio, datetime
from datetime import datetime, timezone, timedelta
from collections import namedtuple

food = []
DB_path = r"./sparktech.db"
conn = sqlite3.connect(DB_path)
cursor = conn.cursor()

def bot_init(path):
    global DB_path
    DB_path = path

def clock():
    class Date:
        now = datetime.now(timezone.utc) + timedelta(hours=8)
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
    return Date


def read_food():
    food = []
    for name in cursor.execute("SELECT name FROM food"):
        food.append(name[0])
    return food

def write_food(food_name):
    food_name = food_name.split(",")
    for food_ in food_name:
        food_ = food_.strip()
        cursor.execute(f"INSERT INTO food VALUES('{food_}')")
    read_food()
    return food

def rm_food(food_name):
    food_name = food_name.split(",")
    for food_ in food_name:
        food_ = food_.strip()
        cursor.execute(f"DELETE FROM food WHERE name == '{food_}'")
    read_food()
    return food

def task(MM, DD, HHMM, description, id, name, server_id, server, channel, who, sucess = False):
    for i in cursor.execute("SELECT _index FROM alarm ORDER BY _index DESC limit 1"):
        index = int(i[0]) + 1 if len(i) >= 1 else i
    cursor.execute(f"INSERT INTO alarm VALUES('{index}', '{sucess}', '{MM}', '{DD}','{HHMM}','{description}','{id}', '{name}', '{server_id}', '{server}', '{channel}', '{who}')")
    conn.commit()
    return index

def tasklist(server_id):
    msg = ""
    i = 0
    query = """SELECT _index, success, MM, DD, HHMM, description, id, name, server_id, server, channel, who
               FROM alarm WHERE success=? AND server_id=? ORDER BY MM, DD ASC"""
    for alarm in cursor.execute(query, ("False", server_id)):
        i += 1
        msg += f"{i}. {alarm[2]}/{alarm[3]}, {alarm[4]}, {alarm[5]}, {alarm[7]} (#{alarm[0]})\n\n"
    return msg.strip() or "目前無任務"

def where(server_id):
    for _server, _server_id, d4 in cursor.execute(f"SELECT * FROM d4channel"):
        if server_id == _server_id:
            return d4

def set_channel(server, server_id, channel_id):
    query = "SELECT * FROM d4channel WHERE server_id = ?"
    result = cursor.execute(query, (server_id,)).fetchone()
    if result is not None:
        cursor.execute("UPDATE d4channel SET d4 = ? WHERE server_id = ?", (channel_id, server_id))
    else:
        cursor.execute("INSERT INTO d4channel VALUES (?, ?, ?)", (str(server), int(server_id), int(channel_id)))
    conn.commit()

def rmalarm(index, id):
    query = "SELECT * FROM alarm WHERE _index = ?"
    result = cursor.execute(query, (index,)).fetchone()
    try:
        if result != None:
            dbID = ''.join(filter(str.isdigit, result[6]))
            if str(dbID) != str(id):
                resultMsg = "欸 你又不是本人, 想亂刪?"
            elif result[1] == "True":
                resultMsg = "已經執行過的任務讓我留個紀錄好嗎?"
            else:
                message = f"{result[2]}/{result[3]}, {result[4]}, {result[5]}, {result[7]} (#{result[0]})"
                query = "UPDATE alarm SET success = ? WHERE _index = ?"
                result = cursor.execute(query, ("Cancel", index,)).fetchone()
                conn.commit()
                resultMsg = f"已刪除 {message}"
        else:
            resultMsg = "這選項是空的, 你再看看"
    except:
        resultMsg = "出了點意外:("
    return resultMsg


Alarm = namedtuple("Alarm", ["index", "check", "month", "day", "time", "description",
                             "id", "name", "server_id", "server", "channel", "who"])

async def check_task():
    nowYear = datetime.now().year
    while True:
        for alarm in cursor.execute("SELECT * FROM alarm"):
            alarm = Alarm(*alarm)
            if alarm.check == "False":
                try:
                    date = clock()
                    now_time = datetime(nowYear, date.month, date.day, date.hour, date.minute)
                    alarm_time = datetime(nowYear, int(alarm.month), int(alarm.day),
                                          int(alarm.time.split(":")[0]), int(alarm.time.split(":")[1]))
                    if now_time >= alarm_time:
                        cursor.execute(f"UPDATE alarm SET success = 'True' WHERE _index = {alarm.index}")
                        conn.commit()
                        _where = where(alarm.server_id)
                        channel = _where or alarm.channel
                        return alarm.description, alarm.id, channel, alarm.who
                except ValueError:
                    print("時間錯誤")
        await asyncio.sleep(1)
