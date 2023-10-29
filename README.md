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

In this section, we'll provide an overview of the key functions used in the advanced Process Manager and their design. These functions are essential for creating, managing, and synchronizing processes and threads.

#### 1. `create_thread(thread_name)`

- **Purpose**: This function is used to create a new thread within a process.

- **Design**: It obtains the process ID and generates a unique thread ID. It defines a `thread_func` that represents the thread's execution logic. Using the `pthread_create` function, a new thread is created and added to the list of threads for the current process.

#### 2. `list_threads()`

- **Purpose**: This function lists the threads within the current process.

- **Design**: It retrieves the process ID and fetches the list of threads associated with that process. It then displays the thread IDs and their names.

#### 3. `process_menu(process_name)`

- **Purpose**: This function is responsible for managing the interaction within a child process.

- **Design**: It provides a menu for creating threads, listing threads, or exiting the child process. The menu options allow users to interact with threads within the process.

#### 4. `create_process(process_name)`

- **Purpose**: This function creates a new child process.

- **Design**: It forks a new child process using `os.fork()`. In the child process, it attempts to execute a new process specified by `process_name`. The function also logs the creation of the child process.

#### 5. `terminate_thread(thread_name)`

- **Purpose**: This function requests the termination of a specific thread within the current process.

- **Design**: It iterates through the threads in the current process, identifies the target thread by name, and requests thread termination using the `pthread_cancel` function. The function waits for the terminated threads and removes them from the list.

#### 6. `list_processes()`

- **Purpose**: This function lists processes created through the code or all processes on the computer.

- **Design**: It provides a menu with options to list processes. It uses the `psutil` library to retrieve information about processes, including their PIDs, parent PIDs, names, and status.

#### 7. `clear_log_file()`

- **Purpose**: This function clears the log file used for logging process and thread activities.

- **Design**: It opens the log file and empties its content, effectively clearing it for future use.

#### 8. `ipc_send_message(message)`

- **Purpose**: This function sends a message via Inter-Process Communication (IPC).

- **Design**: It writes the message to a pipe, allowing communication between processes. The message is also logged for reference.

#### 9. `ipc_receive_message()`

- **Purpose**: This function receives a message via IPC.

- **Design**: It attempts to read a message from a pipe, and if successful, it decodes the received message. It handles non-blocking reads and returns `None` when no message is available.

#### 10. `producer()` and `consumer()`

- **Purpose**: These functions are used for the producer-consumer problem to demonstrate process synchronization.

- **Design**: The `producer` function adds items to a buffer, and the `consumer` function removes items from the buffer. They use semaphores to ensure proper synchronization.

#### 11. `run_producer_consumer_example()`

- **Purpose**: This function runs the producer-consumer example.

- **Design**: It creates producer and consumer threads and simulates the producer-consumer problem using semaphores for synchronization.

These functions are the building blocks of the advanced Process Manager and provide extensive control over processes, threads, and IPC. Understanding their purpose and design is essential for utilizing the Process Manager effectively.





