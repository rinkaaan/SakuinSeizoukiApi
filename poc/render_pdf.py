from fitz import fitz


def render_pdf():
    doc = fitz.open("book.pdf")
    page_number = 14
    test_page = doc.load_page(page_number - 1)

    # print width and height of page
    width, height = test_page.mediabox_size
    print("width: ", width)
    print("height: ", height)

    # # write text to file
    # with open("output.txt", "w") as f:
    #     chars = test_page.get_text()
    #     for char in chars:
    #         if ord(char) > 32:
    #             f.write(char)

    # # write image of page to file
    # zoom = 1
    # mat = fitz.Matrix(zoom, zoom)
    # pix = test_page.get_pixmap(matrix=mat)
    # pix.save("output.png")


if __name__ == "__main__":
    render_pdf("book.pdf")
