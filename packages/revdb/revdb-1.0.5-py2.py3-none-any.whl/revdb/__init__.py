"""a light layer for revtel mongodb"""

__version__ = "1.0.5"

from revdb.db import Model, StrictModel, collection_factory, connect, make_model_class

__all__ = ["make_model_class", "connect", "Model", "StrictModel", "collection_factory"]
