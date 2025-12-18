from app.services.utils.csv_reader import read_csv_with_fallback


def csv_to_sql(csv_bytes: bytes, table_name="my_table") -> bytes:
    rows = read_csv_with_fallback(csv_bytes)

    if not rows:
        return b""

    columns, *body = rows

    if not columns:
        return b""

    sql_lines = []

    for row in body:
        sanitized_values = [value.replace("'", "''") for value in row[: len(columns)]]
        if len(sanitized_values) < len(columns):
            sanitized_values.extend(["" for _ in range(len(columns) - len(sanitized_values))])
        quoted = [f"'{value}'" for value in sanitized_values]
        sql = (
            f"INSERT INTO {table_name} ({', '.join(columns)}) "
            f"VALUES ({', '.join(quoted)});"
        )
        sql_lines.append(sql)

    return "\n".join(sql_lines).encode("utf-8")
