import logging
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import telebot

# Configuracion
EBAY_APP_ID = "<YOUR EBAY APP ID>"
TELEGRAM_BOT_API_TOKEN = "<YOUR TELEGRAM BOT API TOKEN>"

# Inicializacion
bot = telebot.AsyncTeleBot(TELEGRAM_BOT_API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)

# Busqueda en eBay
def eBaySearch(item):
    api = Finding(appid=EBAY_APP_ID, config_file=None)
    response = api.execute(
        "findItemsAdvanced",
        {
            "keywords": item,
            "sortOrder": "CurrentPriceHigher" # Esto es para obtener el mas barato
        }
    )
    try:
        if response.reply.searchResult.item == "":
            return None # Si no hay resultados, no devolvemos nada.
        """

        Como hemos pedido que nos ordene los items por precio de mayor a menor,
        sacamos el ultimo item, que seria el mas barato.

        """
        cheapestitem = response.reply.searchResult.item[-1]
        """

        Ahora devolvemos un tuple con toda la informacion que necesitamos para
        el mensaje

        """
        return (
            cheapestitem.sellingStatus.currentPrice.value, # Precio
            cheapestitem.title, # Titulo
            str(cheapestitem.paymentMethod), # Metodo de pago
            cheapestitem.viewItemURL # URL
        )
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

# Funcion que recibe comando de busqueda
@bot.message_handler(commands=["s", "search"])
def search_by_command(message):
    args = message.text.split()
    bot.send_chat_action(cid, "typing") # Envia estado "escribiendo"
    if len(args) > 2: # Si el comando no tiene el objeto a buscar, no hacer nada
        """

        Para hacer la busqueda, quitamos el /(s)earch del mensaje enviado por el usuario.

        """
        search = eBaySearch(" ".join(args[1:]))
        if search: # Hay resultados?
            """

            Hay resultados; envia un mensaje formateando una string 
            predefinida, con los datos devueltos por la funcion.

            """
            bot.reply_to(message, MESSAGE_TEMPLATE.format(*search))
        else:
            bot.reply_to(message, "Nothing was found.") # No hay resultados; envia un mensaje.

# Funcion que recibe comando /help o /start
@bot.message_handler(commands=["help", "start"])
def welcome(message):
    bot.reply_to(message, WELCOME_MESSAGE) # Envia el mensaje de bienvenida

# Mensaje de bienvenida
WELCOME_MESSAGE = """Welcome to eBay search bot, made by @Etarra

/(s)earch <item> - Search the cheapest offer of an item on eBay."""

# Mensaje posteriormente formateado con los datos del item.
MESSAGE_TEMPLATE = """Item: {0}
Price: {1}
Paying method: {2}
URL: {3}"""

if __name__ == "__main__":
    try:
        bot.polling()
    except KeyboardInterrupt:
        print("Exiting by user request.\n")
        exit()
