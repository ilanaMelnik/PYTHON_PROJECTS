import glob
import os
# to know PC name on which Python script is running
import platform
import socket

import threading
import time
from pathlib import Path

from colored import colored


class logsCollector:

    def __init__(self):
        self.log_files_path = "C:/ILANA/PYTHON_PROJECTS/LOG_GENERATOR/Logs/1/"
        self.backup_logs_folder = "C:/ILANA/PYTHON_PROJECTS/LOG_GENERATOR/Backup_logs/"

        # delete backup_logs file
        if os.path.exists(self.backup_logs_folder + "Backup.txt"):
            os.remove(self.backup_logs_folder + "Backup.txt")

    def printGreen(self, text):
        print("\033[92m {}\033[00m".format(text))

    def read_logs(self, thread_name):
        print("\n Read thread - is started \n")

        last_file_name = ""
        last_read_position = 0
        delta_file_cnt = 0

        while True:
            # check if folder exists and it is folder indeed
            if os.path.exists(self.log_files_path) and os.path.isdir(self.log_files_path):
                if not os.listdir(self.log_files_path):
                    print("Directory {} is empty, keep on checking".format(self.log_files_path))
            else:
                print("Given Directory doesnt exist, exit")
                break

            # folder exists and contains at least 1 log file
            files_list = []

            for root, dirs, files in os.walk(self.log_files_path):
                for file in files:
                    # append the file full name (path) name to the list of found files in the folder
                    files_list.append(os.path.join(root, file))

            # print all the file names
            for name in files_list:
                print(name)

            # find the most recent file - check if already was read by me
            current_last_file_name = max(files_list, key=os.path.getctime)

            print("current last file is: ", current_last_file_name, \
                  ", last  accessed file was: ", last_file_name)

            # define from what file shell I read now:

            # last read file == current last updated file in folder - so we need to open it and keep reading from it
            # if there is something to read that wasn't read before
            if current_last_file_name == last_file_name:
                # set position to read from to be the last read position
                from_position = last_read_position

            # new file added to the folder - we need to open it and read it  from the beginning
            else:
                # store file name  right away !!
                last_file_name = current_last_file_name
                # reset position (by set tit to zero)
                from_position = 0


            # find right away end of file - last read position in the file
            current_last_read_position = Path(last_file_name).stat().st_size

            if current_last_read_position == last_read_position:
                print("In file {} there is no new lines to read".format(last_file_name))
                continue

            # store last read position of the file
            last_read_position = current_last_read_position

            file = open(last_file_name, "r")

            # set read position
            file.seek(from_position)

            ########################################
            # read amount of data, so called Delta
            ########################################
            read_delta = file.read(current_last_read_position - from_position)


            self.printGreen(read_delta)

            if os.path.exists(self.backup_logs_folder + "Backup.txt"):
                append_write = 'a'  # append if already exists
            else:
                append_write = 'w'  # make a new file if not

            with open(self.backup_logs_folder + "Backup.txt", 'a') as file:
                file.write(read_delta)

                # to know PC name on what my script is running
                # print("PC name: ", platform.node())
                # print("PC name: ", socket.gethostname())
                # print("PC name: ", os.environ['COMPUTERNAME'])

            # create small files that will hold only deltas
            delta_file_cnt += 1
            # set file name from comp name + cnt
            delta_file = self.backup_logs_folder + os.environ['COMPUTERNAME'] + str(delta_file_cnt) + ".txt"
            # create file
            with open(delta_file, 'w') as file:
                file.write(read_delta)

            # collect every n secs
            time.sleep(3)






"""if __name__ == "__main__":
    logs_collect = logsCollector()

    print("Main    : before creating Read thread")
    read_thread = threading.Thread(target=logs_collect.read_logs, args=(1,), name='reading Tread')
    print("Main    : before running Read thread")
    read_thread.start()
    # print("Main    : wait for the thread to finish")
    # x.join()
    print("Main    : Thread launched")"""
