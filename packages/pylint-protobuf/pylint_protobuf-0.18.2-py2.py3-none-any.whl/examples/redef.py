class Inner:
    value = 'first'

class Outer:
    def __init__(self):
        self.inner = Inner()

o1 = Outer()

class Inner:
    value = 'second'

o2 = Outer()

print(o1.inner.value)
assert o1.inner.value == 'first'
print(o2.inner.value)
assert o2.inner.value == 'second'
