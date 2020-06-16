import argparse
import os
import random
import datetime
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List

from numpy import double




@dataclass
class TasksActivityLogGenerator:
    activities_list   : List[tuple] = field(default_factory = list)
    task_activity_log_file : str = ""
    sleep_lower_limit      : int = -1
    sleep_upper_limit      : int = -1
    task_id_lower_limit    : int = -1
    task_id_upper_limit    : int = -1
    number_of_entries      : int = 0

    def printRed(self, text):
        print(f'\033[91m {text}\033[00m')

    def get_user_input(self):
        print("Reading command line arguments ... started ")

        # sys.argv contains all the command line arguments
        print(sys.argv)

        # create object to work with command line arguments
        script_args = argparse.ArgumentParser(description="Script will simulate tasks activities log file ")

        # initiate the object with expected required parameters names that your command line script expects to get

        # input_folder_path
        script_args.add_argument('-f',
                                 '--file',
                                 required=False,
                                 help="file - full path to log file that will be created and will contain tasks activities,\n "
                                      "if full file name was not supplied - log file will be created in project folder ")

        script_args.add_argument('-n',
                                 '--number',
                                 required=True,
                                 help="number of entries in log file \n")

        script_args.add_argument('-tl',
                                 '--task_lower_limit',
                                 required=True,
                                 help="task_id lower limit \n")

        script_args.add_argument('-tu',
                                 '--task_upper_limit',
                                 required=True,
                                 help="task_id upper limit \n")

        script_args.add_argument('-sl',
                                 '--sleep_lower_limit',
                                 required=True,
                                 help="sleep lower limit \n")

        script_args.add_argument('-su',
                                 '--sleep_upper_limit',
                                 required=True,
                                 help="sleep upper limit \n")

        # get command line args by the predefined rules
        command_line_arguments = script_args.parse_args()

        return command_line_arguments


    def basic_input_validation_and_update(self, command_line_arguments):
        # check log file
        # ==============
        if not command_line_arguments.file or not command_line_arguments.file.strip():
            self.printRed(f"'file': wasn't supplied by user, so will be created default log file: {self.task_activity_log_file}")
            # set default file name
            self.task_activity_log_file = os.getcwd() + "\\" + 'tasks_activities.log'
        else:
            self.task_activity_log_file = command_line_arguments.file.strip()

        print(f'File name: {self.task_activity_log_file}')

        # check number of entries
        # ==============
        if not command_line_arguments.number or not command_line_arguments.number.strip():
            self.printRed(f"'number' is missing")
            return False

        command_line_arguments.number = int(command_line_arguments.number.strip())

        if command_line_arguments.number <= 0:
            self.printRed(f"'number' is invalid")
            return False

        self.number_of_entries = command_line_arguments.number
        print(f"'number': {self.number_of_entries}")

        # check sleep lower and upper limits existence
        # ===========================================
        if not command_line_arguments.sleep_lower_limit or not command_line_arguments.sleep_lower_limit.strip() or \
           not command_line_arguments.sleep_upper_limit or not command_line_arguments.sleep_upper_limit.strip():
            self.printRed(f'One or both of sleep limits is missing')
            return False

        command_line_arguments.sleep_lower_limit = int(command_line_arguments.sleep_lower_limit.strip())
        command_line_arguments.sleep_upper_limit = int(command_line_arguments.sleep_upper_limit.strip())

        if command_line_arguments.sleep_lower_limit < 0 or \
           command_line_arguments.sleep_upper_limit <= 0 or \
           command_line_arguments.sleep_lower_limit > command_line_arguments.sleep_upper_limit or \
           command_line_arguments.sleep_lower_limit == command_line_arguments.sleep_upper_limit:
            self.printRed(f'One or both sleep limits supplied with invalid value')
            return False

        self.sleep_lower_limit = command_line_arguments.sleep_lower_limit
        self.sleep_upper_limit = command_line_arguments.sleep_upper_limit
        print(f"'sleep_lower_limit': {self.sleep_lower_limit}, 'sleep_upper_limit': {self.sleep_upper_limit}")


        # check task id lower and upper limits existence
        # ==============================================
        if not command_line_arguments.task_lower_limit or not command_line_arguments.task_lower_limit.strip() or \
           not command_line_arguments.task_upper_limit or not command_line_arguments.task_upper_limit.strip():
            self.printRed(f'One of task_id limits is missing')
            return False

        command_line_arguments.task_lower_limit = int(command_line_arguments.task_lower_limit.strip())
        command_line_arguments.task_upper_limit = int(command_line_arguments.task_upper_limit.strip())

        if command_line_arguments.task_lower_limit < 0 or \
           command_line_arguments.task_upper_limit <= 0 or \
           command_line_arguments.task_lower_limit > command_line_arguments.task_upper_limit or \
           command_line_arguments.task_lower_limit == command_line_arguments.task_upper_limit:
            self.printRed(f'One or both task_id limits supplied with invalid value')
            return False

        self.task_id_lower_limit = command_line_arguments.task_lower_limit
        self.task_id_upper_limit = command_line_arguments.task_upper_limit
        print(f"'task_id_lower_limit': {self.task_id_lower_limit}, 'task_id_upper_limit': {self.task_id_upper_limit}")
        return True


    def get_random_task_id(self):
        return random.randint(self.task_id_lower_limit, self.task_id_upper_limit)


    def get_random_delay(self):
        return random.randint(self.sleep_lower_limit, self.sleep_upper_limit)


    def create_task_activities(self):
        prev_result = None

        task_id_list = list()
        task_timestamp_list = list()

        initial_time_stamp = datetime.datetime.now().timestamp()
        time_stamp = initial_time_stamp
        for cnt in range(0, self.number_of_entries, 1):
            task_id = self.get_random_task_id()

            # generate task_id, check that there will no be two same consistent task_IDs
            if task_id == prev_result:
                continue
            prev_result = task_id

            # this is the way to get timestamp from current datetime
            # current_task_time_stamp = datetime.datetime.now().timestamp()

            # update both lists
            task_id_list.append(task_id)
            task_timestamp_list.append(double(time_stamp))

            # wait some random time
            delay_time = self.get_random_delay()
            time_stamp += delay_time
            # time.sleep(delay_time)
            print(f'[{cnt+1}/{self.number_of_entries}], Added task activity: {(task_id, time_stamp)}, printed with delay time: {delay_time}')

        print(f"Task activities list is ready, creation time: {datetime.datetime.now().timestamp() - initial_time_stamp} sec")
        time.sleep(7)

        # unify two lists into one list = it will be list of tuples.
        # list1 = [task_id, ....]
        # list2 = [timestamp, ...]
        # unified_list = [(task_id, timestamp), (), (), ...]
        print(f"length of task ids list: {len(task_id_list)}, length of timestamps list: {len(task_timestamp_list)}")
        self.activities_list = list(zip(task_id_list, task_timestamp_list))

        print('\nPrinting tasks activities list before log file creation ....\n')
        initial_time_stamp = datetime.datetime.now().timestamp()
        for num, task_elem in enumerate(self.activities_list):
            print(f'[{num}/{len(self.activities_list)}], Added task activity: {task_elem}')
        print(f"Printing all activities took: {datetime.datetime.now().timestamp() - initial_time_stamp} sec")
        time.sleep(7)
        self.store_in_file()

    def store_in_file(self):
        # delete backup_logs file before re creation
        if os.path.exists(self.task_activity_log_file):
            os.remove(self.task_activity_log_file)

        initial_time_stamp = datetime.datetime.now().timestamp()
        # write list into file
        with open(self.task_activity_log_file, 'a') as file:
            for task_elem in self.activities_list :
                #                   task_timestam         task_Id
                file.write(f'{double(task_elem[1])}, {int(task_elem[0])} \n')
        print(f"Writing all activities into file took: {datetime.datetime.now().timestamp() - initial_time_stamp} sec")


# ---------------------------------------------------------------------------------- #

if __name__ == "__main__":
    tasks_activity_generator = TasksActivityLogGenerator()
    command_line_arguments = tasks_activity_generator.get_user_input()
    if not tasks_activity_generator.basic_input_validation_and_update(command_line_arguments):
        sys.exit("one or more input parameters is missing or not valid")

    tasks_activities_list = tasks_activity_generator.create_task_activities()





