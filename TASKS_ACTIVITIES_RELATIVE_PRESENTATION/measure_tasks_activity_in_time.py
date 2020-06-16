import argparse
import os
import sys
from dataclasses import dataclass, field
from typing import List, Dict
import time
import datetime
from numpy import double


@dataclass
class TasksActivityMonitor:
    task_activities_dict   : Dict[double, List] = field(default_factory = dict)
    task_activity_log_file : str = ""
    lower_boundary         : int = -1
    upper_boundary         : int = -1
    task_id                : int = -1


    def get_user_input(self):
        print("Reading command line arguments ... started ")

        # sys.argv contains all the command line arguments
        print(sys.argv)

        # create object to work with command line arguments
        script_args = argparse.ArgumentParser(description="Script presents tasks activity in time")

        # initiate the object with expected required parameters names that your command line script expects to get

        # input_folder_path
        script_args.add_argument('-f',
                                 '--file',
                                 required=True,
                                 help="file - log file. Current log file should contain all the tasks activities to work with.\n")

        script_args.add_argument('-t',
                                 '--task_id',
                                 required=False,
                                 help="task_id. Present statistics about current task_id \n")

        script_args.add_argument('-l',
                                 '--lower',
                                 required=False,
                                 help="lower boundary. Showall tasks activities from current boundary timestamp.\n till upper boundary \n")

        script_args.add_argument('-u',
                                 '--upper',
                                 required=False,
                                 help="upper boundary. Show all tasks activities from lower boundary timestamp.\n till current timestamp \n")

        # get command line args by the predefined rules
        command_line_arguments = script_args.parse_args()

        return command_line_arguments


    def printRed(self, text):
        print(f'\033[91m {text}\033[00m')

    """
    method performs basic check and update of command line arguments into class 
    """
    def check_input_and_update(self, command_line_arguments):

        # check log file
        command_line_arguments.file = command_line_arguments.file.strip()

        if not command_line_arguments.file:
            self.printRed(f"Sorry, 'file': wasn't supplied by user !!")
            return False

        # check if log file is a file, exists, not empty
        if not os.path.exists(command_line_arguments.file) or \
           not os.path.isfile(command_line_arguments.file) or \
            os.stat(command_line_arguments.file).st_size == 0:
            self.printRed(f'\nSorry, Invalid or empty file name: {command_line_arguments.file}  !!\n')
            return False

        self.task_activity_log_file = command_line_arguments.file
        print(f'File name: {self.task_activity_log_file}')

        # check lower, upper boundaries existence only, their correctness will be checked later when the dict of
        # tasks activities will be ready only then we can know the real min and max boundaries of the timestamps
        if command_line_arguments.lower:
            self.lower_boundary = double(str(command_line_arguments.lower).strip())

        # check upper, upper boundaries existence, its correctness will be checked later when the dict of
        # tasks activities will be ready only then we can know the real min and max boundaries of the timestamps
        if command_line_arguments.upper:
           self.upper_boundary = double(str(command_line_arguments.upper).strip())

        if command_line_arguments.task_id:
           self.task_id = int(str(command_line_arguments.task_id).strip())
        return True


    def store_task_activity(self, prev_task_timestamp, current_task_timestamp, current_task_id):
        # prepare value per dict key, dict key is task timestamp, value is a pair of (task_id, run time)
        task_activity_list = [current_task_id, 0]

        # update (add) dict with new element
        self.task_activities_dict[current_task_timestamp] = task_activity_list

        # take care of the previous task - extract from dict its entry a value (list element) get to list second elem -run time  update it's run time
        if prev_task_timestamp != -1:
            task_activity_list = self.task_activities_dict[prev_task_timestamp]

            # get task run time from [1]
            task_activity_list[1] = current_task_timestamp - prev_task_timestamp

            # update back the prev task with new value (that now holds the prev task actual run time)
            self.task_activities_dict[prev_task_timestamp] = task_activity_list


    def get_activities_map_length(self):
        return len(self.task_activities_dict) - 1

    def print_tasks_activities_entire_map(self):
        print("Tasks activities dictionary is ready !!!!!!!!!!")
        [print(key, value) for key, value in self.task_activities_dict.items()]


    def get_lower_timestamp_in_map(self):
        map_lower_timestamp = list(self.task_activities_dict.keys())[0]
        return map_lower_timestamp


    def get_upper_timestamp_in_map(self):
        map_upper_timestamp = list(self.task_activities_dict.keys())[self.get_activities_map_length()]
        return map_upper_timestamp


    def check_boundaries(self):
        if not self.lower_boundary or not self.upper_boundary or self.upper_boundary == -1 or self.lower_boundary == -1:
            # one or both of selected boundaries /s/are missing
            return False

        # lower_timestamp_map = self.get_lower_timestamp_in_map()
        # upper_timestamp_map = self.get_upper_timestamp_in_map()
        if self.lower_boundary > self.upper_boundary:
            print(f"lower_boundary > upper_boundary")
            return False
        elif self.lower_boundary == self.upper_boundary:
            print(f"lower_boundary = upper_boundary")
            return False
        elif self.lower_boundary > self.get_upper_timestamp_in_map():
            print(f"lower_boundary is grater than max timestamp in map")
            return False
        elif self.upper_boundary < self.get_lower_timestamp_in_map():
            print(f"upper_boundary is less than min timestamp in map")
            return False
        elif (self.lower_boundary + 1) < self.get_lower_timestamp_in_map() or self.upper_boundary > self.get_upper_timestamp_in_map():
            print(f"lower_boundary and upper_boundary are not existing max and min timestamp ranges ")
            return False
        return True


    def get_all_tasks_activities_in_range(self):
        tasks_activities_list = list()

        # list comprehension :
        # iterate over iterable object (dictionary), per its element check if it is in predefined ranges, if so print it
        tasks_activities_list = [(key, value) for key, value in self.task_activities_dict.items() if key > self.lower_boundary and key < self.upper_boundary]

        return tasks_activities_list


    def print_all_tasks_activities_in_range(self):
        # check boundaries validity
        if not self.check_boundaries():
            return False

        # we query dict according to user's selected in command line boundaries (arguments)
        print(f"\nTasks activities map is in range: \n[{self.get_lower_timestamp_in_map()} - {self.get_upper_timestamp_in_map()}] \n")
        print(f"\nUser selected to see tasks activities in range: \n[{self.lower_boundary} - {self.upper_boundary}]\n")

        # get list
        tasks_activities_list = self.get_all_tasks_activities_in_range()

        if not tasks_activities_list:
            return False

        print(*tasks_activities_list, sep = "\n")

        return True


    def prepare_tasks_activities_map(self):
        prev_task_timestamp = -1

        with open(self.task_activity_log_file, 'r') as log_file:
            while True:
                line = log_file.readline().strip()
                if not line:
                    break  # line is empty - EOF reached
                print(f'Read from log file: {log_file.name}: {line}')

                task_timestamp, task_id = line.strip().split(",")
                print(f'{task_timestamp}, {task_id}')

                self.store_task_activity(double(str(prev_task_timestamp).strip()),
                                         double(str(task_timestamp).strip()),
                                         int(str(task_id).strip()))
                prev_task_timestamp = task_timestamp

        # check if map isn't empty
        if self.get_activities_map_length() == 0:
            return False
        return True


    def calc_relative_time_per_task(self, task_id, tasks_in_range_dict, all_time):
        task_run_time = tasks_in_range_dict.get(task_id, "no_such_task")
        if task_run_time == "no_such_task":
            print(
                f'Task ID: {task_id}, requested by user in command line is not part of the given range: {self.lower_boundary}-{self.upper_boundary}')
            return False
        # calc relative time
        relative_time = double((tasks_in_range_dict.get(task_id) / all_time) * 100)
        print(f"Task ID: {task_id}, run: {tasks_in_range_dict.get(task_id)} sec which is relatively: {relative_time} % of the time")
        return relative_time


    """
        method get lower and upper boundaries (timestamps) 
        method need return relative run time in % of supplied task id among all other tasks in that range
        if task id wasn't supplied in command line than of all task_ids in given boundaries 
        it does it following these steps: 
        1. checks the boundaries are valid
        2. if task id was supplied - check given task exists in given boundaries           
        3. find how match all tasks run in given boundaries represent - it is 100%
        4. find entire time the task run (in given boundaries) 
        5. calculate task time run in % relatively to 100%
        6. if flag all given by user - then calc the same for all tasks in given boundaries           
    """
    def tasks_relative_times_in_range(self):
        # check task id was supplied in command line
        if not self.task_id or self.task_id == -1:
            all_tasks_in_range = True
            print(f"\nTask ID wasn't supplied, relative times will be calculated for all tasks in range")
        else:
            all_tasks_in_range = False

        # check boundaries are given and valid
        if not self.check_boundaries():
            return False

        # run over dictionary (that holds all the tasks info from log file)
        # read only values [task_id, singular run time] for the items where key (timestamp) in given boundaries
        tmp_list = [self.task_activities_dict[key]
                    for key, value in self.task_activities_dict.items()
                    if key > self.lower_boundary and key < self.upper_boundary]
        print(*tmp_list, sep = " \n")
        time.sleep(10)

        tmp_dict = dict()
        all_time = 0

        # sum per task id it's overall run time
        # write this info into tmp dict: {task_id, overall run time)
        for element in tmp_list:
            key = element[0]
            value = element[1]
            # print(f' key: {key}, value: {value}')

            all_time += value

            if key not in tmp_dict.keys():
                tmp_dict[key] = value
            else:
                tmp_dict[key] += value
        print(f'\nThe new tmp dict with accumulated run times per task_id is: ')
        print(tmp_dict, sep = "\n")

        time.sleep(7)
        print(f'\nOverall run time of all tasks in given boundaries is: {all_time} sec - it is 100% \n')
        time.sleep(5)

        # calculating the statistics of relative run time
        relative_run_times_list = []

        # do it for single given task id in given boundaries supplied by user in command line
        if self.task_id and self.task_id != -1:
            relative_run_times_list.append(self.calc_relative_time_per_task(self.task_id, tmp_dict, all_time))

        # do it for all tasks in given range supplied by user
        if all_tasks_in_range:
            # prepare list of result
            print("Relative run times for all tasks in supplied boundaries\n====================================================")

            for task_id, task_run_time in tmp_dict.items():
                relative_run_times_list.append([task_id, self.calc_relative_time_per_task(task_id, tmp_dict, all_time)])

        return relative_run_times_list




# ----------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":

    tasks_activity_monitor = TasksActivityMonitor()

    command_line_arguments = tasks_activity_monitor.get_user_input()

    if not tasks_activity_monitor.check_input_and_update(command_line_arguments):
        sys.exit("one or more input parameters is missing or not valid")

    initial_time_stamp = datetime.datetime.now().timestamp()
    # print all map
    if not tasks_activity_monitor.prepare_tasks_activities_map():
        sys.exit("There is empty activities map !!")

    # print specific range of the map according to the boundaries, if such were supplied via command line argument by user
    tasks_activity_monitor.print_tasks_activities_entire_map()

    if not tasks_activity_monitor.print_all_tasks_activities_in_range():
        sys.exit("There was some problem with user's selected boundaries ...?")

    # task_id and rang are defined by lower and upper boundaries defined by user in command line arguments
    tasks_activity_monitor.tasks_relative_times_in_range()
    print(f"Took: {datetime.datetime.now().timestamp() - initial_time_stamp} sec")













