# -*- coding: utf-8 -*-
import telebot
import requests
import subprocess
import os
import sched, time

bot = telebot.TeleBot("token")

def download_file(url):
    r = requests.get(url, stream=True)
    with open('magister.pdf', 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)

def regular_call(sc,bot):
    download_file("http://priem.bmstu.ru/UserFiles/registered-magister-Moscow.pdf")
    os.system("pdftotext magister.pdf rr.txt")
    count_new = int(subprocess.Popen("grep  'ИУ7' rr.txt | wc -l ", \
                           shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    with open('counter.txt', "r+") as counter:
        old_count = int(counter.readline())
        if old_count<count_new:
            counter.seek(0)
            counter.write(str(count_new))
            bot.send_message(-1001144863254, "Новая заявка на ИУ7! Всего заявок: "+str(count_new))
    s.enter(600, 1, regular_call,(sc,bot))


@bot.message_handler(commands=['retards'])
def handle_current_retards_list(message):
    with open('counter.txt', "r+") as counter:
        retards = int(counter.readline())
        bot.send_message(71301900, "На данный момент на ИУ7 документы подали " + str(retards) + " человек")
        bot.send_message(-1001144863254, "На данный момент на ИУ7 документы подали " + str(retards) + " человек")


s = sched.scheduler(time.time, time.sleep)
s.enter(600, 1, regular_call, (s,bot))
s.run()




