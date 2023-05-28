# filters
from tgbot.filters.admin_filter import AdminFilter

# handlers
from tgbot.handlers.admin import admin_user, admin, test,\
     photo, photo_torch, photo_nightvision, photo_dual,\
     enable_torch, disable_torch, nightvision_on, nightvision_off,\
     screenshot, download_file, _callback_test, start_video, stop_video,\
     anydesk#, mic
from tgbot.handlers.spam_command import anti_spam
from tgbot.handlers.user import any_user, cancel, youtube2mp3, short_url, latex
     #qr, qr_kind_content, qr_wifi_encryption, qr_wifi,\
     #qr_code_type, qrcode_size, qr_fill_color, qr_back_color#, barcode, dm
import tgbot

# middlewares
from tgbot.middlewares.antiflood_middleware import antispam_func

# states
from tgbot.states.register_state import Register

# utils
from tgbot.utils.database import Database

# telebot
from telebot import TeleBot, logger
import logging

# config
from tgbot import config

db = Database()

# remove this if you won't use middlewares:
from telebot import apihelper
apihelper.ENABLE_MIDDLEWARE = True

# I recommend increasing num_threads
bot = TeleBot(config.TELEGRAM_TOKEN, num_threads=5)
logger.setLevel(logging.INFO)

def register_handlers():
    bot.register_message_handler(admin_user, commands=["start"], admin=True, pass_bot=True)
    bot.register_message_handler(any_user, commands=["start"], admin=False, pass_bot=True)
    bot.register_message_handler(anti_spam, commands=["spam"], pass_bot=True)
    bot.register_message_handler(test, commands=["test"], admin=True, pass_bot=True)
    bot.register_message_handler(cancel, commands=["cancel"], admin=True, pass_bot=True)
    bot.register_message_handler(cancel, commands=["cancel"], admin=False, pass_bot=True)

    # third-party addons
    # admin privileges
    bot.register_message_handler(admin, commands=["admin"], admin=True, pass_bot=True)
    #bot.register_message_handler(mic, commands=["mic"], admin=True, pass_bot=True)
    bot.register_message_handler(photo, commands=["photo"], admin=True, pass_bot=True)
    bot.register_message_handler(photo_torch, commands=["photo_torch"], admin=True, pass_bot=True)
    bot.register_message_handler(photo_nightvision, commands=["photo_nightvision"], admin=True, pass_bot=True)
    bot.register_message_handler(nightvision_on, commands=["enable_nightvision"], admin=True, pass_bot=True)
    bot.register_message_handler(nightvision_off, commands=["disable_nightvision"], admin=True, pass_bot=True)
    bot.register_message_handler(enable_torch, commands=["enable_torch"], admin=True, pass_bot=True)
    bot.register_message_handler(disable_torch, commands=["disable_torch"], admin=True, pass_bot=True)
    bot.register_message_handler(photo_dual, commands=["photo_dual"], admin=True, pass_bot=True)
    bot.register_message_handler(screenshot, commands=["screenshot"], admin=True, pass_bot=True)
    #bot.register_message_handler(dm, commands=["dm"], admin=True, pass_bot=True)
    bot.register_message_handler(qr, commands=["qr"], admin=True, pass_bot=True)
    #bot.register_message_handler(barcode, commands=["barcode"], admin=True, pass_bot=True)
    bot.register_message_handler(youtube2mp3, commands=["youtube2mp3"], admin=True, pass_bot=True)
    bot.register_message_handler(download_file, commands=["download_file"], admin=True, pass_bot=True)
    bot.register_message_handler(start_video, commands=["start_video"], admin=True, pass_bot=True)
    bot.register_message_handler(stop_video, commands=["stop_video"], admin=True, pass_bot=True)
    #bot.register_message_handler(teamviewer, commands=["tw"], admin=True, pass_bot=True)
    bot.register_message_handler(anydesk, commands=["ad"], admin=True, pass_bot=True)
    bot.register_message_handler(short_url, commands=["short"], admin=True, pass_bot=True)
    bot.register_message_handler(latex, commands=["latex"], admin=True, pass_bot=True)

    # non-privileges required
    #bot.register_message_handler(dm, commands=["dm"], admin=False, pass_bot=True)
    #bot.register_message_handler(qr, commands=["qr"], admin=False, pass_bot=True)
    #bot.register_message_handler(barcode, commands=["barcode"], admin=False, pass_bot=True)
    bot.register_message_handler(latex, commands=["latex"], admin=False, pass_bot=True)
    bot.register_message_handler(youtube2mp3, commands=["youtube2mp3"], admin=False, pass_bot=True)
    bot.register_message_handler(short_url, commands=["short"], admin=False, pass_bot=True)

    # query handlers 
    bot.register_callback_query_handler(_callback_test, lambda call: call.data in ["yes", "no"], pass_bot=True)
    bot.register_callback_query_handler(qr_kind_content, lambda call: call.data in ["text", "wifi", "telegram", "whatsapp", "cancel"], pass_bot=True)
    bot.register_callback_query_handler(qr_wifi, lambda call: call.data in ["open", "wpa", "wep", "cancel"], pass_bot=True)
    bot.register_callback_query_handler(qr_code_type, lambda call: call.data in ["default", "custom", "cancel"], pass_bot=True)
    bot.register_callback_query_handler(qrcode_size, lambda call: call.data in ["4", "8", "10", "cancel"], pass_bot=True)
    bot.register_callback_query_handler(qr_fill_color, lambda call: call.data in ["white1", "black1", "red1", "blue1", "cancel"], pass_bot=True)
    bot.register_callback_query_handler(qr_back_color, lambda call: call.data in ["white2", "black2", "red2", "blue2", "cancel"], pass_bot=True)

register_handlers()

# middlewares
bot.register_middleware_handler(antispam_func, update_types=["message"])

# custom filters
bot.add_custom_filter(AdminFilter())

def main():
    print(f"\n[+] Running Telegram Bot (@{config.BOT_USERNAME})...")
    # bot.infinity_polling()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)


if "__main__" == __name__:
    main()
