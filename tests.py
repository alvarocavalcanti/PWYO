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

    def test_load_files_in_commit_with_double_spaces(self):
        with mock.patch('pwyo.check_output', return_value=" MM pwyo.py\nM  tests.py\n M tests1.py\n"):
            expected = [
                {"type": "MM", "file": "pwyo.py"},
                {"type": "M", "file": "tests.py"},
                {"type": "M", "file": "tests1.py"}
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

    def test_match_files_against_tech_debts(self):
        tech_debts = [
            {'title': 'Tech Debt Dummy A',
            'file': 'file_a.py'},
            {'title': 'Tech Debt Dummy B',
            'file': 'file_b.py'},
            {'title': 'Tech Debt Dummy D',
            'file': 'file_d.py'}
        ]
        files = [
            {'type': 'A', 'file': 'file_a.py'},
            {'type': 'B', 'file': 'file_b.py'},
            {'type': 'C', 'file': 'file_c.py'}
        ]

        afftected_tech_debts = pwyo.match_files_against_tech_debts(files, tech_debts)

        _ = tech_debts.pop()

        self.assertEqual(tech_debts, afftected_tech_debts)

    def test_user_input_yes_halts_commit(self):
        with mock.patch('pwyo.get_input', return_value='yes'):
            with mock.patch('pwyo.do_print'):
                with mock.patch('pwyo.do_exit') as exit_mock:
                    pwyo.ask_commiter_about_halting_commit([{'title': 'dummy', 'file': 'dummy'}])
                    exit_mock.assert_called_with(1)

    def test_user_input_any_continues_commit(self):
        with mock.patch('pwyo.get_input', return_value='no'):
            with mock.patch('pwyo.do_print'):
                with mock.patch('pwyo.do_exit') as exit_mock:
                    pwyo.ask_commiter_about_halting_commit([{'title': 'dummy', 'file': 'dummy'}])
                    exit_mock.assert_not_called()

    def test_checks_for_missing_tech_debt_files(self):
        tech_debt_a = {'title': 'Tech Debt Dummy A', 'file': 'file_a.py'}
        tech_debts = [
            tech_debt_a,
            {'title': 'Tech Debt Dummy B',
            'file': 'file_b.py'},
            {'title': 'Tech Debt Dummy C',
            'file': 'file_c.py'}
        ]

        def side_effect(file_name):
            if file_name == 'file_a.py':
                return False
            return True

        with mock.patch('pwyo.file_exists', side_effect=side_effect):
            missing_tech_debt_files = pwyo.check_for_missing_tech_debt_files(tech_debts)

        self.assertEqual(1, len(missing_tech_debt_files))
        self.assertEqual(tech_debt_a, missing_tech_debt_files[0])

if __name__ == '__main__':
    unittest.main()
