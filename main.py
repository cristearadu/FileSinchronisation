import threading
from terminal_operations import TerminalOperations
from generate_test_cases import source_structure, create_structure, directory_to_dict
from threading import Event

"""
File Synchronization Tool Documentation
========================================

Overview:
---------
This Python script implements a file synchronization tool designed to keep a replica directory in sync with a source 
directory. By monitoring changes in the source directory and applying them to the replica directory, it ensures 
that the replica is always an exact mirror of the source. The tool is specifically tailored for PowerShell environments 
and avoids using the Python `os` module or third-party synchronization libraries, relying instead on the `subprocess` 
module for executing system commands.

Architecture:
-------------
The tool operates through two concurrent threads:

1. **Update and Verification Thread**: This thread is responsible for updating the source directory's structure based on
a sequence of predefined test cases or dynamic updates. After updating the source, it verifies that the replica 
directory accurately reflects these changes. This is crucial for maintaining the integrity of the synchronization 
process by ensuring the replica directory's state matches the source's expected state.

2. **Synchronization Thread**: This thread is tasked with continually synchronizing the source directory with the 
replica directory. It listens for signals indicating that an update has occurred in the source directory. 
Once signaled, it carries out the synchronization process, ensuring that any new or updated files are copied over and 
that any files or directories no longer present in the source are removed from the replica.

Communication Mechanism:
------------------------
The threads communicate via a synchronization mechanism using Python's `threading.Event` objects. 
The Update and Verification Thread signals an event upon completing an update and verification cycle. 
The Synchronization Thread waits for this event to be signaled before proceeding with the synchronization task. 
This event-based communication allows for efficient and timely synchronization between the source and replica
directories.

Purpose:
--------
The design, featuring two communicating threads, aims to separate the concerns of updating and verifying the source 
directory from synchronizing these changes to the replica. This separation enhances the tool's modularity and 
scalability, enabling continuous and effective directory synchronization in dynamic environments.
"""


update_event = Event()
sync_completed_event = Event()
ONGOING = True


def update_source_structure(ops, source_path, source_structure, replica_path):
    """Updates the source structure periodically"""

    try:
        global ONGOING
        for structure in source_structure:
            ops.clear_directory(source_path)
            create_structure(ops, source_path, [structure])
            update_event.set()
            sync_completed_event.wait()
            sync_completed_event.clear()
            replica_structure = directory_to_dict(ops, replica_path)
            assert structure == replica_structure, \
                f"Failed to match replica with source!\n Source: {structure}\nReplica: {replica_structure}"
        update_event.set()
        ONGOING = False

    except AssertionError as e:
        print(e)
        ONGOING = False
        update_event.set()
        sync_completed_event.set()

    finally:
        ONGOING = False
        update_event.set()
        sync_completed_event.set()


def sync_folders_periodically(ops, source_path, replica_path):
    """Syncs source to replica periodically"""
    global ONGOING
    while ONGOING:
        update_event.wait()
        update_event.clear()

        if ONGOING:
            ops.sync_directories(source_path, replica_path)
            sync_completed_event.set()


def main():
    ops = TerminalOperations()
    source_path = f"{ops.root_directory}\\source"
    replica_path = f"{ops.root_directory}\\replica"

    ops.create_directory(source_path)
    ops.create_directory(replica_path)

    thread1 = threading.Thread(
        target=update_source_structure, args=(ops, source_path, source_structure, replica_path)
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
