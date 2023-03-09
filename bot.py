from environs import Env
from functools import partial
import logging
import redis
from telegram.ext import (
    Filters,
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
)
from moltin import Moltin
from telegram_bot.handlers import (
    start,
    main_menu_handler,
    products_handler,
    product_handler,
    cart_handler,
    contact_handler,
)

logger = logging.getLogger(__name__)


def send_error(state, error):
    logger.warning(f'State {state} caused error {error}')


def handle_users_reply(update, context, db, moltin):
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    elif update.pre_checkout_query:
        user_reply = None
        chat_id = update.pre_checkout_query.from_user.id
    else:
        return

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id)

    states_functions = {
        'START': start,
        'MAIN_MENU': partial(main_menu_handler, moltin=moltin),
        'PRODUCTS': partial(products_handler, moltin=moltin),
        'PRODUCT': partial(product_handler, moltin=moltin),
        'CART': partial(cart_handler, moltin=moltin),
        'GET_CONTACT': partial(contact_handler, moltin=moltin),
    }

    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        db.set(chat_id, next_state)
    except Exception as err:
        send_error(user_state, err)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )
    env = Env()
    env.read_env()
    moltin_id = env('MOLTIN_CLIENT_ID')
    moltin_secret = env('MOLTIN_CLIENT_SECRET')
    tg_token = env('TELEGRAM_TOKEN')

    db = redis.Redis(
        host=env('REDIS_HOST'),
        port=env('REDIS_PORT'),
        password=env('REDIS_PASSWORD'),
        decode_responses=True,
    )
    moltin = Moltin(moltin_id, moltin_secret)

    connected_db_handler = partial(handle_users_reply, db=db, moltin=moltin)

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(connected_db_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, connected_db_handler))
    dispatcher.add_handler(CommandHandler('start', connected_db_handler))

    updater.start_polling()
    updater.idle()
