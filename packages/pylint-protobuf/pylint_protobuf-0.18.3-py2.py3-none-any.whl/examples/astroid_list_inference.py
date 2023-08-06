import astroid


ONE = """
class Entry(object):
    value = "abc"

def entry_list():
    return [Entry()]


entry_list()
"""

TWO = """
class Entry(object):
    value = 'abc'

class EntryContainer(object):
    def add(self, **kwargs):
        return Entry()

c = EntryContainer()
c.add()
"""

TREE = """
class TestMessage(object):
    class Entry(object):
        value = "abc"
    def __init__(self):
        class EntryContainer(object):
            def add(self, **kwargs):
                return TestMessage.Entry()
        self.entries = EntryContainer()

m = TestMessage()
m.entries.add()
"""
#call = astroid.parse(TREE).body[-1].value

FOUR = """
class TestMessage(object):
    class Entry(object):
        value = "abc"
    class EntryContainer(object):
        def add(self, **kwargs):
            return TestMessage.Entry()
    def __init__(self):
        self.entries = self.EntryContainer()

m = TestMessage()
m.entries.add()
"""

FIVE = """
class Entry(object):
    value = "abc"

class TestMessage(object):
    def __init__(self):
        class EntryContainer(object):
            def add(self, **kwargs):
                return Entry()
        self.entries = EntryContainer()

m = TestMessage()
m.entries.add()
"""

import sys

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    print(frame.f_locals.keys())
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    print('trace:%s' % (func_name,))
    return


SIX6 = """
class Inner(object):
    'descriptor=140032233882384'
    __slots__ = {'ClearField', 'ClearExtension', 'DiscardUnknownFields', 'SetInParent', 'SerializePartialToString', 'Clear', 'HasExtension', 'ListFields', 'HasField', 'CopyFrom', 'value', 'IsInitialized', 'DESCRIPTOR', 'MergeFrom', 'MergeFromString', 'WhichOneof', 'ByteSize', 'SerializeToString', 'ParseFromString'}
    def __init__(self, ClearField=None, ClearExtension=None, DiscardUnknownFields=None, SetInParent=None, SerializePartialToString=None, Clear=None, HasExtension=None, ListFields=None, HasField=None, CopyFrom=None, value=None, IsInitialized=None, DESCRIPTOR=None, MergeFrom=None, MergeFromString=None, WhichOneof=None, ByteSize=None, SerializeToString=None, ParseFromString=None):
        pass


class Outer(object):
    'descriptor=140032237255984'
    __slots__ = {'ClearField', 'ClearExtension', 'DiscardUnknownFields', 'SetInParent', 'SerializePartialToString', 'Clear', 'HasExtension', 'ListFields', 'HasField', 'CopyFrom', 'IsInitialized', 'DESCRIPTOR', 'MergeFrom', 'values', 'MergeFromString', 'WhichOneof', 'ByteSize', 'SerializeToString', 'ParseFromString'}
    def __init__(self, ClearField=None, ClearExtension=None, DiscardUnknownFields=None, SetInParent=None, SerializePartialToString=None, Clear=None, HasExtension=None, ListFields=None, HasField=None, CopyFrom=None, IsInitialized=None, DESCRIPTOR=None, MergeFrom=None, values=None, MergeFromString=None, WhichOneof=None, ByteSize=None, SerializeToString=None, ParseFromString=None):
        pass
        # self.values = Inner()  # external_fields

        class InnerCompositeContainer(object):
            def add(self, **kwargs):
                return Inner()
        self.values = InnerCompositeContainer()  # repeated composite_fields

m = Outer()
m.values.add()
"""
call = astroid.parse(SIX6).body[-1].value
print(call.repr_tree())
sys.settrace(trace_calls)
print(call.inferred())
