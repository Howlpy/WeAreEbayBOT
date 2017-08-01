import telebot
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import json
import datetime

respuesta = ''
def buscarebay(busqueda):
	try:
		api = Finding(appid="YOUR EBAY APP ID", config_file=None)
		response = api.execute('findItemsAdvanced', {'keywords': busqueda)
		try:
				if response.reply.searchResult.item != '':
					for a in response.reply.searchResult.item:
						global respuesta
						precio = "El precio es: " + a.sellingStatus.currentPrice.value
						Titulo = "Producto: " + a.title
						metodo_pago = "Pago con: " + str(a.paymentMethod)
						url = "URL: " + a.viewItemURL
						respuesta = Titulo + "\n" + precio + "\n" + metodo_pago + "\n" + url
				else:
					busqueda = "Consolador"
					response = api.execute('findItemsAdvanced', {'keywords': busqueda})
					for a in response.reply.searchResult.item:
						precio = "El precio es: " + a.sellingStatus.currentPrice.value
						Titulo = "Producto: " + a.title
						metodo_pago = "Pago con: " + str(a.paymentMethod)
						url = "URL: " + a.viewItemURsL
						respuesta = Titulo + "\n" + precio + "\n" + metodo_pago + "\n" + url
		except Exception as e:
			raise


	except ConnectionError as e:
		print(e)
		print(e.response.dict())

bot = telebot.TeleBot("Your token")
@bot.message_handler(commands=['buscar'])
def buscar(message):
	cid = message.chat.id
	if message.content_type == 'text':
		if len(message.text.split('/buscar ')) == 2:
			mclear = message.text.split('/buscar ')[1]
			buscarebay(mclear)
			bot.send_chat_action(cid, 'typing')
			print("[" + str(datetime.datetime.now()) + "] " + str(message.chat.first_name) + " [" + str(message.chat.id) + "]: " + message.text)
			bot.reply_to(message, respuesta)
		else:
			bot.reply_to(message, "Que quieres buscar?")
			pass
@bot.message_handler(commands=['help'])
def help(message):
	cid = message.chat.id
	bot.reply_to(message, "Bienvenido al bot de busqueda en ebay, creado por @etarra(Howl)  \n \n/buscar + Articulo para buscar un producto en ebay con el menor precio")

bot.polling()
