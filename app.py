from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
import os
import shutil
import glob
from src.secrets import JWT_SECRET
import threading
import jwt

# Creates the flask app.
app = Flask(__name__)

# Removes the logging, less overhead.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Generates path to the database file (has to be absolute).
path = ('sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'tmp/database.db')).replace('\\', '/')

app.config['SQLALCHEMY_DATABASE_URI'] = path

# Connects database to app.
db = SQLAlchemy(app)

# Method that injects into the `g` variable the logged in state and the user. This make this information available for each view.
@app.before_request
def inject_user_state():
    from src.api.users import Users

    try:
        token = jwt.decode(request.cookies.get('session'), JWT_SECRET)
        user = Users.query.filter_by(user_id=token['user_id']).first()

        if user == None:
            raise Exception()

        g.user = user
        g.logged_in = True
    except Exception as e:
        g.user = None
        g.logged_in = False

if __name__ == '__main__':
    # Post DB init import.
    from src.api.tools import generate_database
    from src.api.users import users
    from src.routes import routes
    
    # Registers the API blueprints.
    app.register_blueprint(users)
    app.register_blueprint(routes)

    # Replaces temp database with new database.
    generate_database()

    # Remove debug mode once in production.
    app.run(debug=True, host='0.0.0.0', port=80)