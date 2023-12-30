import json
import re

import fitz

from poc.parse_xlsx import read_cells_downwards


def parse_pdf(pdf_path, json_path):
    # Open and read the JSON file
    with open(json_path, "r") as file:
        data = json.loads(file.read())

    # Dictionary to store page number and content
    page_contents = {}

    # Dictionary to hold words and the pages they appear on
    word_pages = {}

    missing_pages = []

    pdf_path = data["createIndexIn"]["pdfPath"]
    list_path = data["createIndexIn"]["listPath"]
    sheet_name = data["createIndexIn"]["sheetName"]
    start_cell = data["createIndexIn"]["startCell"]
    end_cell = data["createIndexIn"]["endCell"]

    doc = fitz.open(pdf_path)

    # Process each page type
    for page_type, details in data["createIndexIn"]["pageTypes"].items():
        page_numbers = details["page_numbers"]
        for page_number in page_numbers:
            page = doc.load_page(page_number - 1)
            current_group_index = -1
            content = ""

            for annotation in details["annotations"]:
                x, y = annotation["x"], annotation["y"]
                width, height = annotation["width"], annotation["height"]
                rect = fitz.Rect(x, y, x + width, y + height)
                chars = page.get_textbox(rect)

                if annotation["groupIndex"] == current_group_index:
                    is_first_annotation = False
                else:
                    is_first_annotation = True
                    current_group_index = annotation["groupIndex"]
                    finished_group = False

                if finished_group:
                    continue
                if is_first_annotation:
                    content = "".join(char for char in chars if ord(char) > 32)
                else:
                    actual_page_number = re.sub(r"[^0-9]", "", chars)
                    if actual_page_number and content:
                        page_contents[int(actual_page_number)] = content
                        finished_group = True

    words = read_cells_downwards(list_path, sheet_name, start_cell, end_cell)

    # for each word, iterate through the pages and check if the word is in the page content and update the word_pages dictionary
    # for each page, also combine contents of next page to see if word is being split across pages
    for word in words:
        word_pages[word] = []
        for page_number, content in page_contents.items():
            # remember char length of current page
            # concatenate content of next page to current page
            # check if word is in the concatenated content and that it's start index is less than the char length of current page

            current_page_char_length = len(content)

            if page_number + 1 in page_contents:
                content = content + page_contents[page_number + 1]
            if word in content and content.index(word) < current_page_char_length:
                word_pages[word].append(page_number)

    # check if any pages are missing; set range from 1 to max of all keys in page_contents
    for page_number in range(1, max(page_contents.keys()) + 1):
        if page_number not in page_contents:
            missing_pages.append(page_number)

    return page_contents, word_pages, missing_pages


if __name__ == "__main__":
    page_contents, word_pages, missing_pages = parse_pdf("book.pdf", "createIndex2.json")
    # print(page_contents[50])
    print(word_pages)
    print(missing_pages)
