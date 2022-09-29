import sqlite3, time, asyncio

food = []
DB_path = r".\discord_bot.db"
conn = sqlite3.connect(DB_path)
curson = conn.cursor()

def bot_init(path):
    global DB_path
    DB_path = path

def clock():
    date = time.strftime('%#m-%#d', time.localtime())
    now = time.strftime('%H:%M', time.localtime())
    return date, now


def read_food():
    food = []
    for name in curson.execute("SELECT name FROM food"):
        food.append(name[0])
    return food

def write_food(food_name):
    food_name = food_name.split(",")
    for food_ in food_name:
        food_ = food_.strip()
        curson.execute(f"INSERT INTO food VALUES('{food_}')")
    read_food()
    return food

def rm_food(food_name):
    food_name = food_name.split(",")
    for food_ in food_name:
        food_ = food_.strip()
        curson.execute(f"DELETE FROM food WHERE name == '{food_}'")
    read_food()
    return food

def task(MM, DD, HHMM, description, id, who, server_id, server, channel, sucess = False):
    for i in curson.execute("SELECT _index FROM alarm ORDER BY _index DESC limit 1"):
        index = int(i[0]) + 1 if len(i) >= 1 else i
    curson.execute(f"INSERT INTO alarm VALUES('{index}', '{sucess}', '{MM}', '{DD}','{HHMM}','{description}','{id}', '{who}', '{server_id}', '{server}', '{channel}')")
    conn.commit()

def tasklist(server_id):
    msg = ''
    i = 0
    for index, success, MM, DD, HHMM , description, id, who, _server_id, server, channel in curson.execute("SELECT * FROM alarm"):
        if success == "False" and server_id == _server_id:
            i += 1
            msg = msg + f"{i}. {MM}/{DD}, {HHMM}, {description}, {who}\n"
    if msg.replace(" ", '') == '':
        msg = "目前無任務"
    return msg

def where(server_id):
    for _server, _server_id, d4 in curson.execute(f"SELECT * FROM d4channel"):
        if server_id == _server_id:
            return d4

def set_channel(server, server_id, channel_id):
    for _server, _server_id, d4 in curson.execute(f"SELECT * FROM d4channel"):
        if server_id == _server_id:
            curson.execute(f"UPDATE d4channel set d4 = '{channel_id}' WHERE server_id = {server_id}")
        else:
            curson.execute(f"INSERT INTO d4channel VALUES('{server}', '{server_id}', '{channel_id}')")
        conn.commit()            

async def check_task():
    while True:
        for index, check, month, day, _time, description, id, who, server_id, server, channel in curson.execute(f"SELECT * FROM alarm"):
            # print(index, check, month, day, _time, description, id)              #檢查點1
            if check == "False":
                data, now = clock()
                if data == f"{month}-{day}":
                    # print(data, f"{month}-{day}")                                 #檢查點2
                    if now == _time:
                        # print(description, id)                                   #檢查點3
                        curson.execute(f"UPDATE alarm set success = 'True' WHERE _index = {index}")
                        conn.commit()
                        _where = where(server_id)
                        if _where != channel and _where != None:
                            channel = _where
                        return description, id, channel
        await asyncio.sleep(1)
