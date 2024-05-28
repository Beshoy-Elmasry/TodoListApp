from TodoList import app , db
from flask import current_app

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)