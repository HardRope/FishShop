from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Ассортимент', callback_data='products')],
        [InlineKeyboardButton('Корзина', callback_data='cart')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def products_menu(products):
    inline_keyboard = [
        [InlineKeyboardButton(f'{product.get("attributes").get("name")}', callback_data=product.get('id'))]
        for product in products]
    inline_keyboard += [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def product_menu():
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


def cart_menu(products):
    inline_keyboard = [
        [InlineKeyboardButton(f'Удалить {product.get("name")}', callback_data=product.get('id'))]
        for product in products]
    inline_keyboard += [
        [InlineKeyboardButton('Оплатить', callback_data='pay')],
        [InlineKeyboardButton('В меню', callback_data='main')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def back_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup
