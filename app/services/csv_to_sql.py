def csv_to_sql(csv_bytes: bytes, table_name="my_table") -> bytes:
    csv_text = csv_bytes.decode("utf-8", errors="ignore")
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)

    if not rows:
        return b""

    columns = rows[0]
    sql_lines = []

    for row in rows[1:]:
        values = [f"'{v.replace(\"'\", \"''\")}'" for v in row]
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
        sql_lines.append(sql)

    return "\n".join(sql_lines).encode("utf-8")
