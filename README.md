# Advanced Process Manager with Process Synchronization

## Project Overview

The goal of this project is to design and implement an advanced Process Manager with an emphasis on process synchronization. This Process Manager will allow users to create, manage, and synchronize processes in a multi-threaded environment. It will provide a command-line interface for process creation, management, and synchronization, and it will use system calls for process and thread control.

## Implemented Functionalities
This Process Manager project includes the following functionalities:
1. Process Creation
2. Process Management (Listing, Termination, and Monitoring)
3. Thread Support (Thread Creation and Listing)
4. Inter-Process Communication (IPC)
5. Process Synchronization (Producer-Consumer)
6. Command-Line Interface (CLI)
7. Logging and Reporting

## Installation
1. Ensure you have Python 3.11.6 installed. You can download Python 3.11.6 from the official Python website: [Python Downloads](https://www.python.org/downloads/release/).

2. **Create a Virtual Environment** (recommended):
   - On Windows:
     - Open the Command Prompt.
     - Navigate to your project directory using the `cd` command.
     - Activate the virtual environment:
       ```bash
       venv\Scripts\activate
       ```

   - On macOS and Linux:
     - Open the Terminal.
     - Navigate to your project directory using the `cd` command.
     - Activate the virtual environment:
       ```bash
       source venv/bin/activate
       ```

3. **Install Requirements**:
   In your project directory (with the virtual environment activated if you created one), install the required packages using the following command:
   
   ```bash
   pip install -r requirements.txt

## Usage Menu

```bash
Options:
1. Create a process
2. Create a thread
3. Terminate a thread
4. Monitor all running processes on your device.
5. Send IPC message
6. Receive IPC message
7. Clear log file
8. Process Synchronization (Producer-Consumer)
9. Exit
Select an option:
```

## Function Explanations and Design

In this section, we delve into the technical details of each key function used in the advanced Process Manager, utilizing specific terminology and relevant packages.

### `create_thread(thread_name)`

- **Purpose**: This function's primary objective is to spawn a new POSIX thread (thread) within the current process.

- **Design**: It retrieves the process ID (PID) of the calling process and generates a unique thread ID. Subsequently, it defines a thread function (`thread_func`) to encapsulate the execution logic of the newly created thread. Utilizing the Python `ctypes` package, it converts `thread_func` into a C-compatible function pointer. The function then employs the `pthread_create` function from the C Standard Library (`libc`) via `ctypes` to create the thread. Upon successful creation, the thread ID is stored alongside the thread's given name, and the process log records its creation.

### `list_threads()`

- **Purpose**: This function serves the purpose of enumerating and displaying the threads currently running within the process.

- **Design**: It identifies the PID of the process invoking the function. Next, it retrieves the list of threads associated with that process from the `process_threads` data structure. The function proceeds to enumerate the threads, revealing essential details such as their thread IDs and user-assigned names.

### `process_menu(process_name)`

- **Purpose**: The `process_menu` function manages user interaction within a child process, allowing the user to create threads, list threads, or exit the child process.

- **Design**: This function serves as a menu-based interface within the child process. It provides user options to create threads and list existing threads. The design emphasizes interaction by accepting user input, including the name for new threads. Exiting the child process is also an available option.

### `create_process(process_name)`

- **Purpose**: This function initiates the creation of a new child process through forking.

- **Design**: The function utilizes `os.fork()` to initiate the fork operation, resulting in the generation of a new child process. In the child process context, it endeavors to execute the specified process, as denoted by `process_name`, thereby replacing the current process image. During this process, errors are meticulously logged. In the parent process, the global `running_processes` data structure is updated to include the child process.

### `terminate_thread(thread_name)`

- **Purpose**: The `terminate_thread` function is employed to request the termination of a designated thread within the present process.

- **Design**: It initiates a search through the threads associated with the present process using the acquired PID. Upon locating the target thread, it employs the `pthread_cancel` function to submit a termination request. The function then waits for the selected threads to conclude, and upon successful termination, the threads are removed from the global thread list.

### `list_processes()`

- **Purpose**: This function offers users the ability to list processes generated by the script or all processes running on the host system.

- **Design**: It delivers a submenu with selections for process listing, including a choice to list only processes initiated by the script or to enumerate all processes on the host system. The function employs the `psutil` package to collect detailed process information, including PIDs, parent PIDs, names, and statuses. This information is displayed to the user and recorded in the process log.

### `clear_log_file()`

- **Purpose**: Clearing the log file is the primary purpose of this function, eliminating previous log entries for a fresh start.

- **Design**: The function accesses the log file, effectively emptying its contents. This action resets the log file, making it ready to capture new entries.

### `ipc_send_message(message)`

- **Purpose**: This function is utilized to transmit messages between processes via Inter-Process Communication (IPC).

- **Design**: It writes the provided `message` to a designated pipe, thus enabling communication between different processes. Subsequently, the sent message is recorded in the process log.

### `ipc_receive_message()`

- **Purpose**: The `ipc_receive_message` function facilitates the retrieval of messages through IPC.

- **Design**: This function is configured to read messages from a predefined pipe. It employs non-blocking mode for the pipe to avoid delays in cases where no message is available. Upon successfully reading a message, it decodes and returns the received content. In cases where no message is available, it handles the non-blocking read scenario and returns `None`.

### `producer()` and `consumer()`

- **Purpose**: These functions are instrumental in simulating the producer-consumer problem, demonstrating the principles of process synchronization using semaphores.

- **Design**: The `producer` function generates items, simulating a producer, and places them in a buffer. In contrast, the `consumer` function behaves as a consumer, extracting items from the buffer. Both functions use semaphores (`mutex`, `empty`, and `filled`) to regulate access to the buffer, ensuring thread safety. The simulation involves inter-process synchronization to emulate a real-world producer-consumer scenario.

### `run_producer_consumer_example()`

- **Purpose**: This function is designed to execute the producer-consumer example, showcasing process synchronization through thread coordination.

- **Design**: It orchestrates the execution of producer and consumer threads, simulating the classic producer-consumer problem. The `producers` and `consumers` are thread instances, and their execution is initiated using `start()`. Additionally, the function features a delay period to allow the threads to operate. Finally, it employs `join()` to await the completion of all threads.

These functions are integral to the advanced Process Manager, providing

These functions are the building blocks of the advanced Process Manager and provide extensive control over processes, threads, and IPC. Understanding their purpose and design is essential for utilizing the Process Manager effectively.





