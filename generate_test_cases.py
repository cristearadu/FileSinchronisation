"""
Test Cases generated for this task
"""
from terminal_operations import TerminalOperations

source_structure = [
    {
        "file1.txt": "Hello World",
    },
    {
        "file1.txt": "Hello World",
        "file2.txt": "Hello World",
    },
    {
        "file1.txt": "Hello World",
        "file2.txt": "",
        "file3.txt": "Future subfolder file here",
        "subfolder_1": {},
    },
    {
        "file1.txt": "Hello World",
        "file2.txt": "",
        "subfolder_1": {},
        "subfolder_2": {},
    },
    {
        "file1.txt": "Hello World",
        "file2.txt": "",
        "subfolder_1": {},
        "subfolder_2": {
            "subfolder_3": {},
        },
    },
    {
        "file1.txt": "Hello, World",
        "file2.txt": "Test file 2",
        "subfolder_1": {
            "file3.txt": "Subfolder file here",
        },
    },
    {
        "file1.txt": "Hello, World",
        "file2.txt": "Test file 2",
        "subfolder_1": {
            "file3.txt": "Subfolder file here",
            "file4.txt": "Another file to the subfolder level",
        },
    },
    {
        "file1.txt": "Hello, World!",
        "file2.txt": "Test file 2",
        "subfolder_1": {
            "file3.txt": "Subfolder file here",
            "file4.txt": "Another file to the subfolder level",
        },
    },
    {
        "file1.txt": "Hello, World!",
        "file2.txt": "File 2 has a small change regarding the input",
        "subfolder_1": {
            "file3.txt": "Subfolder file here",
            "file4.txt": "Another file to the subfolder level",
        },
    },
    {
        "file2.txt": "File 2 has a small change regarding the input",
        "subfolder_1": {
            "file3.txt": "Subfolder file here",
            "file4.txt": "Another file to the subfolder level",
        },
    },
    {
        "file5.txt": "Data, data and more data..",
        "file6.txt": "Data, data and more data..",
        "subfolder_2": {"file7.txt": "Unique content in this subfolder"},
    },
    {
        "file8.txt": "Almost almost final file",
        "subfolder_3": {
            "file9.txt": "Almost final file",
            "subfolder_3_1": {"file10.txt": "Final file"},
        },
    },
]


def create_structure(ops: TerminalOperations, base_path: str, structure_list: list) -> None:
    """Recursively creates a directory structure with files based on a given list of structures"""
    def create_items(ops, current_path, items):
        for name, content in items.items():
            path = f"{current_path}\\{name}"
            if isinstance(content, dict):
                ops.create_directory(path)
                create_items(ops, path, content)
            else:
                ops.write_to_file(path, content)

    for structure in structure_list:
        create_items(ops, base_path, structure)


def directory_to_dict(ops: TerminalOperations, directory_path: str) -> dict:
    """
    Creates a nested dictionary that represents the folder structure of a given directory, including the text
    content of all files
    """

    def add_to_dict(path_list: list, current_dict: dict, file_content=None):
        """Recursively adds paths to the dictionary, nesting as needed"""
        if len(path_list) == 1:
            if file_content is not None:
                current_dict[path_list[0]] = file_content
            else:
                current_dict.setdefault(path_list[0], {})
            return

        next_key = path_list.pop(0)
        current_dict.setdefault(next_key, {})
        add_to_dict(path_list, current_dict[next_key], file_content)

    directory_dict = {}
    items = ops.list_files(directory_path)

    for item_rel_path in items:
        item_path = f"{directory_path}\\{item_rel_path}"
        path_components = item_rel_path.split('\\')
        if ops.dir_exists(item_path):
            add_to_dict(path_components, directory_dict)
        else:
            file_content = ops.read_file(item_path)
            add_to_dict(path_components, directory_dict, file_content)

    return directory_dict
