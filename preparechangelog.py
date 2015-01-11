#!/usr/bin/env python
import re
import subprocess
import sys


def main():
    filename = sys.argv[1]
    try:
        mode = sys.argv[2]
    except IndexError:
        mode = 'empty'
    if mode != 'empty':
        return

    changelog_file = cmd('git config --get changelog.filename')
    if not changelog_file:
        changelog_file = 'CHANGES'
    changelog = normalize_log(get_diff(changelog_file))

    with open(filename) as f:
        original = f.read()
    with open(filename, 'w') as output:
        output.write(changelog)
        output.write(original)


def get_diff(filename):
    result = []
    diff = cmd('git diff --no-color --staged {}'.format(filename))
    after_header = False
    for line in diff.splitlines():
        if after_header and (
                line.startswith('+') and not line.startswith('+++')):
            result.append(line[1:].rstrip().expandtabs())
        if line.startswith('@@') and line.endswith('@@'):
            after_header = True
    return result


_bullet_re = re.compile(r'\s*[-+*]\s+')


# Taken from <https://bitbucket.org/birkenfeld/hgchangelog>
def normalize_log(lines):
    """Outdents newly inserted list items."""
    last_indention = 0
    for idx, line in enumerate(lines):
        match = _bullet_re.match(line)
        if match is not None:
            last_indention = match.end()
            lines[idx] = line[last_indention:]
        elif last_indention:
            if not line[:last_indention].strip():
                lines[idx] = line[last_indention:]
    return '\n'.join(lines)


def cmd(cmd):
    process = subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # XXX This simply assumes utf8 -- is that feasible?
    return stdout.strip().decode('utf8')


if __name__ == '__main__':
    main()
