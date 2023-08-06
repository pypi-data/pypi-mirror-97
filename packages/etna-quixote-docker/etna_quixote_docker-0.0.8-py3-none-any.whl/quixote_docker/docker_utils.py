from contextlib import contextmanager
import docker
from docker.errors import APIError, ContainerError
import io
from functools import reduce
import os
import tarfile
import tempfile


@contextmanager
def docker_daemon_autocleanup():
    try:
        yield
    finally:
        client = docker.from_env()

        # Kill any remaining container
        for container in client.containers.list():
            try:
                container.kill()
            except APIError:
                pass

        # Remove any remaining network
        for network in client.networks.list():
            if network.name not in ("none", "bridge", "host"):
                network.remove()


class VolumeExtractionError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self):
        return f"VolumeExtractionError(message={self.message!r})"

    def __str__(self):
        return self.message


class VolumeCopyError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self):
        return f"VolumeCopyError(message={self.message!r})"

    def __str__(self):
        return self.message


class VolumeContents:
    """
    Class representing extracted contents of a named volume

    """

    def __init__(self, temp_dir: tempfile.TemporaryDirectory):
        self._temp_dir = temp_dir

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._temp_dir.cleanup()

    def path(self) -> str:
        """
        Path to where the contents are extracted
        """
        return f"{self._temp_dir.name}/data"


def extract_volume_contents(volume_name: str) -> VolumeContents:
    """
    Extracts named volume contents
    """
    client = docker.from_env(version="1.40")

    try:
        client.images.pull("busybox:latest")
        container = client.containers.create("busybox:latest", volumes=[f"{volume_name}:/data"])
    except (APIError, ContainerError) as e:
        raise VolumeExtractionError(f"internal error: cannot create a 'busybox' container: {e}")

    try:
        byte_chunks, _ = container.get_archive("/data/")
    except APIError as e:
        raise VolumeExtractionError(f"internal error: cannot retrieve the volume data: {e.explanation or e})")

    file_data = reduce(lambda acc, new: acc + new, byte_chunks, bytes())
    tar_stream = io.BytesIO(file_data)

    temp_dir = tempfile.TemporaryDirectory(prefix="volume")

    with tarfile.open(fileobj=tar_stream) as f:
        f.extractall(temp_dir.name)
    return VolumeContents(temp_dir)


def copy_to_volume(volume_name: str, local_path: str, base_path="/"):
    """
    Copies files or directories to a named volume
    """
    client = docker.from_env(version="1.40")

    with tempfile.NamedTemporaryFile(prefix="volume") as temp_file:
        with tarfile.open(temp_file.name, "w") as tar_handle:
            if os.path.isdir(local_path):
                dirname = os.path.dirname(local_path)
                if local_path[-1] == "/":
                    dirname = os.path.dirname(local_path)
                for root, _, files in os.walk(local_path):
                    for file in files:
                        rel = os.path.relpath(root, dirname)
                        tar_handle.add(f"{root}/{file}", arcname=f"{base_path}/{rel}/{file}")
            else:
                tar_handle.add(local_path, f"{base_path}/{os.path.basename(local_path)}")

        try:
            client.images.pull("busybox:latest")
            container = client.containers.create("busybox:latest", volumes=[f"{volume_name}:/data"])
        except (APIError, ContainerError) as e:
            raise VolumeCopyError(f"internal error: cannot create a 'busybox' container: {e}")

        try:
            with open(temp_file.name) as f:
                container.put_archive("/data/", f.read())
        except APIError as e:
            raise VolumeCopyError(f"internal error: cannot retrieve the volume data: {e.explanation or e}")
