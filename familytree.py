'''
Author: Luke AKA:Frazzer
Description: This program will generate a family tree and let you transverse it for add people to it.
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

    _parents = []
    if spouse not in people:
        spouse = None
    else:
        spouse = people[spouse]
    if parents is not None:
        if parents[0] in people:
            _parents.append(people[parents[0]])
        if len(parents) > 1:
            if parents[1] in people:
                _parents.append(people[parents[1]])
        if len(_parents) == 0:
            _parents = None

    people[name] = Person(name, nickname, spouse, _parents)


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
            parents = [row[3], row[4]]
            # print(name, nickname, spouse, parents)
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


def print_menu():
    print("To Exit type:                    'exit'")
    print("To Add a new person type:        'new'")
    print("To Save the current tree type:   'save'")
    print("To look at someone else type their name. I.E. 'Luke'")


if __name__ == '__main__':
    print('Do you want to load a csv with a family tree, or start from the begining?')
    print("Type 'csv' to load a csv, or 'new' for a new tree")
    user_input = input().lower()

    if user_input == 'csv':
        filename = input('Please type the filename for the csv file: ')
        if '.csv' not in filename:
            filename += '.csv'
        print(filename)
        load_people(filename)

    elif user_input == 'new':
        # TODO: Needs Implimentation
        print('new')

    else:
        print(user_input, 'was not an option')
        exit()

    current_person = people[list(people.keys())[0]]
    # print(current_person)

    # for name in people:
    #    print(people[name].get_family())
    print(people)
    while True:
        print(current_person.get_family())

        print_menu()
        user_input = input()

        if user_input.lower() == 'exit':
            exit()
        elif user_input.lower() == 'new':
            # TODO: Needs impimentation
            print('new')
        elif user_input.lower() == 'save':
            new_fn = input(
                'Please enter the filename that you want the tree to be save to: ')
            if '.csv' not in new_fn:
                new_fn += '.csv'
            save_people(new_fn)
        elif user_input == '':
            continue
        else:
            if user_input in people:
                current_person = people[user_input]
            else:
                print('Unknown command/person!')
