import os, glob

cwd = os.getcwd()
os.chdir('/home/zhuww/data/Kepler/archive/data3/keplerpub/')
#subdirs = glob.glob()
for subdir in [d for d in os.listdir('.') if d.startswith('Q') and d.endswith('public')]:
    i = 10
    allfiles = glob.glob(subdir+'/*.fits')
    print allfiles[:3]


