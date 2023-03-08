from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Ассортимент', callback_data='products')],
        [InlineKeyboardButton('Корзина', callback_data='cart')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_products_keyboard(products):
    inline_keyboard = [
        [InlineKeyboardButton(f'{product.get("attributes").get("name")}', callback_data=product.get('id'))]
        for product in products]
    inline_keyboard += [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_product_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('1 кг', callback_data=1),
            InlineKeyboardButton('5 кг', callback_data=5),
            InlineKeyboardButton('10 кг', callback_data=10),
        ],
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_cart_keyboard(products):
    inline_keyboard = [
        [InlineKeyboardButton(f'Удалить {product.get("name")}', callback_data=product.get('id'))]
        for product in products]
    inline_keyboard += [
        [InlineKeyboardButton('Оплатить', callback_data='pay')],
        [InlineKeyboardButton('В меню', callback_data='main')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_back_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup
