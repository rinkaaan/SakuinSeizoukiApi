import os
import sys

from apiflask import APIFlask
from flask import send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

from api.resources.pdf import pdf_bp
from api.resources.project import project_bp
from api.resources.word_list import word_list_bp
from nguylinc_python_utils.pyinstaller import is_pyinstaller, get_bundle_dir

# flask_app = APIFlask(__name__, title="SakuinSeizouki API", version="0.1.0", spec_path="/openapi.yaml", docs_ui="elements")
flask_app = APIFlask(__name__, title="SakuinSeizouki API", version="0.1.0", spec_path="/openapi.yaml", docs_ui="rapidoc")
socketio = SocketIO(flask_app, cors_allowed_origins="*")
flask_app.config["SPEC_FORMAT"] = "yaml"
flask_app.config["LOCAL_SPEC_PATH"] = "openapi.yaml"
flask_app.config["SYNC_LOCAL_SPEC"] = True
CORS(flask_app, supports_credentials=False)

flask_app.register_blueprint(project_bp)
flask_app.register_blueprint(pdf_bp)
flask_app.register_blueprint(word_list_bp)


@flask_app.route("/temp/<path:path>")
def send_file(path):
    return send_from_directory(get_bundle_dir() + "/temp", path)


@socketio.on("connect")
def on_connect():
    print("Client connected!")


if is_pyinstaller():
    port = int(sys.argv[1])
else:
    port = 34200

BASE_URL = "http://127.0.0.1:" + str(port)

if __name__ == "__main__":
    bundle_dir = get_bundle_dir()
    print("Bundle directory:", bundle_dir)
    os.makedirs(os.path.join(bundle_dir, "temp"), exist_ok=True)
    if is_pyinstaller():
        flask_app.run(port=port, debug=False)
    else:
        flask_app.run(port=port, debug=True)
