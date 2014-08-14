from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from userdb import Base, user_table, candidate_table

engine = create_engine('sqlite:///master.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session.commit()
