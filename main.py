from controller.endpoints import app
from database.db_funcs import init_db


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
