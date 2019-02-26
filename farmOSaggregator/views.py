# Import SQLAlchemy ModelView.
from flask_admin.contrib.sqla import ModelView


class FarmView(ModelView):
    """Extend the ModelView class for Farm models."""
