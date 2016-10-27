from database.database import Base
from sqlalchemy import ForeignKey, Column, String
import uuid


# TO:DO needs a one to one mapping faculty to login
# we can retrieve faculty information as soon as the user
# logs in and use it inside the session. Also an important
# task here is manage sessions through flask.
class login(Base):
    __tablename__ = 'login'
    id = Column(String, primary_key=True)
    username = Column(String(100), unique=True, index=True)
    f_id = Column(String, ForeignKey("faculty.id"), nullable=False)
    salt = Column(String(1000))
    hash = Column(String(1000))

    def __init__(self, user_name, login_name, p_f_id, p_salt, p_hash):
        self.id = str(uuid.uuid4())
        self.f_id = p_f_id
        self.username = user_name
        self.name = login_name
        self.salt = p_salt
        self.hash = p_hash

    def __repr__(self):
        return self.name
