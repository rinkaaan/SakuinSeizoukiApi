import os
from threading import Thread, Event

import webview
from flask.cli import load_dotenv

from api.app import flask_app
from nguylinc_python_utils.misc import rename_substring_in_files
from nguylinc_python_utils.pyinstaller import is_pyinstaller, get_path, get_bundle_dir, get_free_port

stop_event = Event()
app_title = "索引製造機"
if is_pyinstaller():
    port = get_free_port()
else:
    port = 34200

if is_pyinstaller():
    load_dotenv(get_path(".env.prod"))
else:
    load_dotenv(".env.dev")


def run_api():
    while not stop_event.is_set():
        flask_app.run(port=port)


if __name__ == '__main__':
    bundle_dir = get_bundle_dir()
    print("Bundle directory:", bundle_dir)
    t = Thread(target=run_api, daemon=True)
    t.start()

    window = webview.create_window(
        app_title,
        url=os.getenv("REACT_APP_URL"),
        maximized=True,
        min_size=(500, 800),
    )

    if is_pyinstaller():
        rename_substring_in_files(bundle_dir + "/static", "http://127.0.0.1:34200", f"http://127.0.0.1:{port}", ["js"])
        webview.start(debug=True, http_server=True, private_mode=False)
    else:
        webview.start(debug=True, http_server=True, private_mode=False)

stop_event.set()
