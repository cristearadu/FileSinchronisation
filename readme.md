# File Synchronization Tool

This tool provides an efficient solution for synchronizing the contents of a source directory to a replica directory, ensuring the replica is an exact mirror of the source. Designed exclusively for PowerShell environments, it leverages multithreading to monitor and synchronize directories in real-time, without relying on the Python `os` module or third-party synchronization libraries.

## Features

- **Directory and File Synchronization**: Recursively synchronizes new and updated files from the source to the replica directory.
- **Deletion of Orphaned Items**: Automatically removes files and directories from the replica that are no longer present in the source.
- **Real-time Monitoring and Synchronization**: Utilizes multithreading to monitor changes in the source directory and synchronize them immediately.
- **Flexible Logging**: Provides comprehensive logging of operations to both the console and a log file, capturing every significant action taken by the tool.

## Modules

- `core.py`: Implements core functionalities for executing shell commands and determining the operating system type.
- `generate_test_cases.py`: Generates structured test cases for evaluating the synchronization functionality.
- `logging_element.py`: Sets up logging mechanisms, directing output to both the console and log files.
- `main.py`: Serves as the primary entry point, orchestrating the automatic synchronization process.
- `main_manual.py`: An alternative entry point for manual testing and monitoring, allowing for real-time synchronization based on detected changes.
- `terminal_operations.py`: Provides a layer of abstraction over file and directory operations, interfacing directly with the file system through PowerShell commands.

## Getting Started

### Prerequisites

- Python 3.6 or later.
- PowerShell environment.

### Running the Tool

1. Clone or download this repository to your local machine.
2. Open a PowerShell window and navigate to the project directory.
3. To run the automatic synchronization process either from Pycharm or from powershell:
   ```powershell
   python main.py