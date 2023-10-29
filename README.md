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

2. **Clone the repository and cd into it**:
   ```bash
      git clone https://github.com/Love-P/Advanced-Process-Manager.git
      cd Advanced-Process-Manager
   ```

3. **Create a Virtual Environment** (recommended):
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

4. **Install Requirements**:
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

## Structural Explaination

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

These functions are integral to the advanced Process Manager, providing fine-grained control over processes, threads, and IPC, with a strong emphasis on process synchronization and thread management. Understanding their design is crucial for harnessing the capabilities of the Process Manager effectively.

# Functionality Test: Process Creation

## Test Description
This test aims to verify the ability to create new processes within the Process Manager.

## Test Procedure
1. Run the Process Manager.
2. Select the option to create a new process.
3. Enter a unique process name and observe the process creation.

## Expected Result
- A new process with the specified name is created.
- The child process is executed independently, and a process menu is available for interaction.
- The main process should continue running and be capable of managing the child process.

## Explanation
This test ensures that the Process Manager successfully creates and manages new processes.

![Process Creation Test](images/process_creation.png)

![Process Creation Test Log](images/process_creation_log.png)
---

# Functionality Test: Thread Creation

## Test Description
This test focuses on the ability to create threads within a process in the Process Manager.

## Test Procedure
1. Run the Process Manager.
2. Create a new process.
3. Within the process menu, select the option to create a new thread.
4. Enter a unique thread name and observe the thread creation.

## Expected Result
- A new thread with the specified name is created within the child process.
- The thread's execution can be monitored and controlled.
- Multiple threads within the same process should work independently.

## Explanation
This test validates the Process Manager's capability to manage threads within a process.

![Thread Creation Test](placeholder_image.png)

---

# Functionality Test: Process Termination

## Test Description
This test assesses the ability to terminate threads within a process in the Process Manager.

## Test Procedure
1. Run the Process Manager.
2. Create a new process.
3. Create multiple threads within the process.
4. Select the option to terminate a thread within the process menu.
5. Enter the name of the thread to be terminated and confirm the termination.

## Expected Result
- The specified thread is successfully terminated.
- The remaining threads continue to execute without disruption.
- The Process Manager effectively handles thread termination requests.

## Explanation
This test verifies that the Process Manager can manage the termination of individual threads.

![Thread Termination Test](placeholder_image.png)



