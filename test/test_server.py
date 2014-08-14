from twisted.trail import unittest
from planetserver.server import UserServerFactory
from twisted.test import proto_helper

class RemoteCommunicateTestCase(unittest.TestCase):
    def setUp(self):
        factory = UserServerFactory()
        self.proto = factory.buildProtocol((127.0.0.1), 5000)
        self.transport = proto_helper.StringTransport()
        self.proto.makeConnection(self.transport)

    def testHello(self):
        pass

    def testAuthenticate(self):
        pass

    def testRegister(self):
        pass

    def testBye(self):
        pass

    def testRequestData(self):
        pass

