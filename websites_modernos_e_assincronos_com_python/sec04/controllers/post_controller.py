from typing import List

from fastapi.requests import Request
from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.post_model import PostModel
from controllers.base_controller import BaseController


class PostController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, PostModel)

    async def post_crud(self) -> None:
        # Recebe dados do form
        form = await self.request.form()

        titulo: str = form.get('titulo')
        tags: List[str] = form.getlist('tag')
        imagem: UploadFile = form.get('imagem')
        texto: str = form.get('texto')
        obj_id: int = form.get('autor')

        # Nome aleatório para a imagem
        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        # Instanciar o objeto
        post: PostModel = PostModel(titulo=titulo, imagem=novo_nome, texto=texto, id_autor=int(obj_id))

        # Busca e adiciona as tags
        for id_tag in tags:
            tag = await self.get_tag(id_tag=int(id_tag))
            post.tags.append(tag)

        # Fazer o upload do arquivo
        async with async_open(f"{settings.MEDIA}/post/{novo_nome}", "wb") as afile:
            await afile.write(imagem.file.read())

        # Cria a sessão e insere no banco de dados
        async with get_session() as session:
            session.add(post)
            await session.commit()


    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            post: PostModel = await session.get(self.model, obj.id)

            if post:
                # Recebe os dados do form
                form = await self.request.form()

                titulo: str = form.get('titulo')
                tags: List[str] = form.getlist('tag')
                imagem: UploadFile = form.get('imagem')
                texto: str = form.get('texto')
                obj_id: int = form.get('autor')

                if titulo and titulo != post.titulo:
                    post.titulo = titulo
                if tags:
                    # Se houver tags, zeramos as presentes no post
                    post.tags = []
                    await session.commit()
                    # Busca e adiciona as tags
                    for id_tag in tags:
                        tag = await self.get_tag(id_tag=int(id_tag))
                        # Operação para juntar o objeto tag que vem de outra
                        # sessão com o objeto post que está nesta sessão.
                        tag_local = await session.merge(tag)
                        post.tags.append(tag_local)
                if texto and texto != post.texto:
                    post.texto = texto
                if obj_id and obj_id != post.autor.id:
                    post.id_autor = int(obj_id)
                if imagem.filename:
                    # Gera um nome aleatório
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"
                    post.imagem = novo_nome
                    # Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/post/{novo_nome}", "wb") as afile:
                        await afile.write(imagem.file.read())
                await session.commit()
