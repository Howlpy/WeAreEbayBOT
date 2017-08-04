import telebot
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import json
import datetime
import threading

respuesta = []
def buscarebay(busqueda):
		api = Finding(appid="HowlJenk-WaLSearc-PRD-c6c5cebfd-8b15464c", config_file=None)
		response = api.execute('findItemsAdvanced', {'keywords': busqueda})
		try:
			if response.reply.searchResult.item != '':
				for a in response.reply.searchResult.item:
					global respuesta
					precio = "El precio es: " + a.sellingStatus.currentPrice.value
					Titulo = "Producto: " + a.title
					metodo_pago = "Pago con: " + str(a.paymentMethod)
					url = "URL: " + a.viewItemURL
					respuesta.append(Titulo + "\n" + precio + "\n" + metodo_pago + "\n" + url)
			else:
				pass

		except ConnectionError as e:
			print(e)
			print(e.response.dict())

bot = telebot.TeleBot("423141802:AAE7Cd8T0a0RtiJroBBsazr7Aij-xUUuHY4")
@bot.message_handler(commands=['buscar'])
def buscarfalso(message):
	threading.Thread(target=buscar, args=(message,)).start()
def buscar(message):
	global respuesta
	cid = message.chat.id
	if message.content_type == 'text':
		if len(message.text.split('/buscar ')) == 2:
			mclear = message.text.split('/buscar ')[1]
			buscarebay(mclear)
			print("[" + str(datetime.datetime.now()) + "] " + str(message.chat.first_name) + " [" + str(message.chat.id) + "]: " + message.text)
			bot.send_chat_action(cid, 'typing')
			while True:
				for a in respuesta:
					bot.reply_to(message,a)

				respuesta = []


		else:
			bot.reply_to(message, "Que quieres buscar?")
			pass
@bot.message_handler(commands=['help'])
def help(message):
	cid = message.chat.id
	bot.reply_to(message, "Bienvenido al bot de busqueda en ebay, creado por @etarra(Howl)  \n \n/buscar + Articulo para buscar un producto en ebay con el menor precio")


bot.polling()
