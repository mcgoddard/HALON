from flask import Flask, render_template, request, redirect, escape, session, url_for, flash

import database, hashlib, models, time, datetime, json

from database import db_session

from models import User, Message, Tile, Character

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    if 'username' in session:
        thisuser = User.query.filter(User.username == session['username']).first()
        messages = Message.query.all()
        now = datetime.datetime.now()
        thisuser.active_until = now + datetime.timedelta(seconds = 30)
        db_session.commit()
        active_users = User.query.filter(User.active_until > datetime.datetime.now())
        if thisuser.character != None:
            return render_template('play.html', name = session['username'], messages = messages, users = active_users, now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), thisuser = thisuser)
        else:
            hal = Character.query.filter(Character.name == 'HAL').first()
            if User.query.filter(User.character == hal).first() != None:
                characters = Character.query.filter(Character.name != 'HAL').all()
                return render_template('choose_character.html', name = session['username'], messages = messages, users = active_users, now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), characters = characters)
            else:
                character = Character.query.filter(Character.name == 'HAL').first()
                thisuser.character = character
                thisuser.x = 50
                thisuser.y = 50
                thisuser.health = character.max_health
                thisuser.direction = 1
                thisuser.moving = False
                db_session.commit()
                return render_template('play.html', name = session['username'], messages = messages, users = active_users, now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return render_template('index.html')

@app.route('/interact')
def interact():
    if 'username' in session:
        thisuser = User.query.filter(User.username == session['username']).first()
        if thisuser != None:
            interactionX = -1;
            interactionY = -1;
            if thisuser.direction == 1:
                interactionX = int(thisuser.x/100)
                interactionY = int((thisuser.y+20)/100)
            elif thisuser.direction == 2:
                interactionX = int((thisuser.x-20)/100)
                interactionY = int(thisuser.y/100)
            elif thisuser.direction == 3:
                interactionX = int((thisuser.x+20)/100)
                interactionY = int(thisuser.y/100)
            elif thisuser.direction == 4:
                interactionX = int(thisuser.x/100)
                interactionY = int((thisuser.y-20)/100)
            else:
                return 'direction error'
            tile = Tile.query.filter(Tile.x == interactionX, Tile.y == interactionY).first()
            if tile != None:
                now = datetime.datetime.now()
                tile.next_change = now + datetime.timedelta(seconds = thisuser.character.decode_time)
                db_session.commit()
                return 'completed'
            else:
                return 'tile not found'
        return 'no user'
    return 'not logged in'

@app.route('/move')
def move():
    if 'username' in session:
        thisuser = User.query.filter(User.username == session['username']).first()
        if thisuser != None:
            direction = int(request.args.get('direction'))
            if direction > 0 and direction < 5:
                if thisuser.direction == direction:
                    thisuser.moving = True
                else:
                    thisuser.moving = False
                    thisuser.direction = direction
                db_session.commit()
                return 'completed'
            return 'direction not detected'
        return 'no user'
    return 'not logged in'

@app.route('/change_character', methods=['GET', 'POST'])
def change_character():
    if 'username' in session:
        thisuser = User.query.filter(User.username == session['username']).first()
        if request.method == 'GET':
            thisuser.character = None
            db_session.commit()
        elif request.method == 'POST':
            character_id = request.form['character_id']
            character = Character.query.filter(Character.id == character_id).first()
            if character != None and character.name != 'HAL':
                thisuser.character = character
                thisuser.x = 150
                thisuser.y = 150
                thisuser.health = character.max_health
                thisuser.direction = 1
                thisuser.moving = False
                db_session.commit()
            else:
                flash('Select a valid character!','danger')
    return redirect(url_for('index'))

def update_frame():
    users = User.query.all()
    for user in users:
        if user.moving:
            if user.direction == 1:
                newY = user.y + user.character.speed
                tile = Tile.query.filter(int((newY + 16)/100) == Tile.y, int(user.x/100) == Tile.x).first()
                if int((newY + 16)/100) < 10 and tile != None and (tile.tile_type > 5 or (tile.tile_type == 4 and tile.status == 0)):
                    user.y = newY
            elif user.direction == 2:
                newX = user.x - user.character.speed
                tile = Tile.query.filter(int((newX - 16)/100) == Tile.x, int(user.y/100) == Tile.y).first()
                if int((newX - 16)/100) >= 0 and tile != None and (tile.tile_type > 5 or (tile.tile_type == 4 and tile.status == 0)):
                    user.x = newX
            elif user.direction == 3:
                newX = user.x + user.character.speed
                tile = Tile.query.filter(int((newX + 16)/100) == Tile.x, int(user.y/100) == Tile.y).first()
                if int((newX + 16)/100) < 10 and tile != None and (tile.tile_type > 5 or (tile.tile_type == 4 and tile.status == 0)):
                    user.x = newX
                user.x += user.character.speed
            elif user.direction == 4:
                newY = user.y - user.character.speed
                tile = Tile.query.filter(int((newY - 16)/100) == Tile.y, int(user.x/100) == Tile.x).first()
                if int((newY - 16)/100) >= 0 and tile != None and (tile.tile_type > 5 or (tile.tile_type == 4 and tile.status == 0)):
                    user.y = newY
            db_session.commit()
    tiles = Tile.query.all()
    for tile in tiles:
        if tile.next_change != None:
            if tile.next_change < datetime.datetime.now():
                tile.next_change = None
                if tile.status == 0:
                    tile.status = 1
                else:
                    tile.status = 0
                db_session.commit()

@app.route('/update')
def update():
    if 'username' in session:
        last_update = request.args.get('last_update','')
        if last_update != '':
            try:
                last_datetime = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
                thisuser = User.query.filter(User.username == session['username']).first()
                now = datetime.datetime.now()
                thisuser.active_until = now + datetime.timedelta(seconds = 30)
                db_session.commit()
                new_messages = Message.query.filter(Message.created_at > last_datetime)
                parsed_new_messages = []
                for message in new_messages:
                    parsed_new_messages.append(dict([("username", message.user.username), ("text", message.text), ("created_at", message.created_at.strftime('%Y-%m-%d %H:%M:%S'))]))
                active_users = User.query.filter(User.active_until > datetime.datetime.now())
                parsed_active_users = []
                for user in active_users:
                    parsed_active_users.append(dict([("username", user.username), ("x", user.x), ("y", user.y), ("direction", user.direction), ("moving", user.moving), ("character_id", user.character_id)]))
                parsed_thisuser = dict([("username", thisuser.username), ("direction", thisuser.direction), ("x", thisuser.x), ("y", thisuser.y), ("health", thisuser.health), ("moving", thisuser.moving), ("character_id", thisuser.character_id), ("max_health", thisuser.character.max_health)])
                tiles = Tile.query.all()
                parsed_tiles = []
                for tile in tiles:
                    parsed_tiles.append(dict([("x", tile.x), ("y", tile.y), ("tile_type", tile.tile_type), ("status", tile.status)]))
                result = dict([("new_messages", parsed_new_messages), ("active_users", parsed_active_users), ("last_updated", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), ("thisuser", parsed_thisuser), ("tiles", parsed_tiles)])
                return json.dumps(result)
            except ValueError:
                return ""
    return ""

@app.route('/send_message')
def sendMessage():
    if 'username' in session:
        message = request.args.get('message','')
        thisuser = User.query.filter(User.username == session['username']).first()
        if message != '':
            new_message = Message(message, thisuser)
            db_session.add(new_message)
            db_session.commit()
    return ""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
        if request.method == 'POST':
            salt = "fewnoi*hduw&Sqywe"
            if User.query.filter(User.username == request.form['username'], User.password == hashlib.sha512(request.form['password'] + salt).hexdigest()).first() != None:
                flash('Login successful!','success')
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                flash('No user found matching that username and password!','danger')
                return redirect(url_for('login'))
        return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' not in session:
        if request.method == 'POST':
            if User.query.filter(User.username == request.form['username']).first() == None:
                salt = "fewnoi*hduw&Sqywe"
                u = User(request.form['username'], hashlib.sha512(request.form['password']+salt).hexdigest())
                db_session.add(u)
                db_session.commit()
                session['username'] = request.form['username']
                flash('Account created!','success')
                return redirect(url_for('index'))
            else:
                flash('That username is taken!','danger')
        return render_template('signup.html')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'tEt90^}\F:|k1`lyZ.-*!i{gVd"*^qbl-SfR)\&p<*K*u!n5:k/Z>&mX.|"D2]@'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)