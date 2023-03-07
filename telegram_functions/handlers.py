from textwrap import dedent

from .keyboards import (
    main_menu,
    products_menu,
    product_menu,
    cart_menu,
)


def send_main_menu(context, chat_id, message_id, message=None):
    message_text = 'Добро пожаловать в самый рыбный магазин!'

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=main_menu()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )



def send_products_menu(context, chat_id, message_id):
    message_text = 'Наш ассортимент'
    products = [{'id': 'name'}]

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=products_menu(products)
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_product_menu(context, chat_id, message_id, product):
    message_text = 'Инфо о продукте'
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=product_menu()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_cart_menu(context, chat_id, message_id):
    message_text = 'Блаблабла корзина'
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=cart_menu()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def start(update, context):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    send_main_menu(context, chat_id, message_id)

    return 'MAIN_MENU'


def main_menu_handler(update, context):
    query = update.callback_query
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    if query.data == 'products':
        send_products_menu(context, chat_id, message_id)
        return 'PRODUCTS'
    if query.data == 'cart':
        send_cart_menu(context, chat_id, message_id)
        return 'CART'


def products_handler(update, context):
    query = update.callback_query
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    if query.data == 'back':
        send_main_menu(context, chat_id, message_id)
        return 'MAIN_MENU'
    else:
        context.user_data['product'] = query.data
        send_product_menu(context, chat_id, message_id)
        return 'PRODUCT'




def product_handler(update, context):
    query = update.callback_query
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    product_id = context.user_data.pop('product')

    if query.data.isdigit():
        #TODO to dooo
        return 'PRODUCT'
    if query.data == 'back':
        send_products_menu(context, chat_id, message_id)
        return 'PRODUCTS'


def cart_handler(update, context):
    query = update.callback_query
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    if query.data == 'main':
        send_main_menu(context, chat_id, message_id)
        return 'MAIN_MENU'
    if query.data == 'pay':
        message_text = 'Введите ваш email и наш менеджер свяжется с Вами'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=cart_menu()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'GET_CONTACT'


def contact_handler(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    else:
        return

    if query and query.data == 'back':
        send_cart_menu(context, chat_id, message_id)
        return 'CART'
    else:
        user_email = update.message.text

        send_main_menu(context, chat_id, message_id)
        return 'MAIN_MENU'