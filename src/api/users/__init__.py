from flask import Blueprint, redirect, request, make_response, g
from sqlalchemy import update
from app import db
from src.errors import LOGIN_ERROR
import hashlib
from src.secrets import PASSWORD_SALT, JWT_SECRET
from src.api.followers import Followers, generate_followers
from src.config import MAX_USERS
import random
import string
import jwt

users = Blueprint('users', __name__, url_prefix='/api/users')

# Simple password hashing using SHA256 + Salting.
def salted_sha256(password: str) -> str:
    m = hashlib.sha256()
    m.update((password + PASSWORD_SALT).encode('utf-8'))
    return m.hexdigest()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    status = db.Column(db.String)

    @property
    def init_password(self):
        # Asserts that there is an init_password.
        raise AttributeError('Password not readable')
    
    @init_password.setter
    def init_password(self, init_password):
        self.password = salted_sha256(init_password)

    def check_password(self, password):
        return self.password == salted_sha256(password)

ALPHABET = string.ascii_letters + string.digits
NAMES = [name.lower() for name in open('./data/users.txt').readlines()]
STATUS = open('./data/status.txt').readlines()

def generate_password():
    return ''.join(random.choice(ALPHABET) for _ in range(20))

def generate_username():
    return random.choice(NAMES).strip() + str(random.randint(0, 5000))

def generate_status():
    return random.choice(STATUS)

def generate_users():
    for _ in range(MAX_USERS):
        db.session.add(Users(username=generate_username(), init_password=generate_password(), status=generate_status()))

    db.session.commit()

    generate_followers()

# Generates a JWT Token using a JWT_SECRET and redirects the user home.
def generate_session(user_id: int) -> str:
    response = make_response(redirect('/'))
    response.set_cookie('session', jwt.encode({'user_id': user_id}, JWT_SECRET, algorithm='HS256'), httponly=True)
    return response

# Attempts to read the information from the session.
# If it fails, it simply redirects home.
@users.route('/me', methods=['GET'])
def me():
    try:
        return jwt.decode(request.cookies.get('session'), JWT_SECRET, algorithm='HS256')
    except:
        return redirect('/')

@users.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Gets user with same useraname.
    user = Users.query.filter_by(username=username).first()

    # If the user is none or the password is incorrect, throw error.
    if user == None or not user.check_password(password):
        return redirect('/login?error=' + LOGIN_ERROR.INVALID_USERNAME_PASSWORD.value)
    else:
        return generate_session(user.user_id)

@users.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Checks if there is already a user with the current name.
    if Users.query.filter_by(username=username).first():
        return redirect('/login?error=' + LOGIN_ERROR.USERNAME_EXIST.value)
    else:
        # Adds the user to the database then creates a session token.
        user = Users(username=username, init_password=password)
        db.session.add(user)
        db.session.commit()
        return generate_session(user.user_id)

@users.route('/logout', methods=['GET'])
def logout():
    # Simply revokes session token.
    response = make_response(redirect('/'))
    response.delete_cookie('session')
    return response

@users.route('/status', methods=['POST'])
def update_status():
    if g.user:
        g.user.status = request.form.get('status')
        db.session.commit()

    return redirect('/')

@users.route('/follow/<id>', methods=['GET'])
def follow(id):
    if g.user and not g.user.user_id == int(id):
        db.session.add(Followers(from_id=g.user.user_id, to_id=id))
        db.session.commit()
    return redirect('/')

@users.route('/random/<key>')
def random_user(key):
    if key == 'Dn92meSg5p':
        return generate_session(random.randint(1, MAX_USERS + 1))
    else:
        return redirect('/fail')