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

### Usage Menu

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

### Usage

Here are the key functionalities and how to use them in the advanced Process Manager:

#### 1. Create a Process

To create a new process, run the Process Manager and choose "Create a process" from the main menu. Enter the name of the process, and a child process will be created. You can interact with the child process by creating threads, listing threads, or exiting the process.

#### 2. Create a Thread

Within a running process, you can create threads. Choose "Create a thread" from the main menu and provide a name for the thread. The new thread will be created and logged.

#### 3. Terminate a Thread

If you wish to terminate a specific thread within a process, choose "Terminate a thread" from the main menu, enter the name of the thread you want to terminate, and the thread will be requested for termination. The terminated threads will be logged and removed.

#### 4. Monitor All Running Processes

You can view and monitor all processes running on your computer. Choose "Monitor all running processes on your device" from the main menu and select whether you want to list processes created through your code or all processes on the computer. The information about these processes will be displayed.

#### 5. Inter-Process Communication (IPC)

The Process Manager supports inter-process communication (IPC). You can send and receive messages between processes. Choose "Send IPC message" to send a message to another process. To receive IPC messages, select "Receive IPC message" from the main menu. You can also clear the log file or exit the program.

#### 6. Process Synchronization (Producer-Consumer)

The program includes an example of process synchronization using the producer-consumer problem. To run the producer-consumer example, select "Process Synchronization (Producer-Consumer)" from the main menu. This demonstrates the synchronization of threads in a multi-threaded environment.

#### 7. Exit

When you're done using the Process Manager, you can exit the program by selecting "Exit" from the main menu.

Make sure to review the log file for detailed information about the processes and threads. The logging can be found in the `processes.log` file.

Enjoy using the advanced Process Manager for process synchronization and management!
