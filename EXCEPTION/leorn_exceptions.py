import logging



def func_raises_exception():
    # throw exception + description + parameters
    raise ValueError('A very specific bad thing happened', 1, 2, 'baz')

def get_file_lines_number():
    file_nane = "C:/ILANA/PYTHON_PROJECTS/april_for_read.txt"

    # here we will need to do 2 operations:
    # 1. open file - that can throw exception if file does not exist
    # 2. read from file - this also can throw exception if file corrupted and impossible to read from it
    # we must take care of both 1 and 2 !!!!

    # but if we succcedded to open file but failed to read from - we will get into except block and not to else block
    # where we close the file - file will remain oppened and catched - nobody else will not be able to work with !!!! )-:

    # this is the correct way to work using finally

    try: # to open file
        f = open(file_nane, "r")
        try: # to read from file
            print("File could be oppenned ok, try to read number of lines: ", len(f.readlines()))
        finally: # no meeter if file could be read or not - close it !!
            f.close()
    except IOError:
        print("IOError exception occurred during opening file: ", file_nane)

# my new type exception class based on Python Exception class
class FactorialArgumentError(Exception):

    # my exception initiated with exception object
    def __init__(self, arg):
        self.exception_argument = arg

    # when exception is thrown the returned string from the exception that is printed on the screen is initiated here
    def __str__(self):
        return "### Provided argument: %s is not a positive integer as expected ###" % self.exception_argument

    # getter of the argument that user entered
    def get_exception_argument(self):
        return self.exception_argument


def find_factorial():
    # try to convert input to the type 'int' - if user enters string the exception will be raised
    # !!!! when you convert number into tint type - say in what base - here I need base 10 (normal int)

    # first get input as is from user
    n = input("Please enter number to make Factorial with ...: ")

    # then try to convert to tint type + check if positive input
    # int(n, base=10) - return from input '4' (which is always a string to int - 4
    # isinstance(int(n, base=10), int) then I check if input is of int type
    # ##### if not or if not positive - I raise exception #######
    try:
        if not isinstance(int(n, base=10), int) or int(n, base=10) < 0:
            # isinstance(n, int) get element and checks if it it of type (instanse) int
            # since input() returns string - this func will fail so we need to try to convert from string to int by:
            # int(n, base=10) - convert into int with base 10 if it fails we will get into except region !!!

            # conclusion: use this check only: if not isinstance(int(n, base=10), int) to know if input is of int type
            raise FactorialArgumentError(n) # at this moment will be called __init__() from class FactorialArgumentError
                                            # then except section will be called
    except FactorialArgumentError as my_error:
        print("Function expected for positive integer but instead got input: %s" % my_error.get_exception_argument())
        # this way will return None from the function
    else:
        number = int(n, base=10)
        fact = 1

        for i in range(1, number + 1, 1):
            fact = fact * i
        return fact  # this way will return factorial from the function


# ================= Exceptions =============================
""" You should never raise Exception directly: it's not specific enough to be helpful """
""" while defining your own Exception class - Always inherit from (at least) Exception """

class CredentialErrors(Exception):
    """Basic exception for errors raised by cars"""
    def __init__(self, arg, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = "An error occurred with credential %s" % msg

        # then in any case initiate Exception (which is super class) with this exception
        super(CredentialErrors, self).__init__(msg)
        self.credential = arg


class UsernameTooShort(CredentialErrors):
    """ Problem with User Name length """

    # my exception initiated with exception object
    def __init__(self, *arg): # args will contain 2 elements, user name string and minimal allowed length
        super(UsernameTooShort, self).__init__(arg, msg="User Name: {} is short than allowed: {}".format(arg[0], arg[1]))
        self.exception_argument = "User Name: {} is short than allowed: {}".format(arg[0], arg[1])

    # getter of the argument that user entered
    def get_exception_argument(self):
        return self.exception_argument


class UsernameTooLong(CredentialErrors):
    """ Problem with User Name length """

    # my exception initiated with exception object
    def __init__(self, *arg):
        super(UsernameTooLong, self).__init__(arg, msg="User Name: {} is long than expected: {}".format(arg[0], arg[1]))
        self.exception_argument = "User Name: {} is long than expected: {}".format(arg[0], arg[1])

    # getter of the argument that user entered
    def get_exception_argument(self):
        return self.exception_argument


class UsernameContainsIllegalCharacter (CredentialErrors):
    """ Problem with User Name content """

    # my exception initiated with exception object
    def __init__(self, *arg):
        super(UsernameContainsIllegalCharacter, self).__init__(arg, msg="User name: {} contains illegal character: {} at index: {}".format(arg[0], arg[1], str(arg[0]).index(arg[1])))
        self.exception_argument = "User name: {} contains illegal character: {} at index: {}".format(arg[0], arg[1], str(arg[0]).index(arg[1]))

    # getter of the argument that user entered
    def get_exception_argument(self):
        return self.exception_argument


class PswTooShort(CredentialErrors):
    """ Problem with Password length """

    # my exception initiated with exception object
    def __init__(self, *arg):
        super(PswTooShort, self).__init__(arg, msg="Password: {} is short than expected: {}".format(arg[0], arg[1]))
        self.exception_argument = "Password: {} is short than expected: {}".format(arg[0], arg[1])

    # getter of the argument that user entered
    def get_exception_argument(self):
        return self.exception_argument


class PswTooLong(CredentialErrors):
    """ Problem with Password length """

    # my exception initiated with exception object
    def __init__(self, *arg):
        super(PswTooLong, self).__init__(arg, msg="Password: {} is long than expected: {}".format(arg[0], arg[1]))
        self.exception_argument = "Password: {} is long than expected: {}".format(arg[0], arg[1])

    # getter of the argument that user entered
    def get_exception_argument(self):
        return self.exception_argument


class PasswordMissingCharacter (CredentialErrors):
    """ Problem with Password content """

    # my exception initiated with exception object
    def __init__(self, *arg):
        super(PasswordMissingCharacter, self).__init__(arg, msg="Password: {} is missing character of type: {}".format(arg[0], arg[1]))
        self.exception_argument = "Password: {} is missing character of type: {}".format(arg[0], arg[1])

    # getter of the argument that user entered
    def get_exception_argument(self):
        return self.exception_argument
# ==============================================


def check_length(str, min_len, max_len):
    if len(str) < min_len:
        return False, "short"
    elif len(str) > max_len:
        return False, "long"
    else:
        return  True, "ignore it ...."


def check_user_name_illegal_characters(user_name):
    # user name must contain only:
    #   numbers
    #   '_'   no other special characters are allowed
    #   letters

    for character in user_name:
        if not character.isdigit() and not character.isalpha() and character != '_':
            raise UsernameContainsIllegalCharacter(user_name, character, user_name.index(character))


def check_psw_illegal_characters(psw):
    # contains at least 1 upper letter
    # contains at least 1 lower letter
    # contains at least 1 number
    # contains at least 1 special character (for exp: ! | . | % | # |@ |* ...)

    upper_letter_flag = False
    lower_letter_flag = False
    digit_flag = False
    special_character_flag = False

    for character in psw:
        if not character.isdigit() and not character.isalpha():
            special_character_flag = True
        elif character.isalpha() and character.isupper():
            upper_letter_flag = True
        elif character.isalpha():
            lower_letter_flag = True
        elif character.isdigit():
            digit_flag = True

    if not lower_letter_flag:
        raise PasswordMissingCharacter(psw, "Lowercase")
    elif not upper_letter_flag:
        raise PasswordMissingCharacter(psw, "Uppercase")
    elif not digit_flag:
        raise PasswordMissingCharacter(psw, "Digit")
    elif not special_character_flag:
        raise PasswordMissingCharacter(psw, "Special")


def check_input(user_name, psw):
    # set color of the printed verdict traces
    red = lambda text: '\033[0;31m' + text + '\033[0m'
    framed = lambda text: '\033[0;51m' + text + '\033[0m'

    try:
        # check user name length
        success, indicator = check_length(user_name, 3, 16)

        if not success and indicator == "short":
            raise UsernameTooShort(user_name, 3)
    except UsernameTooShort as short_user_name_error:
        print(red("(User Name {}, Psw {}):   exception - {}".format(user_name, psw, short_user_name_error.get_exception_argument())))
    else:
        try:
            if not success and indicator == "long":
                raise UsernameTooLong(user_name, 16)
        except UsernameTooLong as long_user_name_error:
            print(red("(User Name {}, Psw {}):   exception - {}".format(user_name, psw, long_user_name_error.get_exception_argument())))
        else:
            try:
                # check user name contains nothing than:
                #   numbers
                #   '_'
                #   letters
                check_user_name_illegal_characters(user_name)

            except UsernameContainsIllegalCharacter as user_name_illegal_character:
                print(red("(User Name {}, Psw {}):   exception - {}".format(user_name, psw, user_name_illegal_character.get_exception_argument())))
            else:
                try:
                    # check psw length
                    success, indicator = check_length(psw, 8, 40)

                    if not success and indicator == "short":
                        raise PswTooShort(psw, len(psw), 8)
                except PswTooShort as short_psw:
                    print(red("(User Name {}, Psw {}):   exception - {}".format(user_name, psw, short_psw.get_exception_argument())))
                else:
                    try:
                        if not success and indicator == "long":
                            raise PswTooLong(psw, len(psw), 40)
                    except PswTooLong as long_psw:
                        print(red("(User Name {}, Psw {}):   exception - {}".format(user_name, psw, long_psw.get_exception_argument())))
                    else:
                        try:
                            # contains at least 1 upper letter
                            # contains at least 1 lower letter
                            # contains at least 1 number
                            # contains at least 1 special character (for exp: ! | . | % | # |@ |* ...)
                            check_psw_illegal_characters(psw)

                        except PasswordMissingCharacter as psw_miss_character:
                            print(red("(Psw {}, Psw {}):   exception - {}".format(user_name, psw,psw_miss_character.get_exception_argument())))
                        else:
                            print(framed("('User Name' {}, 'Password' {}): OK".format(user_name, psw)))


def targil_mesakem():

    # get user's user name - check that it follows next rules:
    # user name
    # user_name = input("Please enter 'User Name': ") # input() automatically converts input into string !!!!!
    # 1. 'User Name' must contain both English letters and numbers and underscore character
    # 2. length must be [3 - 16] characters

    # get user's pasw - check that it follows next rules:
    # psw
    # 1. length [8 - 40]
    # 2. contains at least one upper letter, at least one lower letter,  at least one number, at least one special character (!, ,,,,)
    # psw = input("Please enter 'Password': ")

    # Tests
    check_input("1", "2")
    check_input("0123456789ABCDEFG", "2")
    check_input("A_a1.", "12345678")
    check_input("A_1", "2")
    check_input("A_1", "ThisIsAQuiteLongPasswordAndHonestlyUnnecessary")
    check_input("A_1", "abcdefghijklmnop")
    check_input("A_1", "ABCDEFGHIJLKMNOP")
    check_input("A_1", "ABCDEFGhijklmnop")
    check_input("A_1", "4BCD3F6h1jk1mn0p")
    check_input("A_1", "4BCD3F6.1jk1mn0p")
    check_input("aprilka", "Aprilka2007")

# ---------------------------------------------------------------------------------


if __name__ == "__main__":

    targil_mesakem()


    """fact = find_factorial()
    print(fact) # can return None/ factorial
    get_file_lines_number()

    logger = logging.getLogger(__name__)

    x = 3

    try:
        if x == 2:
            func_raises_exception()
    except ValueError as error:
        print("exception occurred: ", error.args)
        logger.error(error)
    else:
        # this will run only if there were no exception
        print("exception did not occurred: ")
    finally:
        print("even if exception occurred or not - XA XA XA ")
        # this will run any way even if there was an exception"""

