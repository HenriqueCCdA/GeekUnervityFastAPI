from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Função para verificar se a senhaa etáa correta, comporando
    a senha em texto puro, informando pelo usuário, ee o hash da
    senha que estará salvo no banco de daados duraante a criação ad conta.
    """
    return CRIPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    """
    Função que geraa e retorna o hash da senha
    """
    return CRIPTO.hash(senha)
