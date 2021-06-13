from models.SA_models import Base

from sqlalchemy import create_engine


def create_db(base, db_name):
    engine = create_engine("sqlite:///" + db_name)
    base.metadata.create_all(engine)


create_db(Base, "project_5")
