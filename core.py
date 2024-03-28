import subprocess


class Core:
    def __init__(self):
        pass

    def __get_root_directory(self) -> str:
        """Get the current working directory."""
        try:
            cmd = [
                "powershell",
                "-Command",
                "Get-Location | Select-Object -ExpandProperty Path",
            ]
            return subprocess.check_output(cmd, text=True).strip()
        except subprocess.SubprocessError as e:
            print(f"Error getting root directory: {e}")
            return ""

    def ensure_directory_exists(self, directory_path: str) -> None:
        """Ensure a directory exists; create it if it doesn't"""
        try:
            subprocess.run(["mkdir", directory_path], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create directory {directory_path}: {e}")

    def create_file(self, file_path: str) -> None:
        """Create a file at the specified path, including any necessary directories"""
        directory_path = "/".join(file_path.split("/")[:-1])
        self.ensure_directory_exists(directory_path)

        try:
            subprocess.run(f'type nul > "{file_path}"', check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create file {file_path}: {e}")

    @property
    def root_directory(self):
        """Property to lazily get the root directory"""
        return self.__get_root_directory()
