import time
from youtubesearchpython import VideosSearch
import telebot
import os
import requests
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyro4 import *
import subprocess
import sys
from database import *

create_database()
api_id = 26312997
api_hash ="aca0fe0dc1fae5c69309a8c04f487cde"
channel_id=-1001818196521 
knownUsers = []
userStep = {}
dic_quality=dict()
check = dict() 
spam=dict() 
lista=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
list_cid_result=dict()
TOKEN= "6606312653:AAF2bcxE6DEhBOG9lkkHQiJKDVsYl0IKDWY"

commands = {
    'start': 'Get used to the bot',
     'help': 'I will help you, Gives you information about the commands'
}


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0



def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(m.chat.id)
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'photo':
            print(m)
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + 'new photo received')



def checking_spam(cid):
    if cid in spam:
        return
    check.setdefault(cid,{})
    check[cid].setdefault('time1',0)
    check[cid].setdefault('time2' ,0)
    check[cid].setdefault('score' ,0)
    if check[cid]['time1']==0:
        check[cid]['time1']=time.time()
    elif check[cid]['time2']==0:
        check[cid]['time2']=time.time()
        timespam=check[cid]['time2']-check[cid]['time1']
        if int(timespam)<3:
           check[cid]['score']+=1
    else:
       check[cid]['time1']=check[cid]['time2']
       check[cid]['time2']=time.time()
       timespam=check[cid]['time2']-check[cid]['time1']
       if int(timespam)<3:
          check[cid]['score']+=1
          if check[cid]['score']==3:
            spam[cid]=time.time()+10
       elif int(timespam)>3:
          if check[cid]['score']==0:
             pass
          else:
             check[cid]['score']-=1


def unspam(cid):
    if cid in spam:
        if spam[cid]<time.time():
            spam.pop(cid)



def page_markup(pages):
    markups = InlineKeyboardMarkup()
    markups.add(InlineKeyboardButton(f'next pages',callback_data=f'next_{pages+1}'),
                InlineKeyboardButton(f'last pages',callback_data=f'last_{max(pages-1,1)}'))
    return markups


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  



@bot.callback_query_handler(func=lambda call: True)
def call_callback_data(call):
    cid = call.message.chat.id
    unspam(cid)
    checking_spam(cid)
    if cid in spam:
        return
    mid = call.message.message_id
    data = call.data
    if data.startswith('next'):
        pages = data.split('_')[1]
        list_page_result=count(list_cid_result[cid],int(pages))
        for results in list_page_result:
            markup= InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(f'Download',callback_data=f"downloading_{results['video_id']}"))
            try:
               bot.send_photo(cid,results['Url'],caption=f"{results['title']}\n,{results['time']}\n,{results['publishedTime']}\n,{results['short']}\n,{results['channel']}", reply_markup=markup)
            except:
               bot.send_message(cid,f"{results['Url']},{results['title']}\n,{results['time']}\n,{results['publishedTime']}\n,{results['short']}\n,{results['channel']}",reply_markup=markup)
        bot.send_message(cid,"pages",reply_markup=page_markup(int(pages)))
    elif data.startswith('last'):
        pages = data.split('_')[1]
        list_page_result=count(list_cid_result[cid],int(pages))
        for results in list_page_result:
            markup= InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(f'Download',callback_data=f"downloading_{results['video_id']}"))
            try:
               bot.send_photo(cid,results['Url'],caption=f"{results['title']}\n,{results['time']}\n,{results['publishedTime']}\n,{results['short']}\n,{results['channel']}", reply_markup=markup)
            except:
               bot.send_message(cid,f"{results['Url']},{results['title']}\n,{results['time']}\n,{results['publishedTime']}\n,{results['short']}\n,{results['channel']}",reply_markup=markup)
        if int(pages)==1:
             markups=InlineKeyboardMarkup()
             markups.add(InlineKeyboardButton(f'next page',callback_data='next_2'))
             bot.send_message(cid,'next page',reply_markup=markups)
        else:
             bot.send_message(cid,"pages",reply_markup=page_markup(int(pages)))
    elif data.startswith('downloading'):
        video_id=data.split('_')[1]
        list_quality=download_video(video_id)
        mark=InlineKeyboardMarkup()
        for i in list_quality:
            dic_quality.setdefault(cid,{})
            dic_quality[cid].setdefault(i['qualityLabel'],i['url'])
            mark.add(InlineKeyboardButton(i['qualityLabel'],callback_data=f"quality_{i['qualityLabel']}_{video_id}"))
        bot.edit_message_reply_markup(cid, mid, reply_markup=mark)
    elif data.startswith('quality'):
        video_id=data.split('_')[2]
        quality=data.split('_')[1]
        list_checked=use_video_id_where(video_id)
        if len(list_checked)>0:
           bot.forward_message(cid,channel_id,list_checked[0][1])
           
        else:
           download_file(dic_quality[cid][quality],video_id)
           result=subprocess.run([sys.executable,"testpro1.py",str(f'{video_id}.mp4')],capture_output=True,text=True)
           os.remove(f'{video_id}.mp4')
           print("Output:",result.stdout)
           print("Errors:",result.stderr)
           mid_video=int(result.stdout)
           insert_youtube(video_id,mid_video)
           bot.forward_message(cid,channel_id,mid_video)
    
    

def count(lista,marhale=1):
      marahel1=marhale*5
      marahel2=marhale*5-5
      marhale3=lista[marahel2:marahel1]
      return marhale3




@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    # unspam(cid)
    # checking_spam(cid)
    if cid in spam:
        return
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, f"Hello, Welcome to my youtube bot , please search the video:")
        userStep[cid]=1
        command_help(m) 
    else:
        command_help(m)
        




@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    # unspam(cid)
    # checking_spam(cid)
    if cid in spam:
        return
    help_text = "The following commands are available: \n"
    for key in commands: 
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)





def search_youtube(query, max_results=30):
       videos_search = VideosSearch(query, limit=max_results)
       results = videos_search.result()['result']
       videos = []
       for video in results:
           if len(video['thumbnails'])>1:
              print(video)
              videos.append({'title': video['title'],
                            'video_id': video['id'],
                            'publishedTime':video['publishedTime'],
                            'short':video['viewCount']['short'],
                            'Url':video['thumbnails'][len(video['thumbnails'])-1]['url'],
                            'channel':video['channel']['name'],
                            'time':video['duration']})
           else:
               videos.append({'title': video['title'],
                            'video_id': video['id'],
                            'publishedTime':video['publishedTime'],
                            'short':video['viewCount']['short'],
                            'Url':video['thumbnails'][0]['url'],
                            'channel':video['channel']['name'],
                            'time':video['duration']})
               
       return videos
       



@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1)
def search_command(m):
       search=m.text
       cid=m.chat.id
       list_res=count(search_youtube(search))
       list_cid_result.setdefault(cid,search_youtube(search))
       for results in list_res:
         markup = InlineKeyboardMarkup()
         markup.add(InlineKeyboardButton(f'Download',callback_data=f"downloading_{results['video_id']}"))
         try:
           bot.send_photo(cid,results['Url'],caption=f"{results['title']}\n,{results['time']}\n,{results['publishedTime']}\n,{results['short']}\n,{results['channel']}", reply_markup=markup)
         except:
           bot.send_message(cid,f"{results['Url']},{results['title']}\n,{results['time']}\n,{results['publishedTime']}\n,{results['short']}\n,{results['channel']}",reply_markup=markup)
       markups=InlineKeyboardMarkup()
       markups.add(InlineKeyboardButton(f'next page',callback_data='next_2'))
       bot.send_message(cid,'next page',reply_markup=markups)




def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f'{local_filename}.mp4' ,'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)



bot.infinity_polling()

