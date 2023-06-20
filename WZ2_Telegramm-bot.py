import requests
from bs4 import BeautifulSoup as BS
import telebot
import config
from telebot import types
bot = telebot.TeleBot(config.TOKEN)
def list_of_weapons(a, WP1):
    r = requests.get("https://www.wzranked.com/wz2/meta/guns")
    html = BS(r.content, 'html.parser')
    if r.status_code != 200:
        return 'Сайт что то не фурычит, попробуйте позже'
    WP1 = []
    j = 1
    weapons = html.findAll('tr')
    for i in weapons[1:]:
        tp = i.find('td', class_='whitespace-nowrap py-1 px-1 text-xs text-custom-text-secondary')
        wp = i.findAll('div')
        if tp.text == a:
            WP1.append(wp[1].text)
            j += 1
    return WP1

def meta_lodaut(a):
    r = requests.get("https://www.wzranked.com/wz2/meta/guns/" + a.lower().replace(" ", "-"))
    if r.status_code != 200:
        return 'Ой, либо вы написали что то странное, либо сайту поплохело.'
    html = BS(r.content, 'html.parser')
    atach = html.findAll('div', class_="flex justify-between px-2 py-1")
    txt = "Метовая зборка на " + a + ":" + "\n"
    for i in atach:
        p = i.findAll('div')
        txt += p[2].text + "-" + p[1].text + "\n"
    return(txt + "Если хотите посмотреть на другие сборки, напишите /start")
    
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard =True)
    item1 = types.KeyboardButton("BR")
    types_of_weapons = ["BR", "SMG", "Sniper", "AR", "Shotgun", "Handgun", "LMG", "Rifle"]
    for i in types_of_weapons:
        markup.add(types.KeyboardButton(i))
    bot.send_message(message.chat.id, "Добро пожаловать, этот бот позволит быстро и удобно узнать метовые сборки на любое оружие в Warzone 2, Выбери тип оружия:", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def la(message):
    types_of_weapons = ["BR", "SMG", "Sniper", "AR", "Shotgun", "Handgun", "LMG", "Rifle"]
    if message.chat.type == 'private':
        if message.text in types_of_weapons:
            WP = []
            WP = list_of_weapons(message.text, WP)
            WPL = "Выбирите оружие. Рейтинг самых топовых пушек этого класса:"
            k = 1
            for i in WP:
                WPL = WPL + " " + str(k) +":" + i + "\n"
                k += 1
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard =True)
            for i in WP:
                markup.add(types.KeyboardButton(i))
            bot.send_message(message.chat.id, WPL, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, meta_lodaut(message.text))
bot.polling(none_stop=True)
