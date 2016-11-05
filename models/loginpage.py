from database.database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


# TO:DO needs a one to one mapping faculty to login
# we can retrieve faculty information as soon as the user
# logs in and use it inside the session. Also an important
# task here is manage sessions through flask. 


class loginpage(Base):
    __tablename__ = 'login'
    id = Column(String, primary_key=True)
    Email = Column(String(100), unique=True, index=True)
    f_id = Column(String, ForeignKey("faculty.id"), nullable=True)
    s_id = Column(String, ForeignKey("student.id"), nullable=True)
    Password = Column(String(300))
    UserType = Column(String(300))
    fac = relationship("faculty", back_populates="cred")
    stud = relationship("student", back_populates="cred")

    def __repr__(self):
        return self.id
