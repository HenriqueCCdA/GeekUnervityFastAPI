from fastapi.requests import Request
from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.membro_model import MembroModel
from controllers.base_controller import BaseController


class MembroController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, MembroModel)

    async def post_crud(self) -> None:
        # Recebe dados do form
        form = await self.request.form()

        nome: str = form.get('nome')
        funcao: str = form.get('funcao')
        imagem: UploadFile = form.get('imagem')
        email: str = form.get('email')
        senha: str = form.get('senha') # Falta adicionar hash

        # Nome aleatório para a imagem
        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        # Instanciar o objeto
        membro: MembroModel = MembroModel(nome=nome, funcao=funcao, imagem=novo_nome, email=email, senha=senha)

        # Fazer o upload do arquivo
        async with async_open(f"{settings.MEDIA}/membro/{novo_nome}", "wb") as afile:
            await afile.write(imagem.file.read())

        # Cria a sessão e insere no banco de dados
        async with get_session() as session:
            session.add(membro)
            await session.commit()


    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            membro: MembroModel = await session.get(self.model, obj.id)

            if membro:
                # Recebe os dados do form
                form = await self.request.form()

                nome: str = form.get('nome')
                funcao: str = form.get('funcao')
                imagem: UploadFile = form.get('imagem')
                email: str = form.get('email')
                senha: str = form.get('senha') # Falta adicionar hash

                if nome and nome != membro.nome:
                    membro.nome = nome
                if funcao and funcao != membro.funcao:
                    membro.funcao = funcao
                if email and email != membro.email:
                    membro.email = email
                if senha and senha != membro.senha:
                    membro.senha = senha # falta add hash
                if imagem.filename:
                    # Gera um nome aleatório
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"
                    membro.imagem = novo_nome
                    # Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/{novo_nome}", "wb") as afile:
                        await afile.write(imagem.file.read())
                await session.commit()
