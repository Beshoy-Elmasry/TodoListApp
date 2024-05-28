from TodoList import db , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60) , nullable = False)
    todos = db.relationship('Todo', backref = 'author' , lazy = True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(100) , nullable = True)
    achived = db.Column(db.Boolean , default = False , nullable = True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
