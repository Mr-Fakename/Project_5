from sqlalchemy import create_engine
import base_model
import users_model, products_model, categories_model, favourites_model


engine = create_engine("sqlite:///" + "project_5_db")
base_model.Base.metadata.create_all(engine)
