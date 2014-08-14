from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from defdb import Base, file_table

from authentication import *

import numpy as np
from numpy.random import randint
import cPickle,re

engine = create_engine('sqlite:///master.db', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

print isKnown('Weiwei', session)
