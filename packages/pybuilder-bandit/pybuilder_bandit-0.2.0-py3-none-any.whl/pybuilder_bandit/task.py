#   -*- coding: utf-8 -*-
import re
from pybuilder.core import init
from pybuilder.core import task
from pybuilder.core import depends
from pybuilder.errors import BuildFailedException
from pybuilder.pluginhelper.external_command import ExternalCommandBuilder


@init
def init_bandit(project):
    """ initialize complexity task properties
    """
    project.set_property_if_unset('bandit_break_build', False)
    project.set_property_if_unset('bandit_confidence_level', 'LOW')
    project.set_property_if_unset('bandit_severity_level', 'LOW')
    project.set_property_if_unset('bandit_skip_ids', None)
    project.plugin_depends_on('bandit')


@task('bandit', description='execute bandit security linter')
@depends('prepare')
def bandit(project, logger, reactor):
    """ execute bandit security linter
    """
    set_verbose_property(project)
    command = get_command(project, reactor)
    logger.info(f'Executing bandit security linter: \"{command.as_string}\"')
    result = command.run_on_production_source_files(logger, include_dirs_only=True)
    process_result(project, result, logger)


def get_command(project, reactor):
    """ return bandit command
    """
    command = ExternalCommandBuilder('bandit', project, reactor)
    command.use_argument('--recursive')
    command.use_argument('--format')
    command.use_argument('custom')
    command.use_argument('--msg-template')
    command.use_argument("{relpath}:{line}: {test_id}: {severity}: {msg}")
    command.use_argument(translate_confidence_level(project.get_property('bandit_confidence_level')))
    command.use_argument(translate_severity_level(project.get_property('bandit_severity_level')))
    skips = project.get_property('bandit_skip_ids')
    if skips:
        command.use_argument('--skip')
        command.use_argument(skips)
    return command


def set_verbose_property(project):
    """ set verbose property
    """
    verbose = project.get_property('verbose')
    project.set_property('bandit_verbose_output', verbose)


def translate_confidence_level(level):
    """ return confidence level
    """
    if level is None or level == 'LOW':
        return '-i'
    if level == 'MEDIUM':
        return '-ii'
    if level == 'HIGH':
        return '-iii'
    raise ValueError(f'{level} is not a valid confidence level')


def translate_severity_level(level):
    """ return severity level
    """
    if level is None or level == 'LOW':
        return '-l'
    if level == 'MEDIUM':
        return '-ll'
    if level == 'HIGH':
        return '-lll'
    raise ValueError(f'{level} is not a valid severity level')


def process_result(project, result, logger):
    """ process result
    """
    fail_build = project.get_property('bandit_break_build')
    if result.report_lines:
        message = f'Bandit security linter detected issues, see {result.report_file}'
        if fail_build:
            raise BuildFailedException(message)
        else:
            logger.warn(message)
    else:
        logger.info('Bandit security linter found no issues')
