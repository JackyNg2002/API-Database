from flask import Flask, request, jsonify,g, render_template
from database import create_tables, generate_user_id, get_db
import os
from datetime import datetime
import shutil


app = Flask(__name__)
UPLOAD_FOLDER = 'static/videos'

UPLOAD_MAPS = 'static/maps'
app.config['UPLOAD_MAPS'] = UPLOAD_MAPS

UPLOAD_VIDEOS = 'static/VIDEOS'
app.config['UPLOAD_VIDEOS'] = UPLOAD_VIDEOS

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request
def initialize_db():
    with app.app_context():
        create_tables()

@app.before_request
def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)



@app.route('/')
def index():
    return render_template('test.html')


# Start of user api
#for register
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    position = request.form['position']
    password = request.form['password']

    if position not in ['manager', 'admin', 'normal']:
        return 'Invalid position'

    user_id = generate_user_id()
    cursor = get_db().cursor()
    cursor.execute("INSERT INTO User (User_ID, name, position, password) VALUES (?, ?, ?, ?)",
                   (user_id, name, position, password))
    get_db().commit()

    return f'User registered successfully. User ID: {user_id}'

#for login
@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['User_ID']
    password = request.form['password']

    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM User WHERE User_ID = ? AND password = ?", (user_id, password))
    row = cursor.fetchone()

    if row:
        user = {
            'user_id': row['User_ID'],
            'name': row['name'],
            'position': row['position']
        }
        return 'Login successfully, welcome ' + user_id + " your position is " + user['position']
    else:
        return 'Invalid user credentials'

#for change_password
@app.route('/change_password', methods=['POST'])
def change_password():
    user_id = request.form['User_ID']
    old_password = request.form['old_password']
    new_password = request.form['new_password']

    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM User WHERE User_ID = ? AND password = ?", (user_id, old_password))
    row = cursor.fetchone()

    if row:
        cursor.execute("UPDATE User SET password = ? WHERE User_ID = ?", (new_password, user_id))
        get_db().commit()
        return 'Password changed successfully'
    else:
        return 'Invalid user credentials'

#for delete_account
@app.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = request.form['User_ID']
    password = request.form['password']

    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM User WHERE User_ID = ? AND password = ?", (user_id, password))
    row = cursor.fetchone()

    if row:
        cursor.execute("DELETE FROM User WHERE User_ID = ?", (user_id,))
        get_db().commit()
        return 'Account deleted successfully'
    else:
        return 'Invalid user credentials'
    
# End of user api
    
#Start of dog api 
#for create_dog  
@app.route('/create_dog', methods=['POST'])
def create_dog():
    data = request.form
    dogID = data['dogID']
    name = data['name']
    detail = data['detail']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Dog WHERE dogID=?', (dogID,))
    existing_dog = cursor.fetchone()

    if existing_dog:
        return 'Dog with the given ID already exists'
    else:
        
        cursor.execute('INSERT INTO Dog (dogID, name, detail) VALUES (?, ?, ?)', (dogID, name, detail))
        conn.commit()
        return f'Dog data inserted successfully. Dog ID: {dogID}'

#for dog info  
@app.route('/info_dog', methods=['GET'])
def info_dog():
    user_id = request.args.get('User_ID')
    password = request.args.get('password')

    cursor = get_db().cursor()
    
    cursor.execute("SELECT * FROM User WHERE User_ID = ? AND password = ? AND (position ='admin' OR position ='manager')", (user_id, password))
    row = cursor.fetchone()
    if row:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Dog')
        dogs = cursor.fetchall()

        dog_list = []
        if dogs:
            for dog in dogs:
                dog_data = {
                    'dogID': dog[0],
                    'name': dog[1],
                    'detail': dog[2]
                }
                dog_list.append(dog_data)

        return jsonify(dog_list)
    else:
        return 'You do not have permission to check dog info !!!'

#for update_dog  
@app.route('/update_dog', methods=['POST'])
def update_dog():
    data = request.form
    dogID = data['dogID']
    name = data['name']
    detail = data['detail']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Dog WHERE dogID=?', (dogID,))
    existing_dog = cursor.fetchone()

    if existing_dog:
        
        cursor.execute('UPDATE Dog SET name=?, detail=? WHERE dogID=?', (name, detail, dogID))
        conn.commit()
        return f'Dog data updated successfully. Dog ID: {dogID}'
    else:
        return 'Dog with the given ID does not exist'
    
#End of dog api

#Start of video api
#for upload_video
@app.route('/upload_video', methods=['POST'])
def upload_video():
    video_file = request.files['video']
    dog_id = request.form['dog_id']

    if video_file:
        
        # Generate video ID
        cursor = get_db().cursor()
        
        # Add the video details to the database
        # Check if the dog ID exists in the Dog table
        cursor.execute("SELECT COUNT(*) FROM Dog WHERE dogID = ?", (dog_id,))
        dog_exists = cursor.fetchone()[0]

        if dog_exists:
            # Add the video details to the database
            # Save the video file to a folder
            video_folder = os.path.join(app.config['UPLOAD_VIDEOS'], dog_id)
            os.makedirs(video_folder, exist_ok=True)
            
            video_path = os.path.join(video_folder, video_file.filename)
            video_file.save(video_path)
            # Get the current date
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Video")
            video_count = cursor.fetchone()[0] + 1
            video_id = f"V{video_count:03}"
            cursor.execute("INSERT INTO Video (videoID, dogID, datetime, videoSrc) VALUES (?, ?, ?, ?)", (video_id, dog_id, current_date, video_path))
            conn.commit()

            return 'Video uploaded successfully!'
        else:
            return 'Dog id not found.'

    else:
        return 'No video file provided.'

#for search_videos
@app.route('/search_videos', methods=['GET'])
def search_videos():
    user_id = request.args.get('User_ID')
    password = request.args.get('password')
    dog_id = request.args.get('dog_id')

    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM User WHERE User_ID = ? AND password = ? AND (position ='admin' OR position ='manager')", (user_id, password))
    row = cursor.fetchone()
    if row:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Video WHERE dogID = ?", (dog_id,))
        videos = cursor.fetchall()
        conn.close()

        if videos:
            video_data_list = [(video[3], video[2]) for video in videos]
            return render_template('video.html', video_data_list=video_data_list, dog_id=dog_id)
        else:
            return 'Error dogID, cannot found the dog!!!'
        
    else:
        return 'You do not have permission to search videos !!!'

# API路由：创建或更新用户与狗的关联
@app.route('/create_permission', methods=['POST'])
def create_permission():
    user_id = request.form['user_id']
    password = request.form['password']
    target_user_id = request.form['target_user_id']
    dog_id = request.form['dog_id']

    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM User WHERE User_ID = ? AND password = ? AND position ='normal'", (user_id, password))
    row = cursor.fetchone()

    if row:
        conn = get_db()
        cursor = conn.cursor()

        # 检查用户ID是否存在于User表中
        cursor.execute('SELECT * FROM User WHERE User_ID = ?', (target_user_id,))
        target_user = cursor.fetchone()

        if not target_user:
            return 'Invalid User ID'

        # 检查狗ID是否存在于Dog表中
        cursor.execute('SELECT * FROM Dog WHERE dogID = ?', (dog_id,))
        dog = cursor.fetchone()

        if not dog:
            return 'Invalid Dog ID'

        cursor.execute('SELECT * FROM Permission WHERE UserID = ?', (user_id,))
        existing_permission = cursor.fetchone()

        if existing_permission:
            # 用户已存在，更新狗ID
            cursor.execute('UPDATE Permission SET dogID = ? WHERE UserID = ?', (dog_id, user_id))
        else:
            # 创建新的用户-狗关联
            cursor.execute('INSERT INTO Permission (UserID, dogID) VALUES (?, ?)', (user_id, dog_id))

        conn.commit()

        return 'Permission updated successfully'
    else:
        
        return 'You do not have permission to create permission !!!'
        
#End of dog api
# 定义路由，处理上传文件的请求
@app.route('/upload_maps', methods=['POST'])
def upload_maps():
    # 获取上传的文件列表
    files = request.files.getlist('files')

    # 获取用户输入的狗的ID
    dog_id = request.form['dog_id']
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Dog WHERE dogID=?', (dog_id,))
    existing_dog = cursor.fetchone()

    if existing_dog:
    # 创建狗的文件夹
        dog_folder = os.path.join(app.config['UPLOAD_MAPS'], dog_id)
        os.makedirs(dog_folder, exist_ok=True)
        # 遍历文件列表
        # 遍历文件列表
        for file in files:
            # 生成唯一的文件名
            filename = dog_id + '_' + file.filename
            filepath = os.path.join(dog_folder, filename)

            # 保存文件到指定路径
            file.save(filepath)
            
            # 将文件信息插入数据库
            
            map_id = os.path.splitext(filename)[0]
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            map_src = filepath

            # 检查数据库中是否已存在相同的狗ID和文件夹
            cursor = get_db().cursor()
            cursor.execute("SELECT mapID, mapSrc FROM Map WHERE dogID = ? AND mapID = ?", (dog_id, map_id))
            existing_map = cursor.fetchone()

            if existing_map:
                cursor.execute("UPDATE Map SET mapSrc = ? WHERE dogID = ? AND mapID = ?", (map_src, dog_id, map_id))
                get_db().commit()
            else:
                # 执行插入操作
                cursor.execute("INSERT INTO Map (mapID, dogID, datetime, mapSrc) VALUES (?, ?, ?, ?)",
                            (map_id, dog_id, current_datetime, map_src))
            
                get_db().commit()
            

        return 'Files uploaded successfully.'
    else:
        return 'no this dog'

@app.route('/delete_maps', methods=['POST'])
def delete_maps():
    user_id = request.form['user_id']
    password = request.form['password']
    dog_id = request.form['dog_id']
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM User WHERE User_ID = ? AND password = ? AND (position ='admin' OR position ='manager')", (user_id, password))
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM Map WHERE dogID = ?", (dog_id,))
        get_db().commit()
        # 删除文件夹及其内容
        folder_path = os.path.join(app.config['UPLOAD_MAPS'], dog_id)
        shutil.rmtree(folder_path)
        return dog_id + ' Map folder deleted successfully'
    else: 
        return 'You do not have permission to delete maps !!!'

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)