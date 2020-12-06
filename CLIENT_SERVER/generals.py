import subprocess

class generals:
    def __init__(self):
        self.commands_dict = {"GET_ALL_PROCESSES": ("Returns all Running Processes", self.GET_ALL_PROCESSES),
                              "KILL_PROCESS": ("Kill Process", self.KILL_PROCESS)}

    def GET_ALL_PROCESSES(self, params = None):
        cmd = "tasklist";

        if params:
            print(f"CLIENT: command: {cmd}, has no params")
            return None

        # way_1:
        # os.system(f"cmd /c {generals.commands_dict[received_msg]}")

        # way_2 - Get output from shell command using subprocess
        # result = subprocess.check_output(generals.commands_dict[received_msg],
        #                                  shell=True,
        #                                  universal_newlines=True)

        # way 3:
        result = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)

        # stdout is bytes object - to work with it we need to convert it to string object
        stdout, stderr = result.communicate()
        print(f"CLIENT: command: {cmd}, result: \n")

        # convert from bytes object to string object
        result = stdout.decode("utf-8")
        return result


    # proc_name is parameter to the command - givven by server side
    def KILL_PROCESS(self, proc_name):
        cmd = f"taskkill /F /IM {proc_name} /T";

        result = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)

        # stdout is bytes object - to work with it we need to convert it to string object
        stdout, stderr = result.communicate()
        print(f"CLIENT: command: {cmd}, result: \n")

        # convert from bytes object to string object
        result = stdout.decode("utf-8")
        return result

