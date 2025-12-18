from html.parser import HTMLParser


def _decode_html(html_bytes: bytes) -> str:
    encodings = ["utf-8", "utf-8-sig", "windows-1252", "latin-1"]
    last_error = None

    for encoding in encodings:
        try:
            return html_bytes.decode(encoding)
        except UnicodeDecodeError as error:
            last_error = error
            continue

    raise UnicodeDecodeError("", b"", 0, 1, "Falha ao decodificar HTML") from last_error

class SimpleHTMLToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "p":
            self.out.append("\n\n")
        elif tag == "br":
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")

    def handle_data(self, data):
        self.out.append(data)

def html_to_markdown(html_bytes: bytes) -> bytes:
    parser = SimpleHTMLToMarkdown()
    parser.feed(_decode_html(html_bytes))
    return "".join(parser.out).strip().encode("utf-8")
