
import json
from time import time
import asyncio
from datetime import datetime, timedelta
import asyncpg
from telegram.ext import ApplicationBuilder
import telegram


from config import tg_access_token, db_db_name, db_host, db_password, db_user
bot = ApplicationBuilder().token(tg_access_token).build().bot


async def grasp_rows(db_pool, hours = 6):
    """Grasp a banch of data from DB and convert to a dict format"""
    grasp = None
    certain_time = datetime.strftime((datetime.today() - timedelta(hours=hours)), '%Y-%m-%d %H:%M:%S')

    postgres_insert = f"""
    SELECT pd.url
    FROM carousel_db pd
    WHERE pd.content_id in (SELECT cb.content_id FROM content_db cb 
            WHERE save_date > '{str(certain_time)}')"""
    try:
        grasp = await db_pool.fetch(postgres_insert)
    except Exception as _ex:
        print(_ex)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, list, grasp)


async def carousels_sender(data:telegram.InputMediaPhoto) -> None:
    temp_list = []
    for k,v in data.items():
        temp_list.append(v)
    await bot.send_media_group(media = await carousels_converter(temp_list), chat_id = 189382736)


async def carousels_converter(data) -> list:
    some_list = []
    temp_var = None
    for x in data:
        temp_var = telegram.InputMediaPhoto(x)
        some_list.append(temp_var)      
    return some_list

async def job(connection, hours = 6):
    an_array = await grasp_rows(connection, hours)
    temp_array = []
    for x in an_array:
        for y in list(x):
            temp_y = json.loads(y)
            try:
                await carousels_sender(temp_y)
            except Exception as _ex:
                print(f'!Errore in file {__file__} :  THE ERROR is :',_ex)


async def main_carousel_sender(hourse = 6):

    """Main function"""
    try:
        connection = await asyncpg.connect(host = db_host, user = db_user, password = db_password
        , database = db_db_name)
        await asyncio.create_task(job(connection, hours = 7))
    except Exception as _ex:
        print('Error:', _ex)
    finally:
        if connection:
            await connection.close()
            print('connection is closed')


# if __name__ == '__main__':
#     asyncio.run(main_carousel_sender())