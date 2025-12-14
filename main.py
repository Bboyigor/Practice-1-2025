import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


TOKEN = "8354881331:AAFSkhmEjet4YjAtfPHFI_M8rJdKoCWfE4k"


print("=" * 60)
print("🤖 ТЕЛЕГРАМ БОТ - МАГАЗИН ТЕХНІКИ")
print("=" * 60)


# Ініціалізація бота (новий синтаксис для aiogram 3.7+)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# База даних (проста)
users_cart = {}


# ========== МЕНЮ ==========
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Каталог"), KeyboardButton(text="🛒 Кошик")],
            [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="ℹ️ Інфо")]
        ],
        resize_keyboard=True
    )


# ========== ОБРОБНИКИ ==========
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🏠 *Вітаємо в магазині техніки!*\n\n"
        "Оберіть опцію:",
        reply_markup=get_main_menu()
    )


@dp.message(F.text == "📦 Каталог")
async def catalog_cmd(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❄️ Холодильники")],
            [KeyboardButton(text="🧼 Пральні машини")],
            [KeyboardButton(text="🏠 На головну")]
        ],
        resize_keyboard=True
    )
    await message.answer("📦 *Каталог:*", reply_markup=keyboard)


@dp.message(F.text == "❄️ Холодильники")
async def fridges_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Samsung - 25,999 грн", callback_data="buy1")],
            [InlineKeyboardButton(text="LG - 32,500 грн", callback_data="buy2")]
        ]
    )
    await message.answer(
        "❄️ *Холодильники:*\n\n"
        "• Samsung RT38 - 25,999 грн\n"
        "• LG DoorCooling - 32,500 грн",
        reply_markup=keyboard
    )


@dp.message(F.text == "🛒 Кошик")
async def cart_cmd(message: types.Message):
    user_id = message.from_user.id
    if user_id in users_cart and users_cart[user_id]:
        items = "\n".join([f"• {item}" for item in users_cart[user_id]])
        await message.answer(f"🛒 *Ваш кошик:*\n\n{items}")
    else:
        await message.answer("🛒 Ваш кошик порожній")


@dp.message(F.text == "📞 Контакти")
async def contacts_cmd(message: types.Message):
    await message.answer(
        "📞 *Контакти:*\n\n"
        "📍 Київ, вул. Хрещатик, 1\n"
        "📱 +38 (044) 123-45-67\n"
        "🕒 9:00-20:00"
    )


@dp.message(F.text == "ℹ️ Інфо")
async def info_cmd(message: types.Message):
    await message.answer(
        "🏪 *Про нас:*\n\n"
        "Магазин якісної техніки\n"
        "✅ Гарантія 2 роки\n"
        "✅ Доставка по Україні"
    )


@dp.message(F.text == "🏠 На головну")
async def home_cmd(message: types.Message):
    await start_cmd(message)


# ========== ОБРОБКА ПОКУПОК ==========
@dp.callback_query(F.data.startswith("buy"))
async def buy_product(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    products = {
        "buy1": "Холодильник Samsung",
        "buy2": "Холодильник LG"
    }

    product_name = products.get(callback.data, "Товар")

    if user_id not in users_cart:
        users_cart[user_id] = []

    users_cart[user_id].append(product_name)

    await callback.answer(f"✅ {product_name} додано!")
    await callback.message.answer(f"🎉 {product_name} додано до кошика!")


# ========== ЗАПУСК ==========
async def main():
    print("\n" + "=" * 50)
    print("✅ БОТ ПРАЦЮЄ!")
    print("📱 Знайдіть бота в Telegram")
    print("👋 Надішліть /start")
    print("=" * 50)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Помилка: {e}")


if __name__ == "__main__":
    asyncio.run(main())