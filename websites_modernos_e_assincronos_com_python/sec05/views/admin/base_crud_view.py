from datetime import datetime

from fastapi import APIRouter, status
from fastapi.routing import APIRoute
from fastapi.responses import Response
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.base_controller import BaseController



class BaseCrudView:

    def __init__(self, template_base: str) -> None:
        self.template_base: str = template_base

        self.router = APIRouter()

        base = self.template_base

        self.router.routes.append(APIRoute(path=f'/{base}/list', endpoint=self.object_list, methods=["GET",], name=f"{base}_list"))
        self.router.routes.append(APIRoute(path=f'/{base}/create', endpoint=self.object_create, methods=["GET", "POST"], name=f"{base}_create"))
        self.router.routes.append(APIRoute(path=f'/{base}/details/'+'{obj_id:int}', endpoint=self.object_edit, methods=["GET",], name=f"{base}_details"))
        self.router.routes.append(APIRoute(path=f'/{base}/edit/'+'{obj_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name=f"{base}_edit"))
        self.router.routes.append(APIRoute(path=f'/{base}/delete/'+'{obj_id:int}', endpoint=self.object_delete, methods=["DELETE",], name=f"{base}_delete"))



    async def object_create(self) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        raise NotImplementedError("Você precisa implementar este método.")


    async def object_edit(self) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar um objeto [GET, POST]
        """
        raise NotImplementedError("Você precisa implementar este método.")


    async def object_list(self, object_controller: BaseController) -> Response:
        """
        Rota para listar todos os objetos [GET]
        """
        dados = await object_controller.get_all_crud()

        context = {"request": object_controller.request, "ano": datetime.now().year, "dados": dados}

        return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/list.html", context=context)


    async def object_delete(self, object_controller: BaseController, obj_id: int) -> Response:
        """
        Rota para deletar um objeto [DELETE]
        """
        objeto = await object_controller.get_one_crud(id_obj=obj_id)

        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await object_controller.del_crud(id_obj=objeto.id)


        return Response(object_controller.request.url_for(f"{self.template_base}_list"))


    async def object_details(self, object_controller: BaseController, obj_id: int) -> Response:
        """
        Rota para apresentar os detalhes de um objeto [GET]
        """
        objeto = await object_controller.get_one_crud(id_obj=obj_id)

        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        context = {"request": object_controller.request, "ano": datetime.now().year, "objeto": objeto}

        if 'details' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/details.html", context=context)

        elif 'edit' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/edit.html", context=context)

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
