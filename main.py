import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

from models import db, User, Post, UserReact

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
''' End Flask Login Functions '''


def create_app():
	app = Flask(__name__, static_url_path='')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	app.config['SECRET_KEY'] = "MYSECRET"
	#   app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
	CORS(app)
	login_manager.init_app(app)  # uncomment if using flask login
	db.init_app(app)
	return app


app = create_app()

app.app_context().push()

''' End Boilerplate Code '''


@app.route('/')
def login():
	if request.method == 'GET':
		return render_template('index.html')


@app.route('/auth', methods=['POST'])
def authenticate():
	data = request.form.to_dict()
	usernme = data['username']
	password = data['password']
	user = User.query.filter_by(username=usernme).first()
	if user and user.check_password(password):
		flash('Login successful')
		login_user(user)
		return redirect(url_for('index'))
	flash('Invalid credentials')
	return redirect(url_for('login'))


@app.route('/home')
def index():
	return render_template('app.html')


@app.route('/app')
def client_app():
	return app.send_static_file('app.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
