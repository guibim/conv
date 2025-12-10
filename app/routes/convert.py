from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import tempfile

# Importa os conversores
from app.services.dta_to_csv import convert_dta_to_csv
from app.services.csv_to_dta import convert_csv_to_dta

router = APIRouter()

# Mapa das conversões disponíveis
conversion_map = {
    ("dta", "csv"): convert_dta_to_csv,
    ("csv", "dta"): convert_csv_to_dta,
    # Ex: ("pdf", "jpg"): convert_pdf_to_jpg (futuramente)
}


@router.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    from_format: str = Form(...),
    to_format: str = Form(...)
):
    # Validação: conversão suportada?
    conversion_key = (from_format.lower(), to_format.lower())
    if conversion_key not in conversion_map:
        raise HTTPException(status_code=400, detail="Conversão não suportada.")

    # Validação: extensão do arquivo bate com o tipo informado?
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext != from_format.lower():
        raise HTTPException(status_code=400, detail="Extensão do arquivo não bate com o formato de origem.")

    # Cria arquivos temporários
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, f"{uuid.uuid4()}.{from_format}")
    output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.{to_format}")

    # Salva o arquivo enviado
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Chama a função de conversão apropriada
        conversion_function = conversion_map[conversion_key]
        conversion_function(input_path, output_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao converter: {str(e)}")

    # Retorna o arquivo convertido
    return FileResponse(
        output_path,
        media_type="application/octet-stream",
        filename=f"converted.{to_format}"
    )
