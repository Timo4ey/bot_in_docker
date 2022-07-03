# pylint: disable=no-name-in-module
from time import time
import asyncio
from datetime import datetime, timedelta
import aiohttp
import asyncpg
from telegram.ext import ApplicationBuilder


from config import tg_access_token, db_db_name, db_host, db_password, db_user
bot = ApplicationBuilder().token(tg_access_token).build().bot


async def grasp_rows(db_pool, hours = 6):
    """Grasp a banch of data from DB and convert to a dict format"""
    grasp = None
    certain_time = datetime.strftime((datetime.today() - timedelta(hours=hours)), '%Y-%m-%d %H:%M:%S')

    postgres_insert = f"""
    SELECT pd.url, pd.text
    FROM post_db pd
    WHERE pd.content_id in (SELECT cb.content_id FROM content_db cb 
            WHERE save_date > '{str(certain_time)}')"""
    try:
        grasp = await db_pool.fetch(postgres_insert)
    except Exception as _ex:
        print(_ex)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, dict, grasp)



async def get_meta_data(link):
    """"Getting bites from link"""
    async with aiohttp.ClientSession() as session:
        result = await session.get(link)
        read = await result.read()
        return read


async def send_memes(array:bytes, chat_id, text) -> None:
    """"Send memes to a chat"""
    try:
        await bot.send_photo(photo = array, chat_id=chat_id, caption = text)
    except Exception as _ex:
        print(_ex)


async def job(db_pool, chat_id, hours = 6):
    """Does all work"""
    an_array = await grasp_rows(db_pool, hours = hours)
    for key,v in an_array.items():
        read = await get_meta_data(key)
        await send_memes(read, chat_id, v)

async def send_memes_runner(chat_id, hours = 6):
    """Main function"""
    try:
        connection = await asyncpg.connect(host = db_host, user = db_user, password = db_password
        , database = db_db_name)
        await asyncio.sleep(0.3)
        task1 = asyncio.create_task(job(connection, chat_id, hours = hours))
        await asyncio.gather(task1)
    except Exception as _ex:
        print('Error:', _ex)
    finally:
        if connection:
            await connection.close()
            print('connection is closed')
#189382736

if __name__ == '__main__':
    t0 = time()   
    asyncio.run(send_memes_runner(189382736, 12))
    print(time() - t0)
    


# async def download_image(array):
#     """Download messages"""
#     filename = 'memeges/file-{}.jpeg'.format(int(time()* 1000))
#     with open(filename, 'wb') as file:
#         loop = asyncio.get_event_loop()
#         await loop.run_in_executor(None, file.write, array)
