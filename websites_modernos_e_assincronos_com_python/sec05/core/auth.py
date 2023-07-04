import hashlib
from typing import Optional

from fastapi import Response

from core.configs import settings


def __gerar_hash_cookie(texto: str) -> str:
    """Função para gerar um hash de uma string usar na cookie"""

    texto = settings.SALTY + str(texto) + "__geek"
    return hashlib.sha512(texto.encode("utf-8")).hexdigest()


def set_auth(response: Response, membro_id: int) -> None:
    """Função q ue adciona um cookie na response do usuário logado"""
    valor_hash: str = __gerar_hash_cookie(str(membro_id))

    # Gerar o valor hexadecimal do membro_id e pega somento a parte que nos interesssa
    membro_id_hex: str = hex(membro_id)[2:]

    # Montar o valor do token
    valor: str = membro_id_hex + "." + valor_hash

    response.set_cookie(key=settings.AUTH_COOKIE_NAME, value=valor,  httponly=True)
