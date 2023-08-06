import subprocess
import sys
import os
import unittest
from pips.pips import Pips
from unittest.mock import patch


class PipsTest(unittest.TestCase):
    def setUp(self) -> None:
        # import site
        # site.getsitepackages()
        # /home/travis/virtualenv/python3.6.3/lib/python3.6/site-packages
        # on Windows use glob?
        python_version = str(sys.version_info.major)  + str(sys.version_info.minor)
        if sys.platform == 'darwin':
            self.path_to_site_packages = os.path.join("../venv36/lib", python_version, "site-packages")
        elif sys.platform == 'win32':
            self.path_to_site_packages = "../venv" + python_version + "/Lib/site-packages/"
        self.package = "Jinja2"
        self.second_package = "werkzeug"
        self.sub_dependency = "MarkupSafe"
        self.requirements_file = "requirements.txt"
        self.lock_file = "requirements.lock"

    def test_install(self):
        """Tests if all packages from the requirements.txt are installed"""
        print(os.getcwd())
        if not os.path.isfile(self.requirements_file):
            f = open(self.requirements_file, "w+")
            f.close()
        with open(self.requirements_file, "w") as f:
            f.writelines(self.package)
        test_args = ["pips", "install"]

        with patch.object(sys, 'argv', test_args):
            Pips()

        self.assertTrue(os.path.exists(self.path_to_site_packages + self.package.lower()))
        self.assertTrue(os.path.exists(self.requirements_file))
        self.assertTrue(os.path.exists("requirements.lock"))

    def test_install_one_package(self):
        """Tests if a single package can be installed and locked"""

        test_args = ["pips", "install", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()

        self.assertTrue(os.path.exists(self.path_to_site_packages + self.package.lower()))
        self.assertTrue(os.path.exists(self.requirements_file))
        self.assertTrue(os.path.exists("requirements.lock"))

        package_found = self.is_package_in_file(self.requirements_file, self.package)
        self.assertTrue(package_found)

        package_found_in_lock = self.is_package_in_file(self.lock_file, self.package)
        self.assertTrue(package_found_in_lock)

        sub_deb_found_in_lock = self.is_package_in_file(self.lock_file, self.sub_dependency)
        self.assertTrue(sub_deb_found_in_lock)

    def test_install_two_packages(self):
        """Tests if a second package can be installed and is present in the requirements.txt"""

        test_args = ["pips", "install", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()
        test_args = ["pips", "install", self.second_package]
        with patch.object(sys, 'argv', test_args):
            Pips()
        first_package_found = self.is_package_in_file(self.requirements_file, self.package)
        self.assertTrue(first_package_found)
        second_package_found = self.is_package_in_file(self.requirements_file, self.second_package)
        self.assertTrue(second_package_found)

    def test_uninstall_package(self):
        """Tests if a single package can be uninstalled"""

        test_args = ["pips", "install", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()

        test_args = ["pips", "uninstall", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()

        self.assertFalse(os.path.exists(self.path_to_site_packages + self.package.lower()))
        self.assertFalse(os.path.exists(self.path_to_site_packages + self.sub_dependency.lower()))

    def test_uninstall_package_without_de_install_subdep(self):
        """ Tests if a sub-dependency will not be uninstalled if it is a sub dep of another package """
        # install markupsafe and flask
        #
        test_args = ["pips", "install", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()

        test_args = ["pips", "uninstall", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()

        self.assertFalse(os.path.exists(self.path_to_site_packages + self.package.lower()))
        self.assertTrue(os.path.exists(self.path_to_site_packages + self.sub_dependency.lower()))

    def tearDown(self) -> None:
        print("teardown")
        process = subprocess.Popen("pip uninstall --yes " + self.package + "" + self.second_package, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode
        print(out)
        if os.path.exists(self.requirements_file):
            os.remove(self.requirements_file)
        if os.path.exists("requirements.lock"):
            os.remove("requirements.lock")

    def is_package_in_file(self, file_name, package_name):
        package_found = False
        with open(file_name, "r") as f:
            lines = f.readlines()
            for line in lines:
                if package_name in line:
                    package_found = True
        return package_found


if __name__ == '__main__':
    unittest.main()
