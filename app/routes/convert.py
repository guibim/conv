from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import tempfile

#0.1
from app.services.dta_to_csv import convert_dta_to_csv
from app.services.txt_to_csv import convert_txt_to_csv
from app.services.csv_to_txt import convert_csv_to_txt
from app.services.csv_to_json import convert_csv_to_json
from app.services.json_to_csv import convert_json_to_csv
#0.2 
from app.services.csv_to_xml import convert_csv_to_xml
from app.services.xml_to_csv import convert_xml_to_csv
from app.services.csv_to_html import convert_csv_to_html
from app.services.html_to_txt import convert_html_to_txt
from app.services.txt_to_json import convert_txt_to_json
from app.services.json_to_txt import convert_json_to_txt

router = APIRouter()


conversion_map = {
    #0.1
    ("dta", "csv"): convert_dta_to_csv,
    ("txt", "csv"): convert_txt_to_csv,
    ("csv", "txt"): convert_csv_to_txt,
    ("csv", "json"): convert_csv_to_json,
    ("json", "csv"): convert_json_to_csv,
    #0.2
    ("csv", "xml"): convert_csv_to_xml,
    ("xml", "csv"): convert_xml_to_csv,
    ("csv", "html"): convert_csv_to_html,
    ("html", "txt"): convert_html_to_txt,
    ("txt", "json"): convert_txt_to_json,
    ("json", "txt"): convert_json_to_txt,
    
}


@router.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    from_format: str = Form(...),
    to_format: str = Form(...)
):
    # Validação da conversão
    conversion_key = (from_format.lower(), to_format.lower())
    if conversion_key not in conversion_map:
        raise HTTPException(status_code=400, detail="Conversão não suportada.")

    # Verifica se a extensão do arquivo bate com o formato esperado
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext != from_format.lower():
        raise HTTPException(
            status_code=400, 
            detail="Extensão do arquivo não bate com o formato de origem."
        )

    # Cria arquivos temporários
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, f"{uuid.uuid4()}.{from_format}")
    output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.{to_format}")

    # Salva o arquivo recebido
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Chama o serviço de conversão
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
