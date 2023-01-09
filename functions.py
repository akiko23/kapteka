import requests
from aiogram import types
from aiogram.dispatcher.filters import Text

import markups
from config import db, bot, forbidden_chars, dp


def convert_currencies(first_currency='USD', quantity=1, second_currency='RUB'):
    url = f"https://free.currconv.com/api/v7/convert?apiKey=cd2ff852330c08894153&q={first_currency}_{second_currency}&compact=ultra"
    response = requests.get(url).json()

    # return Decimal(response[f"{first_currency}_{second_currency}"] * quantity)
    return round(response[f"{first_currency}_{second_currency}"] * quantity, 3)


async def watch_all_products_process(current_num, user_id, category):
    current_num.append(0)
    all_products = db.get_products_by_category(category)

    if len(all_products) > 0:
        uid, photo_id, name, description, price = all_products[current_num[0]]
        await bot.send_photo(user_id, photo_id,
                             caption=f"Название: {name}\nОписание: {description}\nЦена: {price} грн",
                             reply_markup=markups.set_menu_on_watching(all_ads_len=len(all_products),
                                                                       current_num=current_num[0], category=category))

        @dp.callback_query_handler(Text(startswith='watch'))
        async def watch_logic(callback: types.CallbackQuery):
            act = callback.data.split('-')[1]
            # random_num = random.randint(1, len(db.get_not_user_advertisements_data(id)) - 1)

            current_num[0] += 1 if act == 'next' else -1

            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await watch_all_products_process(current_num, callback.from_user.id, category=category)
    else:
        await bot.send_message(user_id, 'Пока что нет товаров этой категории',
                               reply_markup=markups.back_to_main_menu)


def check_valid_msg(msg):
    try:
        return True if not any([s in msg.text for s in forbidden_chars]) else False
    except:
        return False


clear_value_list = []
