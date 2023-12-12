from threading import Thread, Event

import webview

from api.app import flask_app

stop_event = Event()
app_title = "Flask Pywebview Example"
port = 34200


def run_api():
    while not stop_event.is_set():
        flask_app.run(port=port, debug=False)


if __name__ == '__main__':
    t = Thread(target=run_api, daemon=True)
    t.start()

    window = webview.create_window(
        app_title,
        "static/index.html",
        width=500,
        height=800,
        min_size=(500, 800),
    )

    webview.start(debug=True, http_server=True)

stop_event.set()
