from sqlalchemy import Column
from .__base__ import SchemaBase, get_utc_datetime
from sqlalchemy.dialects.postgresql import TIMESTAMP,VARCHAR,INTEGER,BOOLEAN

class PdMetaEntityMappingLookup(SchemaBase):
   __tablename__ = "pd_meta_entity_mapping_lookup"
   id = Column(INTEGER,primary_key=True,autoincrement=True,nullable=False)
   category = Column(VARCHAR(20))
   input_text = Column(VARCHAR(500))
   iqv_standard_term = Column(VARCHAR(100))
   startdate = Column(TIMESTAMP)
   enddate = Column(TIMESTAMP)
   isvalid = Column(BOOLEAN)
   version = Column(VARCHAR(20))


def insert_meta_entity(session, category, input_text, iqv_standard_term):
   meta_entity = PdMetaEntityMappingLookup()
   meta_entity.category = category
   meta_entity.input_text = input_text
   meta_entity.iqv_standard_term = iqv_standard_term
   meta_entity.startdate = get_utc_datetime()
   meta_entity.isvalid = True
   meta_entity.version = "EM_" + str(meta_entity.startdate.strftime("%Y-%m-%d"))
   session.add(meta_entity)