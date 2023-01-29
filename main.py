import os
import telebot
import yfinance as yfin

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['greet'])
def greet(message):
  bot.reply_to(message, "Howdy")


def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True


@bot.message_handler(func=stock_request)
def send_price(message):
  '''
  request = message.text.split()[-1]
  print(message)
  print(request)
  bot.send_message(message.chat.id, yfin.Ticker(request).basic_info)
  '''

  request = message.text.split()[1]
  data = yfin.download(tickers=request, period='5m', interval='5m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")


bot.polling()
