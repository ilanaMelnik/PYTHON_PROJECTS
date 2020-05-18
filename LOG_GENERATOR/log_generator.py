# built in logging module in python
import logging
import logging.handlers as handlers
import threading
import time
import os
from datetime import datetime
from os import path
from pathlib import Path


"""
       Severity levels:
       * when you set severity level - you actually mean this level and above it (and more important) are only allowed
           DEBUG    - less important
           INFO
           WARNING
           ERROR
           CRITICAL - most important
       """
max_log_file_size = 1024*1024

class LogsGenerator:

    def __init__(self):
        # for all log severities
        self.log_files_path = "C:/ILANA/PYTHON_PROJECTS/LOG_GENERATOR/Logs/"
        self.current_log_file_name = ""
        self.current_logger_obj_name = ""

        # for FATAL log severities
        self.log_fatal_files_path = "C:/ILANA/PYTHON_PROJECTS/LOG_GENERATOR/Logs/Fatal/"
        self.current_fatal_log_file_name = ""
        self.current_fatal_logger_obj_name = ""

    def create_logs_folder_name(self, thread_name):
        # check if folder exists
        try:
            if not os.path.exists(self.log_files_path + str(thread_name)):
                print("folder {} does not exist, creating one ...".format(self.log_files_path))
                # then create the folder
                os.makedirs(self.log_files_path + str(thread_name))

            # set folder name
            self.log_files_path = self.log_files_path + str(thread_name)
            print("folder set to: ", format(self.log_files_path))
        except OSError:
            print('Error: Creating directory. ' + self.log_files_path + str(thread_name))

    def create_fatal_logs_folder_name(self, thread_name):
        # check if folder exists
        try:
            if not os.path.exists(self.log_fatal_files_path + str(thread_name)):
                print("folder {} does not exist, creating one ...".format(self.log_fatal_files_path))
                # then create the folder
                os.makedirs(self.log_fatal_files_path + str(thread_name))

            # set folder name
            self.log_fatal_files_path = self.log_fatal_files_path + str(thread_name)
            print("folder set to: ", format(self.log_fatal_files_path))
        except OSError:
            print('Error: Creating directory. ' + self.log_fatal_files_path + str(thread_name))

    """ 
        !!!!!!!!!!!!!!!
        In these two methods I care to generate new log file name each time the prev log file name reached max size
        I also takes care to generate new logginh object for new log file 
        So I read here and there and found that logging module can do this work for me" so these methods 
        were and replaced by new ones where the creation each time
        of the new log file while the previous reached the max sise and recreation 
        new logger object for this new log file is done for me by logging module itself !!!! 
        !!!!!!!!!!!!!!!
        
        
        def setup_logger(self, logger_name, log_file, level=logging.DEBUG):
            log = logging.getLogger(logger_name)
    
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(pathname)s- %(levelname)s - %(message)s')
            file_handler = logging.FileHandler(log_file, mode='w', )
    
            file_handler.setFormatter(formatter)
    
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
    
            log.setLevel(level)
            log.addHandler(file_handler)
            log.addHandler(stream_handler)
    
        def set_log_file_name(self, cnt):
            try:
                # check if folder exists
                if not path.isdir(self.log_files_path):
                    raise FileNotFoundError
                else:
                    # set new file name
                    self.current_file_name = self.log_files_path + "/" + str(cnt) + '.log'
                    print("file name {} is set ".format(self.current_file_name))
    
                    self.current_logger_obj_name = 'logger' + str(cnt)
                    print("logger name {} is set ".format(self.current_logger_obj_name))
    
                    # reconfigure the logger with new file name
                    self.setup_logger_rotating(logger_name = self.current_logger_obj_name,
                                               log_file    = self.current_file_name)
            except:
                print("folder {} does not exist".format(self.current_file_name))
    """

    # this method is called 1 time only
    def setup_logger_rotating(self, logger_name, log_file, max_log_size, level=logging.DEBUG):
        log = logging.getLogger(logger_name)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(pathname)s- %(levelname)s - %(message)s')

        # !!!!!!!!!!!!
        # by this method I create smart logging module that create new log file while
        # prev log file reached its mac size
        # RotatingFileHandler receives: base log file name,  max file size,  how maximum log files to create -
        # after this number all files will be rewrite
        log_handelr = handlers.RotatingFileHandler(log_file,
                                                   maxBytes=max_log_size,
                                                   backupCount=1000)

        log_handelr.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        log.setLevel(level)
        log.addHandler(log_handelr)
        log.addHandler(stream_handler)


    # this method is called 1 time only - to define base log name - it also sets logging obj name
    def set_log_file_name_rotating(self):
        try:
            # check if folder exists
            if not path.isdir(self.log_files_path):
                raise FileNotFoundError
            else:
                # set base file name for log file that will store log traces of all severities
                self.current_log_file_name = self.log_files_path + "/Log.log"
                print("file name {} is set ".format(self.current_log_file_name))

                self.current_logger_obj_name = 'ilana_logger'
                print("logger name {} is set ".format(self.current_logger_obj_name))

                # reconfigure the logger with new file name
                self.setup_logger_rotating(logger_name  = self.current_logger_obj_name,
                                           log_file     = self.current_log_file_name,
                                           max_log_size = 1024*4) # max_log_file_size
        except:
            print("folder {} does not exist".format(self.current_log_file_name))


    # this method is called 1 time only - to define 2 logs
    def set_log_file_name_different_logs(self):
        try:
            # check if folder exists
            if not path.isdir(self.log_files_path):
                raise FileNotFoundError
            else:
                # set base file name for log file that will store log traces of all severity only
                self.current_log_file_name = self.log_files_path + "/Log.log"
                print("file name {} is set ".format(self.current_log_file_name))

                self.current_logger_obj_name = 'ilana_logger'
                print("logger name {} is set ".format(self.current_logger_obj_name))

                # reconfigure the logger with new file name
                self.setup_logger_rotating(logger_name=self.current_logger_obj_name,
                                           log_file=self.current_log_file_name,
                                           max_log_size=1024 * 4)  # max_log_file_size


                # set base file name for log file that will store log traces of Fatal severity only
                self.current_fatal_log_file_name = self.log_fatal_files_path + "/Fatals_Log.log"
                print("file name {} is set ".format(self.current_fatal_log_file_name))

                self.current_fatal_logger_obj_name = 'ilana_fatal_logger'
                print("logger name {} is set ".format(self.current_fatal_logger_obj_name))

                # reconfigure the logger with new file name
                self.setup_logger_rotating(logger_name=self.current_fatal_logger_obj_name,
                                           log_file=self.current_fatal_log_file_name,
                                           max_log_size=1024 * 4)  # max_log_file_size

        except:
            print("folder {} does not exist".format(self.current_log_file_name))


    ######################################
    # actual func that generates log files
    ######################################
    def write_log_messages_all_in_one_log(self, thread_name):
        print("\n Write thread - all messages in same log - is started \n")
        cnt = 0
        line_cnt = 0

        # creates folder C:/ILANA/PYTHON_PROJECTS/LOG_GENERATOR/Logs/ and set class param
        self.create_logs_folder_name(thread_name)

        # setup logger 1 time only
        self.set_log_file_name_rotating()

        while True:
            try:
                # create log objects that will manager the logging proccess
                log = logging.getLogger(self.current_logger_obj_name)

                line_cnt += 1

                # !!! this operation generates traces that are stored by logging obj into log file !!!!
                log.debug("Task - {}, is writing line: {}".format(str(thread_name), line_cnt))

                # write log every n secs
                time.sleep(1)
            except:
                print("file or folder was not found ##########")


    ######################################
    # actual func that generates log files, log - all messages, separate log for fatal messages
    ######################################
    def write_log_messages_different_logs(self, thread_name):
        print("\n Write thread in different log for fatal messages -  is started \n")
        cnt = 0
        line_cnt = 0

        # creates folder C:/ILANA/PYTHON_PROJECTS/LOG_GENERATOR/Logs/ and set class param
        self.create_logs_folder_name(thread_name)

        self.create_fatal_logs_folder_name(thread_name)

        # setup logger 1 time only
        self.set_log_file_name_different_logs()

        while True:
            try:
                # create log objects that will manager the logging proccess
                log = logging.getLogger(self.current_logger_obj_name)
                fatal_log = logging.getLogger(self.current_fatal_logger_obj_name)

                line_cnt += 1

                # !!! this operation generates traces that are stored by logging obj into log file !!!!
                log.debug("Task - {}, is writing line: {}".format(str(thread_name), line_cnt))

                if line_cnt % 8 == 0:
                    fatal_log.critical("Task - {}, is writing line: {}".format(str(thread_name), line_cnt))

                # write log every n secs
                time.sleep(1)
            except:
                print("file or folder was not found ##########")




if __name__ == "__main__":
    logs_gen = LogsGenerator()

    print("Main    : before creating Write thread")
    write_thread = threading.Thread(target=logs_gen.write_log_messages_different_logs, args=(1,), name='writing Tread')
    print("Main    : before running Write thread")
    write_thread.start()
    # print("Main    : wait for the thread to finish")
    # x.join()
    print("Main    : Thread launched")






