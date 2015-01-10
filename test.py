from preparechangelog import cmd
import pytest
import shutil


@pytest.fixture
def repository(request, tmpdir):
    cmd('cd {dir}; git init'.format(dir=tmpdir))
    shutil.copy(
        'preparechangelog.py', '%s/.git/hooks/prepare-commit-msg' % tmpdir)
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
