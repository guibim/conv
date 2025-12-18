import csv
import io
from typing import Iterable, List, Sequence, Union


class CSVEncodingError(Exception):
    pass


_ENCODINGS: Sequence[str] = (
    "utf-8",
    "utf-8-sig",
    "windows-1252",
    "latin-1",
)


def _decode_csv_bytes(csv_bytes: bytes) -> Iterable[List[str]]:
    last_error: Union[UnicodeDecodeError, None] = None

    for encoding in _ENCODINGS:
        try:
            text = csv_bytes.decode(encoding)
            reader = csv.reader(io.StringIO(text))
            return list(reader)
        except UnicodeDecodeError as error:
            last_error = error
            continue

    raise CSVEncodingError(
        "Não foi possível decodificar o arquivo CSV. "
        "Encodings testados: utf-8, utf-8-sig, windows-1252, latin-1."
    ) from last_error


def read_csv_with_fallback(source: Union[str, bytes]) -> List[List[str]]:
    """
    Lê CSV tentando múltiplos encodings.
    Retorna lista de linhas (list[list[str]]).
    Aceita caminhos de arquivo ou conteúdo em bytes.
    """

    if isinstance(source, (bytes, bytearray)):
        return list(_decode_csv_bytes(bytes(source)))

    last_error: Union[UnicodeDecodeError, None] = None

    for encoding in _ENCODINGS:
        try:
            with open(source, "r", newline="", encoding=encoding) as file:
                reader = csv.reader(file)
                return list(reader)
        except UnicodeDecodeError as error:
            last_error = error
            continue

    raise CSVEncodingError(
        "Não foi possível decodificar o arquivo CSV. "
        "Encodings testados: utf-8, utf-8-sig, windows-1252, latin-1."
    ) from last_error
