from email.mime import image
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile
from pathlib import Path
from aiofile import async_open
from uuid import uuid4


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

media = Path("media")
app.mount("/media", StaticFiles(directory=media), name="media")

@app.get('/')
async def index(request: Request, usuario: str = "Felicity Jones"):
    context = {
        "request": request,
        "usuario": usuario,
    }

    return templates.TemplateResponse("index.html", context=context)


@app.get('/servicos')
async def servico(request: Request):
    context = {
        "request": request,
    }

    return templates.TemplateResponse("servicos.html", context=context)


@app.post("/servicos")
async def cad_servicos(request: Request):

    form = await request.form()

    servico: str = form.get("servico")
    # print(f"Serviço: {servico}")

    arquivo: UploadFile = form.get("arquivo")
    # print(f"Nome do aquivo: {arquivo.filename}")
    # print(f"Tipo do arquivo: {arquivo.content_type}")

    # Nome aleatório para arquivo
    arquivo_ext: str = arquivo.filename.split(".")[1]
    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

    async with async_open(f"{media}/{novo_nome}", "wb") as afile:
        await afile.write(arquivo.file.read())


    context = {
        "request": request,
        "imagem": novo_nome,
    }

    return templates.TemplateResponse("servicos.html", context=context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
