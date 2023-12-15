from apiflask import APIFlask
from flask_cors import CORS
from flask_socketio import SocketIO

from api.resources.book_index import book_index_bp
from api.resources.pdf import pdf_bp
from api.resources.settings import settings_bp
from api.resources.time import time_bp
from models.base import Base
from nguylinc_python_utils.sqlalchemy import init_sqlite_db

flask_app = APIFlask(__name__, title="SakuinSeizouki API", version="0.1.0", spec_path="/openapi.yaml")
socketio = SocketIO(flask_app, cors_allowed_origins="*")
flask_app.config["SPEC_FORMAT"] = "yaml"
flask_app.config["LOCAL_SPEC_PATH"] = "openapi.yaml"
flask_app.config["SYNC_LOCAL_SPEC"] = True
CORS(flask_app, supports_credentials=False)

flask_app.register_blueprint(time_bp)
flask_app.register_blueprint(book_index_bp)
flask_app.register_blueprint(pdf_bp)
flask_app.register_blueprint(settings_bp)

session = init_sqlite_db(Base)


@socketio.on("connect")
def on_connect():
    print("Client connected!")


if __name__ == "__main__":
    flask_app.run(port=34200, debug=True)
