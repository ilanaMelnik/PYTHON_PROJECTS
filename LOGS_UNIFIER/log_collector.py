import argparse
import glob
import os
import re
import sys
from dataclasses import dataclass, field
from   typing import List



@dataclass
class Unifier:
    # user's input
    # attribute
    files_list            : List[str] = field(default_factory = list)

    input_folder_path     : str = ""
    results_file_name     : str = ""
    log_file_name         : str = "" # for exp, MD.WebService, while there can be more logs and we will get names like: MD.WebService.07.log, here 07 is index
    log_file_extension    : str = "" # for exp, .log


    def get_user_input(self):
        print("Reading command line arguments ... started ")

        # sys.argv contains all the command line arguments
        print(sys.argv)

        # create object to work with command line arguments
        script_args = argparse.ArgumentParser(description="Script will unify the log files into single lig file")

        # initiate the object with expected required parameters names that your command line script expects to get

        # input_folder_path
        script_args.add_argument('-p',
                                 '--path',
                                 required=False,
                                 help="input_folder_path - where all the log files. If this parameter is omitted, "
                                      "the script will ask for it in run time.\n")
        # results_file_name
        script_args.add_argument('-r',
                                 '--result',
                                 required=False,
                                 help="results_file_name - a single file that will hold the entire content "
                                      "of all log files from input_folder_path.\n")

        # log_file_name
        script_args.add_argument('-n',
                                 '--name',
                                 required=False,
                                 help="log_file_name - is a log file name without extension and without index numbers. "
                                      "All logs files have same names but might have indexation.\n")

        # log_extension
        script_args.add_argument('-e',
                                 '--extension',
                                 required=False,
                                 help="log_file_extension - log file extension.\n")

        # get command line args by the predefined rules
        command_line_arguments = script_args.parse_args()

        return command_line_arguments


    def printRed(self, text):
        print(f'\033[91m {text}\033[00m')


    def is_file_name_correct(self, file_name):
        # extract file name without path, file name is second element in created tuple of 2 elems (path, name)
        # so I take it with -1 (I take last elem in created tuple)
        file_name_no_path = file_name.split("\\")[-1]

        pattern = f'^{self.log_file_name}(\\.\\d+)?\\.{self.log_file_extension}$'
        result = bool(re.match(pattern, file_name_no_path))
        return result


    """    
        Extracts index from the log file name. Lof file name can have extension or not. 
        So the Log file name pattern as following: 

        <log file name>[.index].<log> 

        Exp:
        MD.WebService.14.log
        MD.WebService.log

        in case there is no index the returned value is -1, else index is returned     
    """
    def log_file_index(self, file_name):
        indexes = re.findall('[0-9]+', file_name)
        if not indexes:
            index = -1
        else:
            index = int(str(indexes[0]))

        print(f'The index of the file name {file_name} is {index}')
        return index


    def check_input_and_update(self, command_line_arguments):
        # logs name --------------
        if not command_line_arguments.name or not command_line_arguments.name.strip():
            self.printRed(f"Sorry, 'name': wasn't supplied by user !!")
            return False
        self.log_file_name = command_line_arguments.name.strip()
        print(f"'name': {self.log_file_name}")

        # logs extension --------------
        if not command_line_arguments.extension or not command_line_arguments.extension.strip():
            self.printRed(f"Sorry, 'extension': wasn't supplied by user !!")
            return False
        self.log_file_extension = command_line_arguments.extension.strip()
        print(f"'extension': {self.log_file_extension}")


        # input folder path --------------
        command_line_arguments.path = command_line_arguments.path.strip()

        if not command_line_arguments.path:
            self.printRed(f"Sorry, 'path': wasn't supplied by user !!")
            return False
        if not command_line_arguments.path.endswith("\\"):
            command_line_arguments.path = command_line_arguments.path + "\\"

        # check that this folder exists on the PC (pay attention, exists() will return True even if
        # it is file with the same name as folder. So we must add check that it is a file !!!
        if not os.path.exists(command_line_arguments.path) or not os.path.isdir(command_line_arguments.path):
            self.printRed(f"Sorry, 'path': {command_line_arguments.path} doesnt exist or isn't a directory !!")
            return False
            # check that path is accessible for READ from
        if not os.access(command_line_arguments.path, os.R_OK):
            self.printRed(f"Sorry, 'path': {command_line_arguments.path} isn't accessible for READ from !!")
            return False

            # check folder is not empty
        if not os.listdir(command_line_arguments.path):
            self.printRed(f"Sorry, 'path': {command_line_arguments.path} is empty !!")
            return False

        # get all file names into a tmp list
        tmp_files_list = list()
        for root, dirs, files in os.walk(command_line_arguments.path):
            for file in files:
                # append the file full name (path+file name) to the list
                full_file_name = os.path.join(root, file)
                tmp_files_list.append(full_file_name)

        # self.files_list = self.files_list[::-1]

        # copy into new list only correct file
        for file_name in tmp_files_list:
            # remove log file name from the list if:
            # file doesnt exist indeed(it was actually a folder) or file exist but empty or file isn't accessible
            # or does not match according to the naming convention
            if not os.path.exists(file_name)            or \
               not os.path.isfile(file_name)            or \
               not self.is_file_name_correct(file_name) or \
               os.stat(file_name).st_size == 0:
                self.printRed(f'\nSorry, Invalid file name: {file_name}  !!\n')
            else:
                self.files_list.append(file_name)
                print(f'checked file name: {file_name}  - file is OK')

        if not self.files_list:
            self.printRed(f"Sorry, 'path': {command_line_arguments.path} contains files types different than expected")
            return False

        # sort files in correct order from the very first to the most recent
        # sorted(iterable, key=key, reverse=reverse) - sorted method does not modify the original list !!!!
        self.files_list = sorted(self.files_list, key=self.log_file_index, reverse=True)
        print('The new list of log files is:')
        print(*self.files_list, sep=" \n")
        # print(*self.files_list)  # * means: print all list elems in a list
        # print(*self.files_list, sep=", ") # print all list elems in a list with separator ", "

        self.input_folder_path = command_line_arguments.path
        print(f"'path': {self.input_folder_path}")


        # result file --------------
        command_line_arguments.result = command_line_arguments.result.strip()

        if not command_line_arguments.result or not command_line_arguments.result:
            self.printRed(f"Sorry, 'result': wasn't supplied by user !!")
            return False

        # result can be file name (without path) - means reate result file in same folder - so we build path
        # or a full path
        if "\\" not in command_line_arguments.result:
            # it means the result is not full path but only file name - means create result file here in place) then build path
            command_line_arguments.result = os.getcwd() + "\\" + command_line_arguments.result
            # check if results file already exists - if so delete it
        elif not command_line_arguments.result.endswith("\\"):
            command_line_arguments.result = command_line_arguments.result + "\\"

        # result file full name is ready - check if exist then delete
        if os.path.exists(command_line_arguments.result):
            os.remove(command_line_arguments.result)

        self.results_file_name = command_line_arguments.result
        print(f"'result': {self.results_file_name}")

        return True


    """    
    arranges all log file names from the user's folder defined by: input_folder_path  
    into a list, sorted from the most ancient log to the most recent log 
        
    Log naming convention tells us who is the most ancient, exp:
    MD.WebService.14.log is most ancient
    MD.WebService.log is most recent (it has no index at all)     
    """

    def copy(self, file_name, result_file):

        with open(file_name, 'r') as log_file:
            # file.readlines() - reads all lines of the file and return them as a list - this atittude is good only for small files
            # as it reads the whole content of the file to the memory of the PC the script is running on.
            # But for the big ones it is very heavy and bad way !!!!
            # lines_list = file.readlines()

            result_file.write(f'\n \n----------------START OF FILE: {log_file.name} -------------------\n')
            # read line by line
            while True:
                single_line = log_file.readline()
                if not single_line:
                    break # line is empty - EOF reached

                print(f'Read File: {log_file.name}, Line: {single_line}')
                result_file.write(single_line)

            result_file.write(f'\n \n--------------END OF FILE: {log_file.name} -----------------\n')


    def copy_logs_content(self):
        with open(self.results_file_name, 'a') as result_file:
            for file_name in self.files_list:
                self.copy(file_name, result_file)


# ----------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":

    unifier_obj = Unifier()

    command_line_arguments = unifier_obj.get_user_input()

    if not unifier_obj.check_input_and_update(command_line_arguments):
        sys.exit("one or more input parameters is missing or not valid")

    unifier_obj.copy_logs_content()


