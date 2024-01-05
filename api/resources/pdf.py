import io

import fitz
from apiflask import APIBlueprint, Schema
from flask import send_file
from marshmallow.fields import String, List, Nested, Integer

from api.schemas.main import PageType

pdf_bp = APIBlueprint("Pdf", __name__, url_prefix="/pdf")


class GetPageTypesIn(Schema):
    pdf_path = String()


class GetPageTypesOut(Schema):
    page_types = List(Nested(PageType))


@pdf_bp.get("/page-types")
@pdf_bp.input(GetPageTypesIn, arg_name="params", location="query")
@pdf_bp.output(GetPageTypesOut)
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

    # Sort the list of page types by the number of sample page numbers in descending order
    page_types.sort(key=lambda x: len(x["page_numbers"]), reverse=True)

    # Assign a type number to each page type; starting from 0
    for index, page_type in enumerate(page_types):
        page_type["type"] = index

    return {"page_types": page_types}


class GetPageImageIn(Schema):
    pdf_path = String()
    page_number = Integer()


@pdf_bp.get("/page-image")
@pdf_bp.input(GetPageImageIn, arg_name="params", location="query")
@pdf_bp.output({}, content_type="image/png")
def get_page_image(params):
    doc = fitz.open(params["pdf_path"])
    page = doc.load_page(params["page_number"] - 1)
    zoom = 1
    mat = fitz.Matrix(zoom, zoom)
    image = page.get_pixmap(matrix=mat).tobytes()
    return send_file(io.BytesIO(image), mimetype="image/png")
