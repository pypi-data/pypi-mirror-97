from typing import List, Set, Any, Optional
import astroid
import astroid.mixins


def import_(mod_node, modname=None):
    # type: (astroid.mixins.ImportFromMixin, Optional[str]) -> astroid.Module
    return mod_node.do_import_module(modname)


def import_module(mod_node, modname):
    # type: (astroid.Import, str) -> astroid.Module
    return import_(mod_node, modname)


def import_from_module(mod_node, modname=None):
    # type: (astroid.ImportFrom, Optional[str]) -> astroid.Module
    return import_(mod_node, modname)


def names(mod_node):
    # type: (astroid.Module) -> Set[str]
    names = set(mod_node.wildcard_import_names())
    names -= {'sys', 'DESCRIPTOR', 'descriptor_pb2'}
    return names


def main():
    # type: () -> Set[str]
    mod_node = astroid.extract_node("import mod")
    if isinstance(mod_node, astroid.Import):
        # TODO: check modname usage?, why can't we give None
        # and re-use the module name from the "import <blah>" line?
        n = names(import_module(mod_node, 'example_for_refactor_pb2'))
    elif isinstance(mod_node, astroid.ImportFrom):
        n = names(import_from_module(mod_node))
    print(n)
    return n


if __name__ == '__main__':
    main()
