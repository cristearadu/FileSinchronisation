"""
Test Cases generated for this task
"""
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
    {
        "file8.txt": "Almost almost final file",
        "subfolder_3": {
            "file9.txt": "Almost final file",
            "subfolder_3_1": {"file10.txt": "Final file"},
        },
    },
]


def create_structure(ops, base_path, structure_list):
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
