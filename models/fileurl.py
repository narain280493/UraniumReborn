from database.database import Base
from sqlalchemy import Column, String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

class fileurl(Base):
    __tablename__ = 'fileurl'
    id = Column(String, primary_key=True)
    email_id = Column(String(100))
    resume_url = Column(String(200))
    coverletter_url = Column(String(200))

