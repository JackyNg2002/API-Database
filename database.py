from flask import g
import sqlite3
import uuid
from flask import Flask

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON;')
    return db

def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                    User_ID TEXT PRIMARY KEY,
                    name TEXT,
                    position TEXT CHECK (position IN ('manager', 'admin', 'normal')),
                    password TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Dog (
                    dogID TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    detail TEXT
                    )''')
 
    
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Video (
                        videoID TEXT PRIMARY KEY,  
                        dogID INTEGER NOT NULL,
                        datetime TEXT NOT NULL,
                        videoSrc TEXT NOT NULL,
                        FOREIGN KEY (dogID) REFERENCES Dog (dogID)                                        
                    )
                    ''')
    
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Map (
                            mapID TEXT PRIMARY KEY,
                            dogID INTEGER NOT NULL,
                            datetime TEXT NOT NULL,
                            mapSrc TEXT NOT NULL,
                            FOREIGN KEY (dogID) REFERENCES Dog (dogID)
                        )
                    ''')
    
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Permission (
                            UserID TEXT PRIMARY KEY,
                            dogID TEXT NOT NULL,
                            FOREIGN KEY (dogID) REFERENCES Dog (dogID),
                            FOREIGN KEY (UserID) REFERENCES User (User_ID)
                        )
                    ''')
    
    conn.commit()  

def generate_user_id():
    cursor = get_db().cursor()
    cursor.execute("SELECT COUNT(*) FROM User")
    count = cursor.fetchone()[0]
    user_id = 'U' + str(count + 1).zfill(3)
    return user_id

with app.app_context():
    
    conn = get_db()
    cursor = conn.cursor()
    
    
    
    conn.commit()
    cursor.execute("SELECT * FROM Map")
    maps = cursor.fetchall()

    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM Dog")
    dogs = cursor.fetchall()
    
    
    cursor.execute("SELECT * FROM Map")
    maps = cursor.fetchall()

    cursor.execute("SELECT * FROM Video")
    videos = cursor.fetchall()

    cursor.execute("SELECT * FROM Permission")
    permissions = cursor.fetchall()

    for user in users:
        
        user_id = user["User_ID"]
        name = user["name"]
        position = user["position"]
        password = user["password"]
        
        print(f"User_ID: {user_id}, name: {name}, position: {position}, password: {password}")

    #show dog data
    for dog in dogs:
        
        dogID = dog["dogID"]
        name = dog["name"]
        detail = dog["detail"]
        
        
        print(f"dogID: {dogID}, name: {name}, detail: {detail}")

    for map in maps:
        
        user_id = map["mapID"]
        name = map["dogID"]
        position = map["datetime"]
        password = map["mapSrc"]
        
        print(f"User_ID: {user_id}, name: {name}, position: {position}, password: {password}")

    for video in videos:
        
        video_id = video["videoID"]
        dog_id = video["dogID"]
        datetime = video["datetime"]
        video_src = video["videoSrc"]
        
        print(f"Video ID: {video_id}, Dog ID: {dog_id}, Datetime: {datetime}, Video Src: {video_src}")