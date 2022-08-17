import abc
from abc import ABC
from sqlalchemy.orm import Session
from aplicacao.db import session
from usuario.orm import UsuarioORM


class RepoLeitura(ABC):
    __db: Session = session

    @abc.abstractmethod
    def buscar(self):
        pass


class RepoEscrita(ABC):
    __db: Session = session

    @abc.abstractmethod
    def adicionar(self):
        pass

    @abc.abstractmethod
    def atualizar(self):
        pass

    @abc.abstractmethod
    def deletar(self):
        pass


class UsuarioRepoLeitura(RepoLeitura):
    def buscar(self):
        usuarios = list()
        resultados = self.__db.query(UsuarioORM).all()
        for usuario in resultados:
            usuarios.append(usuario.para_dicionario())
        session.close()
        return usuarios

    def buscar_por_id(self, id_usuario):
        return session.query(UsuarioORM).filter_by(id=id_usuario).one()

