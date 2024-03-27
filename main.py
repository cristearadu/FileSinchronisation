import threading
import time
from terminal_operations import TerminalOperations
from generate_test_cases import source_structure, create_structure

ONGOING = True


def update_source_structure(ops, source_path, source_structure):
    """Updates the source structure periodically"""
    global ONGOING
    for structure in source_structure:
        ops.clear_directory(source_path)
        create_structure(ops, source_path, [structure])
        time.sleep(30)
    ONGOING = False


def sync_folders_periodically(ops, source_path, replica_path):
    """Syncs source to replica periodically"""
    while ONGOING:
        ops.sync_directories(source_path, replica_path)
        time.sleep(15)


def main():
    ops = TerminalOperations()
    source_path = f"{ops.root_directory}\\source"
    replica_path = f"{ops.root_directory}\\replica"

    ops.create_directory(source_path)
    ops.create_directory(replica_path)

    thread1 = threading.Thread(target=update_source_structure, args=(ops, source_path, source_structure))
    thread2 = threading.Thread(target=sync_folders_periodically, args=(ops, source_path, replica_path))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


if __name__ == "__main__":
    main()
