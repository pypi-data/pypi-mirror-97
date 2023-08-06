import unittest
from pip._internal.utils.misc import get_installed_distributions


class PipTest(unittest.TestCase):
    def setUp(self) -> None:
        self.package_name = "flask"

    def test_pip_install(self):
        from pip._internal import main as pipmain
        pipmain(['install', self.package_name])

    def test_pip_uninstall(self):
        from pip._internal import main as pipmain
        pipmain(['uninstall', "--yes", self.package_name])

    def test_freeze(self):
        with open("requirements.txt", "w") as f:
            for dist in get_installed_distributions():
                req = dist.as_requirement()
                f.write(str(req) + "\n")



if __name__ == '__main__':
    unittest.main()
