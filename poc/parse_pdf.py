from fitz import fitz
import re

# [{'height': 1453, 'width': -986, 'x': 1230, 'y': 248}, {'height': 42, 'width': 50, 'x': 285, 'y': 1711}]


def parse_pdf():
    doc = fitz.open("book.pdf")
    page_number = 14
    test_page = doc.load_page(page_number - 1)

    # for index, page in enumerate(doc.pages()):
    #     print("page: ", page)
    #     # text = page.get_text()
    #     # print(text)
    #
    #     # get text within rectangle
    #     # top left = 498, 85
    #     # width height = 334, 482
    #     rect = fitz.Rect(498, 85, 498 + 334, 85 + 482)
    #
    #     with open("output.txt", "w") as f:
    #         chars = page.get_textbox(rect)
    #         for char in chars:
    #             if ord(char) > 32:
    #                 f.write(char)
    #
    #     if index == 1:
    #         break

    # get text within rectangle
    # top left = 498, 85
    # width height = 334, 482

    # x, y = 1230 / 3, 248 / 3
    # width, height = -986 / 3, 1453 / 3

    # x, y = 244 / 3, 248 / 3
    # width, height = 1453 / 3, 986 / 3

    # x, y = 86, 85
    # width, height = 334, 482

    # left page content
    # x, y = 82, 69
    # width, height = 329, 499

    # left page number
    x, y = 95, 571
    width, height = 17, 13

    rect = fitz.Rect(x, y, x + width, y + height)

    content = ""
    chars = test_page.get_textbox(rect)

    # for char in chars:
    #     if ord(char) > 32:
    #         content += char

    content = re.sub(r"[^0-9]", "", chars)

    print(content)


if __name__ == "__main__":
    parse_pdf()
