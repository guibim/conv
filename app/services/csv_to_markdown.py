def csv_to_markdown(csv_bytes: bytes) -> bytes:
    csv_text = csv_bytes.decode("utf-8", errors="ignore")
    reader = list(csv.reader(io.StringIO(csv_text)))

    if not reader:
        return b""

    header = reader[0]
    body = reader[1:]

    md = []
    md.append("| " + " | ".join(header) + " |")
    md.append("| " + " | ".join("---" for _ in header) + " |")

    for row in body:
        md.append("| " + " | ".join(row) + " |")

    return "\n".join(md).encode("utf-8")
