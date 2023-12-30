import openpyxl


def read_cells_downwards(filename, sheet_name, start_cell):
    # Load the workbook and select the specified sheet
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook[sheet_name]

    # Initialize an empty list to store cell values
    cell_values = []

    # Iterate through the cells in the specified column starting from the start_cell row
    for row in range(sheet[start_cell].row, sheet.max_row + 1):
        cell = sheet[f"{start_cell[0]}{row}"]
        if cell.value is None:
            break  # Stop if a blank cell is encountered
        cell_values.append(str(cell.value))

    return cell_values


if __name__ == "__main__":
    cells = read_cells_downwards("list.xlsx", "Sheet1", "A2")
    print(cells)
