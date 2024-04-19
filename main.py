import telebot
from matplotlib import pyplot as plt

bot = telebot.TeleBot("Не покажу")

@bot.message_handler(commands=["start", "старт"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот для подчёта статистики")

@bot.message_handler(commands=["plot", "график"])
def chart(message):
    bot.send_message(message.chat.id, "Введите через пробел X и Y массивы координат в таком ключе:"
                                      "\n \"0 0 0 0 0, 0 0 0 0 0\"\n"
                                      "С любым кол-вом чисел\n"
                                      "(числа должны быть паложительными)")
    bot.register_next_step_handler(message, chartInput)

def chartInput(message):
    x, y = message.text.split(", ")
    x = str(x).split()
    y = str(y).split()
    for i in range(len(x)):
        x[i] = int(x[i])
    for i in range(len(y)):
        y[i] = int(y[i])
    plt.plot(x, y)
    plt.scatter(x, y)
    plt.savefig('plot.png')
    plotPhoto = open("plot.png", "rb")
    plt.close()
    bot.send_photo(message.chat.id, plotPhoto, 'Вот график по данным значениям')

@bot.message_handler(commands=["bar", "столбчатаяДиаграмма"])
def chart(message):
    bot.send_message(message.chat.id, "Введите названия и высоту столбцов в таком ключе:"
                                      "\n \"название столбца название столбца, 0 0 \"\n"
                                      "С любым кол-вом столбцов")
    bot.register_next_step_handler(message, barInput)

def barInput(message):
    title, height = message.text.split(", ")
    title = str(title).split()
    height = str(height).split()
    for i in range(len(height)):
        height[i] = int(height[i])
    plt.bar(title, height)
    plt.savefig('bar.png')
    plotPhoto = open("bar.png", "rb")
    plt.close()
    bot.send_photo(message.chat.id, plotPhoto, 'Вот диаграмма по данным значениям')

@bot.message_handler(commands=["pie", "круговаяДиаграмма"])
def chart(message):
    bot.send_message(message.chat.id, "Введите названия и высоту столбцов в таком ключе:"
                                      "\n \"название столбца название столбца, 0 0 \"\n"
                                      "С любым кол-вом столбцов")
    bot.register_next_step_handler(message, pieInput)

def pieInput(message):
    title, height = message.text.split(", ")
    title = str(title).split()
    height = str(height).split()
    for i in range(len(height)):
        height[i] = int(height[i])
    plt.pie(height, labels=title, autopct="%.2f%%")
    plt.savefig('pie.png')
    piePhoto = open("pie.png", "rb")
    plt.close()
    bot.send_photo(message.chat.id, piePhoto, 'Вот диаграмма по данным значениям')

@bot.message_handler(commands=["analysis"])
def analysis(message):
    bot.send_message(message.chat.id, "Введите числовой ряд разделяя числа пробелом")
    bot.register_next_step_handler(message, analysisInput)

def analysisInput(message):
    data = list(map(int, message.text.split(" ")))
    data = sorted(data)
    average = sum(data) / len(data)

    if len(data) % 2 == 0:
        median = (data[(len(data)-1)//2] + data[(len(data)+1)//2]) / 2
    else:
        median = data[(len(data))//2]

    fashion = max(set(data), key=data.count)

    deviation = []
    deviation_square = []

    for i in data:
        deviation.append(i-average)
        deviation_square.append((i-average)**2)

    dispersion = sum(deviation_square) / len(deviation_square)

    bot.send_message(message.chat.id, f"Среднее арифметическое ряда: {average}\n"
                                      f"Медиана ряда: {median}\n"
                                      f"Мода ряда: {fashion}\n"
                                      f"Отклонения ряда {deviation}\n"
                                      f"Квадрат отклонений ряда {deviation_square}\n"
                                      f"Дисперсяи ряда: {dispersion}\n")

@bot.message_handler(commands=["info"])
def info(message):
    bot.send_message(message.chat.id, message)

bot.polling(none_stop=True)
