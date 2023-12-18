import json

import fitz
from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Integer, List, Nested

project_bp = APIBlueprint("Project", __name__, url_prefix="/project")


class OpenPdfIn(Schema):
    pdf_path = String()


class PdfPageType(Schema):
    width = Integer()
    height = Integer()
    page_numbers = List(Integer())


class OpenPdfOut(Schema):
    page_types = List(Nested(PdfPageType))


@project_bp.post("/new/pdf")
@project_bp.input(OpenPdfIn, arg_name="params")
@project_bp.output(OpenPdfOut)
def open_pdf(params):
    doc = fitz.open(params["pdf_path"])

    # Initialize an empty dictionary to store page types and their sample page numbers
    page_types = {}

    # Loop through all pages in the document
    for page_number, page in enumerate(doc):
        # Get the current page's width and height; rounded up
        page_width = int(round(page.mediabox_size[0]))
        page_height = int(round(page.mediabox_size[1]))

        # Check if the current page size exists in the `page_types` dictionary
        if (page_width, page_height) not in page_types:
            # Create a new entry for the current page size
            page_types[(page_width, page_height)] = {
                "width": page_width,
                "height": page_height,
                "page_numbers": [],
            }

        # Append the current page number to the sample page numbers for the current page size
        page_types[(page_width, page_height)]["page_numbers"].append(page_number + 1)

    # Convert the dictionary of page types to a list of page types
    page_types = list(page_types.values())

    return {"page_types": page_types}
