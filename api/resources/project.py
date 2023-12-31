import io

import fitz
import openpyxl
from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Integer, List, Nested, Dict
from flask import send_file

project_bp = APIBlueprint("Project", __name__, url_prefix="/project")


class OpenPdfIn(Schema):
    pdf_path = String()


class PdfPageType(Schema):
    width = Integer()
    height = Integer()
    page_numbers = List(Integer())
    type = Integer()


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

    # Sort the list of page types by the number of sample page numbers in descending order
    page_types.sort(key=lambda x: len(x["page_numbers"]), reverse=True)

    # Assign a type number to each page type; starting from 0
    for index, page_type in enumerate(page_types):
        page_type["type"] = index

    return {"page_types": page_types}


class GetPdfPageIn(Schema):
    pdf_path = String()
    page_number = Integer()


@project_bp.get("/get/pdf/page")
@project_bp.input(GetPdfPageIn, arg_name="params", location="query")
@project_bp.output({}, content_type="image/png")
def get_pdf_page(params):
    doc = fitz.open(params["pdf_path"])
    page = doc.load_page(params["page_number"] - 1)
    zoom = 1
    mat = fitz.Matrix(zoom, zoom)
    image = page.get_pixmap(matrix=mat).tobytes()
    return send_file(io.BytesIO(image), mimetype="image/png")


class Annotation(Schema):
    x = Integer()
    y = Integer()
    width = Integer()
    height = Integer()
    group_index = Integer()


class CreateIndexIn(Schema):
    pdf_path = String()
    list_path = String()
    sheet_name = String()
    start_cell = String()
    end_cell = String()
    page_types = Dict(String(), Nested(Annotation))


class CreateIndexOut(Schema):
    page_contents = List(String())
    word_pages = Dict(String(), List(Integer()))
    missing_pages = List(Integer())


@project_bp.post("/create/index")
@project_bp.input(CreateIndexIn, arg_name="params")
@project_bp.output(CreateIndexOut)
def create_index(params):
    print(params)
    return {
        "page_contents": [],
        "word_pages": {},
        "missing_pages": [],
    }


class GetWordListIn(Schema):
    word_list_path = String()
    sheet_name = String()
    start_cell = String()
    end_cell = String()


class GetWordListOut(Schema):
    word_list = List(String())


@project_bp.get("/get/word/list")
@project_bp.input(GetWordListIn, arg_name="params", location="query")
@project_bp.output(GetWordListOut)
def get_word_list(params):
    word_list_path = params["word_list_path"]
    sheet_name = params["sheet_name"]
    start_cell = params["start_cell"]
    end_cell = params["end_cell"]

    # Load the workbook and select the specified sheet
    workbook = openpyxl.load_workbook(word_list_path)
    sheet = workbook[sheet_name]

    # Initialize an empty list to store cell values
    cell_values = []

    # Define the end row for reading
    end_row = sheet.max_row if end_cell is None else sheet[end_cell].row

    # Iterate through the cells in the specified column from start_cell to end_cell
    for row in range(sheet[start_cell].row, end_row + 1):
        cell = sheet[f"{start_cell[0]}{row}"]
        if (cell.value is None) or (cell.value == ""):
            continue
        cell_values.append(str(cell.value))

    return {"word_list": cell_values}
