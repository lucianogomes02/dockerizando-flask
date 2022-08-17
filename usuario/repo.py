import abc
from abc import ABC
from sqlalchemy.orm import Session
from aplicacao.db import session
from usuario.orm import UsuarioORM


class RepoLeitura(ABC):
    __db: Session

    @abc.abstractmethod
    def buscar(self):
        pass


class RepoEscrita(ABC):
    __db: Session

    @abc.abstractmethod
    def adicionar(self, **args):
        pass

    @abc.abstractmethod
    def atualizar(self, **args):
        pass

    @abc.abstractmethod
    def deletar(self, **args):
        pass


class UsuarioRepoLeitura(RepoLeitura):
    def __init__(self, db: Session = session):
        self.__db = db

    def buscar(self):
        usuarios = list()
        resultados = self.__db.query(UsuarioORM).all()
        for usuario in resultados:
            usuarios.append(usuario.para_dicionario())
        self.__db.close()
        return usuarios

    def buscar_por_id(self, id_usuario):
        usuario = self.__db.query(UsuarioORM).filter_by(id=id_usuario).one()
        self.__db.close()
        return usuario


class UsuarioRepoEscrita(RepoEscrita):
    def __init__(self, db: Session = session):
        self.__db = db

    def adicionar(self, usuario):
        try:
            self.__db.begin()
            self.__db.add(usuario)
        except Exception as erro:
            self.__db.rollback()
            return erro
        else:
            self.__db.commit()
        finally:
            self.__db.close()

    def atualizar(self, id_usuario, args):
        try:
            self.__db.begin()
            self.__db.query(UsuarioORM).filter_by(id=id_usuario).update({"nome": args.get("nome")})
        except Exception as erro:
            self.__db.rollback()
            return erro
        else:
            self.__db.commit()
        finally:
            self.__db.close()

    def deletar(self, id_usuario):
        try:
            usuario = self.__db.query(UsuarioORM).filter_by(id=id_usuario).one()
            self.__db.delete(usuario)
        except Exception as erro:
            self.__db.rollback()
            return erro
        else:
            self.__db.commit()
        finally:
            self.__db.close()
