from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from typing import Type


## https://github.com/pallets-eco/flask-sqlalchemy/issues/1312#issuecomment-1975386404
class Base(DeclarativeBase, MappedAsDataclass):
    pass

class ProperlyTypedSQLAlchemy(SQLAlchemy):
    #Temporary type hinting workaround for Flask SQLAlchemy.

    #This is a temporary workaround for the following issue:
    #https://github.com/pallets-eco/flask-sqlalchemy/issues/1312
    #This workaround may not be correct.
    Model: Type[Base]

