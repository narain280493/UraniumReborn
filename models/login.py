from database.database import Base
from sqlalchemy import Column, String
import uuid

class login(Base):
    __tablename__ = 'login'
    id = Column(String, primary_key=True)
    username = Column(String(100),unique=True, index=True)
    name = Column(String(100))
    password = Column(String(100))


    def __init__(self, user_name, login_name, passwd):
        self.id = str(uuid.uuid4())
        self.username = user_name
        self.name = login_name
        self.password = passwd

    def __repr__(self):
        return self.name