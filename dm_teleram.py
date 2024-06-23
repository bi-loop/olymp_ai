import asyncio
import telegram
from telegram import Update

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telegram.Bot(token='6512036614:AAHAT909IhiSwHO8FdVS3UoY2eH5rJeNTlE')

# Replace 'USER_ID' with the user ID you want to send a message to
user_id = '1898221069'

async def send_message():
    await bot.send_message(chat_id=user_id, text="Please Try to Login Again")
    # await bot.send_message(chat_id=user_id,
    #                        text='Income      ₮1.80')

# Create an event loop and run the send_message coroutine
loop = asyncio.get_event_loop()
loop.run_until_complete(send_message())
