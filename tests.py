import unittest
import pwyo

from unittest import mock


class TestPWYO(unittest.TestCase):

    def test_load_files_in_commit(self):
        with mock.patch('pwyo.check_output', return_value=" M pwyo.py\n?? tests.py\n"):
            expected = [
                {"type": "M", "file": "pwyo.py"},
                {"type": "??", "file": "tests.py"}
            ]
            current = pwyo.load_files_in_commit()
            self.assertEqual(expected, current)

if __name__ == '__main__':
    unittest.main()
