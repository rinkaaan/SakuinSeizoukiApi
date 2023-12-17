import os
from threading import Thread

import webview
from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Boolean

settings_bp = APIBlueprint("Settings", __name__, url_prefix="/settings")


class SetAppDataDirectoryIn(Schema):
    app_data_directory = String()


class SetAppDataDirectoryOut(Schema):
    valid = Boolean()


@settings_bp.post("/app-data-directory")
@settings_bp.input(SetAppDataDirectoryIn, arg_name="data")
@settings_bp.output(SetAppDataDirectoryOut)
def set_app_data_directory(data):
    from api.app import session
    success = True

    if not os.path.isdir(data["app_data_directory"]):
        success = False

    try:
        session.update(os.path.join(data["app_data_directory"], "sqlite.db"))
    except Exception:
        success = False

    return {
        "valid": success
    }
