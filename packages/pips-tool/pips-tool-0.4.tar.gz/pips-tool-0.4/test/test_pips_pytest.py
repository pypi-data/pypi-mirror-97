import subprocess
import sys
import os
import pytest
from pips import Pips
from unittest.mock import patch


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    print("teardown")
    process = subprocess.Popen("pip uninstall --yes " + "Jinja2" + "" + "werkzeug", shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode
    print(out)
    # Remove the requirements files
    if os.path.exists("requirements.txt"):
        os.remove("requirements.txt")
    if os.path.exists("requirements.lock"):
        os.remove("requirements.lock")

@pytest.fixture
def site_package_path():
    """
     getting path to the site-packages
     I use "venv37" as a convetion for my venvs to see in which version I'm working
    """
    print(os.getcwd())
    python_version = str(sys.version_info.major) + str(sys.version_info.minor)
    print(f"Python-Verison: {python_version}")
    if sys.platform == 'darwin':
        path_to_site_packages = os.path.join("./venv36/lib", python_version, "site-packages")
    elif sys.platform == 'win32':
        path_to_site_packages = "./venv" + python_version + "/Lib/site-packages/"
    print(f"site packages are located here: {path_to_site_packages}")
    return path_to_site_packages


def is_package_in_file(file_name, package_name):
    print(package_name)
    package_found = False
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            if package_name in line:
                package_found = True
    return package_found


def test_install_one_package(site_package_path):
    """
    Tests if a single package can be installed and locked
    Jinja2 needs "MarkupSafe" as sub-dependecy
    """

    test_args = ["pips", "install", "Jinja2"]
    with patch.object(sys, 'argv', test_args):
        Pips()

    assert os.path.exists(os.path.join(site_package_path, "jinja2"))
    assert os.path.exists("requirements.txt")
    assert os.path.exists("requirements.lock")

    package_found = is_package_in_file("requirements.txt", "Jinja2")
    assert package_found

    package_found_in_lock = is_package_in_file("requirements.lock", "Jinja2")
    assert package_found_in_lock

    sub_deb_found_in_lock = is_package_in_file("requirements.lock", "MarkupSafe")
    assert sub_deb_found_in_lock


def test_uninstall_package(site_package_path):
    """Tests if a single package can be uninstalled"""

    test_args = ["pips", "install", "Jinja2"]
    with patch.object(sys, 'argv', test_args):
        Pips()

    test_args = ["pips", "uninstall", "Jinja2"]
    with patch.object(sys, 'argv', test_args):
        Pips()

    assert not os.path.exists(site_package_path + "jinja2")
    assert not os.path.exists(site_package_path + "MarkupSafe")