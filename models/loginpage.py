from database.database import Base
from sqlalchemy import Column, String
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
    #f_id = Column(String, ForeignKey("faculty.id"), nullable=False)
    passwdhash = Column(String(300))

    def __init__(self, user_name, login_name, password):
        self.id = str(uuid.uuid4())
        #self.f_id = p_f_id
        self.username = user_name
        self.name = login_name
        self.passwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwdhash, password)

    def __repr__(self):
        print "repr"
        return self.username