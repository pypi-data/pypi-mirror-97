class Outer(object):
    class Inner(object):
        def __init__(self):
            self.value = 123

    def __init__(self):
        class InnerCompositeContainer(list):
            def add(inner_self, **kwargs):
                elem = self.Inner(**kwargs)
                inner_self.append(elem)
                return elem
        self.values = InnerCompositeContainer()
