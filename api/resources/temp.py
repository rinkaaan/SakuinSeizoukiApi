import os
import shutil

from apiflask import APIBlueprint, Schema
from marshmallow.fields import String

from nguylinc_python_utils.pyinstaller import get_bundle_dir

temp_bp = APIBlueprint("Temp", __name__, url_prefix="/temp")


class SaveFileIn(Schema):
    path = String()
    save_path = String()


@temp_bp.post("/save-file")
@temp_bp.input(SaveFileIn, arg_name="params", location="query")
def save_file(params):
    os.makedirs(os.path.dirname(params["save_path"]), exist_ok=True)
    shutil.copyfile(get_bundle_dir() + "/temp/" + params["path"], params["save_path"])
    return {"success": True}
