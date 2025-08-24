from controller.endpoints import app
from database.db_funcs import init_db
import os

debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
