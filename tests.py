import unittest
import pwyo

from subprocess import check_output
from unittest import mock


class TestPWYO(unittest.TestCase):

    @mock.patch('check_output')
    def test_load_files_in_commit(self, check_output_mock):
        check_output_mock.return_value = " M pwyo.py\n?? tests.py\n"
        expected = " M pwyo.py\n?? tests.py\n"
        current = pwyo.load_files_in_commit()
        self.assertEqual(expected, current)

if __name__ == '__main__':
    unittest.main()
