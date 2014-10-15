from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from defdb import Base, file_table

#define the classes

engine = create_engine('sqlite:///kic.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#metadata = MetaData(bind=engine)

#file_table = Table('files', metadata,
        #Column('filename', String(36), primary_key=True),
        #Column('dir', String(10)),
        #Column('kic', Integer),
        #Column('cadence', String(3))
        #)

#metadata.create_all()


#conn = engine.connect()

import os, glob

cwd = os.getcwd()
datapath = '/home/zhuww/data/Kepler/archive/data3/keplerpub/'
os.chdir(datapath)
#subdirs = glob.glob()
for subdir in [d for d in os.listdir('.') if d.startswith('Q') and d.endswith('public')]:
    print 'processing ', subdir
    os.chdir('./' + subdir)
    allfiles = glob.glob('*.fits')
    data = []
    for fn in allfiles:
        part1, part2 = fn.split('-')
        kic = int(part1[4:])
        filetype = part2.split('_')[-1]
        cadence = filetype.split('.')[0]
        data.append(file_table(fn,subdir,kic,cadence))
        
    os.chdir('..')

    session.add_all(data)
session.commit()
    #conn.execute(file_table.insert(), data)

#conn.close()

os.chdir(cwd)
