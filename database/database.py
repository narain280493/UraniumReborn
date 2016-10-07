from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import urlparse

# fill out the path to sqlite engine
'''def get_username(file):
        f = open(file)
    uname = ""
    pword = ""
    host = ""
    for line in f:
        split_str = line.split("=")
        if split_str[0] == "username":
            uname = split_str[1]
        if split_str[0] == "password":
            pword = split_str[1]
        if split_str[0] == "host":
            host = split_str[1]
    return [uname, pword, host]

'''

url = urlparse.urlparse(os.environ["DATABASE_URL"])
#file = "../database/config.properties"
#config = get_username(file)
engine = create_engine('postgresql+psycopg2://' + url.username + ':' + url.password +
                       '@' +url.hostname +':' + str(url.port) +'/'+ url.path[1:])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
