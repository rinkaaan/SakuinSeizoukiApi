from apiflask import APIFlask
from flask_cors import CORS

from api.resources.time.api import time_bp

flask_app = APIFlask(__name__, title="Flask Pywebview Example API", version="0.1.0", spec_path="/openapi.yaml")
flask_app.config["SPEC_FORMAT"] = "yaml"
flask_app.config["LOCAL_SPEC_PATH"] = "openapi.yaml"
CORS(flask_app, supports_credentials=False)

flask_app.register_blueprint(time_bp)

if __name__ == "__main__":
    flask_app.run(port=34200, debug=True)
