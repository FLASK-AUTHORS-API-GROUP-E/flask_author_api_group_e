# Main entry point of the application
from __init__ import create_app
from database import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
