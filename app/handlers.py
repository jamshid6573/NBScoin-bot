from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, URLInputFile, InputFile, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_audio import SendAudio
from aiogram.utils.chat_action import ChatActionSender
import keyboards
from functions import NBScoinRPC
from database import Database
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


nbscoin_rpc = NBScoinRPC()
db = Database()

TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

rt = Router()

class TransactionState(StatesGroup):
    waiting_for_wallet = State()
    waiting_for_amount = State()
    waiting_for_confirmation = State()

class GetUserIdState(StatesGroup):
    user_id = State()

class GetUserIdState1(StatesGroup):
    user_id = State()

class GetTXIDState(StatesGroup):
    txid = State()


@rt.message(CommandStart())
async def start(message: Message, menu: InlineKeyboardMarkup):
    user = message.from_user
    await message.answer(f"👋 Привет! {user.first_name}! Добро пожаловать в NBScoin бот.\n Выберите действие:", reply_markup=menu)
    

@rt.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery):
    user_id = callback.from_user.id
    address = str(db.get_user(user_id)[2])
    balance = nbscoin_rpc.get_balance(account=address)
    await bot.send_message(callback.from_user.id, text=f"Баланс: {balance} NBS Coin")

@rt.callback_query(F.data == "upbalance")
async def up_balance(callback: CallbackQuery):
    await bot.send_message(callback.from_user.id, "Введите сумму пополнения:")



# Функция обработки транзакции (замени на свою)
async def process_transaction(wallet: str, amount: float):
    await asyncio.sleep(1)  # Имитируем выполнение (можно убрать)
    print(f"✅ Транзакция: {amount} на кошелёк {wallet}")


# Запуск диалога по кнопке
@rt.callback_query(F.data == "send_coins")
async def send_coins(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите адрес кошелька:")
    await state.set_state(TransactionState.waiting_for_wallet)
    await callback.answer()

# Получаем адрес
@rt.message(TransactionState.waiting_for_wallet)
async def get_wallet(message: Message, state: FSMContext):
    wallet = message.text.strip()
    await state.update_data(wallet=wallet)
    await message.answer("Введите сумму:")
    await state.set_state(TransactionState.waiting_for_amount)

# Получаем сумму
@rt.message(TransactionState.waiting_for_amount)
async def get_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введите корректную сумму (число больше 0)")
        return

    await state.update_data(amount=amount)
    data = await state.get_data()
    
    wallet = data["wallet"]

    await message.answer(f"Вы подтверждаете перевод {amount} NBS Coin на кошелёк:\n{wallet}", 
                        reply_markup=keyboards.confirm_keyboard)
    await state.set_state(TransactionState.waiting_for_confirmation)

# Подтверждение транзакции
@rt.callback_query(F.data == "confirm_payment")
async def confirm_transaction(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    address = data["wallet"]
    amount = data["amount"]

    await callback.message.edit_text("✅ Транзакция выполняется...")
    await process_transaction(wallet, amount)
    txid = nbscoin_rpc.send_to_address(address, amount)
    await callback.message.edit_text(f"✅ Транзакция успешно выполнена! TXID:\n{txid}")
    await state.clear()
    await callback.answer()

# Отмена транзакции
@rt.callback_query(F.data == "cancel_payment")
async def cancel_transaction(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Транзакция отменена.")
    await state.clear()
    await callback.answer()



@rt.callback_query(F.data == "get_coins")
async def get_coins(callback: CallbackQuery):
    user_id = callback.from_user.id
    adress = db.get_user(user_id=user_id)[2]
    await bot.send_message(user_id, f"Ваш адрес кошелька для получения:\n{adress}")

@rt.callback_query(F.data == "ban")
async def ban_user(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, 'Введите ID пользователя:')
    await state.set_state(GetUserIdState.user_id)
    await callback.answer()

@rt.message(GetUserIdState.user_id)
async def get_user_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        ban = db.ban_user(user_id)
        if ban:
            await message.answer(f"Пользователь с ID {user_id} успешно заблокирован.")
            await state.clear()
        else:
            await message.answer(f"Пользователь c ID {user_id} не найден.")
            await state.clear()
    except:
        await message.answer("ID Неккоректный")
        await state.clear()

@rt.callback_query(F.data == "unban")
async def unban_user(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, 'Введите ID пользователя:')
    await state.set_state(GetUserIdState1.user_id)
    await callback.answer()

@rt.message(GetUserIdState1.user_id)
async def get_user_id1(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        unban = db.unban_user(user_id)
        if unban:
            await message.answer(f"Пользователь с ID {user_id} успешно разблокирован.")
            await state.clear()
        else:
            await message.answer(f"Пользователь c ID {user_id} не найден.")
            await state.clear()
    except:
        await message.answer("ID Неккоректный")
        await state.clear()

@rt.callback_query(F.data == "withdraw")
async def withdraw(callback: CallbackQuery):
    await bot.send_message(callback.from_user.id, "Введите сумму вывода:")

@rt.callback_query(F.data == "p2p")
async def p2p(callback: CallbackQuery):
    await bot.send_message(callback.from_user.id, "В разработке! Скоро будет доступно.")

@rt.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await bot.send_message(callback.from_user.id, "Напишите ваш вопрос и наш специалист вам ответит!", reply_markup=keyboards.support_button)


@rt.callback_query(F.data == "check_transaction")
async def check_transaction(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, "Введите TXID Транзакции:")
    await state.set_state(GetTXIDState.txid)
    await callback.answer()

@rt.message(GetTXIDState.txid)
async def get_transaction_txid(message: Message, state: FSMContext):
    txid = message.text
    tx = nbscoin_rpc.get_transaction(txid)
    if tx:
        await message.answer(f"Статус транзакции: {tx['confirmations']} подтверждений")
        await state.clear()
    else:
        await message.answer("Транзакция не найдена")
        await state.clear()

@rt.callback_query(F.data == "get_transaction")
async def get_transactions(callback: CallbackQuery):
    txs = nbscoin_rpc.list_transactions()
    response = "\n".join([f"{tx['category']}: {tx['amount']} NBS ({tx['txid']})" for tx in txs]) if txs else "Нет транзакций"
    await bot.send_message(callback.from_user.id, response)
    await callback.answer()