import argparse
import os
import sys
import time
from unittest.mock import patch

import pipdeptree
from pip._internal import main as pipmain
from pip._internal.utils.misc import get_installed_distributions

lock_file = "requirements.lock"
requirements_file = "requirements.txt"


class Pips:
    def __init__(self):
        parser = argparse.ArgumentParser(
            usage='''pips <command> [<args>]
        ''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        # TODO print help
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def install(self):
        parser = self.create_subparser()
        if sys.argv[2:]:
            self._install_package(parser)
        else:
            self._install_all(parser)

    def _install_package(self, parser):
        args = parser.parse_args(sys.argv[2:])
        print('Running pips install, package=%s' % args.package)
        package = args.package
        pipmain(['install', package])
        self.add_requirements_to_req_txt_file(package)
        #TODO wait before locking
        self.lock_dependencies()

    def _install_all(self, parser):
        print('Running pips install')
        # install requirements from requirements.lock
        if os.path.isfile(lock_file):
            pipmain(['install', '-r', lock_file])
        elif os.path.isfile("requirements.txt"):
            pipmain(['install', '-r', requirements_file])
            time.sleep(3)  # TODO Remove Hack
            self.lock_dependencies()
        else:
            print('No requirements files found')
            parser.print_help()
            exit(1)

    @staticmethod
    def create_subparser():
        parser = argparse.ArgumentParser()
        parser.add_argument('package')
        return parser

    @staticmethod
    def lock_dependencies():
        with open(lock_file, "w") as f:
            installed_dependencies = get_installed_distributions()
            for dist in installed_dependencies:
                req = dist.as_requirement()
                f.write(str(req) + "\n")

    def is_package_in_file(self, file_name, package_name):
        package_found = False
        with open(file_name, "r") as f:
            lines = f.readlines()
            for line in lines:
                if package_name in line:
                    package_found = True
        return package_found

    def add_requirements_to_req_txt_file(self, package):
        if not os.path.isfile(requirements_file):
            f = open(requirements_file, "w+")
            f.close()
        if not self.is_package_in_file(requirements_file, package):
            with open(requirements_file, "a") as f:
                f.writelines(package + "\n")

    @staticmethod
    def get_package_dependencies(package_name):
        test_args = ["pipdeptree", "--package", package_name]
        with patch.object(sys, 'argv', test_args):
            args = pipdeptree._get_args()
            packages = get_installed_distributions(local_only=args.local_only,
                                                   user_only=args.user_only)
            dist_index = pipdeptree.build_dist_index(packages)
            tree = pipdeptree.construct_tree(dist_index)
            dep_names = []
            for entry in tree:
                if entry.key == package_name.lower():
                    dependencies = tree[entry]
                    for dep in dependencies:
                        dep_names.append(dep.key)
                    print(dep_names)
        return dep_names

    def uninstall(self):
        parser = self.create_subparser()
        if sys.argv[2:]:
            args = parser.parse_args(sys.argv[2:])
            package = args.package
            print('Running pips uninstall, package=%s' % package)
            deps = self.get_package_dependencies(package)
            for dep in deps:
                dep_count = deps.count(dep)
                if not self.is_package_in_file(file_name=requirements_file, package_name=dep) and dep_count < 2:
                    pipmain(['uninstall', "--yes", dep])
            pipmain(['uninstall', "--yes", package])
            # remove_requirements_from_req_txt_file(package)
