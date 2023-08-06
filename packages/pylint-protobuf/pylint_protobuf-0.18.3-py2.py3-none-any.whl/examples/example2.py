import addressbook_pb2 as a

book = a.AddressBook()
alice = book.people.add()
alice.name = 'Alice'
alice.id = 1

bob = book.people.add()
bob.name = 'Bob'
bob.id = 2
bob.umail = 2

carol = book.persons.add()
