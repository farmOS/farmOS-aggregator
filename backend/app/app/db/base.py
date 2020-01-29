# Import all the schemas, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.farm import Farm
from app.models.farm_token import FarmToken
