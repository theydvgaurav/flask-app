import datetime
import uuid
from enum import Enum

from sqlalchemy import inspect

from databases.extensions import db


class ApplicationBaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {c.key: self._get_value(c) for c in inspect(self).mapper.column_attrs}

    def _get_value(self, column):
        value = getattr(self, column.key)
        if isinstance(value, (uuid.UUID,)):
            return str(value)
        elif isinstance(value, (datetime.date, datetime.datetime)):
            return value.isoformat()
        elif isinstance(value, Enum):
            return value.name
        return value
