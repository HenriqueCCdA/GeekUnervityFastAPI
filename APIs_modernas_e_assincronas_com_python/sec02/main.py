from fastapi import FastAPI


app = FastAPI()


@app.get("/mensagem")
async def mensagem():
    return {"msg": "FastAPI na Geek University"}
