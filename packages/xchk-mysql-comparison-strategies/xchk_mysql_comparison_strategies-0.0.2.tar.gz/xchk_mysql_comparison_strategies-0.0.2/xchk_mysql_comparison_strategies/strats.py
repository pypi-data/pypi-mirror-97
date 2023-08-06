import subprocess

from django.conf import settings
from xchk_core.strats import *

unspecified_db_cmd = ['mysql', '-u', 'root', '-h', 'mysql', f'--password={settings.MYSQL_ROOT_PASSWORD}']
student_db_cmd = lambda uname, pw: ['mysql', '-u', uname, '-h', 'mysql', f'--password={pw}']

# algemene strategie
# 1) calibratie -> kan dit doen door Strategy te subclassen
# 2) uitvoeren eigenlijke scripts (model en student) en controle op output beide scripts (te testen + aan te passen aan access control)
# 3) controle op tabelstructuur
# 4) controle op aanwezige data
# ???) controle op gelijke constraints, was er nog niet

class ExecutedScriptHasMatchingOutputCheck(CheckingPredicate):

    def __init__(self,model_path):
        super().__init__()
        self.model_path = model_path

    def instructions(self,exercise_name):
        """Returns a hierarchical representation of the explicit conditions to be met for this check to return `True`."""
        return [f"{exercise_name}.sql produceert dezelfde uitvoer als de modeloplossing"]

    def negative_instructions(self,exercise_name):
        """Returns a hierarchical representation of the explicit conditions to be met for this check to return `False`."""
        return [f"{exercise_name}.sql produceert een andere uitvoer dan de modeloplossing"]

    def component_checks(self):
        return []

    def check_submission(self,submission,student_path,desired_outcome,init_check_number,ancestor_has_alternatives,parent_is_negation=False,open=open):
        entry = f'{submission.exercise.slug}.sql'
        with open(self.model_path) as fh:
            model_script_result = subprocess.run(unspecified_db_cmd,text=True,input=fh.read(), capture_output=True)
        with open(os.path.join(student_path,entry)) as fh:
            student_script_result = subprocess.run(student_db_cmd(submission.submitter.username,submission.submitter.initial_pw),text=True,input=fh.read(), capture_output=True)
        same_outputs = model_script_result.stdout == student_script_result.stdout and model_script_result.stderr == student_script_result.stderr
        if desired_outcome and not same_outputs:
            component = OutcomeComponent(component_number=init_check_number,
                                         outcome=False,
                                         desired_outcome=desired_outcome,
                                         # TODO: kan verschil beter in de verf zetten
                                         rendered_data=f'<p>Jouw script produceert een andere output dan de modeloplossing. Jouw script produceert op de output stream:<br>{student_script_result.stdout}<br>Jouw script produceert op de error stream:<br>{student_script_result.stderr}</p><p>Het modelscript produceert op de output stream:<br>{model_script_result.stdout}<br>He tmodelscript produceert op de error stream:<br>{model_script_result.stderr}</p>',
                                         acceptable_to_ancestor=ancestor_has_alternatives)
        elif not desired_outcome and same_outputs:
            # willen verschillende output maar is niet zo
            component = OutcomeComponent(component_number=init_check_number,
                                         outcome=True,
                                         desired_outcome=desired_outcome,
                                         rendered_data=f'<p>De output stream en error stream van jouw script produceren identiek identiek hetzelfde als de output stream en error stream van de modeloplossing.</p>',
                                         acceptable_to_ancestor=ancestor_has_alternatives)
        else:
            component = OutcomeComponent(component_number=init_check_number,
                                         outcome=same_outputs,
                                         desired_outcome=desired_outcome, # = same_outputs
                                         rendered_data=None,
                                         acceptable_to_ancestor=True)
        return OutcomeAnalysis(outcome=same_outputs,
                               outcomes_components=[component])

# if desired, define strategies by subclassing Strategy
# override __init__ so that refusing_check and accepting_check are hardwired
class MySQLCalibrationStrategy(Strategy):

    def __init__(self,refusing_check=Negation(TrueCheck()),accepting_check=Negation(TrueCheck()),student_calibration=None,model_calibration=None):
        super().__init__(refusing_check,accepting_check)
        self.student_calibration = student_calibration
        self.model_calibration = model_calibration

    def check_submission(self,submission,student_path):
        setup_instructions = f"""drop user if exists {submission.submitter.username};
drop database if exists {submission.submitter.username};
create user {submission.submitter.username} identified by '{submission.submitter.initial_pw}';
create database {submission.submitter.username};
grant all on {submission.submitter.username}.* to {submission.submitter.username}@'%';
drop database if exists Model;
create database Model;"""
        subprocess.run(unspecified_db_cmd,text=True,input=setup_instructions)
        subprocess.run(unspecified_db_cmd,text=True,input=self.student_calibration)
        subprocess.run(unspecified_db_cmd,text=True,input=self.model_calibration)
        return super().check_submission(submission,student_path)
