import requests
import telebot 
from telebot import types
from bs4 import BeautifulSoup

token = ""

bot = telebot.TeleBot(token)

menuButton = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnSochi = types.KeyboardButton("Сочи")
btnMoscow = types.KeyboardButton("Москва")
btnKam = types.KeyboardButton("Камчатка")
btnSP = types.KeyboardButton("Санкт-Петербург")


menuButton.row(btnSochi,btnMoscow,btnKam,btnSP)

cities = {
    "Камчатка":"https://m.rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%92%D0%B8%D0%BB%D1%8E%D1%87%D0%B8%D0%BD%D1%81%D0%BA%D0%B5",
    "Москва":"https://m.rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%BC,_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0",
    "Санкт-Петербург":"https://m.rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5",
    "Сочи": "https://m.rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A1%D0%BE%D1%87%D0%B8"
}

def weather_check(city_name):
    url = cities[city_name]
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    finish = soup.find("meta", {"name": "description"})
    return finish

@bot.message_handler(commands=["start"])
def welcome_send(message):
    bot.send_message(message.chat.id,"Добро пожаловать 😀\nЗдесь ты можешь посмотреть погоду",reply_markup=menuButton)
    
@bot.message_handler(func=lambda message: True)
def message_user(message):
    print(f"{message.from_user.username} что-то нажимает")
    
    if message.text in cities:
        bot.send_message(message.chat.id,"Загрузка погоды..")
        print(f"{message.from_user.username} дал запрос на город {message.text}")
        gorod = weather_check(message.text)
        gorod_print = gorod["content"]
        bot.send_message(message.chat.id,gorod_print)
        print(f"Запрос пользователя {message.from_user.username} загружен и успешно отправлен")
    else:
        bot.send_message(message.chat.id, "Мне не удалось найти такой город")
        
bot.polling()
        