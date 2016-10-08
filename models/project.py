from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean
import uuid


class project(Base):
	__tablename__ = 'project'
	id = Column(String, primary_key=True)
	title = Column(String(100))
	is_focused_engg_comm = Column(Boolean)
	website = Column(String(100))
	requirements = Column(String(1000))
	description = Column(String(1000))
	dept_name = Column(String(500))
	amt_supervision_req = Column(String(50))
	supervision_provided = Column(String(50))
	nature_of_work = Column(String(50))
	amt_prior_work = Column(String(50))
	name_specific_student = Column(String(100))
	speed_type = Column(String(50))
	accounting_contact = Column(String(50))
	has_supervised_dla = Column(Boolean)


	def __init__(self,p_title, p_is_focused_engg_comm, p_website, p_requirements, p_description, p_dept_name,p_amt_supervision_req,p_supervision_provided, p_nature_of_work, p_amt_prior_work,p_name_specific_student, p_speed_type, p_accounting_contact, p_has_supervised_dla):
		self.id = str(uuid.uuid4())
		self.title = p_title
		is_focused_engg_comm = p_is_focused_engg_comm
		website = p_website
		requirements = p_requirements
		description = p_description
		dept_name = p_dept_name
		amt_supervision_req = p_amt_supervision_req
		supervision_provided = p_supervision_provided
		nature_of_work = p_nature_of_work
		amt_prior_work = p_amt_prior_work
		name_specific_student = p_name_specific_student
		speed_type = p_speed_type
		accounting_contact = p_accounting_contact
		has_supervised_dla = p_has_supervised_dla
	   

	def __repr__(self):
		return 'Project Name: %r' % self.title.encode('ascii','ignore')

	def get_id(self):
		return self.id
