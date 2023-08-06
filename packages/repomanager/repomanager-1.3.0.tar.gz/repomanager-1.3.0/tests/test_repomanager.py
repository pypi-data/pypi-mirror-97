# See LICENSE for details

from click.testing import CliRunner
from repomanager.main import cli
import pytest 

@pytest.fixture
def runner():
    return CliRunner()

def test_clean(runner):
    '''Testing clean option'''
    result = runner.invoke(cli, ['--clean'])
    assert result.exit_code == 0

def test_version(runner):
    '''Testing version option'''
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0

def test_clean_update_patch(runner):
    result = runner.invoke(cli, ['-cup'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['-c'])
    assert result.exit_code == 0

def test_repolist(runner):
    result = runner.invoke(cli, ['--repolist', 'repolist1.yaml', '-cup'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['--repolist', 'repolist1.yaml', '-c'])
    assert result.exit_code == 0

def test_master(runner):
    result = runner.invoke(cli, ['--repolist', 'repo_master.yaml', '-cup'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['--repolist', 'repo_master.yaml', '-c'])
    assert result.exit_code == 0

def test_nopatch(runner):
    result = runner.invoke(cli, ['--repolist', 'repo_nopatch.yaml', '-cup'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['--repolist', 'repo_nopatch.yaml', '-c'])
    assert result.exit_code == 0

#def test_submodule(runner):
#    result = runner.invoke(cli, ['--repolist', 'repo_submodule.yaml', '-r', '--verbose', 'info'])
#    assert result.exit_code == 0
#    result = runner.invoke(cli, ['--repolist', 'repo_submodule.yaml', '-p'])
#    assert result.exit_code == 0
#    result = runner.invoke(cli, ['--repolist', 'repo_submodule.yaml', '--unpatch'])
#    assert result.exit_code == 0
#    result = runner.invoke(cli, ['--repolist', 'repo_submodule.yaml', '--unpatch'])
#    assert result.exit_code == 0
#    result = runner.invoke(cli, ['--repolist', 'repo_submodule.yaml', '-p'])
#    assert result.exit_code == 0

def test_error(runner):
    result = runner.invoke(cli, ['--repolist', 'error.yaml', '-cup'])
    assert result.exit_code != 0

def test_dir(runner):
    '''Testing dir option'''
    result = runner.invoke(cli, ['--dir', 'work', '-cup'])
    assert result.exit_code == 0

