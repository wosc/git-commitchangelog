#!/usr/bin/env python
#
# git hook that prefills the commit message with the diff to the changelog file
#
# Copyright (c) 2015, Wolfgang Schnerring
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import io
import re
import subprocess
import sys


__version__ = '1.0'


if sys.version_info >= (3,):
    text = str
else:
    text = unicode


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

    preprocess = cmd('git config --get changelog.preprocess')
    if preprocess:
        preprocess = eval(
            preprocess, {'re': re, '__builtins__': __builtins__})
        changelog = preprocess(changelog)

    with io.open(filename) as f:
        original = f.read()
    with io.open(filename, 'w') as output:
        output.write(changelog)
        output.write(original)


def get_diff(filename):
    result = []
    diff = cmd('git diff --no-color --staged {}'.format(filename))
    for line in diff.splitlines():
        if line.startswith('+') and not line.startswith('+++'):
            result.append(line[1:].rstrip().expandtabs())
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
    return text('\n').join(lines)


def cmd(cmd):
    process = subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # XXX This simply assumes utf8 -- is that feasible?
    return stdout.strip().decode('utf8')


if __name__ == '__main__':
    main()
