# FishShop
 
Project is a chat_bot for selling fishes using [ElasticPath](https://www.elasticpath.com/) 
for products management

### `.env` variables

Before run project you need to create `.env` file and add some variables here.

 1. Motlin variables - your application keys from Elasticpath project
 2. Redis - your redis database credentials from [Redis](https://redis.io/)
 3. Telegram - bot-token, write [BotFather](https://t.me/BotFather) to get it

```commandline
MOLTIN_CLIENT_ID=
MOLTIN_CLIENT_SECRET=

REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=

TELEGRAM_TOKEN=
```

### install requirements
Need to install project using libraries

```commandline
pip install -r requirements.txt
```

### run bot

After creating `.env` and appointing variables you should to run bot by next command:

```commandline
python3 bot.py
```