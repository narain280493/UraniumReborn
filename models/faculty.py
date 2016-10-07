from database.database import Base
from sqlalchemy import Column, Integer, String
import uuid
from sqlalchemy import ForeignKey



class faculty(Base):
    __tablename__ = 'faculty'
    id = Column(String, primary_key=True)
    p_id = Column(String, ForeignKey("project.id"), nullable=False)
    faculty_name = Column(String(50))
    faculty_phone = Column(Integer)
    email_addr = Column(String(50))
    dept_name = Column(String(100)) 
    is_grad =  Column(Boolean)

    def __init__(self, f_name, f_phone, f_email_addr, f_dept_name, f_is_grad):
    	self.id = str(uuid.uuid4())
        self.faculty_name = f_name
        self.faculty_phone =f_phone
        self.email_addr = f_email_addr
        self.dept_name = f_dept_name
        is_grad = f_is_grad


    def __repr__(self):
        return '<b>faculty name %r<b>' % self.faculty_name

