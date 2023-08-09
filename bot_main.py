import asyncio
import logging
import csv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import MakeMassage

TOKEN = '6348195837:AAE5vKlNf5lHeagocjLvpz3W974rarR_p-s'

def getIDs():
    with open('data.csv', newline='') as csvf:
        reader = csv.DictReader(csvf)

dp = Dispatcher()
bot = Bot(TOKEN)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    
    dp.include_router(MakeMassage.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())