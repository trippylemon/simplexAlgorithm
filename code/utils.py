#utils for usage in further code

class colours:
    white = '\033[97m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    reset = '\033[0m'

digits = ['0','1','2','3','4','5','6','7','8','9']
pos_signs = ['>', '>=']
neg_signs = ['<', '<=']
signs = ['<', '>','>=','<=', '=','-']
operands = ['+','-']
variables = ['x','y','z','m','n']
intro_text = ' \nWelcome to Simplex World! Using this program you can optimize your solution by using simplex method. Below you can see the main menu. \nBefore proceeding, reading the instructions is recommended for quick and easy use.\n '

instructions = f'{colours.green}     ---INSTRUCTIONS---{colours.reset}' \
               f'\n{colours.green}Only following variables are allowed in that order  as an input: x, y, z, m, n.{colours.reset}' \
               f'\n{colours.green}To input an objective function, ignore the variable you are trying to maximize/minimize and input what goes after "=" sign with coefficients timed by (-1){colours.reset}' \
               f'\n{colours.yellow}  example: If you want to maximize P=3x-2y, your input must be "-3x+2y".{colours.reset}'\
               f'\n{colours.green}If one of the variables is in objective function but not in constraint, put 0 before the variable in the constraint. If the coefficient is 1 or -1, write 1/-1 before the variable.{colours.reset}' \
               f'\n{colours.yellow}  example: Objective function: "x+5y-3z". "y" is not in one of the constraints, so your input must be: "-4x+0y+1z>33".{colours.reset}' \
               f'\n{colours.red}Not following the instructions will be followed with a wrong result. {colours.reset}'

def is_digit(adigit):
    """
    Checks if the parameter is a digit
    :param adigit: input that is checked for type
    :return: True if the parameter is a digit. False otherwise.
    """
    return adigit in digits

def is_sign(achar):
    """
    Checks if the parameter is in signs list
    :param achar: input that is checked
    :return: True if the parameter is a sign specified in the list 'signs'. False otherwise.
    """
    return achar in signs

def is_operand(achar):
    """
    Checks if the parameter is '+' or '-'
    :param achar: input that is checked
    :return: True if the parameter is '+' or '-'. False otherwise
    """
    return achar in operands

def is_variable(achar):
    """
    Checks if the parameter is in variables list
    :param achar: input that is checked
    :return: True if the parameter is in variables list. False otherwise.
    """
    return achar in variables

def display_dictionary(dictionary, title):
    """
    Displays a dictionary with its title
    :param dictionary: a dictionary
    :param title: a title
    """

    print(title)
    for key, value in dictionary.items():
        print(key, value)
    print()

def number_of_negatives(alist):
    """
    Counts the number of negative coefficients in 'alist'
    :param alist: a list to iterate through
    :return: the number of negative coefficients in 'alist'
    """
    neg_num = 0

    for i in alist:
        if i == '-':
            neg_num += 1

    return neg_num

def number_of_signs(alist):
    """
    Counts the number of signs in 'alist'
    :param alist: a list to iterate through
    :return: the number of signs in 'alist'
    """
    signs_num = 0
    ineq_signs = ['>','<','=']
    for i in alist:
        if i in ineq_signs:
            signs_num += 1

    return signs_num

def strip_a_string(astring):
    """
    Strips a string and returns the coefficients of variables and inequality signs
    :param astring: a string to strip
    :return: list of coefficients and inequality signs
    """
    #checks if the user inputted blank spaces by mistake and deletes them if True

    for i in astring:
        if i == ' ':
            astring = astring.replace(i,'')

    last_element = 0
    list_of_elements = []

    #concatenates multiple digits in a row to form one number if applicable

    for i in range(len(astring)):
        if is_operand(astring[i]) or is_sign(astring[i]) or is_variable(astring[i]):
            list_of_elements.append(astring[last_element:i])
            last_element = i + 1
            list_of_elements.append(astring[i])

        if i == len(astring) - 1:
            list_of_elements.append(astring[last_element:])

    #deletes empty spaces

    for i in list_of_elements:
        if i == '':
            list_of_elements.remove(i)

    signs_num = number_of_signs(list_of_elements)

    #concatenates two parts of inequality sign if applicable

    if signs_num > 0:
        for i in range(len(list_of_elements)-signs_num):
            if (list_of_elements[i] == '>' or '<') and list_of_elements[i+1] == '=':
                list_of_elements[i+1] = list_of_elements[i] + list_of_elements[i+1]
                list_of_elements.remove(list_of_elements[i])
            else:
                pass

    coef_list = []

    #converts a string to integer if it is int type

    for i in list_of_elements:
        if is_sign(i):
            coef_list.append(i)
        elif i.isdigit():
            coef_list.append(int(i))

    num_neg = number_of_negatives(coef_list)

    #concatenate '-' with a number

    for i in range(0,len(coef_list)-num_neg):
        if coef_list[i] == '-' and type(coef_list[i+1]) == int:
            coef_list[i+1] = int('-' + str(coef_list[i+1]))
            coef_list.remove(coef_list[i])

    return coef_list
