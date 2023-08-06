"""
Hello world
"""

from person_pb2 import Person
P = Person()
P.should_also_warn = P.invalid_field = 123
