import subprocess
from typing import Union
from core import Core
from core_elements.logging_element import Logger


class TerminalOperations(Core):
    def __init__(self):
        super().__init__()
        self.logger = Logger().logger

    def execute_command(self, command, command_display) -> Union[str, None]:
        """Function that executes a command and logs the command output"""
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.logger.info(
                    f"Executed command: {command_display} - Output: {stdout.strip()}"
                )
                return stdout.strip()
            else:
                self.logger.error(
                    f"Error executing command: {command_display} - Error: {stderr.strip()}"
                )
                return None
        except Exception as e:
            self.logger.error(
                f"Exception executing command: {command_display} - Error: {str(e)}"
            )
            return None

    def copy_file(self, source, destination):
        """Copy file from source to destination"""

        cmd = ["copy", source, destination]
        cmd_display = f"copy {source} {destination}"
        return self.execute_command(cmd, cmd_display)

    def file_exists(self, path: str) -> bool:
        """Check a file exists"""
        cmd = f'if exist "{path}" (echo True) else (echo False)'
        result = self.execute_command(cmd, f"Check if file exists: {path}")
        return "True" in result

    def dir_exists(self, path: str) -> bool:
        """Check a directory exists"""
        cmd = f'if exist "{path}\\" (echo True) else (echo False)'
        result = self.execute_command(cmd, f"Check if directory exists: {path}")
        return "True" in result

    def create_directory(self, path: str) -> None:
        """Create a directory if it doesn't exist"""
        if not self.dir_exists(path):
            cmd = ["mkdir", path]
            self.execute_command(cmd, f"Create directory: {path}")

    def remove_item(self, path: str):
        """Remove a file"""
        cmd = [
            "powershell",
            "-Command",
            f"if (Test-Path -Path '{path}' -PathType Leaf) {{ Remove-Item -Path '{path}' -Force }} else {{ Remove-Item -Path '{path}' -Recurse -Force }}",
        ]
        self.execute_command(cmd, f"Remove item: {path}")

    def write_to_file(self, path: str, content: str):
        """Write content to a file"""
        cmd = [
            "powershell",
            "-Command",
            f"Set-Content -Path '{path}' -Value '{content}'",
        ]
        self.execute_command(cmd, f"Write to file: {content}")

    def clear_directory(self, directory_path: str) -> None:
        """Clears the contents of a directory without deleting the directory itself"""

        cmd = [
            "powershell",
            "-Command",
            f"Get-ChildItem -Path '{directory_path}' -Recurse | Remove-Item -Force -Recurse",
        ]

        result = self.execute_command(cmd, f"Clear directory: {directory_path}")
        if result is not None:
            self.logger.info(f"Cleared directory: {directory_path}")
        else:
            self.logger.error(f"Failed to clear directory: {directory_path}")

    def list_files(self, directory_path: str) -> list:
        """List all files in a directory recursively"""
        cmd = f"powershell -Command \"Get-ChildItem -Path '{directory_path}' -Recurse | ForEach-Object {{ $_.FullName }}\""

        result = self.execute_command(cmd, f"List all items in {directory_path}")
        if result:
            items = result.split("\n")
            items = [item.replace(directory_path + "\\", "") for item in items if item]
            return items
        else:
            self.logger.error(f"Failed to list items in {directory_path}")
            return []

    def sync_directories(self, source: str, replica: str) -> None:
        """Synchronize source directory with replica directory"""
        source_files = self.list_files(source)
        replica_files = self.list_files(replica)

        for src_rel_path in source_files:
            src_file = f"{source}\\{src_rel_path}"
            rep_file = f"{replica}\\{src_rel_path}"

            if "." not in src_rel_path and not self.file_exists(rep_file):
                self.create_directory(rep_file)
                self.logger.info(f"Created directory: {rep_file}")
                continue

            if not self.file_exists(rep_file) or self.calculate_md5(
                src_file
            ) != self.calculate_md5(rep_file):
                self.copy_file(src_file, rep_file)
                self.logger.info(f"Synced: {src_file} to {rep_file}")

        # Sort replica_files by depth (descending) to ensure deeper paths are processed first
        # encountered a situation where i had one folder with another folder inside
        #         "subfolder_2": {
        #             "subfolder_3": {},
        # it would remove at first subfolder 2, then would raise an error hor subfolder 3
        # still, it's a BUG, because subfolder_2\\subfolder_3 does not exist anymore, even though
        # technically it's right
        replica_files_sorted = sorted(
            replica_files, key=lambda x: x.count("\\"), reverse=True
        )

        for rep_rel_path in replica_files_sorted:
            if rep_rel_path not in source_files:
                extra_item = f"{replica}\\{rep_rel_path}"
                self.remove_item(extra_item)
                self.logger.info(f"Removed extra file: {extra_item}")

        self.logger.info("Directory synchronization complete.")

    def calculate_md5(self, file_path: str) -> Union[str, None]:
        """Calculate the MD5 checksum of a file"""
        cmd = [
            "powershell",
            "-Command",
            f"Get-FileHash -Path '{file_path}' -Algorithm MD5 | Format-List",
        ]
        result = self.execute_command(cmd, f"Calculate MD5 for: {file_path}")
        if result:
            # example output: 'Algorithm : MD5\nHash      : AFC53E050A355DEBA218CC38995B10F6\nPath
            # : {absolute_path_root}}\\source\\noting.txt'
            for line in result.split("\n"):
                if "Hash" in line:
                    return line.split(":")[1].strip()

        return None
