import json
import fitz  # PyMuPDF


def parse_pdf(pdf_path, json_path):
    # Open and read the JSON file
    with open(json_path, "r") as file:
        data = json.loads(file.read())

    # Open the PDF document
    doc = fitz.open(pdf_path)

    # Dictionary to store page number and content
    page_contents = {}

    # Process each page type
    for page_type, details in data["createIndexIn"]["pageTypes"].items():
        for page_number in details["page_numbers"]:
            if page_number == 14:
                print("here")
            else:
                continue
            # Load the page
            page = doc.load_page(page_number - 1)
            page_content = ""

            # Process each annotation
            for annotations in details["annotations"].values():
                annotation_rect = annotations[0]
                # Scale down the rectangle coordinates
                scaled_rect = fitz.Rect(annotation_rect["x"] / 3, annotation_rect["y"] / 3, (annotation_rect["x"] + annotation_rect["width"]) / 3, (annotation_rect["y"] + annotation_rect["height"]) / 3)

                # Extract the text from the annotation rectangle
                annotation_content = page.get_textbox(scaled_rect)

                # Filter out chars with ord value less than 32
                # for char in annotation_content:
                #     if ord(char) > 32:
                #         page_content += char
                annotation_content = "".join(char for char in annotation_content if ord(char) > 32)

                # Append the annotation content to the page content
                page_content += annotation_content

            # Store the content with the page number as the key
            page_contents[page_number] = page_content

    return page_contents


if __name__ == "__main__":
    contents = parse_pdf("book.pdf", "createIndex.json")
    print(contents[14])
