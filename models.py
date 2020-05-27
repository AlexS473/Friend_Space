from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def toDict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(280), nullable=False)  # Same length as twitter
    reacts = db.relationship('UserReact')


    def getTotalLikes(self):
        numLikes = 0
        for r in self.reacts:
            if r == "like":
                numLikes += 1
        return numLikes

    def getTotalDislikes(self):
        numDislikes = 0
        for r2 in self.reacts:
            if r2 == "dislike":
                numDislikes += 1
        return numDislikes

    def getusername(self):
        name = User.query(User.username).filter_by(userId=self.userId).first()
        return name

    def toDict(self):
        return {
            'userId': self.userId,
            'username': self.getusername(),  # TODO: somehow fetch username
            'text': self.text,
            'likes': self.getTotalLikes(),
            'dislikes': self.getTotalDislikes()
        }


class UserReact(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    react = db.Column(db.String(10), nullable=False)
