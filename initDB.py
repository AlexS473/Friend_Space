from main import app
from models import db, User

db.create_all(app=app)

firstUser = User(username="bob", email="bob@mail.com")
firstUser.set_password("bobpass")
secUser = User(username="Alice", email="alice@mail.com")
secUser.set_password("alicepass")
db.session.add(firstUser)
db.session.add(secUser)
db.session.commit()

print('database initialized!')