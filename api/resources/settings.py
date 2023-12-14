import webview
from apiflask import APIBlueprint
from fitz import fitz

from nguylinc_python_utils.pyinstaller import get_bundle_dir

settings_bp = APIBlueprint("Settings", __name__, url_prefix="/settings")


@settings_bp.post("/")
@settings_bp.output({})
def post():
    window = webview.active_window()
    file_path = window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG, directory='/')
    if file_path:
        doc = fitz.open(str(file_path[0]))
        page_number = 14
        test_page = doc.load_page(page_number - 1)
        x, y = 498, 85
        dx, dy = 334, 482
        rect = fitz.Rect(x, y, x + dx, y + dy)
        chars = test_page.get_textbox(rect)
        save_path = get_bundle_dir() + "/test.txt"
        with open(save_path, "w") as f:
            for char in chars:
                if ord(char) > 32:
                    f.write(char)

    return ""
