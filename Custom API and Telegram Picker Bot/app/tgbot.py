import telebot
from app import dbhelper
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
import time

bot = telebot.TeleBot("REDACTED:REDACTED", parse_mode=None)
db = dbhelper.DBHelper("mongodb+srv://doadmin:REDACTED@REDACTED.mongo.ondigitalocean.com/admin?authSource=admin", "shirts22")

def one():
	global bot
	global db

	@bot.message_handler(commands=['start'])
	def send_welcome(message):
		picker_id = message.from_user.id
		picker_check = db.picker_isNew(picker_id)
		if picker_check:
			for picker in picker_check:
				bot.send_message(message.chat.id, f"Welcome back, {picker.get('name')}")
		else:
			sent_msg = bot.send_message(message.chat.id, "Thanks for helping out, what's your name?")
			bot.register_next_step_handler(sent_msg, name_handler)  # Next message will call the name_handler function

	def name_handler(message):
		name = message.text
		if db.picker_add(message.from_user.id, name):
			bot.send_message(message.chat.id,
							 f"You've been registered, {name}! Type /shift_start to begin and /shift_end once you leave.")
		else:
			bot.send_message(message.chat.id, "Something went wrong with registration, please contact Putra. [001]")

	@bot.message_handler(commands=['shift_start'])
	def shift_start(message):
		picker_id = message.from_user.id
		picker_status = db.picker_check(picker_id, "status")
		if picker_status == "inactive":
			if db.picker_update_status(picker_id, "status", "active"):
				bot.send_message(message.chat.id,
								 f"You've now begun your shift at {datetime.now().strftime('%I:%M %p')}")
		elif picker_status == "active":
			bot.send_message(message.chat.id, f"You've already started your shift!")
		elif picker_status == False:
			bot.send_message(message.chat.id,
							 "Something went wrong, your records can't be found. Have you registered with /start? [002]")

	@ bot.message_handler(commands=['shift_end'])
	def shift_end(message):
		picker_id = message.from_user.id
		picker_status = db.picker_check(picker_id, "status")
		if picker_status == "active":
			if db.picker_update_status(picker_id, "status", "inactive"):
				bot.send_message(message.chat.id,
								 f"You've ended your shift at {datetime.now().strftime('%I:%M %p')}. Thank you!")
		elif picker_status == "inactive":
			bot.send_message(message.chat.id, f"You haven't begun your shift!")
		elif picker_status == False:
			bot.send_message(message.chat.id,
							 "Something went wrong, your records can't be found. Have you registered with /start? [002]")

	@bot.callback_query_handler(func=lambda call: True)
	def callback_query(call):
		if call.data == "cb_collected":
			db.order_update_status(db.picker_check(call.message.chat.id, "currently_picking"), "collected", "true")
			db.picker_update_status(call.message.chat.id, "status", "active")
			db.picker_update_status(call.message.chat.id, "currently_picking", "false")
			bot.answer_callback_query(call.id, f"Successful Collection")
			edited_message = '<b>[COLLECTED]</b>' + str(call.message.text).split(']')[1]
			bot.edit_message_text(edited_message, call.message.chat.id, call.message.message_id, parse_mode='HTML')
		elif call.data == "cb_noshow":
			db.order_update_status(db.picker_check(call.message.chat.id, "currently_picking"), "collected", "noshow")
			db.picker_update_status(call.message.chat.id, "status", "active")
			db.picker_update_status(call.message.chat.id, "currently_picking", "false")
			bot.answer_callback_query(call.id, "Collection unsuccessful - No Show")
			edited_message = '<b>[! NO SHOW !]</b>\nPlease inform Kai En/Putra' + str(call.message.text).split(']')[1]
			bot.edit_message_text(edited_message, call.message.chat.id, call.message.message_id, parse_mode='HTML')

	print("are polling")
	bot.infinity_polling()

def two():
	global bot
	global db
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
		print('ORDER AND PICKER MATCHED, SENDING ORDER')
		bot.send_message(next_picker_id, message, reply_markup=gen_markup(), parse_mode='HTML')
		db.order_update_status(next_order.get("_id"), "collected", "pending")
		db.picker_update_status(next_picker_id, "status", "busy")
		db.picker_update_status(next_picker_id, "currently_picking", next_order.get('_id'))
		time.sleep(3)

if __name__ == '__main__':
	Thread(target = one).start()
	print("thread one started")
	Thread(target = two).start()
	print("thread two started")
