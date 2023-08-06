import json
import argparse
import subprocess
import shutil
import tempfile
import os
from importlib import import_module
from typing import List, TypedDict

PackagePathItem = TypedDict("PackagePathItem", {"name": str, "path": str})


def parse_packages(target_packages=[]):
    # Use subprocess because of avoiding to conflict argparse which is called in pip-licenses
    packages_list_json_str = subprocess.check_output(
        "pip-licenses --format=json --with-license-file --no-license-path", shell=True
    )

    packages_list_json = json.loads(packages_list_json_str)
    res_list = [o for o in packages_list_json if o["Name"] in target_packages]

    license_text_list: List[str] = []
    package_path_list: List[PackagePathItem] = []

    for data in res_list:
        package_name: str = data["Name"]
        try:
            package_path = import_module(package_name).__path__[0]
            item: PackagePathItem = {"name": package_name, "path": package_path}
            package_path_list.append(item)
            license_text_list.append(
                "\n".join(
                    [
                        package_name,
                        data["Version"],
                        data["License"],
                        data["LicenseText"],
                    ]
                )
            )
        except Exception:
            print("You don't have %s package." % package_name)

    return license_text_list, package_path_list


def write_license_file(license_file_name, license_text):
    if license_file_name is not None:
        path = os.path.dirname(license_file_name)
        if not len(path) == 0:
            os.makedirs(path, exist_ok=True)

        with open(license_file_name, mode="w") as f:
            f.write(license_text)
        print("License file created: %s" % os.path.abspath(license_file_name))


def archive_src_files(archive_file_name, package_path_list):
    if archive_file_name is not None:
        archive_name, archive_extension = os.path.splitext(archive_file_name)
        archive_extension = archive_extension.strip(".")

        with tempfile.TemporaryDirectory() as temp_dir:
            root_dir_path = os.path.join(temp_dir, "temp_packages")
            os.mkdir(root_dir_path)
            for obj in package_path_list:
                package_dir = os.path.join(root_dir_path, obj["name"])
                shutil.copytree(obj["path"], package_dir)

            try:
                shutil.make_archive(archive_name, archive_extension, root_dir_path)
                print(
                    "Archive file created: %s.%s"
                    % (
                        os.path.join(os.path.abspath("."), archive_name),
                        archive_extension,
                    )
                )
            except Exception:
                pass


def exec(
    target_packages=[], license_file_name=None, archive_file_name=None, noprint=False
):
    license_text_list, package_path_list = parse_packages(
        target_packages=target_packages
    )

    if len(license_text_list) == 0:
        print("[Finish] You don't have any target packages.")
        return

    license_text = "\n\n".join(license_text_list)

    if not noprint:
        print(license_text)

    write_license_file(license_file_name, license_text)
    archive_src_files(archive_file_name, package_path_list)


def main():
    parser = argparse.ArgumentParser(
        description="Pack selected packages from site-packages and output packed license file"
    )
    parser.add_argument("--packages", help="target package list", nargs="+", default=[])
    parser.add_argument("--license", help="output license file")
    parser.add_argument("--archive", help="output archive file")
    parser.add_argument(
        "--noprint", help="disable to print packed licenses", action="store_true"
    )
    args = parser.parse_args()

    exec(
        target_packages=args.packages,
        license_file_name=args.license,
        archive_file_name=args.archive,
        noprint=args.noprint,
    )
