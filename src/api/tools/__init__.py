from flask import Blueprint, redirect, request, make_response
import os
import glob
import shutil
from src.api.users import Users, generate_users
from src.api.followers import Followers
from app import db

def generate_database():
    # Checks if tmp folder exists.
    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')

    # Checks if there is a database. If so, delete.
    if os.path.exists('./tmp/database.db'):
        os.remove('./tmp/database.db')

    # Creates the new file and closes.
    open('./tmp/database.db', 'w').close()

    # Creates the tables for the models.
    db.create_all()
    db.session.commit()

    generate_users()