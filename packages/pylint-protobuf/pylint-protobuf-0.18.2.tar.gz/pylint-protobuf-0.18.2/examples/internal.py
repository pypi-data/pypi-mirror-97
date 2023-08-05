import textwrap
import astroid

def transform_module(mod):
    Inner = astroid.extract_node(textwrap.dedent("""
        class Inner(object):
            'descriptor=140032233882384'
            __slots__ = {'ClearField', 'ClearExtension', 'DiscardUnknownFields', 'SetInParent', 'SerializePartialToString', 'Clear', 'HasExtension', 'ListFields', 'HasField', 'CopyFrom', 'value', 'IsInitialized', 'DESCRIPTOR', 'MergeFrom', 'MergeFromString', 'WhichOneof', 'ByteSize', 'SerializeToString', 'ParseFromString'}
            def __init__(self, ClearField=None, ClearExtension=None, DiscardUnknownFields=None, SetInParent=None, SerializePartialToString=None, Clear=None, HasExtension=None, ListFields=None, HasField=None, CopyFrom=None, value=None, IsInitialized=None, DESCRIPTOR=None, MergeFrom=None, MergeFromString=None, WhichOneof=None, ByteSize=None, SerializeToString=None, ParseFromString=None):
                pass
    """))
    Outer = astroid.extract_node(textwrap.dedent("""
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
    """))
    mod.locals['Inner'] = [Inner]
    mod.locals['Outer'] = [Outer]
    mod.body.extend([Inner, Outer])
    return mod


print('-------------------- DIRECTRLY --------------------')
direct_mod = """
import external
m = external.Outer()
m.values.add()
"""

modnode = astroid.parse(direct_mod)
print(modnode.repr_tree())
call = modnode.body[-1].value
icc1 = call.func.inferred()[0]
breakpoint()
a = list(icc1.infer_call_result(modnode))
print(call.inferred())

print('-------------------- INDIRECTRLY --------------------')
indirect_mod = """
import other
m = other.Outer()
m.values.add()
"""

def prevent_recursion(mod):
    return mod.name == 'other'
astroid.MANAGER.register_transform(astroid.Module, transform_module, prevent_recursion)
modnode = astroid.parse(indirect_mod)
print(modnode.repr_tree())
call = modnode.body[-1].value
icc2 = call.func.inferred()[0]
b = list(icc2.infer_call_result(modnode))
print(call.inferred())
