from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link

from markups import product_menu
from functions import *
from states import Product

param_to_change = []
current_num = [0]


async def process_ref_args(user_id: int, inviter_id):
    if inviter_id != '':
        try:
            inviter_id = int(inviter_id)
        except Exception:
            return
        if (inviter_id != user_id) and not (str(user_id) in db.get_invited_users(inviter_id)) and not (
                db.user_exists(user_id)):
            db.add_user(user_id)

            db.set_inviter_id(user_id=user_id, inviter_id=inviter_id)
            db.update_invited_users(user_id, inviter_id)


@dp.message_handler(commands=['start'])
async def reply_menu(msg: types.Message):
    print(msg.from_user.id)
    args = msg.get_args()
    await process_ref_args(user_id=msg.from_user.id, inviter_id=args)

    db.add_user(msg.from_user.id) if not db.user_exists(msg.from_user.id) else None
    await bot.send_message(msg.from_user.id, "Test", reply_markup=markups.main_keyb)


@dp.callback_query_handler(Text('break_load_process'), state=Product.all_states)
async def break_load(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await state.finish()
    await bot.send_message(call.from_user.id, 'Вы отменили процесс❌',
                           reply_markup=markups.back_to_main_menu)

    db.delete_advertisement(call.from_user.id, db.get_last_id())


@dp.callback_query_handler(Text('break_change_process'), state=Product.AdvertisementActions.all_states)
async def break_load(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await state.finish()
    await bot.send_message(call.from_user.id, 'Вы отменили процесс изменения❌'
    if state == Product.AdvertisementActions.change_param
    else 'Вы отменили действие❌')


@dp.callback_query_handler(Text("watch_categories"))
async def watch_categories(call: types.CallbackQuery):
    keyb = markups.get_category_keyb(call.from_user.id)
    await call.message.edit_text("Здесь представлены категории товаров", reply_markup=keyb)


@dp.callback_query_handler(Text("ref"))
async def ref_actions(call: types.CallbackQuery):
    await call.message.edit_text(
        f"Пригласите своих друзей в бота по реферальной ссылке и получайте процент с их покупок!\n"
        f"Ваша реферальная ссылка:\n"
        f"`{await get_start_link(payload=call.from_user.id)}`\n\n"
        f"Пользователей приглашено: {len(db.get_invited_users(call.from_user.id).split())}\n"
        f"Текущий процент с покупок: {db.get_ref_percent()}", parse_mode="MARKDOWN",
        reply_markup=markups.back_to_main_menu)


@dp.callback_query_handler(lambda x: x.data.startswith("cat"))
async def get_category_products(call: types.CallbackQuery):
    category = call.data.split("-")[1]

    if call.from_user.id in [137506556, 5132067462]:
        await call.message.edit_text("Выберите, что хотите сделать", reply_markup=product_menu(category))
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await watch_all_products_process(current_num=current_num, user_id=call.from_user.id, category=category)


@dp.callback_query_handler(Text("back-to_advertisement_menu"))
async def back_to_product_menu(call: types.CallbackQuery):
    try:
        await call.message.edit_text("Test", reply_markup=markups.main_keyb)
    except:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, "Test", reply_markup=markups.main_keyb)


@dp.callback_query_handler(Text(startswith='product'))
async def actions_with_products(call: types.CallbackQuery):
    action, category = call.data.split('_')[1:]

    if action == 'add':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id, 'Отправьте фото товара',
                               reply_markup=markups.break_load_process_keyboard)

        db.create_product(category)
        await Product.photo.set()

    elif action == 'watchall':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await watch_all_products_process(current_num=current_num, user_id=call.from_user.id, category=category)


@dp.callback_query_handler(Text('add_category'))
async def add_category(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, "Введите название категории",
                           reply_markup=markups.break_load_process_keyboard)

    await Product.add_category.set()


@dp.message_handler(content_types=['text'], state=Product.add_category)
async def add_category(msg: types.Message, state: FSMContext):
    categories = db.get_all_categories()
    await bot.delete_message(msg.from_user.id, msg.message_id - 1)

    if not msg.text in categories:
        db.add_category(msg.text)
        await bot.send_message(msg.from_user.id, f"Категория {msg.text} успешно добавлена",
                               reply_markup=markups.back_to_main_menu)

        await state.finish()
    else:
        await bot.send_message(msg.from_user.id, "Такая категория уже существует",
                               reply_markup=markups.break_load_process_keyboard)


@dp.callback_query_handler(Text("support"))
async def support(call: types.CallbackQuery):
    await call.message.edit_text(text="Если вас что то интересует или возникли какие то проблемы, то нажмите \"Начать "
                                      "диалог\" и опишите вашу проблему", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать диалог", callback_data="start_dialog_with_support")],
            [InlineKeyboardButton(text="В главное меню", callback_data="back-to_advertisement_menu")]
        ]
    ))


@dp.callback_query_handler(Text("start_dialog_with_support"))
async def start_dialog_handler(call: types.CallbackQuery):
    await call.message.edit_text("Отправьте сюда вашу проблему")
    await Product.support_dialog.set()


@dp.message_handler(content_types=['text'], state=Product.support_dialog)
async def get_user_problem(msg: types.Message, state: FSMContext):
    if msg.from_user.id == 818525681:
        print(await state.get_data())
        user_id = (await state.get_data())["user"]
        await bot.send_message(user_id, msg.text)
    else:
        await state.set_data({"user": msg.from_user.id, "problem": msg.text})
        if dict(await state.get_data()).get("problem_isSended") is None:
            dict(await state.get_data())["problem_isSended"] = True
            await bot.send_message(818525681, f"У юзера @{msg.from_user.username} проблема:\n"
                                              f"{msg.text}", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Начать диалог", callback_data="start_dialog_with_user")]
                ]
            ))
        else:
            await bot.send_message(818525681, f"{msg.text}")


@dp.callback_query_handler(Text("start_dialog_with_user"))
async def start_dialog_with_user(call: types.CallbackQuery):
    await call.message.edit_text("Вы начали диалог")
    await Product.support_dialog.set()


@dp.message_handler(content_types=['photo'], state=Product.photo)
async def set_product_photo(message: types.Message):
    photo_id = message.photo[0].file_id
    user_id = message.from_user.id

    db.set_something('photo_id', photo_id)

    await bot.send_message(user_id, "Теперь введите название", reply_markup=markups.break_load_process_keyboard)
    await Product.name.set()


@dp.message_handler(content_types=['text'], state=Product.name)
async def set_product_name(message: types.Message, state: FSMContext):
    incorrect_statement = f'Запрещено использовать {", ".join([f"""{s}""" for s in forbidden_chars])}\nЗагрузка товара не удалась❌',

    if check_valid_msg(message):
        await bot.send_message(message.from_user.id, "Теперь добавьте описание",
                               reply_markup=markups.break_load_process_keyboard)
        db.set_something('name', message.text)

        await Product.description.set()
    else:
        await bot.send_message(message.from_user.id, incorrect_statement)
        db.delete_product()

        await state.finish()


@dp.message_handler(content_types=['text'], state=Product.description)
async def set_product_description(message: types.Message):
    db.set_something('description', message.text)
    await bot.send_message(message.from_user.id, 'Введите цену(в грн)',
                           reply_markup=markups.break_load_process_keyboard)
    await Product.price.set()


@dp.message_handler(content_types=['text'], state=Product.price)
async def set_product_price(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.set_something('price', int(message.text))
        last_product = db.get_all_products_data()[-1]

        id, photo_id, name, description, price = last_product
        await bot.send_photo(user_id, photo_id,
                             caption=f"Ваш товар успешно сохранен✅\n"
                                     f"\nУникальный номер: {id}"
                                     f"\nНазвание: {name}"
                                     f"\nОписание: {description}"
                                     f"\nЦена: {price} грн",
                             reply_markup=markups.back_to_main_menu)
        await state.finish()
    except ValueError:
        await bot.send_message(user_id, 'Цена не может включать в себя буквы!',
                               reply_markup=markups.break_load_process_keyboard)


@dp.message_handler(content_types=['text'])
async def get_text_from_user(msg: types.Message):
    try:
        first_currency = msg.text.split(' ')[0].split('_')[1].upper()
        quantity = int(msg.text.split(' ')[0].split('_')[0])
        second_currency = msg.text.split(' ')[1].upper()

        await bot.send_message(msg.from_user.id,
                               f"{quantity} {first_currency} это {convert_currencies(first_currency, quantity, second_currency)} {second_currency}")

    except Exception:
        await bot.send_message(msg.from_user.id, 'Я не понимаю, что это значит')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
