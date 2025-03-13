from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


user_menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            # InlineKeyboardButton(text="💰Баланс", callback_data="balance"),
            InlineKeyboardButton(text="🏦Кошелек", callback_data="wallet"),
            InlineKeyboardButton(text="💰Пополнить", callback_data="upbalance")
        ],
        [
            InlineKeyboardButton(text="✉️Отправить", callback_data="send_coins"),
            InlineKeyboardButton(text="📥Получить NBSCOIN", callback_data="get_coins")
        ],
        [
            InlineKeyboardButton(text="💵Вывести деньги", callback_data="withdraw"),
            InlineKeyboardButton(text="🔻P2P Торговли", callback_data="p2p")
        ],
        [
            InlineKeyboardButton(text="📋Получить транзакции", callback_data="get_transaction"),
            InlineKeyboardButton(text="🔍Проверить транзакцию", callback_data="check_transaction")
        ],
        [
            InlineKeyboardButton(text="🔉Тех. Поддержка", callback_data="support"),
        ]
])


admin_menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            # InlineKeyboardButton(text="💰Баланс", callback_data="balance"),
            InlineKeyboardButton(text="🏦Кошелек", callback_data="wallet"),
            InlineKeyboardButton(text="💰Пополнить", callback_data="upbalance")
        ],
        [
            InlineKeyboardButton(text="✉️Отправить", callback_data="send_coins"),
            InlineKeyboardButton(text="📥Получить NBSCOIN", callback_data="get_coins")
        ],
        [
            InlineKeyboardButton(text="💵Вывести деньги", callback_data="withdraw"),
            InlineKeyboardButton(text="🔻P2P Торговли", callback_data="p2p")
        ],
        [
            InlineKeyboardButton(text="📋Получить транзакции", callback_data="get_transaction"),
            InlineKeyboardButton(text="🔍Проверить транзакцию", callback_data="check_transaction")
        ],
        [
            InlineKeyboardButton(text="🔉Тех. Поддержка", callback_data="support"),
        ],
        [
            InlineKeyboardButton(text="🔓Разблокировать пользователя", callback_data="unban"),
            InlineKeyboardButton(text="🔒Заблокировать пользователя", callback_data="ban")
        ],
])

 # Инлайн-кнопки подтверждения
confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_payment")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_payment")]
    ]
)

support_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Написать", url="https://t.me/UzbElegand")]
    ]
)


