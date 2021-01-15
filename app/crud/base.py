from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# Abstract base class for generic types
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Retrieves a record based on primary key or id"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def duplicate_check(self, db: Session, sponsor: str, protocolNumber: str, versionNumber: str, amendmentNumber: str, documentStatus: str) -> Optional[ModelType]:
        """Duplicate check"""
        return db.query(self.model).filter(self.model.documentStatus=="final").filter(self.model.amendment==amendmentNumber).filter(self.model.versionNumber==versionNumber).filter(self.model.sponsor==sponsor).filter(self.model.protocol==protocolNumber).first()
        

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Retrieves first 100 records by default and limit can be set"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_by_userId(self, db: Session, userId: str) -> List[ModelType]:
        """Retrieves a record based on primary key or id"""
        return db.query(self.model).filter(self.model.userId == userId).all()

    def get_by_user(self, db: Session, user: str) -> Optional[ModelType]:
        """Retrieves a record based on user"""
        return db.query(self.model).filter(self.model.user == user).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Creates as record to DB table"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Updates record in DB table"""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Deletes record in DB table"""
        obj = db.query(self.model).get(id)
        try:
            db.delete(obj)
            db.commit()
        except Exception as ex:
            db.rollback()
        return obj
    
