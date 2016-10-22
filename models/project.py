from database.database import Base
from sqlalchemy import ForeignKey, Column, String, Boolean
import uuid
from sqlalchemy.orm import relationship


class project(Base):
    __tablename__ = 'project'
    id = Column(String, primary_key=True)
    f_id = Column(String, ForeignKey("faculty.id"), nullable=False)
    title = Column(String(100))
    is_focused_engg_comm = Column(Boolean)
    website = Column(String(100))
    requirements = Column(String(1200))
    description = Column(String(1200))
    dept_name = Column(String(500))
    amt_supervision_req = Column(String(100))
    supervision_provided = Column(String(100))
    nature_of_work = Column(String(100))
    amt_prior_work = Column(String(100))
    name_specific_student = Column(String(100))
    speed_type = Column(String(100))
    accounting_contact = Column(String(100))
    fac = relationship("faculty", back_populates="projects")

    def __init__(self,p_title, p_f_id, p_is_focused_engg_comm, p_website, p_requirements, p_description, p_dept_name, p_amt_supervision_req,p_supervision_provided, p_nature_of_work, p_amt_prior_work,p_name_specific_student, p_speed_type, p_accounting_contact):
        self.id = str(uuid.uuid4())
        self.f_id = p_f_id
        self.title = p_title
        self.is_focused_engg_comm = p_is_focused_engg_comm
        self.website = p_website
        self.requirements = p_requirements
        self.description = p_description
        self.dept_name = p_dept_name
        self.amt_supervision_req = p_amt_supervision_req
        self.supervision_provided = p_supervision_provided
        self.nature_of_work = p_nature_of_work
        self.amt_prior_work = p_amt_prior_work
        self.name_specific_student = p_name_specific_student
        self.speed_type = p_speed_type
        self.accounting_contact = p_accounting_contact

    def __repr__(self):
        return self.title

    def get_id(self):
        return self.id
