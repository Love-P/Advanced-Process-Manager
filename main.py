import os, sys, logging, multiprocessing, psutil, ctypes, time, random, threading, fcntl, errno
from queue import Queue

# Initialize the logging configuration
logging.basicConfig(filename='processes.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')
process_log = logging.getLogger('processes')
process_log.setLevel(logging.INFO)

# Data structures to keep track of running processes and threads
running_processes = {}
process_threads = {}
threads = []

# Create multiprocessing Pipes and Queue for inter-process communication
pipe_conn, child_conn = multiprocessing.Pipe()
shared_queue = Queue()

# Mutex to protect shared resource (running_processes dictionary)
mutex = multiprocessing.Lock()

# Create two pipes for inter-process communication
read_pipe, write_pipe = os.pipe()

# Define the buffer size for the producer-consumer problem
BUFFER_SIZE = 5
buffer = []

# Semaphores for producer-consumer problem
mutex = threading.Semaphore(1)  # Mutex for buffer access
empty = threading.Semaphore(BUFFER_SIZE)  # Semaphore for empty slots
filled = threading.Semaphore(0)  # Semaphore for filled slots

# Determine the platform and load the appropriate C library for pthread functions
if sys.platform.startswith('win'):
    libc = ctypes.CDLL('msvcrt')
elif sys.platform.startswith('linux'):
    libc = ctypes.CDLL('libc')
elif sys.platform == 'darwin':
    libc = ctypes.CDLL('libc.dylib')
else:
    raise OSError("Unsupported platform")

# Function to create a new thread
def create_thread(thread_name):
    process_pid = os.getpid()
    thread_id = ctypes.c_long()

    def thread_func():
        logging.info(f"Thread '{thread_name}' running")

    # Convert the thread_func to a C-compatible function pointer
    thread_func_ptr = ctypes.CFUNCTYPE(None)(thread_func)

    # Create a new thread
    if libc.pthread_create(ctypes.byref(thread_id), None, thread_func_ptr, None) == 0:
        threads.append((thread_id, thread_name))
        process_threads.setdefault(process_pid, []).append((thread_id, thread_name))
        logging.info(f"Thread '{thread_name}' created successfully")
    else:
        logging.error("Failed to create thread")

# Function to list threads in the current process
def list_threads():
    process_pid = os.getpid()
    threads = process_threads.get(process_pid, [])

    if not threads:
        print("No threads in this process.")
    else:
        print("Threads in this process:")
        for thread_id, thread_name in threads:
            print(f"Thread ID: {thread_id}, Name: {thread_name}")

# Function to interact with the created child process
def process_menu(process_name):
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
            create_thread(thread_name)  # Call create_thread to create a new thread
            print('\n')
        elif choice == "2":
            list_threads()  # Call list_threads to display the threads in this process
            print('\n')
        elif choice == "3":
            print("Exited process.")
            break
        else:
            print("Invalid option. Try again.")
    return

# Function to create a new child process
def create_process(process_name):
    pid = os.fork()  # Fork a new child process

    if pid == 0:  # In the child process
        try:
            os.execlp(process_name, process_name)  # Replace the current process image with the new process
        except Exception as e:
            logging.error(f"Child process '{process_name}' with PID {os.getpid()} encountered an error: {str(e)}")
        os._exit(1)  # Exit the child process
    else:
        with mutex:
            running_processes[pid] = process_name
        logging.info(f"Child process '{process_name}' with PID {pid} created.")
        process_menu(process_name)  # Enter the process menu for the child process


# Function to terminate a thread within the current process
def terminate_thread(thread_name):
    global threads
    threads_to_remove = []

    process_pid = os.getpid()
    
    # Iterate through the threads in the current process
    for thread_id, name in process_threads.get(process_pid, []):
        if name == thread_name:
            # Request thread termination using the pthread_cancel function
            if libc.pthread_cancel(thread_id) == 0:
                print(f"Thread '{thread_name}' termination requested.")
                logging.info(f"Thread '{thread_name}' termination requested.")
                threads_to_remove.append((thread_id, name))
            else:
                logging.error(f"Failed to request termination for thread '{thread_name}'")
    
    # Wait for the terminated threads and remove them from the threads list
    for thread_id, name in threads_to_remove:
        if libc.pthread_join(thread_id, None) == 0:
            print(f"Thread '{name}' terminated.")
            logging.info(f"Thread '{name}' terminated.")
    
    # Update the threads list, removing the terminated threads
    threads = [(t, n) for t, n in threads if (t, n) not in threads_to_remove]


# Function to list processes (created through the code or all processes on the computer)
def list_processes():
    while True:
        print("List Processes Sub-Menu:")
        print("1. Processes created through your code")
        print("2. All processes on the computer")
        print("3. Back to the main menu")
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

# Function to clear the log file
def clear_log_file():
    with open('processes.log', 'w'):
        pass
    print('\nlog file cleared.')

# Function to send a message via IPC
def ipc_send_message(message):
    os.write(write_pipe, message.encode())  # Write the message to the pipe
    process_log.info(f"Message sent: {message}")

# Function to receive a message via IPC
def ipc_receive_message():
    try:
        flags = fcntl.fcntl(read_pipe, fcntl.F_GETFL)
        fcntl.fcntl(read_pipe, fcntl.F_SETFL, flags | os.O_NONBLOCK)  # Set non-blocking mode for the pipe
        
        # Attempt to read a message from the pipe (non-blocking)
        message = os.read(read_pipe, 1024)  # Read from the pipe
        
        return message.decode()  # Decode the received message
    except OSError as e:
        if e.errno == errno.EAGAIN or errno == errno.EWOULDBLOCK:
            # Handle non-blocking read by returning None if no message is available
            return None
        else:
            raise  # Raise any other OS-related exceptions



# Producer function for the producer-consumer problem
def producer():
    for i in range(10):
        item = f"Item-{i}"  # You can generate your items here
        empty.acquire()  # Wait for an empty slot
        mutex.acquire()  # Get exclusive access to the buffer
        buffer.append(item)  # Add item to the buffer
        print(f"Produced {item}. Buffer: {buffer}")
        process_log.info(f"Produced {item}. Buffer: {buffer}")
        mutex.release()  # Release the mutex
        filled.release()  # Notify that a slot is filled
        time.sleep(random.uniform(0.1, 0.5))  # Simulate work

# Consumer function for the producer-consumer problem
def consumer():
    for i in range(10):
        filled.acquire()  # Wait for a filled slot
        mutex.acquire()  # Get exclusive access to the buffer
        item = buffer.pop(0)  # Remove and consume the first item
        print(f"Consumed {item}. Buffer: {buffer}")
        process_log.info(f"Consumed {item}. Buffer: {buffer}")
        mutex.release()  # Release the mutex
        empty.release()  # Notify that a slot is empty
        time.sleep(random.uniform(0.1, 0.5))  # Simulate work

# Function to run the producer-consumer example
def run_producer_consumer_example():
    # Create two producer threads and two consumer threads
    producers = [threading.Thread(target=producer) for _ in range(2)]
    consumers = [threading.Thread(target=consumer) for _ in range(2)]

    # Start the producer threads
    for producer_thread in producers:
        producer_thread.start()
    
    # Start the consumer threads
    for consumer_thread in consumers:
        consumer_thread.start()

    time.sleep(5)  # Allow the producer and consumer threads to run for some time

    # Wait for the producer threads to complete
    for producer_thread in producers:
        producer_thread.join()

    # Wait for the consumer threads to complete
    for consumer_thread in consumers:
        consumer_thread.join()


# Main program
if __name__ == "__main__":
    while True:
        print("Options:")
        print("1. Create a process")
        print("2. Create a thread")
        print("3. Terminate a thread")
        print("4. Monitor all running processes on your device.")
        print("5. Send IPC message")
        print("6. Receive IPC message")
        print("7. Clear log file")
        print("8. Process Synchronization (Producer-Consumer)")
        print("9. Exit")
        choice = input("Select an option: ").lower()

        # Menu options based on user choice
        match choice:
            case "1":
                process_name = input("Enter the process name: ")
                create_process(process_name)
                print('\n')
            case "2":
                thread_name = input("Enter the thread name: ")
                create_thread(thread_name)
                print('\n')
            case "3":
                thread_name = input("Enter thread name to terminate: ")
                terminate_thread(thread_name)
                print('\n')
            case "4":
                list_processes()
                print('\n')
            case "5":
                message = input("Enter message to send: ")
                ipc_send_message(message)
                print('\n')
            case "6":
                received_message = ipc_receive_message()
                print('\n')
                if received_message:
                    print(f"Received message: {received_message}")
                else:
                    print("No message available")
                print('\n')
            case "7":
                clear_log_file()
                print('\n')
            case "8":
                run_producer_consumer_example()
            case "9":
                print("Exited successfully")
                exit(0)
            case _:
                print("Invalid option. Try again.")
