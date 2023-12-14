from threading import Thread

import webview
from apiflask import APIBlueprint

book_index_bp = APIBlueprint("Book Index", __name__, url_prefix="/book-index")


@book_index_bp.get("/")
@book_index_bp.output({})
def get():
    def run():
        window = webview.active_window()
        save_path = window.create_file_dialog(dialog_type=webview.SAVE_DIALOG, save_filename='test.txt')
        if save_path:
            with open(save_path, 'w') as f:
                f.write('Hello World')

    t = Thread(target=run)
    t.start()

    return ""
