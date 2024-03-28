# File Synchronization Tool

This tool provides a straightforward solution for synchronizing the contents of a source directory to a replica directory. It's designed to work only on powershell. Also it has a few interesting limitations:
- No third-party libraries that implement folder synchronization;
- Every step will be logged to a file and also to the console
- Is performed periodically (multithreading in this case)
- No usage of `OS` module, only `subprocess`

## Features
- **Directory and File Synchronization**: Recursively copies new and updated files from the source to the replica directory.
- **Deletion of Orphaned Items**: Removes files and directories in the replica that no longer exist in the source.
- **Flexible Logging**: Logs operations to both the console and to a file.

## Modules

- `core.py`: Contains core functionalities for executing shell commands and determining the operating system type.
- `generate_test_cases.py`: Generates a structured set of test cases for synchronization tasks.
- `logging_element.py`: Configures logging for the application, directing output to both console and file.
- `main.py`: The entry point for the application, orchestrating the synchronization process.
- `terminal_operations.py`: Encapsulates file and directory operations, interfacing with the filesystem through shell commands.

## Getting Started

To use this tool, ensure Python 3.6 or later is installed on your system. No external dependencies are required.

1. Clone or download this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Make sure you run from powershell
4. Run the tool with Python: `python main.py` or it could be run from pycharm