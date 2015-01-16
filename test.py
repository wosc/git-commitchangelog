# coding: utf8
from preparechangelog import cmd
import pytest
import shutil
import sys


@pytest.fixture(scope='session')
def gitconfig(request):
    config = cmd('git config --global --get-regexp changelog')
    if not config:
        return

    cmd('git config --global --rename-section changelog changelogpytest')

    def teardown():
        cmd('git config --global --rename-section changelogpytest changelog')
    request.addfinalizer(teardown)


@pytest.fixture
def repository(request, gitconfig, tmpdir):
    cmd('cd {dir}; git init'.format(dir=tmpdir))
    hook = '%s/.git/hooks/prepare-commit-msg' % tmpdir
    shutil.copy('preparechangelog.py', hook)
    cmd('sed -i -e "s+/usr/bin/env python+{}+" {}'.format(
        sys.executable, hook))
    return str(tmpdir)


def test_prefills_commit_message_from_changelog_diff(repository):
    message = cmd('cd {dir}; echo "foo" > CHANGES; echo "qux" > bar;'
                  'git add .; EDITOR=cat git commit'.format(dir=repository))
    assert message.startswith('foo\n')
    assert 'qux' not in message


def test_normalizes_bullets(repository):
    message = cmd('cd {dir}; echo "- One\\n  Two\\n- Three\n" > CHANGES;'
                  'git add .; EDITOR=cat git commit'.format(dir=repository))
    assert message.startswith('One\nTwo\nThree\n')


def test_changelog_filename_is_configurable(repository):
    cmd('cd {dir}; git config changelog.filename qux'.format(dir=repository))
    message = cmd('cd {dir}; echo "foo" > qux; git add .;'
                  'EDITOR=cat git commit'.format(dir=repository))
    assert message.startswith('foo\n')


def test_handles_non_ascii(repository):
    message = cmd('cd {dir}; echo "Ümläut" > CHANGES;'
                  'git add .; EDITOR=cat git commit'.format(dir=repository))
    assert message.startswith(u'Ümläut')


def test_result_of_preprocess_is_used_as_message(repository):
    cmd('cd {dir}; git config changelog.preprocess "lambda x: x.upper()"'
        .format(dir=repository))
    message = cmd('cd {dir}; echo "foo" > CHANGES;'
                  'git add .; EDITOR=cat git commit'.format(dir=repository))
    assert message.startswith('FOO')
