import logging
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import telebot

EBAY_APP_ID = "HowlJenk-WaLSearc-PRD-c6c5cebfd-8b15464c"
TELEGRAM_BOT_API_TOKEN = "423141802:AAE7Cd8T0a0RtiJroBBsazr7Aij-xUUuHY4"

bot = telebot.AsyncTeleBot(TELEGRAM_BOT_API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)

def eBaySearch(item):
    api = Finding(appid=EBAY_APP_ID, config_file=None)
    response = api.execute(
        "findItemsAdvanced",
        {
            "keywords": item,
            "sortOrder": "CurrentPriceHigher"
        }
    )
    try:
        if response.reply.searchResult.item == "":
            return None
        cheapestitem = response.reply.searchResult.item[-1]
        return (
            cheapestitem.sellingStatus.currentPrice.value,
            cheapestitem.title,
            str(cheapestitem.paymentMethod),
            cheapestitem.viewItemURL
        )
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

@bot.message_handler(commands=["s", "search"])
def search_by_command(message):
    args = message.text.split()
    bot.send_chat_action(cid, "typing")
    if len(args) > 2:
        search = eBaySearch(" ".join(args[1:]))
        if search:
            bot.reply_to(message, MESSAGE_TEMPLATE.format(*search))
        else:
            bot.reply_to(message, "Nothing was found.")

@bot.message_handler(commands=["help", "start"])
def welcome(message):
    bot.reply_to(message, WELCOME_MESSAGE)

WELCOME_MESSAGE = """Welcome to eBay search bot, made by @Etarra

/(s)earch <item> - Search the cheapest offer of an item on eBay."""

MESSAGE_TEMPLATE = """Item: {0}
Price: {1}
Paying method: {2}
URL: {3}
"""

if __name__ == "__main__":
    try:
        bot.polling()
    except KeyboardInterrupt:
        print("Exiting by user request.\n")
        exit()
