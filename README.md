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

2. **Create a Virtual Environment** (Optional but recommended):
   
   - On Windows:
     - Open the Command Prompt.
     - Navigate to your project directory using the `cd` command.
     - Create a virtual environment using the following command:
       ```bash
       python3.11 -m venv venv
       ```
     - Activate the virtual environment:
       ```bash
       venv\Scripts\activate
       ```

   - On macOS and Linux:
     - Open the Terminal.
     - Navigate to your project directory using the `cd` command.
     - Create a virtual environment using the following command:
       ```bash
       python3.11 -m venv venv
       ```
     - Activate the virtual environment:
       ```bash
       source venv/bin/activate
       ```

3. **Install Requirements**:
   
   In your project directory (with the virtual environment activated if you created one), install the required packages using the following command:
   
   ```bash
   pip install -r requirements.txt
