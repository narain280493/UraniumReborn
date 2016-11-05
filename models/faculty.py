from database.database import Base
from sqlalchemy import Column, String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship


class faculty(Base):
    __tablename__ = 'faculty'
    id = Column(String, primary_key=True)
    FirstName = Column(String(100))
    LastName = Column(String(100))
    Phone = Column(String(15))
    Email = Column(String(100))
    Department = Column(String(100))
    is_grad = Column(Boolean)
    isSupervisedBefore = Column(Boolean)
    projects = relationship("project", back_populates="fac", primaryjoin="faculty.id==project.f_id")
    cred = relationship("loginpage", back_populates="fac")

    def __repr__(self):
        return "<faculty:" + self.FirstName + " " + self.LastName + ">"
