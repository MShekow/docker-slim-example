import argparse

import docker
from boltons.strutils import bytes2human


def print_image_sizes_and_optimization_ratio(slim_image_name: str, fat_image_name: str):
    client = docker.from_env()

    slim_inspect_output = client.api.inspect_image(slim_image_name)
    slim_image_size_bytes: int = slim_inspect_output["Size"]
    fat_inspect_output = client.api.inspect_image(fat_image_name)
    fat_image_size_bytes: int = fat_inspect_output["Size"]

    ratio = fat_image_size_bytes / slim_image_size_bytes

    print(f"Fat image size: {fat_image_size_bytes} ({bytes2human(fat_image_size_bytes)}), "
          f"Slim image size: {slim_image_size_bytes} ({bytes2human(slim_image_size_bytes)}), "
          f"optimization factor: {ratio}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docker-Slim File Analyser")
    parser.add_argument('fat_image_name')
    parser.add_argument('slim_image_name')
    args = parser.parse_args()

    print_image_sizes_and_optimization_ratio(args.slim_image_name, args.fat_image_name)
