import sys

from apiflask import APIFlask
from flask_cors import CORS
from flask_socketio import SocketIO

from api.resources.settings import settings_bp
from api.resources.time import time_bp
from models.base import Base
from nguylinc_python_utils.pyinstaller import is_pyinstaller, get_bundle_dir
from nguylinc_python_utils.sqlalchemy import SessionManager

flask_app = APIFlask(__name__, title="SakuinSeizouki API", version="0.1.0", spec_path="/openapi.yaml")
socketio = SocketIO(flask_app, cors_allowed_origins="*")
flask_app.config["SPEC_FORMAT"] = "yaml"
flask_app.config["LOCAL_SPEC_PATH"] = "openapi.yaml"
flask_app.config["SYNC_LOCAL_SPEC"] = True
CORS(flask_app, supports_credentials=False)

flask_app.register_blueprint(time_bp)
flask_app.register_blueprint(settings_bp)

session = SessionManager(Base)


@socketio.on("connect")
def on_connect():
    print("Client connected!")


if is_pyinstaller():
    port = int(sys.argv[1])
else:
    port = 34200

if __name__ == "__main__":
    bundle_dir = get_bundle_dir()
    print("Bundle directory:", bundle_dir)
    if is_pyinstaller():
        flask_app.run(port=port, debug=False)
    else:
        flask_app.run(port=port, debug=True)
