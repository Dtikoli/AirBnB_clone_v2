#!/usr/bin/python3
""" This module defines a base class for all models in our hbnb clone """
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

Base = declarative_base()


class BaseModel:
    """Defines the class BaseModel.
    Attributes:
        id (sqlalchemy String): BaseModel id.
        created_at (sqlalchemy DateTime): datetime at creation.
        updated_at (sqlalchemy DateTime): datetime of last update.
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize an instance of BaseModel.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pair of attributes.
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    val = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, val)

    def save(self):
        """Updates updated_at with the current datetime."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        rep_dict = self.__dict__.copy()
        rep_dict["__class__"] = str(type(self).__name__)
        rep_dict["created_at"] = self.created_at.isoformat()
        rep_dict["updated_at"] = self.updated_at.isoformat()
        rep_dict.pop("_sa_instance_state", None)
        return rep_dict

    def delete(self):
        """Deletes the current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """Returns an str representation of the BaseModel instance."""
        dic = self.__dict__.copy()
        dic.pop("_sa_instance_state", None)
        return f"[{type(self).__name__}] ({self.id}) {dic}"
