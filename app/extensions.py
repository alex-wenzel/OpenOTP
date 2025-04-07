from flask_sqlalchemy import SQLAlchemy
from app.models import Base, ProperlyTypedSQLAlchemy
from typing import cast

## SQLAlchemy
db = SQLAlchemy(model_class=Base)
db = cast(ProperlyTypedSQLAlchemy, db)