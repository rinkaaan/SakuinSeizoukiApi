import os
from threading import Thread, Event

import webview
from flask.cli import load_dotenv

from api.app import flask_app
from nguylinc_python_utils.pyinstaller import is_pyinstaller, get_path, get_bundle_dir

stop_event = Event()
app_title = "索引製造機"
port = 34200

if is_pyinstaller():
    load_dotenv(get_path(".env.prod"))
else:
    load_dotenv(".env.dev")


def run_api():
    while not stop_event.is_set():
        flask_app.run(port=port)


if __name__ == '__main__':
    print("Bundle directory:", get_bundle_dir())
    t = Thread(target=run_api)
    t.start()

    window = webview.create_window(
        app_title,
        url=os.getenv("REACT_APP_URL"),
        maximized=True,
        min_size=(500, 800),
    )

    if is_pyinstaller():
        webview.start(debug=False, http_server=True)
    else:
        webview.start(debug=True, http_server=True)

stop_event.set()
