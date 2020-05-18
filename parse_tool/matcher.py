# to work with command line arguments
import argparse
import sys
# to parse test by regex
import re
# work with files
import os.path
# to highlight the printed text
import colored as colored
from pip._vendor.distlib.compat import raw_input


def read_command_line_arguments():
    print("Reading command line arguments ... started ")

    # sys.argv contains all the command line arguments
    print(sys.argv)

    # create object to work with command line arguments
    script_args = argparse.ArgumentParser(description="Parsing file/s to find strings by regex")

    # initiate the object with expected required parameters names that your command line script expects to get
    script_args.add_argument('-r', '--regex', required=True, help="Regex - the pattern to search for.")
    script_args.add_argument('-f', '--files', required=False,help="Files - A list of files to search in. If this parameter is omitted, "
                                  "the script will ask for this input in run time.")

    # add object that holds parameters with additional parameters (mutually exclusive params)
    mut_exclus_group = script_args.add_mutually_exclusive_group()

    mut_exclus_group.add_argument("-u", "--underline", required=False, action="store_true",
                                  help="Underline - '^' is printed underneath the matched text.")

    mut_exclus_group.add_argument("-c", "--color", required=False, action="store_true",
                                  help="Color - the matched text is highlighted in color [1]")

    mut_exclus_group.add_argument("-m", "--machine", required=False, action="store_true",
                                  help="Machine - print the output in the format: "
                                       "'file_name:line_number:start_position:matched_text' ")

    # get command line args by the predefined rules
    command_line_arguments = script_args.parse_args()

    return command_line_arguments


def get_files(command_line_arguments):
    files_list = list()

    # here I first do the check if parameter files contains something or it is empty
    # if command_line_arguments.files is empty string (not the " " but "") or in case it is " " then clean white spaces
    # and then ask if it is empty string
    if (not command_line_arguments.files) or (not command_line_arguments.files.strip()):
        # in case user did not supplied files as argument - we ask for input from STDIN
        print("Command line arguments do not contain file/s to check, please enter file/s or press q to exit: ")

        while True:
            file_name = raw_input()  #TODO:  raw_input() is depricated in python 3, you better use input() !!!!!!
            if file_name == 'q':
                break

            files_list.append(file_name.strip())
            print('Input is: ' + file_name + ', please enter file name or q to exit')
    else:
        print("\ncommand line arguments contain the next file/s: {}".format(command_line_arguments.files))

        # in case of few files separated with comma
        if ',' in command_line_arguments.files:
            tmp_list = command_line_arguments.files.split(',')
            # self.files_list = [tmp_elem.strip() for tmp_elem in tmp_list]
            for tmp_elem in tmp_list:
                if tmp_elem:
                    files_list.append(tmp_elem.strip())

        # in case of few files separated with ' ' or single file
        elif ' ' in command_line_arguments.files:
            tmp_list = command_line_arguments.files.split(' ')
            # self.files_list = [tmp_elem.strip() for tmp_elem in tmp_list]
            for tmp_elem in tmp_list:
                if tmp_elem:
                    files_list.append(tmp_elem.strip())
        else:
            # single file in command line, without ' '
            files_list = [command_line_arguments.files.strip()]

    return files_list


def check_regex(command_line_arguments):
    if(not command_line_arguments.regex) or (not command_line_arguments.regex.strip()):
        print("Bad or not existing regex !!")
        sys.exit()


class RegMatcher:
    """
        This class check if there is a match by pattern (regex) given by user via command line argument
    """
    # here we write class members - members that are per class and not per object from this class (static)
    # all objects from the class will see same value when access these members


    # in __init__() we write objects members (members that will be unique to each object of this class)
    def __init__(self, files_list, regex, color_flag, underline_flag, machine_flag):

        self.files_list     = files_list
        self.regex          = regex
        self.color_flag     = color_flag
        self.underline_flag = underline_flag
        self.machine_flag   = machine_flag

    def check_file_match_by_regex(self, file_name):
        print('\n\nParsing file: {}, line by line to find matches by regex {}'.format(file_name, self.regex))
        print('-------------------------------------------------------\n')

        # prepare regular expression - pattern
        pattern = re.compile(self.regex, re.IGNORECASE)

        # read all lines of the file
        # 'with' is a block that will takes care to close the file - so we do not ned to take care of it
        with open(file_name, 'r') as file:
            # read all lines of the file and return them as a list
            lines_list = file.readlines()

            # iterate over file lines parse by regex to find matches
            # enumerate returns me a tuple (line and line number)
            for line_num, line in enumerate(lines_list):
                # reset the temp variable before reuse
                new_line = ""

                # check line only if it is not empty
                if line.strip():
                    # find if were match/s - put them all in iterator obj (we cannot check if iterator is empty !!
                    match_iterator_obj = pattern.finditer(line)

                    # after the matches is/are ready (potentially holds the matches per line) go by command arguments

                    # -c - color the the matched substrings
                    if self.color_flag:
                        # for coloring the matched
                        red = lambda text: '\033[0;31m' + text + '\033[0m'

                        for matches_obj in match_iterator_obj:
                            # find in line each match (that iterator found) and color it in current line
                            # per line color all occurrences of the matched string
                            # if line contains matche/s, color them
                            new_line = 'File name: {}, Line number: {}, Line: {}'.format(file_name, line_num, line.replace(matches_obj.group(),
                                                                                                                           red(str(matches_obj.group()))))

                        # print line while end of line is omitted from the line
                        print('{} : {}'.format(line_num, line.rstrip()))
                        print(new_line)

                    # -m - machine print details about what was found
                    elif self.machine_flag:
                        for matches_obj in match_iterator_obj:
                            new_line = 'File name: {}, Line number: {}, Line: {}, start_position: {}'\
                                       .format(file_name, line_num, line, matches_obj.start())

                            # print line while end of line is omitted from the line
                            print('{} : {}'.format(line_num, line.rstrip()))
                            print(new_line)

                    # -u - underline the matched substrings
                    elif self.underline_flag:
                        new_line = ""
                        for matches_obj in match_iterator_obj:
                            # print 'File name: {}, Line number: {}, Line: {}'.format(file_name, line_num, line)
                            new_line += (" " * (matches_obj.start() - len(new_line))) + "^" * (matches_obj.end() - matches_obj.start())

                        # print line while end of line is omitted from the line
                        print('{} : {}'.format(line_num, line.rstrip()))
                        print(" " * 4 + new_line)

                    else:
                        for matches_obj in match_iterator_obj:
                            print('{} : {}'.format(line_num, line.rstrip()))

    def check_files_by_regex(self):
        # parse files only if such vere given by user
        if not self.files_list:
            print('Sorry, no files to check for match !!')
            sys.exit()

        for file_name in self.files_list:
            # check that list contains file, such File exists and File is not empty
            if False is os.path.isfile(file_name):
                print('File: {} does not exist !!'.format(file_name))

            elif 0 == os.stat(file_name).st_size:
                print('File: {} is empty !!'.format(file_name))

            else:
                self.check_file_match_by_regex(file_name)


if __name__== "__main__":

    """ get command line arguments: I put them as script parameter instead of letting user enter them each time 
        For exp, I run the script with these params: -r "\w*reg\w" -c -f "C:\ILANA\PYTHON_PROJECTS\parse_tool\File4.txt
    """
    command_line_arguments = read_command_line_arguments()

    """
    I check if Params command line params contain regex expression
    """
    check_regex(command_line_arguments)

    """
    get file/s from the user to check for regex = prepare a list of file/s
    """
    files = get_files(command_line_arguments)

    """
    create reg matcher object, deliver it all info about from the user command line: 
    regex rule, addition user commands in case the natch was /were found, such as: 
        color:     color in red the matched words
        underline: underline the matched words
        machine:   double the line and indicated the indexes from till the match was found 
    """
    matcher = RegMatcher(files,
                         command_line_arguments.regex,
                         command_line_arguments.color,
                         command_line_arguments.underline,
                         command_line_arguments.machine)

    matcher.check_files_by_regex()