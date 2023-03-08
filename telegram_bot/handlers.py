from textwrap import dedent

from .keyboards import (
    get_main_menu_keyboard,
    get_products_keyboard,
    get_product_keyboard,
    get_cart_keyboard,
    get_back_keyboard
)

def format_product_to_text(product):
    name = product.get('name')
    description = product.get('description')
    quantity = product.get('quantity')
    price = product.get('meta').get('display_price').get('without_tax').get('unit').get('formatted')
    value = product.get('meta').get('display_price').get('without_tax').get('value').get('formatted')
    product_text = f'''{name}\n{description}\n{price} per kg\n{quantity} kg in cart for {value}\n\n'''
    return product_text


def send_main_menu(context, chat_id, message_id):
    message_text = 'Добро пожаловать в самый рыбный магазин!'

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_main_menu_keyboard()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_products_menu(context, chat_id, message_id, products):
    message_text = 'Наш ассортимент'
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_products_keyboard(products)
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_product_menu(context, chat_id, message_id, product, image_url):
    product_id = product.get('id')
    name = product.get('attributes').get('name')
    description = product.get('attributes').get('description')
    cost = product.get('meta').get('display_price').get('without_tax').get('formatted')

    message_text = f'''{name}\nОписание:\n{description}\nСтоимость: {cost}'''
    context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=dedent(message_text),
        reply_markup=get_product_keyboard()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )
    context.user_data['product_id'] = product_id


def send_cart_menu(context, chat_id, message_id, products):
    message_text = ''
    for product in products:
        message_text += format_product_to_text(product)

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_cart_keyboard(products)
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


def main_menu_handler(update, context, moltin):
    query = update.callback_query
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    if query.data == 'products':
        products = moltin.get_products()
        send_products_menu(context, chat_id, message_id, products)
        return 'PRODUCTS'
    if query.data == 'cart':
        products = moltin.get_cart_items(chat_id)
        send_cart_menu(context, chat_id, message_id, products)
        return 'CART'


def products_handler(update, context, moltin):
    query = update.callback_query
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    if query.data == 'back':
        send_main_menu(context, chat_id, message_id)
        return 'MAIN_MENU'
    else:
        product_id = query.data
        product = moltin.get_product(product_id)
        image_id = product.get('relationships').get('main_image').get('data').get('id')
        image_url = moltin.get_image_url(image_id)
        send_product_menu(context, chat_id, message_id, product, image_url)
        return 'PRODUCT'


def product_handler(update, context, moltin):
    query = update.callback_query
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    product_id = context.user_data.get('product_id')

    if query.data.isdigit():
        quantity = query.data
        product = moltin.get_product(product_id)
        moltin.add_product_to_cart(chat_id, product, quantity)
        return 'PRODUCT'
    if query.data == 'back':
        context.user_data.pop('product_id')
        products = moltin.get_products()
        send_products_menu(context, chat_id, message_id, products)
        return 'PRODUCTS'


def cart_handler(update, context, moltin):
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
            reply_markup=get_back_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'GET_CONTACT'
    else:
        product_id = query.data
        moltin.delete_item(chat_id, product_id)
        products = moltin.get_cart_items(chat_id)
        send_cart_menu(context, chat_id, message_id, products)
        return 'CART'


def contact_handler(update, context, moltin):
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
        products = moltin.get_cart_items(chat_id)
        send_cart_menu(context, chat_id, message_id, products)
        return 'CART'
    else:
        customer_email = update.message.text
        customer_name = update.message.chat.username
        moltin.create_customer(customer_name, customer_email)
        send_main_menu(context, chat_id, message_id)
        return 'MAIN_MENU'
