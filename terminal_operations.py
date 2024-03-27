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

    def get_current_directory(self):
        """Get current directory"""
        if self.os_type == "Windows":
            cmd = ["powershell", "-Command", "Get-Location"]
            cmd_display = "powershell -Command Get-Location"
        else:
            cmd = ["pwd"]
            cmd_display = "pwd"
        return self.execute_command(cmd, cmd_display)

    def copy_file(self, source, destination):
        """Copy file from source to destination"""
        if self.os_type == "Windows":
            cmd = ["copy", source, destination]
            cmd_display = f"copy {source} {destination}"
        else:
            cmd = ["cp", source, destination]
            cmd_display = f"cp {source} {destination}"
        return self.execute_command(cmd, cmd_display)

    def list_directory(self, path=""):
        """List all files inside directory"""
        if self.os_type == "Windows":
            cmd = ["dir", path]
            cmd_display = f"dir {path}"
        else:
            cmd = ["ls", "-l", path]
            cmd_display = f"ls -l {path}"
        return self.execute_command(cmd, cmd_display)

    def file_exists(self, path: str) -> bool:
        """Check if a file exists"""
        cmd = (
            f'test -f "{path}" && echo True || echo False'
            if self.os_type == "Unix-like"
            else f'if exist "{path}" (echo True) else (echo False)'
        )
        result = self.execute_command(cmd, f"Check if file exists: {path}")
        return "True" in result

    def dir_exists(self, path: str) -> bool:
        """Check if a directory exists"""
        cmd = (
            f'test -d "{path}" && echo True || echo False'
            if self.os_type == "Unix-like"
            else f'if exist "{path}\\" (echo True) else (echo False)'
        )
        result = self.execute_command(cmd, f"Check if directory exists: {path}")
        return "True" in result

    def create_directory(self, path: str):
        """Create a directory if it doesn't exist"""
        if not self.dir_exists(path):
            cmd = (
                ["mkdir", "-p", path]
                if self.os_type == "Unix-like"
                else ["mkdir", path]
            )
            self.execute_command(cmd, f"Create directory: {path}")

    def remove_file(self, path: str):
        """Remove a file"""
        cmd = ["rm", "-f", path] if self.os_type == "Unix-like" else ["del", "/f", path]
        self.execute_command(cmd, f"Remove file: {path}")

    def write_to_file(self, path: str, content: str):
        """Write content to a file"""
        if self.os_type == "Windows":
            cmd = [
                "powershell",
                "-Command",
                f"Set-Content -Path '{path}' -Value '{content}'",
            ]
        else:
            cmd = ["bash", "-c", f"echo '{content}' > '{path}'"]
        self.execute_command(cmd, f"Write to file: {path}")


    def list_files(self, directory_path):
        """List all files in a directory recursively."""
        if self.os_type == "Windows":
            cmd = f'powershell -Command "Get-ChildItem -Path \'{directory_path}\' -Recurse | Where-Object {{ !$_.PSIsContainer }} | ForEach-Object {{ $_.FullName.Substring((Get-Location).Path.Length + 1) }}"'
        else:
            cmd = f'cd "{directory_path}" && find . -type f'
        return self.execute_command(cmd, f"List all files in {directory_path}").split('\n')
        # if self.os_type == "Windows":
        #     cmd = f'powershell -Command "Get-ChildItem -Path \'{directory_path}\' -Recurse | Where-Object {{ !$_.PSIsContainer }} | ForEach-Object {{ $_.FullName }}"'
        # else:
        #     cmd = f'find "{directory_path}" -type f'
        #
        # result = self.execute_command(cmd, f"List all files in {directory_path}")
        # if result:
        #     files = result.split('\n')
        #     files = [file for file in files if file]
        #     return files
        # else:
        #     self.logger.error(f"Failed to list files in {directory_path}")
        #     return []

    def remove_extra_files(self, source_files, replica, replica_files):
        """Remove files in the replica that aren't in the source based on relative paths"""
        extra_files = set(replica_files) - set(source_files)
        for file_rel_path in extra_files:
            file_path = f"{replica}/{file_rel_path}"
            if self.os_type == "Windows":
                cmd = f'del "{file_path}"'
            else:
                cmd = f'rm "{file_path}"'
            self.execute_command(cmd, f"Remove extra file: {file_rel_path}")
            self.logger.info(f"Removed extra file in replica: {file_rel_path}")

    def sync_directories(self, source, replica):
        """Synchronize source directory with replica directory"""
        source_files = self.list_files(source)
        replica_files = self.list_files(replica)

        for src_rel_path in source_files:
            src_file = f"{source}/{src_rel_path}"
            rep_file = f"{replica}/{src_rel_path}"

            rep_file_dir = '/'.join(rep_file.split('/')[:-1])
            if not self.dir_exists(rep_file_dir):
                self.create_directory(rep_file_dir)

            if not self.file_exists(rep_file) or self.calculate_md5(src_file) != self.calculate_md5(rep_file):
                self.copy_file(src_file, rep_file)
                self.logger.info(f"Synced: {src_file} to {rep_file}")

        for rep_rel_path in replica_files:
            if rep_rel_path not in source_files:
                extra_file = f"{replica}/{rep_rel_path}"
                self.remove_file(extra_file)
                self.logger.info(f"Removed extra file: {extra_file}")

        self.logger.info("Directory synchronization complete.")

    def calculate_md5(self, file_path):
        """Calculate the MD5 checksum of a file using Python's hashlib"""
        cmd = ['powershell', '-Command',
               f"Get-FileHash -Path '{file_path}' -Algorithm MD5 | Format-List"] if self.os_type == "Windows" else [
            "md5sum", file_path]
        result = self.execute_command(cmd, f"Calculate MD5 for: {file_path}")
        if result:
            md5_value = result.split()[-1] if self.os_type == "Unix-like" else result.split(":")[-1].strip()
            return md5_value
        return None

# x = TerminalOperations()
# x.get_current_directory()
