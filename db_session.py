import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None
__engine = None


def global_init():
    global __factory

    if __factory:
        return

    conn_str = 'postgresql://postgres:1234@localhost:5432/library'
    print(f"Подключение к базе данных по адресу {conn_str}")

    __engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=__engine)

    # noinspection PyUnresolvedReferences
    from models import books
    from models import authors
    from models import publishers

    SqlAlchemyBase.metadata.create_all(__engine)


def create_session() -> Session:
    global __factory
    return __factory()


def get_engine():
    global __engine
    return __engine
