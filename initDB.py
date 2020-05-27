from main import app
from models import db, User

db.create_all(app=app)

firstUser = User(username = "bob", password = "bobpass", email = "bob@mail.com")
secUser = User(username = "Alice", password = "alicepass", email = "alice@mail.com")
db.session.add(firstUser)
db.session.add(secUser)
db.session.commit()

print('database initialized!')