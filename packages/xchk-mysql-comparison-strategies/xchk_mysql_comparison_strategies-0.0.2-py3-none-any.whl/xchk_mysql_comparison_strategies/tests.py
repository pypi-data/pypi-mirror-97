import pathlib
import unittest
from django.test import TestCase
from unittest.mock import Mock, patch, MagicMock
from xchk_core.models import Submission
from xchk_core.templatetags.xchk_instructions import node_instructions_2_ul
from xchk_core.strats import StratInstructions, AT_LEAST_ONE_TEXT, ALL_OF_TEXT
import xchk_mysql_comparison_strategies.strats as strats

original_unspecified_db_cmd = strats.unspecified_db_cmd

# assumes a container with port forwarding is in place
TEST_CONTAINER_NAME = '127.0.0.1'
TEST_CONTAINER_PORT = '3307'
TEST_CONTAINER_PW = 'my-secret-pw'

class IdenticalOutputTest(TestCase):

    def setUp(self):
        substitute_db_cmd = ['mysql', '-u', 'root', '-h', TEST_CONTAINER_NAME, f'--password={TEST_CONTAINER_PW}', '-P', TEST_CONTAINER_PORT]
        strats.unspecified_db_cmd = substitute_db_cmd

    def tearDown(self):
        strats.unspecified_db_cmd = original_unspecified_db_cmd

    def test_identical_output_simple_script(self):
        # Beetje raar dat een file is en ander bepaald wordt in de check...
        model_path = pathlib.Path(__file__).parent / 'solutions' / 'simple_select.sql'
        student_path = pathlib.Path(__file__).parent / 'submitted_files'
        check = strats.ExecutedScriptHasMatchingOutputCheck(model_path=model_path)
        submission = MagicMock()
        exercise = MagicMock
        submission.exercise = exercise
        exercise.slug = 'simple_select'
        analysis = check.check_submission(submission,student_path,True,1,False,False)
        self.assertTrue(analysis.outcome)

    def test_nonidentical_output_simple_script(self):
        # Beetje raar dat een file is en ander bepaald wordt in de check...
        model_path = pathlib.Path(__file__).parent / 'solutions' / 'other_simple_select.sql'
        student_path = pathlib.Path(__file__).parent / 'submitted_files'
        check = strats.ExecutedScriptHasMatchingOutputCheck(model_path=model_path)
        submission = MagicMock()
        exercise = MagicMock
        submission.exercise = exercise
        exercise.slug = 'simple_select'
        analysis = check.check_submission(submission,student_path,True,1,False,False)
        print(analysis)
        self.assertFalse(analysis.outcome)

if __name__ == '__main__':
    unittest.main()
