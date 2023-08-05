from unittest import TestCase
from ftsa.cli.utils import sanitize, get_base_project_path, Caps


class FilesTest(TestCase):

    def setUp(self) -> None:
        self._myDirName = 'MyDír nâMè'

    def test_sanitize_standard(self):
        self.assertEqual(sanitize(self._myDirName), 'mydir-name')

    def test_sanitize_lowercase(self):
        self.assertEqual(sanitize(self._myDirName, Caps.LOWER), 'mydir-name')

    def test_sanitize_uppercase(self):
        self.assertEqual(sanitize(self._myDirName, Caps.UPPER), 'MYDIR-NAME')

    def test_sanitize_firstuppercase(self):
        self.assertEqual(sanitize(self._myDirName, Caps.FIRST), 'Mydir-Name')

    def test_sanitize_standard_change_blank_for_underline(self):
        self.assertEqual(sanitize(self._myDirName, inn=' ', out='_'), 'mydir_name')

    def test_sanitize_lowercase_change_blank_for_underline(self):
        self.assertEqual(sanitize(self._myDirName, Caps.LOWER, inn=' ', out='_'), 'mydir_name')

    def test_sanitize_uppercase_change_blank_for_underline(self):
        self.assertEqual(sanitize(self._myDirName, Caps.UPPER, inn=' ', out='_'), 'MYDIR_NAME')

    def test_sanitize_firstuppercase_change_blank_for_underline(self):
        self.assertEqual(sanitize(self._myDirName, Caps.FIRST, inn=' ', out='_'), 'Mydir_Name')

    def test_get_base_project_path(self):
        path = get_base_project_path()
        print(f'Path is: {path}')
        self.assertIsNotNone(path)