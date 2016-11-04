from database.database import Base
from sqlalchemy import Column, String, ForeignKey
import uuid
from werkzeug import generate_password_hash, check_password_hash


# TO:DO needs a one to one mapping faculty to login
# we can retrieve faculty information as soon as the user
# logs in and use it inside the session. Also an important
# task here is manage sessions through flask. 


class loginpage(Base):
    __tablename__ = 'login'
    id = Column(String, primary_key=True)
    username = Column(String(100), unique=True, index=True)
    name = Column(String(100))
    # f_id = Column(String, ForeignKey("faculty.id"), nullable=True)
    # for student foreign key
    # s_id = Column(String, ForeignKey("faculty.id"), nullable=True)
    passwdhash = Column(String(300))

    def __init__(self, user_name, login_name, password):
        self.id = str(uuid.uuid4())
        # self.f_id = p_f_id
        # for student foreign key
        # self.f_id = p_f_id
        self.username = user_name
        self.name = login_name
        self.passwdhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def __repr__(self):
        return self.username
