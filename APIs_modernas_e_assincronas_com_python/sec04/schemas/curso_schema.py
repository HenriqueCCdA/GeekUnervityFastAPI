from typing import Optinal

from pydantic import BaseModel as SCBaseModel


class CursoSchema(SCBaseModel):
    id: Optinal[int]
    titulo: str
    aulas: int
    horas: int

    class Config:
        orm_mode = True
