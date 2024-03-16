from flask import Flask, request, jsonify,g, render_template
from database import create_tables, generate_user_id, get_db
import os
import datetime


app = Flask(__name__)
UPLOAD_FOLDER = 'static/videos'


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
        return 'Login successfully'
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
    cursor.execute("SELECT * FROM User WHERE User_ID = ? AND password = ? AND position ='normal'", (user_id, password))
    row = cursor.fetchone()
    if row:
        return 'Your position is normal, you cannot check dog info!!!'
    else:
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
            video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
            video_file.save(video_path)
            # Get the current date
            current_date = datetime.date.today().strftime("%d/%m/%Y")
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
    dog_id = request.args.get('dog_id')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Video WHERE dogID = ?", (dog_id,))
    videos = cursor.fetchall()
    conn.close()

    video_data_list = [(video[3], video[2]) for video in videos]

    return render_template('video.html', video_data_list=video_data_list, dog_id=dog_id)

# API路由：创建或更新用户与狗的关联
@app.route('/create_permission', methods=['POST'])
def create_permission():
    user_id = request.form['user_id']
    dog_id = request.form['dog_id']

    conn = get_db()
    cursor = conn.cursor()

    # 检查用户ID是否存在于User表中
    cursor.execute('SELECT * FROM User WHERE User_ID = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'Invalid User ID'})

    # 检查狗ID是否存在于Dog表中
    cursor.execute('SELECT * FROM Dog WHERE dogID = ?', (dog_id,))
    dog = cursor.fetchone()

    if not dog:
        return jsonify({'error': 'Invalid Dog ID'})

    cursor.execute('SELECT * FROM Permission WHERE UserID = ?', (user_id,))
    existing_permission = cursor.fetchone()

    if existing_permission:
        # 用户已存在，更新狗ID
        cursor.execute('UPDATE Permission SET dogID = ? WHERE UserID = ?', (dog_id, user_id))
    else:
        # 创建新的用户-狗关联
        cursor.execute('INSERT INTO Permission (UserID, dogID) VALUES (?, ?)', (user_id, dog_id))

    conn.commit()

    return jsonify({'message': 'Permission updated successfully'})

#End of dog api

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)