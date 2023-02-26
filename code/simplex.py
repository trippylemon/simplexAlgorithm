from table import tableau

class simplex_method(object):

    def __init__(self, tableau):
        """
        Constructor for simplex_method class
        :param tableau: a tableau to do operations on
        """
        super(simplex_method, self).__init__()
        self.tableau = tableau

        self.run()

    def run(self):
        """
        Runs the simplex algorithm in two stages depending on the step-by-step result
        """
        if self.stage1() == True:
            if self.stage2() == True:
                self.print_solution()
            else:
                print("Infeasible solution")
        else:
            print("Infeasible solution")

        #self.print_solution()

    def stage1(self):
        """
        Stage 1 of simplex method
        Minimizes the sum of the artificial variables
        Iterates the tableau with artificial function as the last row
        If there are no negative values for variables in artificial function or no positive value for a single theta value:
            Checks the artificial sum
            If it is 0:
                Proceed to stage 2
            else:
                Infeasible region. No solutions exist for that problem

        :return: True if the sum of the artificial variables. False otherwise.
        """

        done = False

        print('---Start of stage 1---' + '\n')
        print(self.tableau)

        if self.tableau.artif_num > 0:

            while self.continue_iteration() == True:
                self.iterate_stage_1()
                if self.is_feasible():
                    done = True
                else:
                    done = False
            else:
                done = True

            self.tableau.delete_row(-1)

            for i in range(self.tableau.artif_num):
                self.tableau.delete_column(self.tableau.columns - 2)
            self.tableau.artif_num = 0
        else:
            done = True

        print('---End of stage 1---' + '\n')

        return done

    def stage2(self):
        """
        Stage 2 of simplex method
        Works only with constraints and original objective function if the sum of artificial variables is 0 or there are no artificial variables from the start
        Works as the basic simplex method
        See Diagram 1.5 in Documented Design to see how the method works
        Maximizes the value for objective function
        :return:
        """
        done = False

        print('---Start of stage 2---' + '\n')
        print(self.tableau)

        while self.continue_iteration() == True:
            self.iterate_stage_2()
        else:
            if self.is_value_greater_0() == False and self.tableau.max_or_min == 'max':
                done = False
            else:
                done = True
        print('---End of stage 2---' + '\n')

        return done

    def find_pivot_in_last_row(self):
        """
        Finds the most negative value(pivot column) in the bottom
        If there are no negative values in bottom row during stage 1 and sum of artificial vars is not 0:
            No feasible solution
        :return: Index of most negative value in the bottom row of the tableau
        """
        cost_function = self.tableau.rows - 1
        temp = 0
        for i in range(0, self.tableau.columns - 1):
            if self.tableau[cost_function][i] < temp and self.tableau[cost_function][i] < 0:
                temp = self.tableau[cost_function][i]

        if temp == 0:
            print('No feasible solution')
            exit()
        else:
            return self.tableau[cost_function].index(temp)

    def find_scalar_main_row(self):
        """
        Finds a value that should divide each element in the row with least positive theta value to obtain 1 at the pivot by doing the following:
        Iterating through every constraint row to find the least theta value(ratio between last element and column_pivot values in the row)
        There is a special case of degeneracy: when the value of basic variable is 0
        If so, theta value is 0 and the row with such case becomes a main row for the next iteration
        :return: Value that should divide each element in the row with least positive theta value to obtain 1 at the pivot
        """
        self.n_row = 0
        self.column_pivot = self.find_pivot_in_last_row()
        theta_value = float('inf')

        for i in range(self.tableau.constr_num):
            #checking for degeneracy
            if self.tableau[i][-1] == 0:
                print("Possible degeneracy, see next iterations \n")
                theta_value = 0
                self.n_row = i
            elif self.tableau[i][self.column_pivot] and self.tableau[i][-1] > 0:
                temp = self.tableau[i][-1] / self.tableau[i][self.column_pivot]
                if temp > 0 and temp < theta_value:
                    theta_value = temp
                    self.n_row = i

        return self.tableau[self.n_row][self.column_pivot]

    def get_scalar(self,row):
        """
        Finds a scalar in a 'row' with an index of column_pivot variable
        :param row: A row to operate on
        :return: Returns a scalar that is used in scaling the tableau
        """
        return self.tableau[row][self.column_pivot]

    def scale(self):
        """
        Scales the tableau
        In a row with least positive theta value each element is divided by the scalar to obtain 1 at index of pivot column
        Other rows are manipulated to get 0 at index of pivot column
        So that the column with pivot value would look like(assuming there are 3 constraints and 1 function and pivot row is random):
        [0]
        [0]
        [1]
        [0]
        """
        scalar = self.find_scalar_main_row()

        for i in range(len(self.tableau[self.n_row])):
            if self.tableau[self.n_row][i] != 0.0:
                self.tableau[self.n_row][i] = self.tableau[self.n_row][i] / scalar

        for i in range(self.tableau.rows):
            if self.tableau[i] != self.tableau[self.n_row]:
                temp = self.get_scalar(i)
                for j in range(len(self.tableau[i])):
                    self.tableau[i][j] = self.tableau[i][j] + temp * (-1) * self.tableau[self.n_row][j]

        self.change_non_zero_var(self.n_row,self.tableau.var_row[self.column_pivot])

        print(self.tableau)

    def change_non_zero_var(self,row,new):
        """
        Changes a non-zero variable in a list
        :param row: index in a list
        :param new: new non-zero variable
        """
        self.tableau.non_zero_variables[row] = new

    def is_last_row_negative(self):
        """
        Checks if there are negative values in the last row except for 'Value' column
        :return: True if there are negative values in the last row except for 'Value' column. False otherwise
        """
        for i in range(len(self.tableau[self.tableau.rows-1])-1):
            if self.tableau[self.tableau.rows-1][i] < 0:
                return True
        return False

    def is_theta_positive(self):
        """
        Checks if there are negative values in the right column
        Implemented with defensive programming when there is division by 0 when looking for theta value
        :return: True if there are negative values in the right column
        """
        for i in range(self.tableau.constr_num):
            try:
                if (self.tableau[i][-1]) / (self.tableau[i][self.find_pivot_in_last_row()]) > 0:
                    return True
            except ZeroDivisionError:
                i += 1
        return False

    def continue_iteration(self):
        """
        Checks whether the program can continue the iteration by 2 factors:
            There are still negative values for variables in the last row
            There is still at least one positive theta value
        :return: True if it can continue. False otherwise
        """
        continue_iter = False
        if self.is_last_row_negative() == True:
            if self.is_theta_positive() == True:
                continue_iter = True
            else:
                print('The solution is unbounded. Another method is required for finding the optimal solution.')
                exit()
        return continue_iter

    def is_feasible(self):
        """
        Checks if the sum of artificial variables(value in the bottom right corner) is 0
        :return: True if the sum of artificial variables is 0. False otherwise
        """
        return self.tableau[self.tableau.rows-1][self.tableau.columns-1] == 0

    def iterate_stage_1(self):
        """
        Iterations for stage 1
        Scales the tableau until the sum of artificial variables is 0
        """
        while not self.is_feasible():
            self.scale()

    def is_value_greater_0(self):
        """
        Checks if the value in the bottom right corner is greater than 0
        :return: True if the value in the bottom right corner is greater than 0. False otherwise
        """
        return self.tableau[self.tableau.rows-1][self.tableau.columns-1] > 0

    def iterate_stage_2(self):
        """
        Iteration for stage 2
        Scales the tableau until there are no negative values in the bottom row except for 'Value' column
        """
        self.scale()

    def print_solution(self):
        """
        Prints the value for the optimal solution if exists and for each of the variables(basic and non-basic)
        """
        if self.tableau.max_or_min == 'max':
            print('Optimal solution for maximization is ' + str(round(self.tableau[-1][-1],3)) + '\n')
        elif self.tableau.max_or_min == 'min':
            print('Optimal solution for minimization is ' + str((-1) * round(self.tableau[-1][-1],3)) + '\n')

        print('Values of variables: ')

        for i in range(len(self.tableau.non_zero_variables)):
            print(self.tableau.non_zero_variables[i] + ' : ' + str(round(self.tableau[i][-1],4)))

        for i in self.tableau.var_row[:-1]:
            if i not in self.tableau.non_zero_variables:
                print(i + ' : 0.0')
