from pytube import YouTube
from pyrogram import Client
import asyncio
from pprint import pprint
channel_id=-1001818196521
api_id = 26312997
api_hash ="aca0fe0dc1fae5c69309a8c04f487cde"
def download_video(video_id):
    """
    دانلود ویدئو با استفاده از شناسه ویدئو
    :param video_id: شناسه ویدئو
    :param save_path: مسیر ذخیره سازی فایل
    """
    yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    test=yt.streaming_data["formats"]
    pprint(test)
    return test


async def main():
    # کد شما اینجا
    
  if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# URL فایل مورد نظر و مسیر محلی برای ذخیره فایل
#file_url = download_video()
#local_filename = "file_name.mp4"

# دانلود فایل
#download_file(file_url, local_filename)
# 