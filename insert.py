# python insert.py {domain}

import os
import sys
import psycopg2
import base64
import telebot

bot = telebot.TeleBot(os.environ['API_KEY'])
chat_id = os.environ['CHAT_ID']
last = False

url = sys.argv[1]
DATABASE_URL = os.environ['DATABASE_URL']

try:
  temp = sys.argv[2]
  last = True
except:
  pass

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

#checking if any previous entry in the database to avoid duplicates

cur.execute("select * from output;")
t = cur.fetchall()

doms = [i[0] for i in t]

if url in doms:
  try:
    with open(f'results/{url}-output.txt', 'r') as f:
      res1 = f.read()
    with open(f'results/{url}-gau.txt', 'r') as f:
      res2 = f.read()
    res1 = bytes(res1, 'utf-8')
    final1 = base64.standard_b64encode(res1)
    final1 = final1.decode('utf-8')

    res2 = bytes(res2, 'utf-8')
    final2 = base64.standard_b64encode(res2)
    final2 = final2.decode('utf-8')


    cur.execute(f"update output set result = '{final1}' where domain = '{url}';")
    conn.commit()
    cur.execute(f"update output set gau = '{final2}' where domain = '{url}';")
    conn.commit()
  except:
    with open(f'results/{url}-output.txt', 'r') as f:
      res1 = f.read()
    res1 = bytes(res1, 'utf-8')
    final1 = base64.standard_b64encode(res1)
    final1 = final1.decode('utf-8')

    cur.execute(f"update output set result = '{final1}' where domain = '{url}';")
    conn.commit()
    cur.execute(f"update output set gau = 'The Gathered URLs not run yet !' where domain = '{url}';")
    conn.commit()

else:
  try:
    with open(f'results/{url}-output.txt', 'r') as f:
      res1 = f.read()
    with open(f'results/{url}-gau.txt', 'r') as f:
      res2 = f.read()
    res1 = bytes(res1, 'utf-8')
    final1 = base64.standard_b64encode(res1)
    final1 = final1.decode('utf-8')

    res2 = bytes(res2, 'utf-8')
    final2 = base64.standard_b64encode(res2)
    final2 = final2.decode('utf-8')

    cur.execute(f"insert into output values ('{url}', '{final1}', '{final2}');")
    conn.commit()
  except:
    with open(f'results/{url}-output.txt', 'r') as f:
      res1 = f.read()
    res1 = bytes(res1, 'utf-8')
    final1 = base64.standard_b64encode(res1)
    final1 = final1.decode('utf-8')

    cur.execute(f"insert into output values ('{url}', '{final1}', 'The Gathered URLs not run yet !');")
    conn.commit()

conn.commit()

if last:
   bot.send_message(chat_id, f"scanned results of {url} is saved in db")
cur.close()
conn.close()
