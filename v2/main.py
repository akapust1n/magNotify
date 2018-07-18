# -*- coding: utf-8 -*-
import telebot
import requests
import subprocess
import os
import sched, time
import threading
import sys
from random import randint
import sqlite3
import datetime

token = str(sys.argv[1])
bot = telebot.TeleBot(token,threaded=False)
conn = sqlite3.connect('ban.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS 
             banTable( id int primary key, dt datetime default current_timestamp)''')

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
        elif old_count > count_new:
            counter.seek(0)
            counter.write(str(count_new))
            bot.send_message(-1001144863254, "Количество заявок на ИУ7 уменьшилось! ¯\_(ツ)_/¯ Всего заявок: "+str(count_new) +" . Из них иностранцев " + str(count_in) + " , целевиков " + str(count_cp))
    sc.enter(600, 1, regular_call,(sc,bot))


@bot.message_handler(commands=['getstat'])
def handle_current_retards_list(message):
    count_new = int(subprocess.Popen("grep  'ИУ7' rr.txt | wc -l ", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    count_in = int(subprocess.Popen("grep  'ИУ7-И' rr.txt | wc -l ",shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    count_cp = int(subprocess.Popen("grep 'ИУ7 (ЦП)' rr.txt | wc -l ", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    print("Request", message)
    bot.reply_to(message," Всего заявок: "+str(count_new) +" . Из них иностранцев " + str(count_in) + " , целевиков " + str(count_cp))

@bot.message_handler(commands=['retards'])
def handle_current_retards_list(message):
    count_new = int(subprocess.Popen("grep  'ИУ7' rr.txt | wc -l ", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    count_in = int(subprocess.Popen("grep  'ИУ7-И' rr.txt | wc -l ",shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    count_cp = int(subprocess.Popen("grep 'ИУ7 (ЦП)' rr.txt | wc -l ", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8','ignore'))
    print("Request\n", message)
    proh = randint(1,100)
    if proh>3:
        conn = sqlite3.connect('ban.db') 
        c = conn.cursor()
        c.execute('''SELECT id,dt FROM banTable WHERE id=?''',(str(message.from_user.id),))
        user1 = c.fetchone()
        if not(user1 is None):
            c.execute("SELECT julianday('now') - julianday(dt) from banTable WHERE id={id}".format(id=message.from_user.id))
            days = c.fetchone()
            print("DAYS\n")
            print(days[0])
            if(days[0]<3):
                c.execute("UPDATE banTable SET dt=DATETIME(dt,'+600 minutes') WHERE id={id}".format(id=message.from_user.id))
                bot.reply_to(message, "Poshel nahui! Ban uvelichen na 10 chasov. Ostalos:{dn} dnya".format(dn=str(3-days[0]+10/24)))
                conn.commit()
                return
            else:
                c.execute("DELETE FROM banTable WHERE id={id}".format(id=message.from_user.id))
                conn.commit()

        if (proh>3 and proh<11):
            c.execute("INSERT OR IGNORE  INTO banTable (id,dt) VALUES(?, CURRENT_TIMESTAMP)",(str(message.from_user.id),))
            c.execute("UPDATE banTable SET dt=CURRENT_TIMESTAMP WHERE id={id}".format(id=message.from_user.id))
            bot.reply_to(message,"ПРИЗ - БАН на 3 дня�")
            conn.commit()
            return
        if (proh>10 and proh<21):
            bot.reply_to(message,"а может сам ты ретард? посмотри на сайте всё")
        elif (proh>20 and proh<31):
            bot.reply_to(message,"ты неудачник, тебе не скажу")
        else:
            bot.reply_to(message," Всего заявок: "+str(count_new) +" . Из них иностранцев " + str(count_in) + " , целевиков " + str(count_cp))
    else:
        banExpired = datetime.datetime.now() + 60*60*24
        bot.restrict_chat_member(message.chat.id,message.from_user.id, until_date=banExpired)
        bot.reply_to(message,"СУПЕРПРИЗ - МУТ НА ДЕНЬ !")

def timer(bot):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(5, 1, regular_call, (s,bot))
    s.run()
   
t=threading.Thread(target=timer, args=(bot,)) 
t.start()

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)



