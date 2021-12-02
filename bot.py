# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
import info
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
from emoji import emojize


from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot('2135447201:AAFpS4Lmje3ABYILz0d64ygshbITNlq3OeY')
vip=[441399484, 55888804]
games={}
skills=[]

client1=os.environ['database']
client=MongoClient(client1)
db=client.mafia
users=db.users



def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)



    
    
@bot.message_handler(commands=['start'])
def start(m):
    x=user.find_one({'id':m.from_user.id})
    if x==None:      
        user.insert_one(createuser(m.from_user.id))
        print('Юзер создал аккаунт! Его имя: '+m.from_user.first_name)
    x=m.text.split('/start')
    if len(x)==2:
       try:
        if m.from_user.id==m.chat.id:
         if m.from_user.id not in games[int(x[1])]['players']:
          if len(games[int(x[1])]['players'])<35:
           if int(x[1])<0:
            i=0              
            if games[int(x[1])]['play']==0:
                games[int(x[1])]['players'].update(createuser(m.from_user.id, m.from_user.first_name))
                text=''           
                for ids in games[int(x[1])]['players']:
                    if games[int(x[1])]['players'][ids]['id']==m.from_user.id:
                        player=games[int(x[1])]['players'][ids]
                bot.send_message(m.from_user.id, 'Вы успешно присоединились!')
                b=0
                for g in games[int(x[1])]['players']:
                    text+=games[int(x[1])]['players'][g]['name']+'\n'
                    b+=1
                medit('Игроки: '+str(b)+'\n\n*'+text+'*', games[int(x[1])]['id'], games[int(x[1])]['users'])
                games[int(x[1])]['userlist']+=text+'\n'
                bot.send_message(games[int(x[1])]['id'], player['name']+' присоединился!')
          else:
            bot.send_message(m.from_user.id, 'Слишком много игроков! Мест не осталось!')
       except:
        if m.chat.id==m.from_user.id:
            bot.send_message(m.from_user.id, 'Игра crossfire')

            
@bot.message_handler(commands=['extend']) 
def extendd(m):
    if m.chat.id in games:
        if games[m.chat.id]['play']!=1:
            if m.from_user.id in games[m.chat.id]['players']:
                x=m.text.split('/extend')
                if len(x)==2:
                    try:
                        if int(x[1])>=1:
                            games[m.chat.id]['timebeforestart']+=int(x[1])
                            if games[m.chat.id]['timebeforestart']>=300:
                                games[m.chat.id]['timebeforestart']=300
                                bot.send_message(m.chat.id, 'Время до начала перестрелки увеличено! Осталось 5 минут.')
                            else:
                                bot.send_message(m.chat.id, 'Время до начала перестрелки увеличено на '+x[1]+'! Осталось '+str(games[m.chat.id]['timebeforestart'])+' секунд.')
                        else:
                            x=bot.get_chat_administrators(m.chat.id)
                            i=10
                            for z in x:       
                                if m.from_user.id==z.user.id:
                                    i=1
                                else:
                                    if i!=1:
                                        i=10
                            if i==1:
                                games[m.chat.id]['timebeforestart']+=int(x[1])
                                a=x[1]
                                if games[m.chat.id]['timebeforestart']<=0:
                                    pass
                                else:
                                    bot.send_message(m.chat.id,'Время до начала перестрелки увеличено на '+a+'! Осталось '+str(games[m.chat.id]['timebeforestart'])+' секунд.')
                            else:
                                bot.send_message(m.chat.id, 'Только администратор может использовать эту команду!')
                    except:
                        games[m.chat.id]['timebeforestart']+=30
                        if games[m.chat.id]['timebeforestart']>=300:
                            games[m.chat.id]['timebeforestart']=300
                        bot.send_message(m.chat.id, 'Время до начала перестрелки увеличено на 30! Осталось '+str(games[m.chat.id]['timebeforestart'])+' секунд.')
                else:
                    games[m.chat.id]['timebeforestart']+=30
                    if games[m.chat.id]['timebeforestart']>=300:
                            games[m.chat.id]['timebeforestart']=300
                    bot.send_message(m.chat.id, 'Время до начала перестрелки увеличено на 30! Осталось '+str(games[m.chat.id]['timebeforestart'])+' секунд.')
    
            
@bot.message_handler(commands=['flee'])
def flee(m):
    if m.chat.id in games:
     if games[m.chat.id]['play']!=1:
      if m.from_user.id in games[m.chat.id]['players']:
        del games[m.chat.id]['players'][m.from_user.id]
        text=''
        for g in games[m.chat.id]['players']:
            text+=games[m.chat.id]['players'][g]['name']+'\n'
        bot.send_message(m.chat.id, m.from_user.first_name+' сбежал!')
        medit('Игроки: \n\n*'+text+'*', m.chat.id, games[m.chat.id]['users'])
  

@bot.message_handler(commands=['players'])
def playerss(m):
    if m.chat.id in games:
        bot.send_message(m.chat.id, 'Список игроков', reply_to_message_id=games[m.chat.id]['users'])

            
def secnd(id):
    games[id]['timebeforestart']-=1
    if games[id]['timebeforestart']<=0:
        begin(id)
    else:
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/crossfirebot?start='+str(id)))
        if games[id]['timebeforestart']==180:
            msg=bot.send_message(id, 'Осталось 3 минуты! Жмите "Присоединиться", чтобы поучаствовать в перестрелке!', reply_markup=Keyboard)
            games[id]['todel'].append(msg.message_id)
        elif games[id]['timebeforestart']==60:
            msg=bot.send_message(id, 'Осталось 60 секунд! Жмите "Присоединиться", чтобы поучаствовать в перестрелке!', reply_markup=Keyboard)
            games[id]['todel'].append(msg.message_id)
        elif games[id]['timebeforestart']==30:
            msg=bot.send_message(id, 'Осталось 30 секунд! Жмите "Присоединиться", чтобы поучаствовать в перестрелке!', reply_markup=Keyboard)
            games[id]['todel'].append(msg.message_id)
        elif games[id]['timebeforestart']==10:
            msg=bot.send_message(id, 'Осталось 10 секунд! Жмите "Присоединиться", чтобы поучаствовать в перестрелке!', reply_markup=Keyboard)
            games[id]['todel'].append(msg.message_id)
        t=threading.Timer(1, secnd, args=[id])
        t.start()
            
            
@bot.message_handler(commands=['startgame'])
def startgame(m):
  if m.chat.id<0:
    if m.chat.id not in games:
        games.update(creategame(m.chat.id))  
        tt=threading.Timer(1, secnd, args=[m.chat.id])
        tt.start()
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/themafiyabot?start='+str(m.chat.id)))
        msg=bot.send_message(m.chat.id, m.from_user.first_name+' Начал(а) игру! Жмите кнопку ниже, чтобы присоединиться', reply_markup=Keyboard)
        msg2=bot.send_message(m.chat.id, 'Игроки:\n', parse_mode='markdown')
        games[m.chat.id]['users']=msg2.message_id
        for ids in games:
            if games[ids]['id']==m.chat.id:
                game=games[ids]
        game['todel'].append(msg.message_id)
    else:
      if games[m.chat.id]['play']==0:
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/themafiyabot?start='+str(m.chat.id)))
        msg=bot.send_message(m.chat.id, 'Игра уже запущена! Жмите "присоединиться"!', reply_markup=Keyboard)
        for ids in games:
            if games[ids]['id']==m.chat.id:
                game=games[ids]
        game['todel'].append(msg.message_id)
  else:
    bot.send_message(m.chat.id, 'Играть можно только в группах!')
    
   
def begin(id):
  if id in games:
   if games[id]['play']==0:
    if len(games[id]['players'])>=2:
        for ids in games[id]['todel']:
            try:
                bot.delete_message(id, ids)
            except:
                pass
        i=1
        for ids in games[id]['players']:
            games[id]['players'][ids]['number']=i
            i+=1
        bot.send_message(id, 'Игра начинается!')
        games[id]['play']=1
        xod(games[id])
    else:
        for ids in games[id]['todel']:
            try:
                bot.delete_message(id, ids)
            except:
                pass
        bot.send_message(id, 'Недостаточно игроков!')
        try:
            del games[id]
        except:
            pass


          
def xod(id):
  zlo7p=['volk','alpha']
  zlo15p=['volk','alpha','sekta','lycan']
  zlo35p=['volk','alpha','sekta','lycan']
  rolelist7p=['gunner','volk','selo','alpha','rock','chlp','seer','fool','lycan']
  rolelist15p=['gunner','volk','selo','alpha','rock','chlp','seer','fool','sekta','dikii','suicide']
  rolelist35p=['gunner','volk','selo','alpha','kamen']
  allroles=[]
  onerole=['gunner','alpha','chlp','seer','fool','dikii','suicide']
  i=0
  x=len(games[id]['players'])
  if x<=7:
    mode=1
    rolelist=rolelist7p
    zlo=zlo7p
  if x<=15:
    rolelist=rolelist15p
    zlo=zlo15p
    mode=2
  if x<=35:
    rolelist=rolelist35p
    zlo=zlo35p
    mode=3
  while i<x:
        i+=1
        if i==x:
            z=0
            for idss in allroles:
                if idss in zlo:
                    z=1
            if z==0:
                allroles.append(random.choice(zlo))
            else:
                allroles.append(rolechoice(onerole,allroles,mode))
        else:
            allroles.append(rolechoice(onerole,allroles,mode))
  for ids in games[id]['players']:
    if len(allroles)>0:
        role=random.choice(allroles)
        games[id]['players']['role']=role
        allroles.remove(role)
  night(id)
     

   
          
          
rolechoice(onerole,allroles,mode):
        returnn=0
        while returnn==0:
                role=random.choice(rolelist)
                if role in onerole and role in allroles:
                    returnn=0
                else:
                    rocks=0
                    selo=0
                    if role=='rock':
                        for rl in allroles:
                            if rl=='rock':
                                rocks+=1
                        if mode==1:
                            if rocks<1:
                                returnn=1
                        elif mode==2:
                            if rocks<2:
                                returnn=1
                        elif mode==3:
                            if rocks<4:
                                returnn=1
                    elif role=='selo':
                        for rl in allroles:
                            if rl=='selo':
                                selo+=1
                        if mode==1:
                            if selo<2:
                                returnn=1
                        elif mode==2:
                            if selo<3:
                                returnn=1
                        elif mode==3:
                            if selo<6:
                                returnn=1
        return role


  
def night(id):
    t=threading.Timer(100,day,args=[id])
    t.start()
    games[id]['xod']+=1
    if games[id]['xod']==1:
        for ids in games[id]['players']:
            bot.send_message(games[id]['players'][ids]['id'],roletotext(games[id]['players'][ids]['role']))
    for ids in games[id]['players']:
        roletoaction(id,games[id]['players'][ids])

def day(id):
    t=threading.Timer(100,lynch,args=[id])
    t.start()
    for ids in games[id]['players']:
      if games[id]['players'][ids]['checked']==0:
        player=games[id]['players'][ids]
        if player['role']=='wolf' or player['role']=='alpha' or player['role']=='lycan':
            targets=[]
            if games[id]['players'][ids]['target']!=None:
                targets.append(games[id]['players'][ids]['target'])
            games[id]['players'][ids]['checked']=1
            for idss in games[id]['players']:
                if games[id]['players'][idss]['role']=='alpha' or games[id]['players'][idss]['role']=='wolf' or games[id]['players'][idss]['role']=='lycan':
                  games[id]['players'][idss]['checked']=1
                  if games[id]['players'][idss]['target']!=None:
                    targets.append(games[id]['players'][idss]['target'])
            x=random.choice(targets)
            for trgt in games[id]['players']:
                if games[id]['players'][trgt]['number']==x:
                    games[id]['players'][trgt]['eaten']=1
                    
        if player['role']=='chlp':
            if player['target']!=None:
                for idss in games[id]['players']:
                    if games[id]['players'][idss]['number']==player['target']:
                        games[id]['players'][idss]['nothome']=1
                        player['chlp']=1
        if player['role']=='seer':
          if player['target']!=None:
            for idss in games[id]['players']:
                if games[id]['players'][idss]['number']==player['target']:
                    bot.send_message(player['id'],'Ты видишь, что '+games[id]['players'][idss]['name']+' - это '+games[id]['players'][idss]['role']+'!')
        
        
def lynch(id):
    kb=types.InlineKeyboardMarkup()
    for ids in games[id]['players']:
      player=games[id]['players'][ids]
      for idss in games[id]['players']:
        if games[id]['players'][idss]['id']!=player['id']:
            kb.add(types.InlineKeyboardButton(text=games[id]['players'][idss]['name'], callback_data='lynch'+games[id]['players'][idss]['number'])
    
    
        
def roletoaction(id,player):  
    kb=types.InlineKeyboardMarkup()
    if player['role']=='volk' or player['role']=='alpha':
      for ids in games[id]['players']:
       if games[id]['players'][ids]['id']!=player['id']:
        kb.add(types.InlineKeyboardButton(text=games[id]['players'][ids]['name'], callback_data=games[id]['players'][ids]['number']))
      bot.send_message(player['id'],'Кого вы хотите скушать?',reply_markup=kb)
    if player['role']=='chlp':
      for ids in games[id]['players']:
       if games[id]['players'][ids]['id']!=player['id']:
        kb.add(types.InlineKeyboardButton(text=games[id]['players'][ids]['name'], callback_data=games[id]['players'][ids]['number']))
      bot.send_message(player['id'],'Кого вы хотите посетить?',reply_markup=kb)
    if player['role']=='seer' or player['role']=='fool':
      for ids in games[id]['players']:
       if games[id]['players'][ids]['id']!=player['id']:
        kb.add(types.InlineKeyboardButton(text=games[id]['players'][ids]['name'], callback_data=games[id]['players'][ids]['number']))
      bot.send_message(player['id'],'Кого вы хотите увидеть?',reply_markup=kb)
    if player['role']=='dikii':
      for ids in games[id]['players']:
       if games[id]['players'][ids]['id']!=player['id']:
        kb.add(types.InlineKeyboardButton(text=games[id]['players'][ids]['name'], callback_data=games[id]['players'][ids]['number']))
      bot.send_message(player['id'],'Кого вы хотите выбрать примером?',reply_markup=kb)
        
        
        
        

#['gunner','volk','selo','alpha','rock','chlp','seer','fool','sekta','dikii','suicide']
def roletotext(role):
    x='У роли нет описания, обратитесь к @Loshadkin'
    if role=='chlp':
        x='Вы - Ксен'
    if role=='gunner':
        x='Вы стрелок'
    if role=='volk':
        x='Вы волк'
    if role=='selo':
        x='Вы село'
    if role=='alpha':
        x='Вы альфа-волк'
    if role=='rock':
        x='Вы камень'
    if role=='seer':
        x='Вы провидец'
    if role=='fool':
        x='Вы провидец'
    if role=='sekta':
        x='Вы секта'
    if role=='dikii':
        x='Вы дикий ребенок'
    if role=='suicide':
        x='Вы самоубийца'
    return x
                   
      
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
  if 'lynch' not in call.data:
    user=None
    for ids in games:
      for idss in games[ids]['players']:
        if games[ids]['players'][idss]['id']==call.from_user.id:
            user=games[ids]['players'][idss]
            yes=0
            for n in games[ids]['players']:
                if games[ids]['players'][n]['number']==int(call.data):
                    yes=1
                    name=games[ids]['players'][n]['name']
            if yes==0:
                user=None
    if user!=None:
        user['target']=int(call.data)
        medit('Выбор принят - '+name, call.from_user.id, call.message.message_id)
  else:
      pass             
     

        
        
        
@bot.message_handler(commands=['forcestart'])
def forcem(m):
  if m.chat.id in games:
    i=0
    x=bot.get_chat_administrators(m.chat.id)
    for z in x:       
        if m.from_user.id==z.user.id:
           i=1
        else:
            if i!=1:
                i=10
    if i==1:
        if m.chat.id in games:
            games[m.chat.id]['timebeforestart']=1
    else:
        bot.send_message(m.chat.id, 'Только администратор может использовать эту команду!')
        
        


 
def creategame(id):
    return {id:{
        'players':{},
        'id':id,
        'todel':[],
        'toedit':[],
        'play':0,
        'xod':0,
        'timebeforestart':300,
        'users':None,
        'userlist':'Игроки:\n\n'
    }
           }


def createuser(id,name):
    return{'id':id,
           'role':None,
           'checked':0,
           'die':0,
           'name':name,
           'number':None,
           'target':None,
           'eaten':0,
           'killed':0,
           'def':0,
           'chlp':0,
           'nothome':0
          }
  
  
if True:
 try:
   print('7777')
   bot.send_message(-1001521640895, 'Бот был перезагружен!')
   bot.polling(none_stop=True,timeout=600)
 except (requests.ReadTimeout):
        print('!!! READTIME OUT !!!')           
        bot.stop_polling()
        time.sleep(1)
        check = True
        while check==True:
          try:
            bot.polling(none_stop=True,timeout=1)
            print('checkkk')
            check = False
          except (requests.exceptions.ConnectionError):
            time.sleep(1)
   
#if __name__ == '__main__':
 # bot.polling(none_stop=True)

#while True:
#    try:
  #      bot.polling()
 #   except:
  #      pass
#    time.sleep(0.1)
       
