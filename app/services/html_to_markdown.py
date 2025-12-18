from html.parser import HTMLParser

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
    parser.feed(html_bytes.decode("utf-8", errors="ignore"))
    return "".join(parser.out).strip().encode("utf-8")
