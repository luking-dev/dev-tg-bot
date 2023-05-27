from telebot import TeleBot, logger
from telebot import types
from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from addons import cam, mic as miclib
from .. import config
from ..config import data, BASE_DIR, MULTIMEDIA_DIR
import os
import subprocess
import time
import inspect

def admin_user(message: Message, bot: TeleBot):
    """Says if you are admin"""

    bot.send_message(message.chat.id, "Hello, admin!")

def send_alert(text, bot: TeleBot, photo=None):
    """Sends an alert to defined channel"""

    channel_id = f"-100{config.ALERTS_CHANNEL}"

    if photo:
        bot.send_chat_action(channel_id, "upload_photo")
        bot.send_photo(channel_id, open(photo, "rb"), caption=text)
    else:
        bot.send_message(channel_id, text)

def test(message: Message, bot: TeleBot):
    """Tests some feature under development"""

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="yes"),
                InlineKeyboardButton("No", callback_data="no"))
    bot.send_message(message.chat.id, "Select an option:", reply_markup=markup)

def _callback_test(call: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(call.id, call.data)
    bot.send_message(call.message.chat.id, call.data, reply_to_message_id=call.message.id)

def photo(message: Message, bot: TeleBot):
    """Takes an instant photo from webcam"""

    photo = cam.photo()
    bot.send_chat_action(message.chat.id, "upload_photo")
    bot.send_photo(message.chat.id, open(photo, "rb"), caption="Now in living room", reply_to_message_id=message.id)
    os.remove(photo)

def photo_torch(message: Message, bot: TeleBot):
    """Enables torch and takes a photo"""

    cam.torch(True)
    time.sleep(1)
    photo = cam.photo()
    cam.torch(False)
    bot.send_chat_action(message.chat.id, "upload_photo")
    bot.send_photo(message.chat.id, open(photo, "rb"), caption="Now in living room with torch enabled", reply_to_message_id=message.id)
    os.remove(photo)

def photo_nightvision(message: Message, bot: TeleBot):
    """Takes a photo with nightvision"""

    cam.nightvision(True)
    time.sleep(1)
    photo = cam.photo()
    cam.nightvision(False)
    bot.send_chat_action(message.chat.id, "upload_photo")
    bot.send_photo(message.chat.id, open(photo, "rb"), caption="Now in living room with nightvision enabled", reply_to_message_id=message.id)
    os.remove(photo)

def enable_torch(message: Message, bot: TeleBot):
    """Turns torch on"""
    
    cam.torch(True)
    bot.reply_to(message, "Torch enabled")

def disable_torch(message: Message, bot: TeleBot):
    """Turns torch off"""

    cam.torch(False)
    bot.reply_to(message, "Torch disabled")

def nightvision_on(message: Message, bot: TeleBot):
    """Turns nightvision on"""

    cam.nightvision(True)
    bot.reply_to(message, "Nightvision enabled")

def nightvision_off(message: Message, bot: TeleBot):
    """Turns nightvision off"""

    cam.nightvision(False)
    bot.reply_to(message, "Nightvision disabled")

def photo_dual(message: Message, bot: TeleBot):
    """Takes a photo with and without nightvision"""

    photo(message)
    photo_nightvision(message)

def start_video(message: Message, bot: TeleBot):
    """Starts video recording"""

    cam.record_video(True)
    bot.reply_to(message, "Recording video...")

def stop_video(message: Message, bot: TeleBot):
    """Stops video recording"""

    cam.record_video(False)
    bot.reply_to(message, "Video record stopped")

def mic(message: Message, bot: TeleBot):
    """Record voice from microphone"""
    
    data["voice_message"] = message.id
    markup = types.ForceReply(selective=False)
    bot.reply_to(message, "How long want you to record? (default: 5)", reply_markup=markup)
    bot.register_next_step_handler(message, _select_unit, bot)

def _select_unit(message: Message, bot: TeleBot):
    global data
    data["mic_long"] = message.text
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("Seconds", callback_data="seconds"),
                InlineKeyboardButton("Minutes", callback_data="minutes"),
                InlineKeyboardButton("Hours", callback_data="hours"),
                InlineKeyboardButton("Cancel", callback_data="cancel"))
    bot.send_message(message.chat.id, "Which unit want to you use?", reply_markup=markup)
    bot.register_next_step_handler(message, _select_mic_record_time, bot)

def _select_mic_record_time(message: Message, bot: TeleBot):
    global data
    callback = data["callback"]
    unit = data["units"][callback]["text"]
    long = float(data["mic_long"])
    if long > 1.0:
        unit += "s"

    bot.send_message(message.chat.id, f"You selected {long} {unit}")
    bot.send_chat_action(message.chat.id, "record_audio")
    record_name = miclib.record(long=long)
    voice = os.path.join(BASE_DIR, record_name)
    bot.send_chat_action(message.chat.id, "upload_audio")
    bot.send_voice(message.chat.id, open(voice, "rb"), reply_to_message_id=data["voice_message"])

    os.remove(voice)

def screenshot(message: Message, bot: TeleBot):
    """Takes a screenshot"""

    pyautogui.screenshot("screenshot.png")
    bot.send_chat_action(message.chat.id, "upload_photo")
    bot.send_photo(message.chat.id, open("screenshot.png", "rb"), caption="Screenshot", reply_to_message_id=message.id)
    os.remove("screenshot.png")

def download_file(message: Message, bot: TeleBot):
    """Downloads a received file"""

    bot.send_message(message.chat.id, "Send me a message attaching a file")        
    bot.register_next_step_handler(message, _waiting_attach, bot)

def _waiting_attach(message: Message, bot: TeleBot):
    if message.content_type in ["photo", "audio", "document", "video", "video_note", "voice", "contact"]:
        try:
            if message.content_type == "photo":
                file_id = message.__getattribute__(message.content_type)[-1].file_id
            else:
                file_id = message.__getattribute__(message.content_type).file_id

            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            folder, file_name = file_info.file_path.split("/")
            if not os.path.exists(os.path.join(MULTIMEDIA_DIR, folder)):
                os.makedirs(os.path.join(MULTIMEDIA_DIR, folder))

            multimedia_file = os.path.join(MULTIMEDIA_DIR, folder, file_name)

            with open(multimedia_file, "wb") as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, "Multimedia downloaded succesfully!", reply_to_message_id=message.id)

        except Exception as error:
            logger.error(error)
            bot.send_message(message.chat.id, f"An error has ocurred:\n{error}", reply_to_message_id=message.id)
    else:
        logger.error("This content are not supported")
        bot.send_message(message.chat.id, f"This content are not supported", reply_to_message_id=message.id)

def anydesk(message: Message, bot: TeleBot):
    """Executes AnyDesk to remote administrate PC"""

    subprocess.Popen("C:\Program Files\AnyDesk\AnyDesk.exe")
    
    bot.send_message(message.chat.id, "AnyDesk has executed", reply_to_message_id=message.id)

def admin(message: Message, bot: TeleBot):
    text = ''
    method_list = _get_methods(exclude=['admin'])
    pairs = [f"<code>{method_name}</code> - {method_doc}" for method_name, method_doc in method_list]
    for element in pairs:
        text += f'{element}\n'            
    
    bot.send_message(message.chat.id, text, reply_to_message_id=message.id, parse_mode='HTML')

def _get_methods(exclude=[]):
    method_list = []

    current_module = inspect.getmodule(inspect.currentframe())
    for name, obj in inspect.getmembers(current_module):
        if inspect.isfunction(obj) and not name.startswith('_') and name not in exclude:
            method_list.append((name, obj.__doc__))
    
    return method_list