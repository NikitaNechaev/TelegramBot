from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
import csv
from collections import defaultdict
import bot_main
import numpy as np

router = Router()

with open('data.csv', newline='') as f:
    contacts_data = list(csv.reader(f))
del contacts_data[0]
available_contacts = []
for i in range(len(contacts_data)):
    available_contacts.append(contacts_data[i][0])
print(f"available_contacts: {available_contacts}")

class MakeMessage(StatesGroup):
    choose_contact = State()
    choose_msg = State()

@router.message(Command("start"))
async def reg(msg:Message, state:FSMContext):
    await state.clear()
    await msg.answer(
        text="Registration"
    )
    with open('data.csv', 'a', newline='') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=['botid', 'tgid', 'name'])
        print(msg.from_user.id, msg.from_user.username, msg.from_user.first_name)
        if str(msg.from_user.id) not in available_contacts:
            writer.writerow({'botid': msg.from_user.id, 'tgid': msg.from_user.username, 'name': msg.from_user.first_name})
            print("new user registered")   
        else:
            print("already registered")     

@router.message(Command("mkmsg"))
async def mkmgs(msg: Message, state: FSMContext):
    await msg.answer(
        text=f"Choose contact (bot_id) from the list: {contacts_data}"
        )
    await state.set_state(MakeMessage.choose_contact)

contactid = None

@router.message(
    MakeMessage.choose_contact,
    F.text.in_(available_contacts))
async def contact_choosen(msg: Message, state:FSMContext):
    await state.update_data(targetContact=msg.text)
    await msg.answer(text=f"contact choosen - {msg.text}")
    contactid = msg.text
    await state.set_state(MakeMessage.choose_msg)

@router.message(MakeMessage.choose_contact)
async def contact_choosen_incor(msg: Message):
    await msg.answer(text = "Incorrect contact")

@router.message(MakeMessage.choose_msg)
async def msg_choosen(msg: Message, state:FSMContext):
    udata = await state.get_data()
    await msg.answer(
        text=f"Message - {msg.text} to {udata['targetContact']}")
    await bot_main.bot.send_message(377702618, udata['targetContact'])
    print(type(msg.from_user.id))
    await state.clear()
