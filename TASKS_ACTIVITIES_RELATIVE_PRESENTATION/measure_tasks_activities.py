import argparse
import os
import sys
from dataclasses import dataclass, field
from typing import List, Dict
import time
import datetime
from numpy import double
from MEASURE_TASKS_ACTIVITY_IN_TIME.Tasks_statistics_types import TasksStatisticsTypes


@dataclass
class TasksActivityMonitor:
    task_activities_dict   : Dict[double, List] = field(default_factory = dict)

    # class params will get their values from command line
    task_activity_log_file : str = ""
    task_id                : int = -1
    lower_boundary         : int = -1
    upper_boundary         : int = -1

    get_all_time           : int = -1
    tasks_statistics_type  : TasksStatisticsTypes = TasksStatisticsTypes.ALL_TASKS


    def define_user_input(self):
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
        return script_args


    # this method performs 2 things: defines and reads.
    # It defines the rules for input (what command line arguments the input is built from) then it reads the command line arguments by these rules
    def get_user_input_by_rules(self, arg_parser):

        # read the command line arguments by predefined rules
        # methos parse_args reads the command line = it also can get the list of arguments (like it is command line)
        command_line_arguments = arg_parser.parse_args()
        return command_line_arguments


    def printRed(self, text):
        print(f'\033[91m {text}\033[00m')

    """
    method performs basic input check and update of command line arguments into class 
    raise relevant flags that tells us what type of statistics user wishes to get
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
        if command_line_arguments.lower != None and command_line_arguments.lower != 'None':
            self.lower_boundary = double(str(command_line_arguments.lower).strip())

        # check upper, upper boundaries existence, its correctness will be checked later when the dict of
        # tasks activities will be ready only then we can know the real min and max boundaries of the timestamps
        if command_line_arguments.upper != None and command_line_arguments.upper != 'None':
           self.upper_boundary = double(str(command_line_arguments.upper).strip())

        # if user supplied task id - he can supply limits if limits were not supplied
        if command_line_arguments.task_id != None and command_line_arguments.task_id != 'None':
           self.task_id = int(str(command_line_arguments.task_id).strip())

        # set statistic type flag - for further analyze
        if self.task_id != -1 and self.lower_boundary != -1 and self.upper_boundary != -1:
            self.tasks_statistics_type = TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_UPPER
            print(f"User requested statistics for specific task id: {self.task_id} within supplied boundaries: [{self.lower_boundary} - {self.upper_boundary}]")

        elif self.task_id != -1 and self.lower_boundary == -1 and self.upper_boundary == -1:
            self.tasks_statistics_type = TasksStatisticsTypes.TASK_ID_ALL_LOG
            print(f"User requested statistics for specific task id: {self.task_id} from all supplied log file")

        elif self.task_id != -1 and self.lower_boundary != -1 and self.upper_boundary == -1:
            self.tasks_statistics_type = TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_LOG_END
            print(f"User requested statistics for specific task id: {self.task_id} from lower boundary: {self.lower_boundary} till end of log file")

        elif self.task_id != -1 and self.lower_boundary == -1 and self.upper_boundary != -1:
            self.tasks_statistics_type = TasksStatisticsTypes.TASK_ID_FROM_LOG_START_TILL_UPPER
            print(f"User requested statistics for specific task id: {self.task_id} from start of log file till upper boundary: {self.upper_boundary}")

        # for all tasks
        elif self.task_id == -1 and self.lower_boundary == -1 and self.upper_boundary == -1:
            self.tasks_statistics_type = TasksStatisticsTypes.ALL_TASKS
            print(f"User requested statistics for all tasks in entire log file")

        elif self.task_id == -1 and self.lower_boundary != -1 and self.upper_boundary == -1:
            self.tasks_statistics_type = TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_LOG_END
            print(f"User requested statistics for all tasks from lower boundary: {self.lower_boundary} till end of log file")

        elif self.task_id == -1 and self.lower_boundary == -1 and self.upper_boundary != -1:
            self.tasks_statistics_type = TasksStatisticsTypes.ALL_TASKS_FROM_LOG_START_TILL_UPPER
            print(f"User requested statistics for all tasks from log file start till upper boundary [{self.upper_boundary}]")

        elif self.task_id == -1 and self.lower_boundary != -1 and self.upper_boundary != -1:
            self.tasks_statistics_type = TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_UPPER
            print(f"User requested statistics for all tasks within supplied boundaries: [{self.lower_boundary} - {self.upper_boundary}]")

        return True

    # method perform 2 things:
    # 1. add single task activity - (read as line from log file) to the dict as new entry
    # (task activity will be added as list of 2 elems[task_id, run time]
    # 2. updates previous task record in dict with its singular run time (task id current activity run time)

    # above is done by the next steps:
    # create
    def store_raw_task_activity(self, prev_task_timestamp, current_task_timestamp, current_task_id):

        # prepare list of 2 elems [task_id, 0] I put 0 for task _id run time - this run time will be updated
        # with real value only when next task will run then we know its timestamp and can calc run time of prev task id
        task_activity_list = [current_task_id, 0]

        # update (add) dict with new element
        self.task_activities_dict[current_task_timestamp] = task_activity_list

        # take care of the previous task - extract from dict its entry a value (list element)
        # get to list second elem -run time  update it's run time
        if prev_task_timestamp and prev_task_timestamp != -1 and \
            prev_task_timestamp in self.task_activities_dict.keys(): # if this timestamp is in dict

            # get the element from dict - that represent task_id activity
            task_activity_list = self.task_activities_dict[prev_task_timestamp]

            # update task_id run time
            task_activity_list[1] = current_task_timestamp - prev_task_timestamp

            # write back the prev task with new value (that now holds the prev task actual run time)
            self.task_activities_dict[prev_task_timestamp] = task_activity_list


    def get_activities_dict_length(self):
        return len(self.task_activities_dict) - 1


    def print_tasks_activities_entire_dict(self):
        if self.get_activities_dict_length() == 0:
            return False
        print("\ntimestamp(sec)    task_id  run_time(Sec)\n------------------------------------------")
        [print(key, value) for key, value in self.task_activities_dict.items()]
        # another way to print dict
        # print(*self.task_activities_dict.items(), sep=" \n")
        return True


    def get_lower_timestamp_in_dict(self):
        dict_lower_timestamp = list(self.task_activities_dict.keys())[0]
        return dict_lower_timestamp


    def get_upper_timestamp_in_dict(self):
        dict_upper_timestamp = list(self.task_activities_dict.keys())[self.get_activities_dict_length()]
        return dict_upper_timestamp

    # check if boundaries supplied by user exist in log file, else finish
    def preliminar_check_boundaries(self):

        # first get actual lower and upper timestams from log - without loading log into memory
        with open(self.task_activity_log_file, "r") as file:
            first_log_line = file.readline().strip()
            for line in file:
                pass
            last_log_line = line.strip()

        # check in what mode we work then use what you found to check if requested by user boundaries exist in log file
        if self.tasks_statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_UPPER or \
           self.tasks_statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_UPPER:

            # check all about both limits
            if self.lower_boundary + 1 < double(first_log_line.strip().split(",")[0]) or \
               self.upper_boundary > double(last_log_line.strip().split(",")[0]) or \
               self.upper_boundary < double(first_log_line.strip().split(",")[0]) or \
               self.lower_boundary + 1 > self.upper_boundary or self.lower_boundary == self.upper_boundary:
                print(f"\n #### One of or both supplied boundary/ies [{self.lower_boundary}, {self.upper_boundary}] are out of range of log file,  \n "
                      f'where lower boundary is: {double(first_log_line.strip().split(",")[0])} and upper boundary is: {double(last_log_line.strip().split(",")[0])} !!')
                return False

        elif self.tasks_statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOG_START_TILL_UPPER or \
             self.tasks_statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOG_START_TILL_UPPER:

            # check all about upper limit only
            if self.upper_boundary > double(last_log_line.strip().split(",")[0]) or \
               self.upper_boundary < double(first_log_line.strip().split(",")[0]):
                print(f"\n #### Upper boundary {self.upper_boundary} is out of range of log file ! \n "
                      f'where upper boundary is: {double(last_log_line.strip().split(",")[0])}')
                return False

        elif self.tasks_statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_LOG_END or \
             self.tasks_statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_LOG_END:

            # check all about lower limit only
            if self.lower_boundary + 1 < double(first_log_line.strip().split(",")[0]) or \
               self.lower_boundary + 1 > double(last_log_line.strip().split(",")[0]):
                print(f"\n #### Lower supplied boundary/ies {self.lower_boundary} is out of range of log file ! \n "
                      f'where lower boundary is: {double(first_log_line.strip().split(",")[0])}')
                return False

        elif self.tasks_statistics_type == TasksStatisticsTypes.ALL_TASKS or \
             self.tasks_statistics_type == TasksStatisticsTypes.TASK_ID_ALL_LOG:
            pass # here no check required since user asked statistics for entire log file

        # we are here - it means user selected boundaries (in command line) are with log file boundaries and we can
        # proceed to check the relationships between these boundaries
        return True


    # user can supply task_id, or not, user can specify limits or not
    # that is why this check must be done after log file loaded into dict and limits are known
    def check_task_id_valid(self):
        task_id_found = False

        if not self.task_activities_dict:
            return False

        for timestamp, task_info_list_element in self.task_activities_dict.items():
            if self.tasks_statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_UPPER:
                if timestamp > self.lower_boundary and timestamp < self.upper_boundary and \
                        task_info_list_element[0] == self.task_id:
                    task_id_found = True
                    break
            elif self.tasks_statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOG_START_TILL_UPPER:
                if timestamp < self.upper_boundary and task_info_list_element[0] == self.task_id:
                    task_id_found = True
                    break
            elif self.tasks_statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_LOG_END:
                if timestamp > self.lower_boundary and task_info_list_element[0] == self.task_id:
                    task_id_found = True
                    break
            elif self.tasks_statistics_type == TasksStatisticsTypes.TASK_ID_ALL_LOG:
                if task_info_list_element[0] == self.task_id:
                    task_id_found = True
                    break
            # for the next case do nothing - here user did not supply task_id
            elif self.tasks_statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOG_START_TILL_UPPER or \
                 self.tasks_statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_LOG_END or \
                 self.tasks_statistics_type == TasksStatisticsTypes.ALL_TASKS or \
                 self.tasks_statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_UPPER:
                task_id_found = True
                pass

        if not task_id_found:
            return False

        return True


    def get_all_tasks_activities_in_range(self):
        tasks_activities_list = list()

        # list comprehension :
        # iterate over iterable object (dictionary), per its element check if it is in predefined ranges, if so print it
        tasks_activities_list = [(key, value) for key, value in self.task_activities_dict.items() if key > self.lower_boundary and key < self.upper_boundary]

        return tasks_activities_list


    def print_statistics(self):

        # we query dict according to user's selected in command line boundaries (arguments)
        print(f"\nEntire tasks activities dict limits are: \n[{self.get_lower_timestamp_in_dict()} - {self.get_upper_timestamp_in_dict()}] \n")
        print(f"\nUser selected to see tasks activities in limits: \n[{self.lower_boundary} - {self.upper_boundary}]\n")

        # get list
        tasks_activities_list = self.get_all_tasks_activities_in_range()

        if not tasks_activities_list:
            return False

        print(*tasks_activities_list, sep = "\n")
        return True


    # preparation of dict + make checks such as:
    # 1. check that supplied boundaries are exist in log file
    # 2. load log file into dict
    # 2. check the relations between supplied boundaries against actual timestams that were loaded from file, exp:
    #   lower < upper, lower > log file lower boundary, upper < upper log file boundary
    # 3.
    def prepare_tasks_activities_dict(self):

        # check boundaries first
        initial_time_stamp = datetime.datetime.now().timestamp()
        if not self.preliminar_check_boundaries():
            return False
        print(f"Making preliminary boundary checks took: {datetime.datetime.now().timestamp() - initial_time_stamp} sec")
        time.sleep(7)

        prev_task_timestamp = -1

        initial_time_stamp = datetime.datetime.now().timestamp()
        with open(self.task_activity_log_file, 'r') as log_file:
            while True:
                line = log_file.readline().strip()
                if not line:
                    break  # line is empty - EOF reached

                task_timestamp, task_id = line.strip().split(",")

                self.store_raw_task_activity(double(str(prev_task_timestamp).strip()), # previous timestamp
                                             double(str(task_timestamp).strip()),      # current timestamp
                                             int(str(task_id).strip()))                # current task_id
                prev_task_timestamp = task_timestamp

        # check if dict isn't empty
        if self.get_activities_dict_length() == 0:
            return False
        print(f"Loading log file into internal dict took: {datetime.datetime.now().timestamp() - initial_time_stamp} sec")
        time.sleep(7)
        # check if task_id given by user, exists in log file

        # it is not enought to know that requested task id is in log file - we must check that task_id were found between given boundaries
        """ 
        if not any(list(task_id for task_id, run_time in self.task_activities_dict.values() if self.task_id == task_id)):
            print(f"#### Task id: {self.task_id} not in log file !!")
            return False
        """
        initial_time_stamp = datetime.datetime.now().timestamp()
        if not self.check_task_id_valid():
            print(f"#### Task id: {self.task_id} was not found in log file between supplied boundaries  !!")
            return False
        print(f"Checking validity of task_id (if supplied) took: {datetime.datetime.now().timestamp() - initial_time_stamp} sec")
        time.sleep(7)
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


    def calc_relative_info(self, statistics_type):
        all_time = 0
        requested_task_run_time = 0
        tmp_dict = dict()
        take_statistics = False

        initial_time_stamp = datetime.datetime.now().timestamp()
        # dict contains entries as in exp:
        # key,            value
        # timestamp, [task_it, run time]
        if (statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_UPPER or
            statistics_type == TasksStatisticsTypes.ALL_TASKS or
            statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_LOG_END or
            statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOG_START_TILL_UPPER):

            for actual_timestamp, task_activity_list in self.task_activities_dict.items():

                if statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_UPPER and \
                   actual_timestamp > self.lower_boundary and actual_timestamp < self.upper_boundary: # [lower - upper)
                    take_statistics = True

                elif statistics_type == TasksStatisticsTypes.ALL_TASKS:
                    take_statistics = True

                elif statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOWER_TILL_LOG_END and \
                     actual_timestamp > self.lower_boundary:
                    take_statistics = True

                elif statistics_type == TasksStatisticsTypes.ALL_TASKS_FROM_LOG_START_TILL_UPPER and \
                     actual_timestamp < self.upper_boundary:
                    take_statistics = True

                if take_statistics:
                    # prepare info that later will be used for calc of relative time
                    task_id = task_activity_list[0]
                    run_time = task_activity_list[1]

                    # sum 100% time in given range
                    all_time += run_time

                    if task_id not in tmp_dict.keys():
                        tmp_dict[task_id] = run_time
                    else:
                        tmp_dict[task_id] += run_time

                take_statistics = False

        elif (statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_UPPER or
              statistics_type == TasksStatisticsTypes.TASK_ID_ALL_LOG or
              statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_LOG_END or
              statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOG_START_TILL_UPPER):

            for actual_timestamp, task_activity_list in self.task_activities_dict.items():

                if statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_UPPER and \
                   actual_timestamp > self.lower_boundary and actual_timestamp < self.upper_boundary: # [lower - upper)
                    take_statistics = True

                elif statistics_type == TasksStatisticsTypes.TASK_ID_ALL_LOG:
                    take_statistics = True

                elif statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOWER_TILL_LOG_END and \
                     actual_timestamp > self.lower_boundary:
                    take_statistics = True

                elif statistics_type == TasksStatisticsTypes.TASK_ID_FROM_LOG_START_TILL_UPPER and \
                     actual_timestamp < self.upper_boundary:
                    take_statistics = True

                if take_statistics:
                    # take run time - from each task that in limits - because if we here we are within limits
                    run_time = task_activity_list[1]
                    if self.task_id == task_activity_list[0]:
                        requested_task_run_time = run_time

                    # sum 100% time in given range
                    all_time += run_time

                    if requested_task_run_time and requested_task_run_time != 0:
                        if self.task_id not in tmp_dict.keys():
                            tmp_dict[self.task_id] = requested_task_run_time
                        else:
                            tmp_dict[self.task_id] += requested_task_run_time

                take_statistics = False
                requested_task_run_time = 0

        print(f"Summarizing run times per task took: {datetime.datetime.now().timestamp() - initial_time_stamp} sec")
        print(f"{tmp_dict}", sep = "\n")
        time.sleep(7)


        # check the work
        if all_time == 0 or len(tmp_dict) == 0:
            return False
        print(f'\nEntire time is: {all_time} sec will be referenced as 100%')


        initial_time_stamp = datetime.datetime.now().timestamp()
        # calc relative times per task_id and update tmp dict
        tmp_dict = {task_id: (overall_run_time / all_time) * 100
                    for task_id, overall_run_time in tmp_dict.items()}
        print(f"Calculating relative times per task took (%) : {datetime.datetime.now().timestamp() - initial_time_stamp} sec")
        time.sleep(7)

        return tmp_dict

    def prepare_statistics(self):
        tmp_dict = dict()
        tmp_dict = self.calc_relative_info(self.tasks_statistics_type)

        if not tmp_dict:
            return False

        print(f'\nRelative run times (%) for all tasks in supplied boundaries\n====================================================')
        print(tmp_dict, sep="\n")
        return True



# ----------------------------------------------------------------------------------------------------------------- #
""" this is the way I recommend to use this class
if __name__ == "__main__":

    tasks_activity_monitor = TasksActivityMonitor()

    # define the command line arguments
    command_line_arguments_parser = tasks_activity_monitor.define_user_input()

    # get command line arguments from user
    command_line_arguments = tasks_activity_monitor.get_user_input_by_rules(command_line_arguments_parser)

    if not tasks_activity_monitor.check_input_and_update(command_line_arguments):
        sys.exit("one or more input parameters is missing or not valid")

    if not tasks_activity_monitor.prepare_tasks_activities_dict():
        sys.exit("There were some errors during preparation of activities dict !!")

    if not tasks_activity_monitor.print_tasks_activities_entire_dict():
        sys.exit("Nothing to print ...there is empty activities dict !!")

    # if not tasks_activity_monitor.print_statistics():
    #    sys.exit("There was some problem with user's selected boundaries ...?") 

    if not tasks_activity_monitor.prepare_statistics():
        sys.exit("Some errors during preparation of the statistics ... !!")
    print("Done")
"""











