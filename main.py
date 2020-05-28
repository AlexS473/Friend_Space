# 816001671 Web Programming and Technologies 1 Final May 2020
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError

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
    CORS(app)
    login_manager.init_app(app)
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
        return redirect(url_for('loadhome'))
    flash('Invalid credentials')
    return redirect(url_for('login'))


# Code previously used for project ref: https://flask-login.readthedocs.io/en/latest/
@login_manager.unauthorized_handler
def unauthorized():
    flash('You\'ve got to login first.')
    return redirect(url_for('login'))


@app.route('/myfriendspace', methods=['GET'])
@login_required
def loadhome():
    posts = Post.query.all()
    posts = posts[::-1]  # Lists the last post added first
    posts = [p.toDict() for p in posts]
    return render_template("app.html", posts=posts)


@app.route('/myfriendspace', methods=['POST'])
@login_required
def createpost():
    newpost = request.form.to_dict()
    u_id = current_user.id
    content = newpost['posttext']
    if content == "":
        flash('You gotta add words buddy.')
        return redirect(url_for('loadhome'))
    addpost = Post(userId=u_id, text=content)
    try:
        db.session.add(addpost)
        db.session.commit()
        flash('New Post added!')
        return redirect(url_for('loadhome'))
    except IntegrityError:
        db.session.rollback()
        flash('Oops something went wrong.')
        return redirect(url_for('loadhome'))


@app.route('/myfriendspace/like/<pid>', methods=['GET'])
@login_required
def likepost(pid):
    newlike = UserReact(userId=current_user.id, postId=pid, react="like")
    try:
        db.session.add(newlike)
        db.session.commit()
        return redirect(url_for('loadhome'))
    # If the post already has a reaction from this user it will be updated:
    except IntegrityError:
        db.session.rollback()
        UserReact.query.filter_by(postId=pid, userId=current_user.id).update(dict(react="like"))
        db.session.commit()
        return redirect(url_for('loadhome'))


@app.route('/myfriendspace/dislike/<pid>', methods=['GET'])
@login_required
def dislikepost(pid):
    newdislike = UserReact(userId=current_user.id, postId=pid, react="dislike")
    try:
        db.session.add(newdislike)
        db.session.commit()
        return redirect(url_for('loadhome'))
    # If the post already has a reaction from this user it will be updated:
    except IntegrityError:
        db.session.rollback()
        UserReact.query.filter_by(postId=pid, userId=current_user.id).update(dict(react="dislike"))
        db.session.commit()
        return redirect(url_for('loadhome'))


@app.route('/myfriendspace/delete/<pid>', methods=['GET'])
@login_required
def deletepost(pid):
    post = Post.query.filter_by(id=pid).first()
    db.session.delete(post)
    db.session.commit()
    flash('Posted deleted.')
    return redirect(url_for('loadhome'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
