import os
from threading import Thread

import webview
from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Boolean

settings_bp = APIBlueprint("Settings", __name__, url_prefix="/settings")


@settings_bp.post("/app-data-directory")
@settings_bp.output({})
def select_app_data_directory():
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


class AppDataDirectoryValidateIn(Schema):
    app_data_directory = String()


class AppDataDirectoryValidateOut(Schema):
    valid = Boolean()


@settings_bp.post("/app-data-directory/validate")
@settings_bp.input(AppDataDirectoryValidateIn, arg_name="data")
@settings_bp.output(AppDataDirectoryValidateOut)
def validate_app_data_directory(data):
    return {
        "valid": os.path.isdir(data["app_data_directory"])
    }
