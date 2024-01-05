import openpyxl
from apiflask import APIBlueprint, Schema
from marshmallow.fields import String, List

word_list_bp = APIBlueprint("Word List", __name__, url_prefix="/word-list")


class GetWordListIn(Schema):
    word_list_path = String()
    sheet_name = String()
    start_cell = String()
    end_cell = String()


class GetWordListOut(Schema):
    word_list = List(String())


@word_list_bp.get("/")
@word_list_bp.input(GetWordListIn, arg_name="params", location="query")
@word_list_bp.output(GetWordListOut)
def get_word_list(params):
    word_list_path = params["word_list_path"]
    sheet_name = params["sheet_name"]
    start_cell = params["start_cell"]
    end_cell = params["end_cell"]

    return {"word_list": parse_word_list(word_list_path, sheet_name, start_cell, end_cell)}


def parse_word_list(word_list_path, sheet_name, start_cell, end_cell):
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

    return cell_values
