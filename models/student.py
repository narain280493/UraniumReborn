from database.database import Base
from sqlalchemy import Column, String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship


class student(Base):
    __tablename__ = 'student'

    ## Basic student info
    id = Column(String, primary_key=True)
    Student_id = Column(String(30))
    Phone = Column(String(15))
    Email = Column(String(100))

    FirstName = Column(String(100))
    LastName = Column(String(100))
    Gender = Column(String(10))
    isSpanishOrigin = Column(String(20))
    Race = Column(String(100))

    ## address
    LocalAddressLine1 = Column(String(100))
    LocalAddressLine2 = Column(String(100))
    LocalAddressCity = Column(String(100))
    LocalAddressState = Column(String(100))
    LocalAddressZip = Column(String(10))

    ## summer address
    SummerAddressLine_1 = Column(String(100))
    SummerAddressLine_2 = Column(String(100))
    SummerAddressCity = Column(String(100))
    SummerAddressState = Column(String(100))
    SummerAddressZip = Column(String(10))

    ## academic info
    PrimaryMajor = Column(String(100))
    SecondaryMajor = Column(String(100))
    GPA = Column(String(10))
    StudentId = Column(String(20))
    SchoolLevel = Column(String(20))
    GraduationMonth = Column(String(20))
    GraduationYear = Column(String(5))
    isResearchExperience = Column(Boolean)

    isAppliedBefore = Column(Boolean)
    isWorkedBefore = Column(Boolean)
    isGoldShirt = Column(Boolean)
    isMSBSStudent = Column(Boolean)
    isBackgroundCheckDone = Column(String(20))
    LastBackgroundCheckMonth = Column(String(20))
    LastBackgroundCheckYear = Column(String(5))
    isHarassmentTrainingDone = Column(String(20))
    LastHarassmentTrainingMonth = Column(String(20))
    LastHarassmentTrainingYear = Column(String(5))

    isAvailability = Column(String(20))
    students = relationship("studentapplication", back_populates="stuapp",
                            primaryjoin="student.id==studentapplication.s_id")
    cred = relationship("loginpage", back_populates="stud")

    def __repr__(self):
        return "<student:" + self.FirstName + ">"
