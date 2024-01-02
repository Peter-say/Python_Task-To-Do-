from app import app, db  # Import app and db from app.py
from task import create_app

if __name__ == '__main__':
    with app.app_context():
        # Create the database table
        db.create_all()
    create_app().run(debug=True)