import utils

class tableau(object):

    def __init__(self, max_or_min, obj_function, constraints):
        """
        Constructor if tableau class
        :param max_or_min: a parameter that contains either 'max' or 'min'
        :param obj_function: objective function
        :param constraints: list of constraints
        """
        super(tableau, self).__init__()
        self.max_or_min = max_or_min
        self.obj_function = obj_function
        self.constraints = constraints
        self.generate_tableau()

    def generate_tableau(self):
        """
        Creates a tableau from the objective function and constraints.
        Creates a matrix m*n
        """
        self.tableau = []

        self.var_num = len(self.obj_function)
        self.constr_num = len(self.constraints)

        self.artif_vars_rows = []
        self.artif_num = 0



        self.columns = self.var_num + self.constr_num + 1
        self.rows = self.constr_num

        self.count_artif_var()
        self.add_constraints()
        self.add_artif_var()
        self.add_obj_function()
        self.add_artificial_function()
        self.non_zero_variables = self.set_up_non_zero_var()

    def to_maximize(self):
        """
        Checks if parameter max_or_min is 'max'
        :return: True if parameter is 'max'. False otherwise
        """
        return self.max_or_min == 'max'

    def add_obj_function(self):
        """
        Adds objective function coefficients to the tableau by doing the following:
        Creates a new row with 0.0 as every element in a list
        Inserts coefficients of the objective function
        Coefficients are multiplied by (-1) if it is minimization problem
        """

        self.add_row(self.rows, 0.0)
        if self.to_maximize() == True:
            for i in range(self.var_num):
                self.tableau[-1][i] = float(self.obj_function[i])
        else:
            for i in range(self.var_num):
                self.tableau[-1][i] = (-1) * float(self.obj_function[i])

    def add_constraints(self):
        """
        Adds constraints' coefficients to the tableau by doing the following:
        Adds new rows to the tableau
        Inserts constraints' coefficients to each row
        """
        for row in range(self.constr_num):
            self.tableau.append([])

            for column in range(self.var_num):
                self.tableau[row].append(float(self.constraints[row][column]))

            for i in range(self.constr_num+self.artif_num):
                self.tableau[row].append(0.0)

            self.tableau[row].append(float(self.constraints[row][-1]))

    def is_artificial_row(self, row):
        """
        checks if the constraint has an artificial variable
        :param row: a constraint in coefficient form
        :return: True if there is an artificial variable. False otherwise.
        """
        return row in self.artif_vars_rows

    def set_up_non_zero_var(self):
        """
        Sets up the first list of non-zero(basic) variables by doing the following:
        Creates a list of basic variables with 0.0 as every element
        Checks each row for a artificial variable
        If exists:
            Insert it to the list
        else:
            Insert the surplus var to the list
        :return: a list of non-zero variables
        """

        temp = []

        for i in range(self.constr_num):
            temp.append(0.0)

        try:
            for row in range(self.artif_num):
                if self.is_artificial_row(self.artif_vars_rows[row]):
                    temp[self.artif_vars_rows[row]] = self.set_var_row()[self.var_num + self.constr_num + row]
        except IndexError:
            print('No artificial variables')

        for i in range(len(temp)):
            if type(temp[i]) == float:
                temp[i] = self.set_var_row()[self.var_num + i]

        return temp

    def count_artif_var(self):
        """
        Counts the number of artificial variables
        :return:  number of artificial variables
        """
        for i in range(self.constr_num):
            for j in self.constraints[i]:
                if j in utils.pos_signs:
                    self.artif_num += 1
                    self.artif_vars_rows.append(i)

        self.columns += self.artif_num

        return self.artif_num

    def add_artif_var(self):
        """
        Adds artificial variables to the tableau by doing the following:
        if there is a artificial variable in a row:
            assign -1 to surplus var
            assign 1 to artificial var
        """
        for row in range(self.constr_num):
                if self.constraints[row][self.var_num] in utils.neg_signs:
                    self.tableau[row][self.var_num + row] = 1.0

        if self.artif_num > 0:

            for row in range(self.constr_num):
                if self.constraints[row][self.var_num] in utils.pos_signs:
                    self.tableau[row][self.var_num + row] = -1.0

            pointer = self.var_num + self.constr_num
            for i in self.artif_vars_rows:
                self.tableau[i][pointer] = 1.0
                pointer += 1

    def add_artificial_function(self):
        """
        Adds artificial function's coefficients to the tableau by doing the following:
        New obj function is I = (-) * sum of artif vars
        Manipulates rows of the tableau to get I
        """
        if self.artif_num > 0:

            self.add_row(self.rows, 0.0)

            for row in self.artif_vars_rows:
                for i in range(len(self.tableau[row])):
                    self.tableau[-1][i] = self.tableau[-1][i] + self.tableau[row][i]

            for i in range(len(self.tableau[-1])):
                if self.tableau[-1][i] != -0.0:
                    self.tableau[-1][i] = (-1) * self.tableau[-1][i]

            pointer = self.var_num + self.constr_num

            for i in range(self.artif_num):
                self.tableau[-1][pointer] = 0.0
                pointer += 1

    def set_var_row(self):
        """
        Prints variable row above the tableau
        :return: a list of variables
        """
        variables = ['x', 'y', 'z', 'm', 'n']

        self.var_row = []

        for i in range(self.columns):
            self.var_row.append(0.0)

        for i in range(self.var_num):
            self.var_row[i] = variables[i]

        for i in range(self.constr_num):
            self.var_row[self.var_num + i] = 's%i' % (i + 1)

        for i in range(self.artif_num):
            self.var_row[self.constr_num + self.var_num + i] = 'a%i' % (i + 1)

        self.var_row[-1] = 'Value'

        return self.var_row

    def print_tableau(self):
        """
        Prints a tableau without the variables row
        :return: printed tableau
        """
        printed_tableau = ''
        printed_tableau += str(self.set_var_row()) + '\n'
        for i in range(len(self.tableau)):
            printed_tableau += str(self.tableau[i]) + '\n'

        return printed_tableau

    def add_row(self,pointer,new_value):
        """
        Adds a row to the tableau
        :param pointer: Index of the row
        :param new_value: New value for each element in row
        """
        self.tableau.insert(pointer, [])
        for i in range(self.columns):
            self.tableau[pointer].append(new_value)
        self.rows += 1

    def delete_row(self,pointer):
        """
        Deletes a row from the tableau
        :param pointer: Index of the row
        """
        self.rows -= 1
        self.tableau.pop(pointer)


    def add_column(self,pointer,new_value):
        """
        Adds a column to the tableau
        :param pointer: Index of the column
        :param new_value: New value for each element in the column
        """
        self.columns += 1
        for i in range(self.rows):
            self.tableau[i].insert(pointer,new_value)

    def delete_column(self,pointer):
        """
        Deletes a column from the tableau
        :param pointer: Index of the column
        """
        self.columns -= 1
        for i in range(self.rows):
            self.tableau[i].pop(pointer)

    def __str__(self):
        """
        Prints a tableau
        :return: a tableau in string type
        """
        return_string = ""

        return_string += self.print_tableau() + '\n'
        return_string += "Basic variables: " + str(self.non_zero_variables) + '\n'

        return return_string

    def __getitem__(self, pointer):
        """
        Returns an element from the tableau
        :param pointer: an index
        :return: item from the tableau
        """
        return self.tableau[pointer]

    def __setitem__(self, pointer, new_value):
        """
        Sets a value to the element at location specified by 'pointer' in the tableau
        :param pointer: an index
        :param new_value: new value for the element
        """
        self.tableau.insert(pointer, new_value)
