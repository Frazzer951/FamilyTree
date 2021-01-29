'''

Person
    Name
    Nickname
    Parents

'''

import csv


class Person:
    def __init__(self, name, nickname=None, spouse=None, parents=None):
        self.name = name
        self.nickname = nickname
        self.spouse = None
        self.parents = None
        self.children = None

        if spouse is not None:
            self.change_spouse(spouse)
        if parents is not None:
            for parent in parents:
                self.add_parent(parent)

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


people = {}


def add_person(name, nickname=None, spouse=None, parents=None):
    people[name] = Person(name, nickname, spouse, parents)


def find_siblings(person):
    siblings = []
    for parent in person.parents:
        for child in parent.children:
            if child is not person and child not in siblings:
                siblings.append(child)
    return siblings


def load_people(filename):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] == 'Name':
                continue

            name = row[0]
            nickname = row[1]
            spouse = row[2]
            parent1 = row[3]
            parent2 = row[4]
            parents = []
            # print(name,nickname,spouse,parent1,parent2)
            if spouse not in people:
                spouse = None
            else:
                spouse = people[spouse]
            if parent1 in people:
                parents.append(people[parent1])
            if parent2 in people:
                parents.append(people[parent2])
            if len(parents) == 0:
                parents = None
            #print(name, nickname, spouse, parents)
            add_person(name, nickname, spouse, parents)


def save_people(people, filename=None):
    if filename is None:
        filename = 'tree.csv'

    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(
            ['Name', 'Nickname', 'Spouse', 'Parent 1', 'Parent 2'])
        for name in people:
            person = people[name]
            row = [person.name, person.nickname]
            if person.spouse is not None:
                row.append(person.spouse.name)
            else:
                row.append('')
            if person.parents is not None:
                row.append(person.parents[0].name)
                if len(person.parents) > 1:
                    row.append(person.parents[1].name)
            else:
                row.append('')
                row.append('')
            csv_writer.writerow(row)


'''
add_person('Luke', 'Frazzer')
add_person('John', 'Ratman', people['Luke'])
add_person('Alfonso', 'Owl', parents=[people['Luke'], people['John']])

for name in people:
    print(people[name].get_family())
'''

load_people('tree.csv')

for name in people:
    print(people[name].get_family())
