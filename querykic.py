from defdb import file_table
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///kic.db', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#allkics = np.load("allkic.npz")["allkics"]
koitab = np.array(np.genfromtxt('planetserver/cumulative.tab', delimiter='\t')[...,1], dtype=int)
print koitab[0]
print ['/'.join([f.path, f.filename]) for f in session.query(file_table).filter(file_table.kic == int(koitab[0]) and file_table.cadence == 'llc')]

