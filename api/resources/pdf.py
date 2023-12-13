import webview
from apiflask import APIBlueprint
from fitz import fitz

from nguylinc_python_utils.pyinstaller import get_bundle_dir

pdf_bp = APIBlueprint("Pdf", __name__, url_prefix="/pdf")


@pdf_bp.post("/")
@pdf_bp.output({})
def post():
    window = webview.active_window()
    file_types = ('PDF Files (*.pdf)',)
    file_path = window.create_file_dialog(dialog_type=webview.OPEN_DIALOG, directory='/', file_types=file_types)

    if file_path:
        doc = fitz.open(str(file_path[0]))
        page_number = 14
        test_page = doc.load_page(page_number - 1)
        rect = fitz.Rect(498, 85, 498 + 334, 85 + 482)
        chars = test_page.get_textbox(rect)
        save_path = get_bundle_dir() + "/test.txt"
        with open(save_path, "w") as f:
            for char in chars:
                if ord(char) > 32:
                    f.write(char)

    return ""
