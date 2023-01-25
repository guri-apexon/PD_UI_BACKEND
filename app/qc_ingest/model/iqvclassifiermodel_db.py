from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvclassifiermodelDb(SchemaBase):
   __tablename__ = "iqvclassifiermodel_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   Full_Classification_List_list = Column(TEXT)
   Doc_Class = Column(TEXT)
   Language = Column(TEXT)
   Country = Column(TEXT)
   Base_Model_Version = Column(TEXT)
   Model_Sequence = Column(TEXT)
   Model_Index = Column(TEXT)
   Model_Label = Column(TEXT)
   Model_Name = Column(TEXT)
   Model_Directory = Column(TEXT)

