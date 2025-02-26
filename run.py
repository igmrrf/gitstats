from src import create_app
from src.common.db import db

app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
