#This file contains the main menu class and its methods.

import utils
from table import tableau
from simplex import simplex_method

class mainmenu(object):

    def __init__(self):
        """
        Constructor of mainmenu class.
        Creates variables for objective function, list of constraints, minimize or maximize input
        """
        super(mainmenu, self).__init__()
        self.__objective_function = None
        self.list_of_constraints = []
        self.min_or_max = ''

    def set_objective_function(self):
        """
        Sets an objective function by:
        User input is stripped into a list of coefficients and (in)equality signs and assigned to the obj_function variable
        """
        self.__objective_function = utils.strip_a_string(input('Enter your objective function: \n'))

    def return_obj_function(self):
        """
        Returns objective function
        :return: objective function
        """
        return self.__objective_function

    def display_obj_function(self):
        print("Your objective function is " + str(self.return_obj_function()))

    def add_constraints(self):
        """
        Adds constraints to the list of constraints
        Program will not until the user enters a valid input
        """
        try:
            constr_num = input('How many constraints: ')
            assert utils.is_digit(constr_num), 'Input has to be a digit in [0-9]'
            for i in range(int(constr_num)):
                constraint_input = utils.strip_a_string(input('Input your constraint #%i: ' % (i + 1)))
                self.list_of_constraints.append(constraint_input)
        except AssertionError as msg:
            print(msg)

    def change_constraint(self):
        """
        Changes constraints in the list of constraints
        """
        if len(self.list_of_constraints) == 0:
            print('There are no constraints. Use [AC] to add new constraints.')
            pass
        else:
            try:
                how_many_to_change = input('How many constraints do you wish to change? ')
                assert utils.is_digit(how_many_to_change), 'Input has to be a digit in between 1 and %i. Try again. \n' %len(self.list_of_constraints)
                if int(how_many_to_change) > len(self.list_of_constraints):
                    print("Number of constraints: %i. Add new constraints using [AC] instruction" %len(self.list_of_constraints))
                    pass
                else:
                    for i in range(int(how_many_to_change)):
                        self.display_constraints()
                        index_of_constraint = input('Which constraint do you wish to change? \n')
                        assert utils.is_digit(index_of_constraint), 'Input has to be a digit in between 1 and %i. Try again. \n' %len(self.list_of_constraints)
                        while int(index_of_constraint) > len(self.list_of_constraints):
                            print('Index of constraint is out of range. There are only %i constraints.' %len(self.list_of_constraints))
                            index_of_constraint = input('Out of %i constraints, which one do you wish to change? ' %len(self.list_of_constraints))
                            while not utils.is_digit(index_of_constraint):
                                index_of_constraint = input('Input has to be a digit between 1 and %i. Try again: \n' % len(self.list_of_constraints))
                        new_constraint = utils.strip_a_string(input('Input your new constraint: \n '))
                        self.list_of_constraints[int(index_of_constraint)-1] = new_constraint
                        print("A constraint is changed successfully")
            except AssertionError as msg:
                print(msg)

    def delete_constraint(self):
        """
        Deletes a constraint from the list of constraints
        """
        if len(self.list_of_constraints) == 0:
            print('There are no constraints. Use [SC] to add new constraints.')
            pass
        else:
            try:
                how_many_to_delete = input("How many constraints you wish to delete? \n ")
                assert utils.is_digit(how_many_to_delete), 'Input has to be a digit in between 1 and %i. Try again. \n' %len(self.list_of_constraints)

                while int(how_many_to_delete) > len(self.list_of_constraints):
                    how_many_to_delete = input('Input has to be a digit between 1 and %i. Try again. \n' % len(self.list_of_constraints))
                    assert utils.is_digit(
                        how_many_to_delete), 'Input has to be a digit in between 1 and %i. Try again. \n' % len(
                        self.list_of_constraints)
                for i in range(int(how_many_to_delete)):
                    self.display_constraints()
                    constraint_index = input('Which constraint do you wish to delete? \n ')
                    while not utils.is_digit(constraint_index):
                        constraint_index = input('Input has to be a digit between 1 and %i. Try again: \n' % len(self.list_of_constraints))
                        assert utils.is_digit(
                            constraint_index), 'Input has to be a digit in between 1 and %i. Try again. \n' % len(
                            self.list_of_constraints)
                    while int(constraint_index) > len(self.list_of_constraints):
                        constraint_index = input('Input has to be a digit between 1 and %i. Try again: \n' % len(self.list_of_constraints))
                        assert utils.is_digit(
                            how_many_to_delete), 'Input has to be a digit in between 1 and %i. Try again. \n' % len(
                            self.list_of_constraints)
                    self.list_of_constraints.pop(int(constraint_index)-1)
                    print('The constraint is successfully deleted')
            except AssertionError as msg:
                print(msg)

    def display_constraints(self):
        """
        Displays constraints
        """
        if len(self.list_of_constraints) == 0:
            print("There are no constraints. Please, use [SC] instruction to add new constraints.")
            pass
        else:
            adictionary = {}
            count = 0
            for i in self.list_of_constraints:
                count += 1
                x = 'constraint #%s: ' %count
                adictionary[x] = i
            utils.display_dictionary(adictionary,'---Constraints---')

    def solve(self):
        """
        Solves the problem using simplex method
        Creates an instance of tableau class and passing variables below to tableau's arguments
        Creates an instance of simplex_method class with instance of the tableau passed as an argument
        After the run of the simulation, the program shuts down
        """
        new_table = tableau(self.min_or_max, self.__objective_function,self.list_of_constraints)
        new_simplex = simplex_method(new_table)
        quit()

def mainmenudict(object):
    """
    Displays main menu dictionary and lets user interact with it
    The program will return back to main menu in most cases when the input is invalid
    It is done by defensive programming techniques and exception handling(see below for evidence)
    After every valid input from the user, a prompt will be printed to show the user the instructions
    It only halts when the user chooses "X" as his input in the main menu. After that, the program instantly shuts down
    :param object: instance of main menu class
    :return: Choice made by the user
    """
    mainmenu_dictionary = \
    {'[I]   : ': 'Display instructions',
        '[SF]  : ': 'set an objective function',
        '[CF]  : ': 'change the objective function',
        '[DF]  : ': 'display the objective function',
        '[AC]  : ': 'add constraints',
        '[CC]  : ': 'change a constraint',
        '[DC]  : ': 'delete a constraint',
        '[SC]  : ': 'display the constraints',
        '[S]   : ': 'solve the problem',
        '[X]   : ': 'exit the program',}

    utils.display_dictionary(mainmenu_dictionary, '---Main Menu--- \n')

    choice = input()

    while not choice.upper() in ['SF', 'SC', 'DF', 'DC', 'S', 'X', 'CF', 'I', 'CC', 'AC']:
        choice = input('Enter one of the instructions: \n')

    choice = choice.upper()

    if choice == 'I':
        print(utils.instructions)
        pass

    elif choice == 'SF':
        if object.return_obj_function() == None:
            max_or_min = ['max','min']
            try:
                object.min_or_max = input('Do you wish to maximize or minimize? Enter "max" or "min": \n')
                assert  object.min_or_max in max_or_min, 'Wrong input. Please, enter "max" or "min". \n'
                print(object.min_or_max)
                object.set_objective_function()
            except AssertionError as msg:
                print(msg)
        else:
            print('You have already set an objective function. If you wish to change it, use instruction [CF] in the main menu. ')

    elif choice == 'CF':
        try:
            cf_input = input('Do you really wish to change objective function?(Yes/No) \n')
            assert cf_input in ['yes','no'], 'Wrong input. Please, enter yes/no. \n'
            if cf_input.lower() == 'yes':
                if object.return_obj_function() == None:
                    max_or_min = ['max', 'min']
                    object.min_or_max = input('Do you wish to maximize or minimize? Enter "max" or "min": \n')
                    assert object.min_or_max in max_or_min, 'Wrong input. Please, enter "max" or "min". \n'
                    object.set_objective_function()
                object.set_objective_function()
            else:
                pass
        except AssertionError as msg:
            print(msg)

    elif choice == 'DF':
        if object.return_obj_function() == None:
            print("You have not set an objective function. Use [SF] to set one ")
        else:
            print()
            print('Your objective function is: ' + str(object.return_obj_function()))
            print()

    elif choice == 'AC':
        object.add_constraints()

    elif choice == 'CC':
        object.change_constraint()

    elif choice == 'DC':
        object.delete_constraint()

    elif choice == 'SC':
        object.display_constraints()

    elif choice == 'X':
        print('Thank you very much for using my program. See you! ')

    elif choice == 'S':
        if object.return_obj_function() == None:
            print("You have not set an objective function.")
        else:
            object.display_obj_function()

        if len(object.list_of_constraints) == 0:
            print("You have not set constraints yet.")
        else:
            object.display_constraints()
        input_choice = input("Is the input for your objective function and constraints correct? (Yes/No) \n")

        while input_choice.lower() not in ['yes','no']:
            input_choice = input("Wrong input. Please, enter 'yes' or 'no'. \n ")

        input_choice = input_choice.lower()

        if input_choice == 'yes' and (object.return_obj_function() == None or len(object.list_of_constraints) == 0):
            print("\nCannot use simplex method without setting the objective function or constraints. Please, try again... ")
        elif input_choice == 'yes':
            print(object.solve())
        elif input_choice == 'no':
            print('\n Getting back to the main menu...')

    return choice.upper()

myfunct = mainmenu()

if __name__ == '__main__':
    print(utils.intro_text)
    print(utils.instructions)

    while not mainmenudict(myfunct) == 'X':
        pass
