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
