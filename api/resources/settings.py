from threading import Thread

import webview
from apiflask import APIBlueprint, Schema

settings_bp = APIBlueprint("Settings", __name__, url_prefix="/settings")


@settings_bp.post("/app-data-directory")
@settings_bp.output({})
def post():
    def run():
        from api.app import socketio
        window = webview.active_window()
        file_path = window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG, directory='/')
        if file_path:
            print(file_path[0])
            socketio.emit("app-data-directory", file_path[0])

    t = Thread(target=run)
    t.start()

    return ""
