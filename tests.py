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

    def test_filter_files(self):
        source_files = [
            {'type': 'A', 'file': 'file_a.py'},
            {'type': 'B', 'file': 'file_b.py'},
            {'type': 'C', 'file': 'file_c.py'}
        ]
        types = ['A', 'B']
        result = pwyo.filter_files(source_files, types)
        expected_files = [
            {'type': 'A', 'file': 'file_a.py'},
            {'type': 'B', 'file': 'file_b.py'}
        ]
        self.assertEqual(expected_files, result)

if __name__ == '__main__':
    unittest.main()
