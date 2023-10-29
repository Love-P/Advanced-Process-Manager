# Advanced Process Manager with Process Synchronization

## Project Overview

The goal of this project is to design and implement an advanced Process Manager with an emphasis on process synchronization. This Process Manager will allow users to create, manage, and synchronize processes in a multi-threaded environment. It will provide a command-line interface for process creation, management, and synchronization, and it will use system calls for process and thread control.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Usage Menu](#usage-menu)
4. [Structural Explanation](#structural-explanation)
   1. [`create_thread(thread_name)`](#create_thread)
   2. [`list_threads()`](#list_threads)
   3. [`process_menu(process_name)`](#process_menu)
   4. [`create_process(process_name)`](#create_process)
   5. [`terminate_thread(thread_name)`](#terminate_thread)
   6. [`list_processes()`](#list_processes)
   7. [`clear_log_file()`](#clear_log_file)
   8. [`ipc_send_message(message)`](#ipc_send_message)
   9. [`ipc_receive_message()`](#ipc_receive_message)
   10. [`producer()` and `consumer()`](#producer-and-consumer)
   11. [`run_producer_consumer_example()`](#run_producer_consumer_example)
5. [Functionality Test: Process Creation](#functionality-test-process-creation)
   1. [Test Description](#test-description)
   2. [Test Procedure](#test-procedure)
   3. [Expected Result](#expected-result)
   4. [Explanation](#explanation)
6. [Functionality Test: Thread Creation](#functionality-test-thread-creation)
   1. [Test Description](#test-description-1)
   2. [Test Procedure (Single Thread)](#test-procedure-single-thread)
   3. [Expected Result](#expected-result-1)
   4. [Explanation](#explanation-1)
   5. [Test Procedure (Multi-Thread)](#test-procedure-multi-thread)
   6. [Expected Result](#expected-result-2)
   7. [Explanation](#explanation-2)
7. [Functionality Test: Thread Termination](#functionality-test-thread-termination)
   1. [Test Description](#test-description-2)
   2. [Test Procedure](#test-procedure-2)
   3. [Expected Result](#expected-result-3)
   4. [Explanation](#explanation-3)
8. [Functionality Test: List Processes](#functionality-test-list-processes)
   1. [Test Description](#test-description-3)
   2. [Test Procedure](#test-procedure-3)
   3. [Expected Result](#expected-result-4)
   4. [Explanation](#explanation-4)
9. [Functionality Test: Inter-Process Communication (IPC)](#functionality-test-inter-process-communication-ipc)
   1. [Test Description](#test-description-4)
   2. [Test Procedure (Send Message)](#test-procedure-send-message)
   3. [Expected Result](#expected-result-5)
   4. [Explanation](#explanation-5)
   5. [Test Procedure (Receive Message)](#test-procedure-receive-message)
   6. [Expected Result](#expected-result-6)
   7. [Explanation](#explanation-6)
10. [Functionality Test: Process Synchronization (Producer-Consumer)](#functionality-test-process-synchronization-producer-consumer)
   1. [Test Description](#test-description-5)
   2. [Test Procedure](#test-procedure-4)
   3. [Expected Result](#expected-result-7)
   4. [Explanation](#explanation-7)
11. [Logging and Reporting](#logging-and-reporting)
   1. [Logging Details](#logging-details)
   2. [Reporting and Analysis](#reporting-and-analysis)
   3. [Accessing the Log File](#accessing-the-log-file)
12. [Discussion](#discussion)

## Installation
1. **Ensure you have Python 3.11.6 installed. You can download Python 3.11.6 from the official Python website**: [Python Downloads](https://www.python.org/downloads/release/).

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
This test focuses on the ability to create threads within a process in the Process Manager. There is the ability to create a single thread, or multi-threads.

## Test Procedure (Single Thread)
1. Run the Process Manager.
2. Create a new thread.
4. Enter a unique thread name and observe the thread creation.

## Expected Result
- A new thread with the specified name is created.
- The thread's execution can be monitored and controlled.

## Explanation
This test validates the Process Manager's capability to manage single thread creation.

![Thread Creation Test Single](images/thread_creation.png)
![Thread Creation Test Single Log](images/thread_creation_log.png)
---

## Test Procedure (Multi-Thread)
1. Run the Process Manager.
2. Create a new process.
3. Within the process menu, select the option to create a new thread.
4. Enter a unique thread name and observe the thread creation.

## Expected Result
- A new thread with the specified name is created within the child process.
- The thread's execution can be monitored and controlled.
- Multiple threads within the same process should work independently.

## Explanation
This test validates the Process Manager's capability to manage multiple threads within a process.

![Thread Creation Test Multi](images/multi_thread_create.png)
![Thread Creation Test Multi Log](images/multi_thread_create_log.png)
---

# Functionality Test: Thread Termination

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

![Thread Termination Test](images/terminate_thread.png)
![Thread Termination Test](images/terminate_thread_log.png)
---

# Functionality Test: List Processes

## Test Description
This test evaluates the capability of the Process Manager to list and provide information about running processes. It includes the option to list processes created through the code and all processes on the computer.

## Test Procedure
1. Run the Process Manager.
2. Select the option to list processes.
3. Choose to list processes created through your code or all processes on the computer.
4. Observe the displayed information about the processes.

## Expected Result
- If the user selects "Processes created through your code," the Process Manager successfully lists and displays information about processes created by the script. The information includes the process PID, parent PID, name, and status.
- If the user selects "All processes on the computer," the Process Manager lists and displays information about all processes running on the computer, not limited to those created by the script.

## Explanation
This test ensures that the Process Manager can accurately list and provide information about processes, offering insight into both processes created by the code and all processes on the computer.

![List Processes Test](images/list_processes.png)
![List Processes Test Log](images/list_processes_log.png)
---

# Functionality Test: Inter-Process Communication (IPC)

## Test Description
This test focuses on the capability of the Process Manager to transmit and receive messages between processes via Inter-Process Communication (IPC).

## Test Procedure (Send Message)
1. Run the Process Manager.
2. Select the option to send an IPC message.
3. Enter a message and send it to another process.

## Expected Result
- The message is successfully sent to the designated process.
- The recipient process receives the message and can display it.

## Explanation
This test validates the Process Manager's ability to send messages between processes using IPC.

![IPC Send Test](images/ipc_send.png)
![IPC Send Test Log](images/ipc_send_log.png)
---

## Test Procedure (Receive Message)
1. Run the Process Manager.
2. Select the option to receive an IPC message.
3. Wait for a message to be sent from another process.

## Expected Result
- The process successfully receives a message sent by another process.
- The received message can be displayed.

## Explanation
This test verifies the Process Manager's ability to receive messages sent by other processes using IPC.

![IPC Receive Test](images/ipc_receive.png)
---

# Functionality Test: Process Synchronization (Producer-Consumer)

## Test Description
This test evaluates the process synchronization functionality within the Process Manager, focusing on the Producer-Consumer problem.

## Test Procedure
1. Run the Process Manager.
2. Select the option to execute the Producer-Consumer example.
3. Observe the behavior of the producer and consumer threads as they interact with the shared buffer.

## Expected Result
- Two producer threads and two consumer threads are created.
- The producer threads successfully produce items and place them in the shared buffer.
- The consumer threads successfully consume items from the shared buffer.
- The synchronization mechanisms, including mutex, empty, and filled semaphores, operate effectively to ensure thread safety.
- The Producer-Consumer problem is simulated with proper synchronization.

## Explanation
This test demonstrates the Process Manager's capability to implement process synchronization and coordinate threads to solve the classic Producer-Consumer problem.

![Producer-Consumer Test](images/producer_consumer.png)
![Producer-Consumer Test Log](images/producer_consumer_log.png)
---

# Logging and Reporting

The Advanced Process Manager utilizes logging extensively to capture essential information about processes, threads, IPC activities, and synchronization events. All this logged information is stored in a file called `processes.log`.

## Logging Details

- **Process and Thread Creation**: Whenever a process or thread is created, details such as the process ID (PID), thread ID (TID), name, and status are recorded in the log.

- **Thread Termination**: When a thread is terminated, the log records the action, including the name of the terminated thread.

- **Inter-Process Communication (IPC)**: Messages sent via IPC are logged, including the source process, target process, and message content. This provides a comprehensive record of IPC activities within the Process Manager.

- **Process Synchronization (Producer-Consumer)**: Events in the producer-consumer example, including production and consumption of items, are logged to reflect the synchronization between producer and consumer threads.

- **Listing Processes and Threads**: Information about listed processes and threads, whether generated by the script or all processes on the computer, is captured in the log.

- **Log Clearance**: The ability to clear the log file is provided through the "Clear log file" option, ensuring the log can be reset for new sessions.

## Reporting and Analysis

The log file serves as a valuable tool for analyzing process and thread behavior, debugging issues, and understanding how synchronization mechanisms work in the Process Manager. It enables users to review past activities, investigate errors, and trace the sequence of events in both individual processes and multi-threaded contexts.

## Accessing the Log File

The `processes.log` file is created in the root directory of the Process Manager project. Users can access this file to view and analyze the logged information.

### Log File Location

```plaintext
Advanced-Process-Manager/
├── processes.log
├── ...
```
# Discussion

The Advanced Process Manager project represents a comprehensive and multifaceted system for managing processes and threads in a multi-threaded environment. This discussion aims to provide an overview of the project results, including its functionalities, design, and the broader implications of its capabilities.

## Comprehensive Functionality

The project successfully allows the creation of new processes, each with its menu for further interactions. This modularity in process creation lends itself well to managing different tasks or services within the system. The management options for processes, including process listing and termination, offer essential control over these entities.

## Thread Support

The support for threads within processes significantly enhances the project's functionality. It demonstrates the ability to handle multi-threaded applications and can serve as a basis for more complex parallel computing tasks. Thread creation and termination are well-implemented, showcasing the control the Process Manager has over its threads.

## Inter-Process Communication (IPC)

The IPC feature, allowing messages to be sent between processes, is a valuable addition. It emphasizes the ability to coordinate actions and share information across processes. In distributed and networked systems, IPC becomes crucial, and this functionality demonstrates its feasibility.

## Process Synchronization

One of the most noteworthy aspects of the project is the process synchronization example, the Producer-Consumer problem. By simulating real-world synchronization challenges, it highlights the capabilities of the Process Manager in orchestrating complex thread interactions. Semaphore-based synchronization ensures that only one thread accesses shared resources at a time, a fundamental requirement in parallel computing.

## Logging and Reporting

The inclusion of a detailed logging system, where all relevant information is recorded in the `processes.log` file, enhances the project's accountability and visibility. This log provides a historical record of processes, threads, IPC activities, and synchronization events. It serves as a useful tool for debugging, performance analysis, and gaining insights into system behavior. The "Log Clearance" feature allows users to reset the log for new sessions, maintaining log integrity.

## Real-World Applicability

The Advanced Process Manager is not just an isolated demonstration of concepts but a practical tool. It can be employed in a variety of scenarios:

- **System Administration**: It provides insights into all running processes on a system, assisting administrators in monitoring and managing system resources.

- **Parallel Computing**: The support for multi-threaded applications and IPC is crucial for parallel computing, where tasks are broken down and executed in parallel for performance gains.

- **Distributed Systems**: IPC is vital in distributed systems where processes on different machines need to communicate.

- **Educational Tool**: It can be a valuable tool for educational purposes, illustrating process management and synchronization concepts to students.

## Future Enhancements

While the Advanced Process Manager demonstrates impressive capabilities, there's always room for expansion and improvement. Some areas of future enhancement include:

- **Enhanced IPC**: Extending IPC with more advanced communication mechanisms like shared memory and message queues.

- **User Interface**: Developing a graphical user interface (GUI) for more user-friendly interaction.

- **Resource Monitoring**: Adding resource monitoring capabilities, such as CPU and memory usage, would be valuable for system administrators.

## Conclusion

The Advanced Process Manager is a versatile project that offers extensive functionality for process and thread management, IPC, and process synchronization. The project demonstrates a fundamental understanding of process management and synchronization concepts and serves as a practical tool with real-world applications. Its meticulous logging and reporting ensure transparency and accountability in system operations. This project lays the foundation for further exploration and development of process management and parallel computing tools, benefiting system administrators, developers, and educators.

