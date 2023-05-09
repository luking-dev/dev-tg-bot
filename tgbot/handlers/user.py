import os
import urllib.parse
from ..config import data, BASE_DIR
from telebot import TeleBot, logger
from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from addons import yt2mp3, qr as qrlib, datamatrix, bc, latex as tex
from barcode.writer import ImageWriter

def any_user(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    bot.send_message(message.chat.id, "Hello, user!")

def cancel(message: Message, bot: TeleBot, call=None):
    if call:
        bot.answer_callback_query(call.id, call.data)
    bot.clear_step_handler(message)
    bot.clear_reply_handlers(message)
    bot.send_message(message.chat.id, "Command canceled")

def youtube2mp3(message: Message, bot: TeleBot):
    markup = types.ForceReply(selective=False)
    bot.reply_to(message, "Send YouTube video URL to extract audio", reply_markup=markup)
    bot.register_next_step_handler(message, download_youtube_mp3, bot)

def download_youtube_mp3(message: Message, bot: TeleBot):
    url = message.text
    downloading = bot.send_message(message.chat.id, "Downloading audio. Please, wait a moment...", reply_to_message_id=message.id)
    downloaded_audio = yt2mp3.download(url)
    logger.info(f"Downloaded: {downloaded_audio['title']}")
    audio = os.path.join(BASE_DIR, f"{downloaded_audio['id']}.mp3")
    bot.delete_message(message.chat.id, downloading.message_id)
    bot.send_chat_action(message.chat.id, "upload_audio")
    bot.send_audio(message.chat.id, open(audio, "rb"), caption=downloaded_audio["title"], reply_to_message_id=message.id)
    os.remove(audio)

def dm(message: Message, bot: TeleBot):
    data["dm_id"] = message.id

    markup = types.ForceReply(selective=False)

    bot.send_message(message.chat.id, "Write your datamatrix data", reply_markup=markup, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, dm_data, bot)

def dm_data(message: Message, bot:TeleBot, app=None):
    global data
    data["dm_message"] = message.text

    dm_image = datamatrix.make_datamatrix(data["dm_message"])
    dm_path = os.path.join(BASE_DIR, dm_image)
    bot.send_chat_action(message.chat.id, "upload_photo")
    bot.send_photo(message.chat.id, open(dm_path, "rb"), caption=f"Datamatrix requested", reply_to_message_id=message.id)
    os.remove(dm_path)
    

def qr(message: Message, bot: TeleBot):
    data["qr_id"] = message.id

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Text", callback_data="text"),
               InlineKeyboardButton("Wi-Fi", callback_data="wifi"))
    markup.row(InlineKeyboardButton("Telegram", callback_data="telegram"),
               InlineKeyboardButton("WhatsApp", callback_data="whatsapp"))
    markup.row(InlineKeyboardButton("Cancel", callback_data="cancel"))

    bot.send_message(message.chat.id, "What kind of content will your QR code have?", reply_markup=markup, reply_to_message_id=message.id)

def qr_kind_content(call: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(call.id, call.data)

    data["qr_kind_content"] = call.data

    if call.data == "text":
        qr_text(call.message, bot)
    elif call.data == "wifi":
        qr_wifi_ssid(call.message, bot)
    elif call.data == "telegram":
        qr_telegram(call.message, bot)
    elif call.data == "whatsapp":
        qr_whatsapp_number(call.message, bot)
    elif call.data == "cancel":
        cancel(call.message, bot, call)

def qr_text(message: Message, bot: TeleBot):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Write your QR Code data", reply_markup=markup, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, qr_data, bot)

def qr_wifi_ssid(message: Message, bot: TeleBot):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Wi-Fi SSID (network name)", reply_markup=markup, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, qr_wifi_password, bot)

def qr_wifi_password(message: Message, bot: TeleBot):
    global data
    data["qr_wifi_ssid"] = message.text

    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Wi-Fi password", reply_markup=markup, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, qr_wifi_encryption, bot)

def qr_wifi_encryption(message: Message, bot: TeleBot):
    global data
    data["qr_wifi_password"] = message.text

    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Open", callback_data="open"),
               InlineKeyboardButton("WPA/WPA2", callback_data="wpa"),
               InlineKeyboardButton("WEP", callback_data="wep"))
    markup.row(InlineKeyboardButton("Cancel", callback_data="cancel"))

    bot.send_message(message.chat.id, "Wi-Fi encryption", reply_markup=markup, reply_to_message_id=message.id)

def qr_wifi(call: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(call.id, call.data)
    
    global data
    if call.data == "open":
        data["qr_wifi_encryption"] = ""
    elif call.data == "cancel":
        cancel(call.message, bot, call)
    else:
        data["qr_wifi_encryption"] = call.data
    
    bot.register_next_step_handler(call.message, qr_data, bot, "wifi")

def qr_wifi_last_step(call: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(call.id, call.data)
    

def qr_telegram(message: Message, bot: TeleBot):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Telegram username", reply_markup=markup, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, qr_data, bot, "telegram")

def qr_whatsapp_number(message: Message, bot: TeleBot):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "WhatsApp phone number\n\nPattern:\n<country><area><phone without '15'>", reply_markup=markup, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, qr_whatsapp_message, bot)

def qr_whatsapp_message(message: Message, bot: TeleBot):
    global data
    data["qr_whatsapp_number"] = message.text

    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "WhatsApp predefined message", reply_markup=markup, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, qr_data, bot, "whatsapp")

def qr_data(message: Message, bot:TeleBot, app=None):
    global data
    data["qr_message"] = message.text
    if app == "wifi":
        data["qr_message"] = "WIFI:S:{};T:{};P:{};;".format(data["qr_wifi_ssid"], data["qr_wifi_encryption"].upper(), data["qr_wifi_password"])
    elif app == "telegram":
        data["qr_message"] = "https://t.me/{}".format(data["qr_message"])
    elif app == "whatsapp":
        data["qr_message"] = "https://wa.me/{}?text={}&type=phone_number&app_absent=0".format(data["qr_whatsapp_number"], urllib.parse.quote(data["qr_message"]))
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Default", callback_data="default"),
               InlineKeyboardButton("Custom", callback_data="custom"))
    markup.row(InlineKeyboardButton("Cancel", callback_data="cancel"))
    bot.send_message(message.chat.id, "Select QR Code type", reply_markup=markup, reply_to_message_id=message.id)

def qr_code_type(call: CallbackQuery, bot:TeleBot):
    bot.answer_callback_query(call.id, call.data)
    
    global data
    data["qr_type"] = call.data

    if call.data == "default":
        generate_qrcode(call.message, bot, data["qr_message"])
    elif call.data == "custom":
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        markup.add(InlineKeyboardButton("Small", callback_data="4"),
                InlineKeyboardButton("Medium", callback_data="8"),
                InlineKeyboardButton("Large", callback_data="10"))
        markup.add(InlineKeyboardButton("Cancel", callback_data="cancel"))
        bot.send_message(call.message.chat.id, "Select size", reply_markup=markup, reply_to_message_id=call.message.id)
    elif call.data == "cancel":
        cancel(call.message, bot, call)

def qrcode_size(call: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(call.id, call.data)
    
    global data
    data["qr_size"] = int(call.data)

    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("White", callback_data="white1"),
               InlineKeyboardButton("Black", callback_data="black1"),
               InlineKeyboardButton("Red", callback_data="red1"),
               InlineKeyboardButton("Blue", callback_data="blue1"))
    markup.add(InlineKeyboardButton("Cancel", callback_data="cancel"))
    bot.send_message(call.message.chat.id, f"Select fill color", reply_markup=markup, reply_to_message_id=call.message.id)
    
def qr_fill_color(call: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(call.id, call.data)

    global data
    data["qr_fill_color"] = call.data

    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("White", callback_data="white2"),
               InlineKeyboardButton("Black", callback_data="black2"),
               InlineKeyboardButton("Red", callback_data="red2"),
               InlineKeyboardButton("Blue", callback_data="blue2"))
    markup.add(InlineKeyboardButton("Cancel", callback_data="cancel"))
    bot.send_message(call.message.chat.id, f"Select background color", reply_markup=markup, reply_to_message_id=call.message.id)

def qr_back_color(call: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(call.id, call.data)

    global data
    data["qr_back_color"] = call.data

    generate_qrcode(call.message, bot, data["qr_message"], box_size=data["qr_size"], fill_color=data["qr_fill_color"][:len(data["qr_fill_color"]) - 1], back_color=data["qr_back_color"][:len(data["qr_back_color"]) - 1])

def generate_qrcode(message: Message, bot: TeleBot, content=None, box_size=8, border=2, fill_color="black", back_color="white"):
    # qr_image = qrlib.make_qr(content, box_size=box_size, border=border, fill_color=fill_color, back_color=back_color)
    qr_image = qrlib.make_qr(content, box_size=box_size, border=border, fill_color=fill_color, back_color=back_color)
    qrcode = os.path.join(BASE_DIR, qr_image)
    bot.send_chat_action(message.chat.id, "upload_photo")
    bot.send_photo(message.chat.id, open(qrcode, "rb"), caption=f"{data['qr_type'].capitalize()} QR code requested", reply_to_message_id=message.id)
    os.remove(qrcode)

def barcode(message: Message, bot: TeleBot):
    data["bc_id"] = message.id

    markup = types.ForceReply(selective=False)

    bot.send_message(message.chat.id, "Write your 12-digits barcode data", reply_markup=markup, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, bc_data, bot)

def bc_data(message: Message, bot:TeleBot, app=None):
    global data
    data["bc_message"] = message.text

    bc_image = bc.make_barcode(data["bc_message"])
    bc_path = os.path.join(BASE_DIR, bc_image)
    bot.send_chat_action(message.chat.id, "upload_photo")
    bot.send_photo(message.chat.id, open(bc_path, "rb"), caption=f"Barcode requested", reply_to_message_id=message.id)
    os.remove(bc_path)

def latex(message: Message, bot:TeleBot, app=None):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "To get help, read %s" % "https://en.wikipedia.org/wiki/List_of_mathematical_symbols_by_subject", disable_web_page_preview=True)
    bot.reply_to(message, "Write your LaTeX formula", reply_markup=markup)
    bot.register_next_step_handler(message, latex_step, bot)

def latex_step(message: Message, bot:TeleBot, app=None):
    formula = message.text
    image = tex.make_formula(formula)
    bot.send_photo(message.chat.id, open(image, "rb"), reply_to_message_id=message.id)
    os.remove(image)

def short_url(message: Message, bot: TeleBot):
    import bitly_api

    BITLY_CLIENT_SECRET = os.getenv("BITLY_CLIENT_SECRET")
    connection = bitly_api.Connection(access_token=BITLY_CLIENT_SECRET)
    url = input()
    shorten_url = connection.shorten(url)
    bot.send_message(message.chat.id, shorten_url, reply_to_message_id=message.id)
