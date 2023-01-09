from aiogram.dispatcher.filters.state import StatesGroup, State


class Product(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

    add_category = State()
    support_dialog = State()

    class AdvertisementActions(StatesGroup):
        class SearchStates(StatesGroup):
            get_value = State()
            check_value = State()
            processing_value = State()

        del_action = State()
        change_param = State()
