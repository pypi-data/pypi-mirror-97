from oneof_example_pb2 import ScalarMessage, CompositeMessage

m = ScalarMessage()
m.name = 'hello'
assert m.code == 0
m.code = 123
assert m.name == ''


msg = CompositeMessage()
