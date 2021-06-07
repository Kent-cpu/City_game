import telebot
import json
from random import randint

bot = telebot.TeleBot("1749167783:AAHrE-uxbsp4MiwFqNi24bMmgYhLeZz6uTY")
city = {}
previousWords = ""
isBotMove = False

@bot.message_handler(commands=['start'])
def start(message):
    sortedCity()
    bot.send_message(message.chat.id, "Поехали, ты начинаешь первый")   

@bot.message_handler(content_types='[text]')
def game(message):
    currentCity = message.text.lower()
    if currentCity in city[currentCity[0]]:
        city[currentCity[0]].remove(currentCity)
    else:
        bot.send_message(message.chat.id, "Такого города не существует или уже был использован в игре")
        return
    if isBotMove and currentCity[0] != previousWords[len(previousWords) - 1]:
        bot.send_message(message.chat.id, "Город начинается на неправильную букву")
        return
    moveBot(message)

def sortedCity():
    jsonContent = ""
    with open("cities.json", "r", encoding = "utf8") as cityFile:
        jsonContent = json.load(cityFile)
    for index in range(len(jsonContent["city"])):
        currentCity = jsonContent["city"][index]["name"].lower()
        if currentCity[0] in city:
            city[currentCity[0]].append(currentCity)
        else:
            city[currentCity[0].lower()] = []
    


def moveBot(enterCityFromUser):
    global previousWords, isBotMove
    cityStr = enterCityFromUser.text.lower()
    lastLetter = ""
    if cityStr[len(cityStr) - 1] == "й" or cityStr[len(cityStr) - 1] == "ы" or  cityStr[len(cityStr) - 1] == "ь" or cityStr[len(cityStr) - 1] == "ъ": # тут верное удаление
        for index in reversed(range(len(cityStr) - 1)):
            if cityStr[index] != "й" and cityStr[index] != "ы" and  cityStr[index] != "ь" and cityStr[index] != "ъ":
                lastLetter = cityStr[index]
                break
        rIndexCity = randint(0, len(city[lastLetter]))
        city[lastLetter].remove(city[lastLetter][rIndexCity])
        previousWords = city[lastLetter][rIndexCity]
        bot.send_message(enterCityFromUser.chat.id, city[lastLetter][rIndexCity])    
    else:
        lastLetter = cityStr[len(cityStr) - 1]
        print(lastLetter)
        rIndexCity = randint(0, len(city[lastLetter]))
        previousWords = city[lastLetter][rIndexCity]
        print(city[lastLetter][rIndexCity])
        bot.send_message(enterCityFromUser.chat.id, city[lastLetter][rIndexCity])
        city[lastLetter].remove(city[lastLetter][rIndexCity])
    isBotMove = True

   
bot.polling()