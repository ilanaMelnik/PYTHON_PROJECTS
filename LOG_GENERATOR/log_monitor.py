import threading
import time

from LOG_GENERATOR.log_generator import LogsGenerator
from LOG_GENERATOR.logs_collector import logsCollector

if __name__ == "__main__":
    logs_generator = LogsGenerator()
    logs_collector = logsCollector()

    print("Main    : creating Write thread")
    write_thread = threading.Thread(target=logs_generator.write_logs, args=(1,), name='writing Tread')
    print("Main    : running Write thread")
    write_thread.start()
    print("Main    : Write thread launched")
    time.sleep(5)

    print("Main    : creating Read thread")
    read_thread = threading.Thread(target=logs_collector.write_log_messages_all_in_one_log, args=(1,), name='reading Tread')
    print("Main    : running Read thread")
    read_thread.start()
    # x.join()
    print("Main    : Read thread launched")