import openpyxl


def read_cells_downwards(filename, sheet_name, start_cell, end_cell):
    # Load the workbook and select the specified sheet
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook[sheet_name]

    # Initialize an empty list to store cell values
    cell_values = []

    # Define the end row for reading
    end_row = sheet.max_row if end_cell is None else sheet[end_cell].row

    # Iterate through the cells in the specified column from start_cell to end_cell
    for row in range(sheet[start_cell].row, end_row + 1):
        cell = sheet[f"{start_cell[0]}{row}"]
        cell_values.append(str(cell.value))

    return cell_values


if __name__ == "__main__":
    # Example usage
    file = "/Users/nguylinc/Desktop/list.xlsx"
    cells = read_cells_downwards(file, "Sheet1", "A2", "A377")
    print(cells)
