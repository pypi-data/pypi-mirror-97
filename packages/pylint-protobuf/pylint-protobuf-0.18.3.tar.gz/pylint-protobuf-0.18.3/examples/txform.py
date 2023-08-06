from fixture.foo_pb2 import Message as Blah

#class Message(object):
#    __slots__ = ('ts', )
#    def __init__(self):
#        self.ts = None

m = Blah()
m.ts = 123
m.missing = 456
