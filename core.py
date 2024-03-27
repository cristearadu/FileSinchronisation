import subprocess


class Core:
    def __init__(self):
        self.os_type = self.__determine_os_type()

    def __determine_os_type(self):
        """Determine the operating system type"""
        try:
            subprocess.check_output(["uname"], stderr=subprocess.STDOUT)
            return "Unix-like"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "Windows"

    def __get_root_directory(self):
        """Get the current working directory."""
        try:
            cmd = (
                [
                    "powershell",
                    "-Command",
                    "Get-Location | Select-Object -ExpandProperty Path",
                ]
                if self.os_type == "Windows"
                else ["pwd"]
            )
            return subprocess.check_output(cmd, text=True).strip()
        except subprocess.SubprocessError as e:
            print(f"Error getting root directory: {e}")
            return ""

    def ensure_directory_exists(self, directory_path):
        """Ensure a directory exists; create it if it doesn't"""
        try:
            if self.os_type == "Windows":
                subprocess.run(["mkdir", directory_path], check=True, shell=True)
            else:
                subprocess.run(["mkdir", "-p", directory_path], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create directory {directory_path}: {e}")

    def create_file(self, file_path):
        """Create a file at the specified path, including any necessary directories"""
        directory_path = "/".join(file_path.split("/")[:-1])
        self.ensure_directory_exists(directory_path)

        try:
            if self.os_type == "Windows":
                subprocess.run(f'type nul > "{file_path}"', check=True, shell=True)
            else:
                subprocess.run(["touch", file_path], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create file {file_path}: {e}")

    @property
    def root_directory(self):
        """Property to lazily get the root directory"""
        return self.__get_root_directory()
