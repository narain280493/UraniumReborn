# need a table to store CEAS staff overrides
# override id
# student id
# assigned project id
# assigned by fac(CEAS) id not required
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, String


class overrides(Base):
    __tablename__ = 'overrides'
    s_id = Column(String, ForeignKey("student.id"), nullable=False, primary_key=True)
    p_id = Column(String, ForeignKey("project.id"), nullable=False)

    stud = relationship("student", foreign_keys='overrides.s_id')
    proj = relationship("project", foreign_keys='overrides.p_id')

def __repr__(self):
        return "<override:" + self.s_id + ">"
