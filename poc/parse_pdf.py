from fitz import fitz


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
    rect = fitz.Rect(498, 85, 498 + 334, 85 + 482)

    with open("output.txt", "w") as f:
        chars = test_page.get_textbox(rect)
        for char in chars:
            if ord(char) > 32:
                f.write(char)


if __name__ == "__main__":
    parse_pdf("book.pdf")
