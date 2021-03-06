from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

import ephem

from datetime import datetime

def greet_user(update, context):
    print("Вызван /start")
    update.message.reply_text("Hello! To know in what constellation a planet is today, enter the planet name in the '/planet Planet' format.")

def planet(update, context):
    user_text = update.message.text 
    print(user_text)

# Задаем возможные варианты для обработки - список планет

    planets_list = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

# Разбиваем пользовательский ввод на отдельные слова

    per_word = user_text.split()

# Проверяем каждое из полученных слов на совпадение с элементом списка "planets_list". 


    for word_in_text in per_word:        

        if word_in_text in planets_list:

# При появлении совпадения производим вычисление созвездия для планеты на текущую дату             

            planet = getattr(ephem, word_in_text)
            planet_position = planet(datetime.now())
            constellation = ephem.constellation(planet_position)

            update.message.reply_text(f"Planet {word_in_text} is in the {constellation} constellation today.")

# Реализовал задание про подсчет слов прямо в функции "Planet"

        if word_in_text == '/wordcount':
            per_word.remove('/wordcount')
            if len(per_word) == 0:
                update.message.reply_text('Please, type something.')
                break   
            else:
                words_num = len(per_word)
                update.message.reply_text(f"{words_num} words.")
                break

# Реализовал задание про ближайшее полнолуние также в функции "Planet"

        if word_in_text == '/next_full_moon':
            full_moon_date = ephem.next_full_moon(datetime.now())

            update.message.reply_text(f"Next full moon date is {full_moon_date}.")
            break
#_____________________________________________________________________________________
# Калькулятор, выполняющий действия с двумя любыми int/float числами

        if word_in_text == '/calc':
            per_word.remove('/calc')
            sep = ' '
            calc = sep.join(per_word)

            multifig = False
            calc_list = []

            for calc_symbol in calc:

                calc_list.append(calc_symbol)
                calc_symbol_index = len(calc_list) - 1

                if calc_symbol.isdigit() or calc_symbol == '.':

                    if multifig == True:

                        calc_list[calc_symbol_index - 1] += calc_list[calc_symbol_index]
                        calc_list.remove(calc_symbol)

                    else:
                        multifig = True
    
                elif calc_symbol == ',':
                    if multifig == True:

                        calc_list[calc_symbol_index - 1] += '.'
                        calc_list.remove(calc_symbol)

                    else:
                        multifig = True      
    
                elif calc_symbol == ' ' or calc_symbol == '=':
        
                    calc_list.remove(calc_symbol)
                    multifig = False
    
                else:
                    multifig = False


            calc_list[0] = float(calc_list[0])
            calc_list[2] = float(calc_list[2])

            if calc_list[1] == '+':
                calc_result = calc_list[0] + calc_list[2]

            elif calc_list[1] == '-':
                calc_result = calc_list[0] - calc_list[2]

            elif calc_list[1] == '*':
                calc_result = calc_list[0] * calc_list[2]

            elif calc_list[1] == '/':

                if calc_list[2] != 0:
                    calc_result = calc_list[0] / calc_list[2]
                else:
                    calc_result = 'I can not divide by zero'

            else:
                calc_result = 'This math function has not been implemented yet.'
                break

            update.message.reply_text(f"Here is your result: {calc_result}")
            break
        else:
            update.message.reply_text("Sorry, what again?")
            break
#_________________________________________________________________________________


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, planet))


    mybot.start_polling()

    mybot.idle()

if __name__ == "__main__":
    main()