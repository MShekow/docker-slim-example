import argparse
import os
import os.path
import sys
import tarfile
from enum import Enum
from tempfile import TemporaryDirectory
from typing import Mapping, Optional

from boltons.strutils import bytes2human
from testcontainers.core.container import DockerContainer


class SortType(Enum):
    Path = 1
    Size = 2


def get_contained_files_and_dirs(dir_path: str) -> Mapping[str, Optional[int]]:
    files_and_dirs = {}

    for root, dirs, files in os.walk(dir_path):
        relative_root = root[len(dir_path):]
        for file in files:
            files_and_dirs[os.path.join(relative_root, file)] = os.stat(os.path.join(root, file)).st_size
        for dir in dirs:
            files_and_dirs[os.path.join(relative_root, dir)] = None

    return files_and_dirs


def compare_image_contents(slim_image_contents: Mapping[str, Optional[int]],
                           fat_image_contents: Mapping[str, Optional[int]], sort_type: SortType):
    def print_entry(path: str):
        size = fat_image_contents[path]
        human_readable_size = "---" if size is None else bytes2human(size)
        print(f"{human_readable_size:<{10}}{path}")

    removed_files_and_dir_paths = fat_image_contents.keys() - slim_image_contents.keys()

    if sort_type is SortType.Path:
        sorted_removed_files_and_dir_paths = sorted(removed_files_and_dir_paths)
        for p in sorted_removed_files_and_dir_paths:
            print_entry(p)
    elif sort_type is SortType.Size:
        removed_files_and_dirs = {k: v for (k, v) in fat_image_contents.items() if k in removed_files_and_dir_paths}
        for path, size in sorted(removed_files_and_dirs.items(), key=lambda x: x[1], reverse=True):
            print_entry(path)


def get_image_contents(image_name: str) -> Mapping[str, int]:
    with TemporaryDirectory(dir=".") as temp_dir_path:
        exported_archive_path = os.path.join(temp_dir_path, "container.tar")
        with DockerContainer(image=image_name) as container:
            with open(exported_archive_path, "wb") as f:
                for chunk in container.get_wrapped_container().export():
                    f.write(chunk)
        tar_file = tarfile.open(exported_archive_path)
        files_and_dirs = {}
        for entry in tar_file.getmembers():
            files_and_dirs[entry.path] = entry.size
        tar_file.close()
        return files_and_dirs


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')  # fixes console output redirection on Windows
    parser = argparse.ArgumentParser(description="Docker-Slim File Analyser")
    parser.add_argument('fat_image_name')
    parser.add_argument('slim_image_name')
    args = parser.parse_args()

    print("Determining difference of images - this may take a few minutes")

    slim_image_contents = get_image_contents(args.slim_image_name)
    fat_image_contents = get_image_contents(args.fat_image_name)

    print("Listing all paths that were removed in the final image, sorted by path")
    compare_image_contents(slim_image_contents, fat_image_contents, sort_type=SortType.Path)

    for i in range(5):
        print("===========================")

    print("Listing all paths that were removed in the final image, sorted by size")
    compare_image_contents(slim_image_contents, fat_image_contents, sort_type=SortType.Size)
