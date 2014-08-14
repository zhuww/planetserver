from twisted.protocols import basic
from twisted.internet import protocol


#class UserProxy(object):
    #def __init__(self, users):
        #self.user = user
        #self.name = None
        #self.state = "GETNAME"
        

class UserCommunicationProtocol(basic.LineReceiver):
#class UserCommunicationProtocol(protocol.Protocol):
    def __init__(self, users):
        #self.proxy = UserProxy(users)
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        pass
        #self.transport.write("Welcome new user. What is your name?")

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            print "%s connection lost" % self.name
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CMD(line)

    def handle_GETNAME(self, name):
        if self.users.has_key(name):
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s" % (name))
        self.name = name
        self.users[name] = self
        print "User %s connected." % name
        self.state = "CHAT"
    
    def handle_CMD(self, cmd):
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






