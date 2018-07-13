# -*- coding: utf-8 -*-
import telebot
import requests
import subprocess
import os
import sched, time
import threading
import sys

token = str(sys.argv[1])
bot = telebot.TeleBot(token)

def download_file(url):
    r = requests.get(url, stream=True)
    with open('magister.pdf', 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)

def regular_call(sc,bot):
    download_file("http://priem.bmstu.ru/UserFiles/registered-magister-Moscow.pdf")
    os.system("pdftotext magister.pdf rr.txt")
    count_new = int(subprocess.Popen("grep  'ИУ7' rr.txt | wc -l ", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    count_in = int(subprocess.Popen("grep  'ИУ7-И' rr.txt | wc -l ",shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore')) 
    count_cp = int(subprocess.Popen("grep 'ИУ7 (ЦП)' rr.txt | wc -l ", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore')) 
    with open('counter.txt', "r+") as counter:
        old_count = int(counter.readline())
        if old_count<count_new:
            counter.seek(0)
            counter.write(str(count_new))
            bot.send_message(-1001144863254, "Новая заявка на ИУ7! Всего заявок: "+str(count_new) +" . Из них иностранцев " + str(count_in) + " , целевиков " + str(count_cp))
    sc.enter(600, 1, regular_call,(sc,bot))


@bot.message_handler(commands=['getstat','retards'])
def handle_current_retards_list(message):
    count_new = int(subprocess.Popen("grep  'ИУ7' rr.txt | wc -l ", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    count_in = int(subprocess.Popen("grep  'ИУ7-И' rr.txt | wc -l ",shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    count_cp = int(subprocess.Popen("grep 'ИУ7 (ЦП)' rr.txt | wc -l ", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    bot.reply_to(message," Всего заявок: "+str(count_new) +" . Из них иностранцев " + str(count_in) + " , целевиков " + str(count_cp))

def timer(bot):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(5, 1, regular_call, (s,bot))
    s.run()

   
t=threading.Thread(target=timer, args=(bot,)) 
t.start()
bot.polling(none_stop=True)



