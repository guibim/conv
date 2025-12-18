from app.services.utils.csv_reader import read_csv_with_fallback


def csv_to_markdown(csv_bytes: bytes) -> bytes:
    rows = read_csv_with_fallback(csv_bytes)

    if not rows:
        return b""

    header, *body = rows

    if not header:
        return b""

    md = []
    md.append("| " + " | ".join(header) + " |")
    md.append("| " + " | ".join("---" for _ in header) + " |")

    for row in body:
        md.append("| " + " | ".join(row) + " |")

    return "\n".join(md).encode("utf-8")
