from twisted.protocols import basic
from twisted.internet import protocol

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from authentication import *

import numpy as np
from numpy.random import randint
import cPickle,re

engine = create_engine('sqlite:///master.db', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#data_engine = create_engine('sqlite:///../kic.db', echo=True)
#DataSession = sessionmaker()
#DataSession.configure(bind=data_engine)
#data_session = DataSession()

allkics = np.load("allkic.npz")["allkics"]
kicsize = allkics.size
koitab = np.array(np.genfromtxt('cumulative.tab', delimiter='\t')[...,1], dtype=int)
koisize = koitab.size

class UserCommunicationProtocol(basic.LineReceiver):
#class UserCommunicationProtocol(protocol.Protocol):
    def __init__(self, users):
        #self.proxy = UserProxy(users)
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        #self.transport.write("Welcome to the planet search system test server.")
        pass

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            print "%s connection lost" % self.name
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        elif self.state == "GETPASSWORD":
            self.get_password(line)
            self.state = "TAKECMD"
        elif self.state == "SETPASSWORD":
            self.set_password(line)
            self.state =  "TAKECMD"
        elif self.state == "TAKECMD":
            self.handle_CMD(line)
        else:
            self.other_CMD(line)
            print self.state

    def handle_GETNAME(self, name):
        #if self.users.has_key(name):
        print "User %s connected." % name
        self.name = name
        if isKnown(name, session): #immplement this!!!
            self.sendLine("#LOGIN")
            self.state = "GETPASSWORD"
            self.users[name] = self
        elif len(name) > 10 \
            or not name.find(' ')==-1 \
            or not name.find(':')==-1 \
            or not name.find('!')==-1 \
            or not name.find('&')==-1 \
            or not name.find('%')==-1 \
            or not name.find('$')==-1 \
            or not name.find('@')==-1 \
            or not name.find('^')==-1 \
            or not name.find('*')==-1 \
            or not name.find('#')==-1:
            self.sendLine("Invalid User name, must be less equal to 10 character, no special characters like space or !@#$%^&*\nPlease re-enter your username")
            self.state = "GETNAME"
        else:
            self.sendLine("#NEWUSER")
            self.state = "SETPASSWORD"
        #self.state = "CHAT"

    def get_password(self, password):
        if authenticate(self.name, password, session):
            self.sendLine("Welcome, %s" % (self.name))
            self.state = "TAKECMD"
        else:
            self.sendLine("Password incorrect, try again.")
            self.state = "GETNAME"

    def set_password(self, password):
        adduser(self.name, password, session)
        self.sendLine("Welcome, %s" % self.name)

    def handle_CMD(self, cmd):
        if cmd == "random":
            randchoice = randint(0,2)
            #print "#KIC " + str(allkics[randidx][0])
            if randchoice == 0:
                randidx = randint(0, kicsize-1,1)
                self.sendLine("#KIC " + str(allkics[randidx][0]))
            else:
                randidx = randint(0, koisize-1,1)
                self.sendLine("#KIC " + str(koitab[randidx][0]))
            self.state = "TAKECMD"
        elif cmd.startswith("kic"):
            try:
                kic = int(cmd.split()[-1].lstrip("0"))
            except:pass
            if kic in allkics:
                self.sendLine("#KIC " + str(kic))
            else:
                self.sendLine("Don't recognize the kic %s" % kic)
            self.state = "TAKECMD"
        elif cmd.startswith("SAVE:"):
            result = cPickle.loads(cmd.lstrip("SAVE:"))
            saveresult(self.name, session, result)
            self.state = "TAKECMD"
        elif cmd.startswith("users"):
            listofusers = userlist(session)
            self.sendLine(' '.join([str(u) for u in listofusers]))
            self.state = "TAKECMD"
        elif cmd.startswith("profile"):
            user = cmd.split()[-1]
            if not isKnown(user, session):
                self.sendLine("%s is not a known user." % user)
                self.state = "TAKECMD"
            else:
                good, bad, total = QueryUserProfile(user, session)
                self.sendLine("""
USER      |\tgood\tbad\ttotal
%s|\t%s\t%s\t%s
                """ % (user.ljust(10), good, bad, total))
                self.state = "TAKECMD"

        elif cmd.startswith("ladder"):
            users = userlist(session)
            data = []
            for user in users:
                good, bad, total = QueryUserProfile(user, session)
                data.append([user, good, bad, total])
            data = sorted(data, key=lambda x:x[-1], reverse=True)
            ladder = "USER      |\tgood\tbad\ttotal\n" + '\n'.join(["%s|\t%s\t%s\t%s"% tuple([d[0].ljust(10)] + d[1:]) for d in data])
            self.sendLine(str(ladder))
            self.state = "TAKECMD"

        elif cmd.startswith("?"):
            self.sendLine("kic ladder profile random users ")
            self.state = "TAKECMD"
        else:
            self.sendLine("""Use command '>random' to download a random kic and start a GUI,
or kic #kic to download data for a known target,
or type ? for a list of commands.""")
            self.state = "TAKECMD"




    
    def other_CMD(self, cmd):
        cmdline = "<%s>, %s" % (self.name, cmd)
        for name, protocol in self.users.iteritems():
            #if protocol == self:
            if True:
                protocol.sendLine(cmdline)
                print "sending %s command %s" %  (self.name, cmdline)




class UserServerFactory(protocol.Factory):
    def __init__(self):
        self.users = {}
    def buildProtocol(self, addr):
        return UserCommunicationProtocol(self.users)


def main():
    from twisted.internet import reactor
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)
    reactor.listenTCP(8123, UserServerFactory())
    reactor.run()

if __name__ == "__main__":
    main()






