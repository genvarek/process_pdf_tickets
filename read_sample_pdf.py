from helpers import sanitize_string, extract_key_value
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox
from pprint import pprint
from docbarcodes.extract import process_document


def handle_unpaired_data(line: str, data: dict, reading_notes_rect: bool) -> dict:
    if reading_notes_rect:
        data["NOTES"] = line
    else:
        data[line] = line
    return data


def pdf_to_dict(filepath: str) -> dict:
    """Return the content of a pdf file in the dict format"""
    barcodes_raw = process_document(filepath)[0]
    data = {
        'barcodes': [barcodes_raw]
    }
    for page in extract_pages(filepath):
        reading_notes_rect = False

        for element in page:
            if not isinstance(element, LTTextBox):
                continue

            line = element.get_text()
            if ":" in line:
                key, value = extract_key_value(line)
                data[key] = value
                if "NOTES" in line:
                    reading_notes_rect = True

            else:
                line = sanitize_string(line)
                data = handle_unpaired_data(line, data, reading_notes_rect)

        return data


# Paste the path to the pdf file, for example "files/reference.pdf"
path_to_file = ''
pdf_data = pdf_to_dict(path_to_file)
pprint(pdf_data)
