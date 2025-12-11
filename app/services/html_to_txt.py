from html.parser import HTMLParser

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

    with open(input_path, "r", encoding="utf-8") as file:
        parser.feed(file.read())

    with open(output_path, "w", encoding="utf-8") as txtfile:
        txtfile.write("\n".join(parser.text))
