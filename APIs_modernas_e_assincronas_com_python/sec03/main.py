from typing import Optional

from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Response,
    Path,
    Query,
    Header,
)

from models import Curso

app  = FastAPI()


cursos = {
    1:  {
        "titulo": "Programação para Leigos",
        "aulas": 112,
        "horas": 58,
    },
    2:  {
        "titulo": "Algoritmos e Lógica de Programação",
        "aulas": 87,
        "horas": 67,
    },
}

@app.get("/cursos")
async def get_cursos():
    return cursos


@app.get("/cursos/{curso_id}")
async def get_curso(
    curso_id: int = Path(
        default=None,
        title="ID do curso",
        description="Deve ser entre 1 e 2",
        gt=0,
        lt=3,
    )
):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não  encontrado.")


@app.post("/cursos", status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso


@app.put("/cursos/{curso_id}")
async def put_curso(curso_id: int, curso: Curso):
    if curso_id  in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe um curso com id {curso_id}",
        )


@app.delete("/cursos/{curso_id}")
async def delete_curso(curso_id: int):
    print(curso_id)
    if curso_id in cursos:
        del cursos[curso_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe um curso com id {curso_id}",
        )


@app.get("/calculadora")
async def calcular(
    a: int = Query(default=None, gt=5),
    b: int = Query(default=None, gt=10),
    c: Optional[int] = None,
    x_geek: str = Header(default=None),
):
    soma = a + b
    if c:
        soma += c
    print(f'X-GEEK: {x_geek}')
    return {"resultado": soma}


if __name__  == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
