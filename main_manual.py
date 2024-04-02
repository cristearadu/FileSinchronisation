import threading
import time
from terminal_operations import TerminalOperations
from generate_test_cases import directory_to_dict
from threading import Event


update_event = Event()
sync_completed_event = Event()
ONGOING = True


def monitor_source_changes(ops, source_path, check_interval=5):
    """Monitors source directory for changes and triggers synchronization"""
    previous_structure = directory_to_dict(ops, source_path)

    while True:
        time.sleep(check_interval)
        current_structure = directory_to_dict(ops, source_path)
        if current_structure != previous_structure:
            update_event.set()
            sync_completed_event.wait()
            sync_completed_event.clear()
            previous_structure = current_structure


def sync_folders_periodically(ops, source_path, replica_path):
    """Syncs source to replica periodically upon being triggered, running forever"""
    while True:
        update_event.wait()
        update_event.clear()
        ops.sync_directories(source_path, replica_path)
        sync_completed_event.set()


def main_manual():
    ops = TerminalOperations()
    source_path = f"{ops.root_directory}\\source"
    replica_path = f"{ops.root_directory}\\replica"

    ops.create_directory(source_path)
    ops.create_directory(replica_path)

    monitoring_thread = threading.Thread(target=monitor_source_changes, args=(ops, source_path))

    syncing_thread = threading.Thread(target=sync_folders_periodically, args=(ops, source_path, replica_path))

    monitoring_thread.start()
    syncing_thread.start()

    monitoring_thread.join()
    syncing_thread.join()


if __name__ == "__main__":
    main_manual()
