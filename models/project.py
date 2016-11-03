from database.database import Base
from sqlalchemy import ForeignKey, Column, String, Boolean
from sqlalchemy.orm import relationship


class project(Base):
    __tablename__ = 'project'
    id = Column(String, primary_key=True)
    f_id = Column(String, ForeignKey("faculty.id"), nullable=False)
    sf_id = Column(String, ForeignKey("faculty.id"), nullable=True)
    g_id = Column(String, ForeignKey("faculty.id"), nullable=True)
    Title = Column(String(100))
    isDevelopingCommunities = Column(Boolean)
    WebLink = Column(String(100))
    specialRequirements = Column(String(1200))
    Description = Column(String(1200))
    Department = Column(String(500))
    amountOfSupervision = Column(String(100))
    supervisor = Column(String(100))
    primaryNature = Column(String(100))
    priorWork = Column(String(100))
    desiredStudent = Column(String(100))
    speedType = Column(String(100))
    accountingContactName = Column(String(100))
    fac = relationship("faculty", back_populates="projects")
    secfac = relationship("faculty", back_populates="projects")
    gradstud = relationship("faculty", back_populates="projects")

    def __repr__(self):
        return self.title