import os
import uuid

import fitz
from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Integer, List, Nested

from nguylinc_python_utils.pyinstaller import get_bundle_dir

project_bp = APIBlueprint("Project", __name__, url_prefix="/project")


class OpenPdfIn(Schema):
    pdf_path = String()


class PdfPageType(Schema):
    width = Integer()
    height = Integer()
    sample_urls = List(String())


class OpenPdfOut(Schema):
    pages = List(Nested(PdfPageType))


@project_bp.post("/new/pdf")
@project_bp.input(OpenPdfIn, arg_name="params")
@project_bp.output(OpenPdfOut)
def open_pdf(params):
    from api.app import BASE_URL
    doc = fitz.open(params["pdf_path"])
    page_number = 14
    test_page = doc.load_page(page_number - 1)

    # x, y = 498, 85
    # dx, dy = 334, 482
    # rect = fitz.Rect(x, y, x + dx, y + dy)
    # chars = test_page.get_textbox(rect)
    # save_path = get_bundle_dir() + "/test.txt"
    # with open(save_path, "w") as f:
    #     for char in chars:
    #         if ord(char) > 32:
    #             f.write(char)

    zoom = 2
    mat = fitz.Matrix(zoom, zoom)
    pix = test_page.get_pixmap(matrix=mat)
    filename = uuid.uuid4()
    save_path = os.path.join(get_bundle_dir(), "temp", f"{filename}.png")
    pix.save(save_path)

    return {
        "pages": [
            {
                "width": test_page.mediabox_size[0],
                "height": test_page.mediabox_size[1],
                "sample_urls": [
                    f"{BASE_URL}/temp/{filename}.png"
                ]
            }
            # for page_number, page in enumerate(doc)
        ]
    }
