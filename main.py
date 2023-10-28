import os, sys, logging, multiprocessing, psutil, ctypes
from queue import Queue

logging.basicConfig(filename='processes.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')
process_log = logging.getLogger('processes')
process_log.setLevel(logging.INFO)

running_processes = {}
process_threads = {}
threads = []
pipe_conn, child_conn = multiprocessing.Pipe()
shared_queue = Queue()
mutex = multiprocessing.Lock()
process_threads = {}

if sys.platform.startswith('win'):
    libc = ctypes.CDLL('msvcrt')
elif sys.platform.startswith('linux'):
    libc = ctypes.CDLL('libc')
elif sys.platform == 'darwin':
    libc = ctypes.CDLL('libc.dylib')
else:
    raise OSError("Unsupported platform")

def create_thread(thread_name):
    process_pid = os.getpid()
    thread_id = ctypes.c_long()
    
    def thread_func():
        logging.info(f"Thread '{thread_name}' running")
    
    thread_func_ptr = ctypes.CFUNCTYPE(None)(thread_func)

    if libc.pthread_create(ctypes.byref(thread_id), None, thread_func_ptr, None) == 0:
        threads.append((thread_id, thread_name))
        process_threads.setdefault(process_pid, []).append((thread_id, thread_name))
        logging.info(f"Thread '{thread_name}' created successfully")
    else:
        logging.error("Failed to create thread")

def list_threads():
    process_pid = os.getpid()
    threads = process_threads.get(process_pid, [])

    if not threads:
        print("No threads in this process.")
    else:
        print("Threads in this process:")
        for thread_id, thread_name in threads:
            print(f"Thread ID: {thread_id}, Name: {thread_name}")

def process_function(process_name):
    process_log.info(f"Child process '{process_name}' with PID {os.getpid()} running")
    process_threads[os.getpid()] = []

    while True:
        print("Options within the process:")
        print("1. Create a thread")
        print("2. List threads")
        print("3. Exit process")
        choice = input("Select an option: ")

        if choice == "1":
            thread_name = input("Enter a name for the thread: ")
            create_thread(thread_name)
            print('\n')
        elif choice == "2":
            list_threads()
            print('\n')
        elif choice == "3":
            print("Exited process.")
            break
        else:
            print("Invalid option. Try again.")
    return

def create_process(process_name):
    pid = os.fork()
    if pid == 0:
        try:
            os.execlp(process_name, process_name)
        except Exception as e:
            logging.error(f"Child process '{process_name}' with PID {os.getpid()} encountered an error: {str(e)}")
        os._exit(1)
    else:
        running_processes[pid] = process_name
        logging.info(f"Child process '{process_name}' with PID {pid} created.")
        process_function(process_name)

def terminate_thread(thread_name):
    global threads
    threads_to_remove = []
    
    process_pid = os.getpid()
    for thread_id, name in process_threads.get(process_pid, []):
        if name == thread_name:
            if libc.pthread_cancel(thread_id) == 0:
                print(f"Thread '{thread_name}' termination requested.")
                logging.info(f"Thread '{thread_name}' termination requested.")
                threads_to_remove.append((thread_id, name))
            else:
                logging.error(f"Failed to request termination for thread '{thread_name}'")
    
    for thread_id, name in threads_to_remove:
        if libc.pthread_join(thread_id, None) == 0:
            print(f"Thread '{name}' terminated.")
            logging.info(f"Thread '{name}' terminated.")
    threads = [(t, n) for t, n in threads if (t, n) not in threads_to_remove]

def list_processes():
    while True:
        print("List Processes Sub-Menu:")
        print("1. Processes created through your code")
        print("2. All processes on the computer")
        print("3. Back to main menu")
        choice = input("Select an option: ")

        if choice == "1":
            process_log.info("Processes created through your code:")
            for pid, process_name in running_processes.items():
                process_info = psutil.Process(pid)
                parent_pid = process_info.ppid()
                state = process_info.status()
                process_log.info(f"Process with PID: {pid}, Name: {process_name}, Parent PID: {parent_pid}, State: {state}")
                print(f"Process with PID: {pid}, Name: {process_name}, Parent PID: {parent_pid}, State: {state}")
        elif choice == "2":
            process_log.info("All processes on the computer:")
            for process in psutil.process_iter(attrs=['pid', 'ppid', 'name', 'status']):
                process_info = process.info
                pid = process_info['pid']
                ppid = process_info['ppid']
                name = process_info['name']
                status = process_info['status']
                process_log.info(f"Process with PID: {pid}, Parent PID: {ppid}, Name: {name}, Status: {status}")
                print(f"Process with PID: {pid}, Parent PID: {ppid}, Name: {name}, Status: {status}")
        elif choice == "3":
            print("Returning to the main menu.")
            break
        else:
            print("Invalid option. Try again.")
    print('\n')
    print('To monitor all running processes, go to the log file or view them above.')

def clear_log_file():
    with open('processes.log', 'w'):
        pass
    print('\nlog file cleared.')

read_pipe, write_pipe = os.pipe()

def ipc_send_message(message):
    os.write(write_pipe, message.encode())
    process_log.info(f"Message sent: {message}")

def ipc_receive_message():
    message = os.read(read_pipe, 1024)
    return message.decode()

if __name__ == "__main__":
    while True:
        print("Options:")
        print("1. Create a process")
        print("2. Create a thread")
        print("3. List processes")
        print("4. Terminate a thread")
        print("5. Monitor all running processes on your device.")
        print("6. Send IPC message")
        print("7. Receive IPC message")
        print("8. Clear log file")
        print("9. Exit")
        choice = input("Select an option: ").lower()

        if choice == "1":
            process_name = input("Enter the process name: ")
            create_process(process_name)
            print('\n')
        elif choice == "2":
            thread_name = input("Enter the thread name: ")
            create_thread(thread_name)
            print('\n')
        elif choice == "4":
            thread_name = input("Enter thread name to terminate: ")
            terminate_thread(thread_name)
            print('\n')
        elif choice == "3":
            list_processes()
            print('\n')
        elif choice == "5":
            list_processes()
            print('\n')
        elif choice == "6":
            message = input("Enter message to send: ")
            ipc_send_message(message)
            print('\n')
        elif choice == "7":
            received_message = ipc_receive_message()
            print('\n')
            if received_message:
                print(f"Received message: {received_message}")
            else:
                print("No message available")
            print('\n')
        elif choice == "8":
            clear_log_file()
            print('\n')
        elif choice == "9":
            print("Exited successfully")
            exit(0)
        else:
            print("Invalid option. Try again.")
