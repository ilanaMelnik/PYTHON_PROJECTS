import argparse
import time
from termcolor import colored

from MEASURE_TASKS_ACTIVITY_IN_TIME.measure_tasks_activities import TasksActivityMonitor

# red
def printError(text):
    text = colored(text, 'red')
    print(text)

# blue
def printInfo(text):
    text = colored(text, 'blue')
    print(text)

# green
def printSuccess(text):
    text = colored(text, 'green')
    print(text)


def prepare_command_line_arguments(file_name = None, task_id = None, lower = None, upper = None):
    tasks_activity_monitor = TasksActivityMonitor()
    # set the form of user
    parser = tasks_activity_monitor.define_user_input()

    # parse_args read the command line as list of pairs key and value - it also can get this command line as parameter
    # arrange in list of pairs - as we do it here - we simply simulate command line arguments by giving it as parameter
    command_line_arguments = parser.parse_args(['-f', file_name,
                                               '-t', str(task_id),
                                               '-l', str(lower),
                                               '-u', str(upper)])
    return command_line_arguments


def run_test(obj):

    # if argument were not supplied it is -1 so I should check it and present nothing (not -1)
    empty = " "
    text = f"Test will run with these params: \n" \
           f"Log file: {obj.task_activity_log_file},\n" \
           f"Task_id: {obj.task_id if (obj.task_id and obj.task_id != 'None' and obj.task_id != -1) else empty}\n"\
           f"Lower boundary: {obj.lower_boundary if (obj.lower_boundary and obj.lower_boundary != 'None' and obj.lower_boundary != -1) else empty}\n"\
           f"Upper boundary: {obj.upper_boundary if (obj.upper_boundary and obj.upper_boundary != 'None' and obj.upper_boundary != -1) else empty}"

    printInfo(text)

    if not obj.prepare_tasks_activities_dict():
        printError("There were some errors during preparation of activities dict !!")
        return False

    if not obj.print_tasks_activities_entire_dict():
        printError("Nothing to print ...there is empty activities dict !!")
        return False

    if not obj.prepare_statistics():
        printError("Some errors during preparation of the statistics ... !!")
        return False

    return True


def test_scenario(to_run, file_name = None, task_id = None, lower = None, upper = None):
    if not to_run:
        return True

    printInfo("\n\nTest Started")
    tasks_activity_monitor = TasksActivityMonitor()

    command_line_arguments = prepare_command_line_arguments(file_name, task_id, lower, upper)
    if not command_line_arguments:
        return False

    if not tasks_activity_monitor.check_input_and_update(command_line_arguments):
        printError("one or more input parameters is missing or not valid")
        return False

    if not run_test(tasks_activity_monitor):
        printError("Test Failed ####")
        return False

    printSuccess("Test Succeeded !!!! ")
    return True


if __name__ == "__main__":
    """
    test_scenario(True, file_name = 'C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                  task_id = 4,
                  lower = 1,
                  upper = 3)
    time.sleep(2)     

    # first last limits ok, task_id exist
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                  task_id=4,
                  lower=1592307418,
                  upper=1592307433)
    time.sleep(3)
    # first last limits ok, task_id exist
    test_scenario(True,
                  file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log',
                  task_id=4,
                  lower=1592336712,
                  upper=1593617593)    
    time.sleep(3)
    
    # some limits ok, task_id exist
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                 task_id=4,
                 lower=1592307424,
                 upper=1592307431)
    time.sleep(2)

    # some limits ok, task_id doesnt exist
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                 task_id=1,
                 lower=1592307418,
                 upper=1592307433)
    time.sleep(2)

    # unexisting limits ok, some task_id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                 task_id=1,
                 lower=1592307477,
                 upper=1592307433)
    time.sleep(2)

    # unexisting limits ok, unexisting task_id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                 task_id=1,
                 lower=1592307418,
                 upper=1592307477)
    time.sleep(2)

    # first and last limits, task_id doesnt exist
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                 task_id=15,
                 lower=1592307424,
                 upper=1592307431)
    time.sleep(2)

    # first lower exist unexisitng upper task id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                 task_id=5,
                 lower=1592307424,
                 upper=20)
    time.sleep(2)
    
    # unexisitng lower some upper task id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                 task_id=5,
                 lower=20,
                 upper=1592307431)
    time.sleep(2)
    
    # some lower last upper no task id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                 lower=1592307424,
                 upper=1592307431)
    time.sleep(2)    
    """
    # no limits, no task id (do for all tasks over entire log file)
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100')
    time.sleep(5)
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log')

    """
    # unexisting lower last upper no task id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                    lower=2,
                    upper=1592307431)
    time.sleep(2)
    
    # some lower unexisitg upper no task id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                    lower=1592307424,
                    upper=10)
    time.sleep(2)
    
    # no limits, some task_id exist
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                  task_id=2)
    time.sleep(2)
    
    # no limits, task_id doesnt exist
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                  task_id=15)
    time.sleep(2)

    # no limits, first task_id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                  task_id=5)
    time.sleep(2)

    # no limits, last task_id
    test_scenario(True, file_name='C:\\ILANA\\PYTHON_PROJECTS\\MEASURE_TASKS_ACTIVITY_IN_TIME\\tasks_activities.log.100',
                  task_id=2)
    """
