from flask import Blueprint, redirect, request, render_template, send_from_directory, g
from src.errors import getLoginErrorMessage
from src.config import MAX_USERS
import random

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    # Simple example of using logged_in feature to change layout.
    if g.logged_in:
        from src.api.users import Users
        from src.api.followers import Followers

        following = [x.to_id for x in Followers.query.filter_by(from_id=g.user.user_id).all()]

        g.following = Users.query.filter(Users.user_id.in_(following)).all()
        g.followers = Users.query.filter(Users.user_id.in_([x.from_id for x in Followers.query.filter_by(to_id=g.user.user_id).all()])).all()

        not_following = Users.query.filter(~Users.user_id.in_(following + [g.user.user_id])).all()

        g.users = random.sample(not_following, k=min(10, len(not_following)))

        if(len(g.followers) > MAX_USERS * 0.75):
            return render_template('app.html', flag='MTL{X55_15_8483}')
        else:
            return render_template('app.html')
    else:
        return render_template('home.html')

@routes.route('/tools')
def tools():
    return render_template('tools.html')

@routes.route('/public/<path:path>')
def public(path):
    return send_from_directory('./public', path)

@routes.route('/login')
def login():
    # If user is already logged in, simply redirect home.
    if g.logged_in:
        return redirect('/')

    error = request.args.get('error')

    # Depending if there is an error or not, change the render.
    if error:
        return render_template('login.html', error_message=getLoginErrorMessage(error))
    else:
        return render_template('login.html')

@routes.route('/logout')
def logout():
    # Logout using the api (simple redirect).
    return redirect('/api/users/logout')