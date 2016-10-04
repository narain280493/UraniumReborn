from database.database import Base
from sqlalchemy import Column, Integer, String


class project_name(Base):
    __tablename__ = 'project_name'
    id = Column(Integer, primary_key=True)
    p_name = Column(String(50), unique=True)

    def __init__(self, name):
        self.p_name = name

    def __repr__(self):
        return '<project name %r>' % self.p_name

