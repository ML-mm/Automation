import sys
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import extensions

folder_logged = 'DOWNLOADSPATH'
folder_target = 'TARGETFOLDERPATH'

class MMhandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filenames in os.listdir(folder_logged):
            file_id = 1
            new_file_name = filenames
            sep_name = filenames.split('.')
            exts = '.' + sep_name[1]
            try:
                paths = extensions.ext_paths[exts]
            except Exception:
                exts = 'misc'
            check_file = os.path.isfile(folder_target + "/" + extensions.ext_paths[exts] + "/" + new_file_name)
            print("check file" + str(check_file) + " n ")
            print("check str" + " " + folder_target + "/" + extensions.ext_paths[exts] + new_file_name)
            while check_file:
                file_id += 1
                new_file_name = sep_name[0] + str(file_id) + '.' + sep_name[1]
                #Verification purposes
                print(os.path.splitext(folder_logged + '/' + new_file_name)[0])
                print(os.path.splitext(folder_logged + '/' + new_file_name)[1])
                print(sep_name[1])
                check_file = os.path.isfile(folder_target + "/" + extensions.ext_paths[exts] + "/" + new_file_name)

            source = folder_logged + "/" + filenames
            new_destination = folder_target + "/" + extensions.ext_paths[exts] + "/" + new_file_name
            #Verification purposes
            print("nfname" + new_file_name)
            print("source" + source)
            print("new dest" + new_destination)
            print("id" + str(file_id))
            os.rename(source, new_destination)



logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
path = 'DOWNLOADSPATH'
event_handler = LoggingEventHandler()
event_handler2 = MMhandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer2 = Observer()
observer2.schedule(event_handler2, folder_logged, recursive=True)
observer.start()
observer2.start()
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
     observer.stop()
     observer2.stop()

observer.join()
observer2.join()