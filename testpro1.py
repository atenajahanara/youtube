from pytube import YouTube 
from pyrogram import Client 
from database import *
from pprint import pprint 
import sys

channel_id=-1001818196521 
api_id = 26312997 
api_hash ="aca0fe0dc1fae5c69309a8c04f487cde"


def upl(local_filename):
    #print('local_filename',f'{local_filename}.mp4')
    with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
      file=app.send_video(channel_id ,local_filename)
    print(file.id)

localfilename=sys.argv[1]

upl(localfilename)