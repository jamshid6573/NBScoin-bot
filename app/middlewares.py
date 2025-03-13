from aiogram import BaseMiddleware, Bot, Dispatcher, types
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from database import Database
from keyboards import user_menu, admin_menu
from functions.nbscoin_rpc import NBScoinRPC
import os
from dotenv import load_dotenv

load_dotenv()

db = Database()
nbscoin_rpc = NBScoinRPC()

ADMIN_ID=os.getenv("ADMIN_ID")


class CheckAdminAndBanMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем ID пользователя из события (например, сообщения)
        user_id = event.from_user.id if hasattr(event, "from_user") else None
        first_name = event.from_user.first_name if hasattr(event, "from_user") else None

        # Получаем данные пользователя из "БД"
        user_data = db.get_user(user_id)

        if user_data is None:
            adress = nbscoin_rpc.get_new_address()
            db.add_user(user_id, first_name, adress)
            user_data = db.get_user(user_id)

        

        # Проверка на бан
        if user_data[3] == 1:
            if isinstance(event, types.Message):
                await event.answer("Вы заблокированы и не можете использовать бота.")
            # Для других типов событий (например, callback) просто прерываем
            return  # Прерываем выполнение полностью

        # Проверка на админа
        if user_id == ADMIN_ID:
            data["menu"] = admin_menu  # Передаём админское меню
        else:
            data["menu"] = user_menu  # Передаём обычное меню

        # Передаём управление дальше
        return await handler(event, data)
    
class BanCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id if hasattr(event, "from_user") else None

        if not user_id:
            return

        user_data = db.get_user(user_id)

        if user_data[3] == 1:
            # Можно отправить уведомление, но для CallbackQuery лучше просто прервать
            await event.answer()  # Пустой ответ, чтобы завершить запрос
            return

        # Передаём управление дальше, если не забанен
        return await handler(event, data)
