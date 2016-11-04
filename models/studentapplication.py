from database.database import Base
from sqlalchemy import ForeignKey,Column, String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

class studentapplication(Base):
    __tablename__ = 'studentapplication'
    id = Column(String, primary_key=True)
    s_id = Column(String, ForeignKey("student.id"), nullable=False)
    isAppliedBefore = Column(Boolean)
    OtherFallEmployment = Column(String(500))
    ProjectPreference1 = Column(String(200))
    ProjectPreference2 = Column(String(200))
    ProjectPreference3 = Column(String(200))
    ProjectPreference4 = Column(String(200))
    ProjectPreference5 = Column(String(200))
    isBackgroundCheckDone = Column(Boolean)
    LastBackgroundCheckMonth = Column(String(20))
    LastBackgroundCheckYear = Column(String(5))
    isHarassmentTrainingDone = Column(Boolean)
    LastHarassmentTrainingMonth = Column(String(20))
    LastHarassmentTrainingYear = Column(String(5))
    Skill1 = Column(String(100))
    Skill2 = Column(String(100))
    Skill3 = Column(String(100))
    stuapp = relationship("student", foreign_keys='studentapplication.s_id', back_populates="students")



def __repr__(self):
        return "<student-application:" + self.FirstName + " " + self.LastName + ">"