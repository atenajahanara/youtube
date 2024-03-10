import sqlite3

def create_database():
    connect=sqlite3.connect('data.db')
    cursor=connect.cursor()
    cursor.execute('create table if not exists youtube(video_id varchar(50),message_id int(500))')
    connect.commit()
    connect.close()


def insert_youtube(video_id,message_id):
    connect=sqlite3.connect('data.db')
    cursor=connect.cursor()
    cursor.execute(f"""insert into youtube(video_id,message_id)values('{video_id}',{message_id})""")
    connect.commit()
    connect.close()


def use_video_id_where(video_id):
    connect=sqlite3.connect('data.db')
    cursor=connect.cursor()
    cursor.execute(f"""select * from youtube where video_id='{video_id}' """)
    dict_video_id=cursor.fetchall()
    connect.commit()
    connect.close()
    return dict_video_id





create_database()