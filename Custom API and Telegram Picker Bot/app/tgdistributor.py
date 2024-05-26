import telebot
from app import dbhelper
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

db = dbhelper.DBHelper("mongodb+srv://doadmin:REDACTED@REDACTED.mongo.ondigitalocean.com/admin?authSource=admin", "shirts22")

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Collected!", callback_data="cb_collected"),
                               InlineKeyboardButton("No-show", callback_data="cb_noshow"))
    return markup


while True:
    next_order = db.order_queue_next()
    try:
        message = f"<b>[NEW PICK-UP]</b>\n{next_order.get('orderName')}\n"
        item_list = list(next_order.get("items"))
        for item in item_list:
            message = message + f"\n x{item['itemQuantity']} {item['itemName']}"
    except AttributeError:
        continue
    try:
        next_picker_id = db.picker_queue_next().get("_id")
    except AttributeError:
        continue

    bot = telebot.TeleBot("REDACTED:REDACTED", parse_mode=None)
    bot.send_message(next_picker_id, message, reply_markup=gen_markup(), parse_mode='HTML')
    bot.close()
    db.order_update_status(next_order.get("_id"), "collected", "pending")
    db.picker_update_status(next_picker_id, "status", "busy")
    db.picker_update_status(next_picker_id, "currently_picking", next_order.get('_id'))
    time.sleep(1)