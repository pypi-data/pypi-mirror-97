#   -*- coding: utf-8 -*-
import re
from pybuilder.core import init
from pybuilder.core import task
from pybuilder.core import depends
from pybuilder.errors import BuildFailedException
from pybuilder.pluginhelper.external_command import ExternalCommandBuilder
from pybuilder.utils import assert_can_execute


@init
def init_radon(project):
    """ initialize radon task properties
    """
    project.set_property_if_unset('radon_break_build_average_complexity_threshold', None)
    project.set_property_if_unset('radon_break_build_complexity_threshold', None)
    project.plugin_depends_on('radon')


@task('radon', description='execute radon cyclomatic complexity')
@depends('prepare')
def radon(project, logger):
    """ execute radon cyclomatic complexity
    """
    set_verbose_property(project)
    command = get_command(project)
    logger.info(f'Executing radon cyclomatic complexity: \"{command.as_string}\"')
    # assert_can_execute(command.parts, prerequisite='radon', caller='complexity')
    result = command.run_on_production_source_files(logger)
    if not verify_result(result, logger, command):
        return
    complexity_data = get_complexity(project, result, logger)
    if not verify_complexity(complexity_data):
        return
    process_complexity(project, complexity_data)


def get_command(project):
    """ return radon command
    """
    command = ExternalCommandBuilder('radon', project)
    command.use_argument('cc')
    command.use_argument('-a')
    command.use_argument('-s')
    return command


def set_verbose_property(project):
    """ set verbose property
    """
    verbose = project.get_property('verbose')
    project.set_property('radon_verbose_output', verbose)


def verify_result(result, logger, command):
    """ return True if result contains lines, False otherwise
    """
    if not result.report_lines:
        logger.warn(f"Command {command.as_string} produced no output")
        return False
    if len(result.error_report_lines) > 0:
        logger.error(f"Command {command.as_string} produced errors, see {result.error_report_file}")
        return False
    return True


def get_complexity(project, result, logger):
    """ return complexity info and if verbose log contents of result
    """
    complexity_data = {
        'average': None,
        'highest': {
            'name': None,
            'score': 0
        }
    }
    regex_line = r'[A-Z] \d+:\d+ (?P<name>.*) - [A-Z] \((?P<score>\d+)\)'
    for line in result.report_lines[:-1]:
        line = line.strip()
        match = re.match(regex_line, line)
        if match:
            score = float(match.group('score'))
            if score > complexity_data['highest']['score']:
                complexity_data['highest']['score'] = score
                complexity_data['highest']['name'] = match.group('name')

    average_complexity = result.report_lines[-1].strip()
    logger.info(average_complexity)
    regex_average = r'Average complexity: [A-Z] \((?P<average>.*)\)'
    match = re.match(regex_average, average_complexity)
    if match:
        complexity_data['average'] = float(match.group('average'))

    return complexity_data


def verify_complexity(complexity_data):
    """ return True if complexity structure is valid, False otherwise
    """
    if complexity_data['average'] is None:
        return False
    if complexity_data['highest']['name'] is None:
        return False
    return True


def process_complexity(project, complexity_data):
    """ process complexity
    """
    average_complexity_threshold = project.get_property('radon_break_build_average_complexity_threshold')
    if average_complexity_threshold:
        average = complexity_data['average']
        if float(average) > average_complexity_threshold:
            raise BuildFailedException(f'average complexity {average} is greater than {average_complexity_threshold}')

    complexity_threshold = project.get_property('radon_break_build_complexity_threshold')
    if complexity_threshold:
        highest_score = complexity_data['highest']['score']
        if float(highest_score) > complexity_threshold:
            name = complexity_data['highest']['name']
            raise BuildFailedException(f'{name} complexity {highest_score} is greater than {complexity_threshold}')
