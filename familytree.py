'''

Person
    Name
    Nickname
    Parents

'''


class Person:
    def __init__(self, name, nickname=None, spouse=None, parents=None, children=None):
        self.name = name
        self.nickname = nickname
        self.spouse = spouse
        self.parents = parents
        self.children = children

    def __str__(self):
        return f'{self.name} ({self.nickname})'

    def add_child(self, child):
        if self.children == None:
            self.children = []
        if child in self.children:
            return
        self.children.append(child)
        child.add_parent(self)
        if self.spouse is not None:
            self.spouse.add_child(child)

    def add_parent(self, parent):
        if self.parents == None:
            self.parents = []
        if parent in self.parents:
            return
        self.parents.append(parent)
        parent.add_child(self)

    def change_spouse(self, new_spouse):
        if self.spouse == new_spouse:
            return
        self.spouse = new_spouse
        new_spouse.change_spouse(self)

    def get_family(self):
        children = []
        parents = []
        if self.children is not None:
            for child in self.children:
                children.append(child.__str__())
        if self.parents is not None:
            for parent in self.parents:
                parents.append(parent.__str__())

        return f'''
Name     : {self.__str__()}
Spouse   : {self.spouse}
Children : {str(children).strip("[]").replace("'", "")}
Parents  : {str(parents).strip("[]").replace("'", "")}'''


def find_siblings(person):
    siblings = []
    for parent in person.parents:
        for child in parent.children:
            if child is not person and child not in siblings:
                siblings.append(child)
    return siblings


luke = Person('Luke', 'Frazzer')
john = Person('John', 'Ratman')
owl = Person('Alfonso', 'Owl')
luke.change_spouse(john)
john.add_child(owl)

print(luke.get_family())
print(john.get_family())
print(owl.get_family())
