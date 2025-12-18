from html.parser import HTMLParser


def _read_html_file(input_path: str) -> str:
    encodings = ["utf-8", "utf-8-sig", "windows-1252", "latin-1"]
    last_error = None

    for encoding in encodings:
        try:
            with open(input_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError as error:
            last_error = error
            continue

    raise UnicodeDecodeError("", b"", 0, 1, "Falha ao decodificar HTML") from last_error

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.text.append(cleaned)

def convert_html_to_txt(input_path, output_path):
    parser = TextExtractor()

    parser.feed(_read_html_file(input_path))

    with open(output_path, "w", encoding="utf-8") as txtfile:
        txtfile.write("\n".join(parser.text))
