import threading
import time
from terminal_operations import TerminalOperations
from generate_test_cases import source_structure, create_structure
from threading import Event

"""
File Synchronization Tool Documentation
========================================

Overview
--------
This tool is designed to synchronize files and directories from a source to a replica directory, 
ensuring that the replica is an exact mirror of the source. It achieves this by monitoring changes in the source 
directory and replicating these changes to the replica directory in real-time. 
Designed to work only on powershell!

Architecture
-------------
It's centered around two main threads that work concurrently:

1. Update and Verification Thread: Responsible for updating the structure of the source directory based on predefined 
test cases or dynamic updates. After each update, it verifies that the changes are accurately reflected in the 
replica directory. This ensures the integrity of the synchronization process by comparing the expected state of the 
replica with its actual state after synchronization.

2. Synchronization Thread: Continually synchronizes the source directory with the replica directory. It listens for 
signals from the Update and Verification Thread indicating that an update has occurred. Upon receiving a signal, 
it performs synchronization, ensuring that new and updated files are copied over, and that files and directories no 
longer present in the source are removed from the replica.

Communication Mechanism
-----------------------
The two threads communicate using a synchronization primitive from Python's `threading` module, specifically an `Event`
object.

- The Update and Verification Thread sets (signals) the `Event` after completing an update and verification cycle.
- The Synchronization Thread waits for this event to be set. Once the event is signaled, indicating that an update 
has occurred, it proceeds with the synchronization task. After completing the synchronization, it clears the event and 
waits for the next signal.

Purpose
-------
The purpose of having two threads communicating with each other is to decouple the concerns of updating and verifying 
the source structure from the task of synchronizing these changes to the replica. This separation of concerns enhances 
the tool's modularity and scalability. It allows for the continuous and efficient synchronization of directories in 
environments where the source directory's structure may change frequently.

Usage
-----
To start the synchronization process, simply run the `main.py` script. The script initializes both threads and manages 
their execution. Ensure to configure the paths for the source and replica directories within the script according to 
your needs.

"""


update_event = Event()
ONGOING = True


def update_source_structure(ops, source_path, source_structure):
    """Updates the source structure periodically"""
    global ONGOING
    for structure in source_structure:
        ops.clear_directory(source_path)
        create_structure(ops, source_path, [structure])
        update_event.set()
        time.sleep(5)  # adjust as needed

    update_event.set()
    ONGOING = False


def sync_folders_periodically(ops, source_path, replica_path):
    """Syncs source to replica periodically"""
    while ONGOING:
        update_event.wait()
        ops.sync_directories(source_path, replica_path)
        update_event.clear()


def main():
    ops = TerminalOperations()
    source_path = f"{ops.root_directory}\\source"
    replica_path = f"{ops.root_directory}\\replica"

    ops.create_directory(source_path)
    ops.create_directory(replica_path)

    thread1 = threading.Thread(
        target=update_source_structure, args=(ops, source_path, source_structure)
    )
    thread2 = threading.Thread(
        target=sync_folders_periodically, args=(ops, source_path, replica_path)
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


if __name__ == "__main__":
    main()
