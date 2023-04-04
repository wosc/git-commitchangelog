git-commitchangelog
===================

This is a git hook that prefills the commit message with the diff to the
changelog file. It is inspired by the mercurial extension
[hgchangelog](https://bitbucket.org/birkenfeld/hgchangelog).

The hook is written in Python and requires at least Python 3.3.

To install it, copy `preparechangelog.py` to
`.git/hooks/prepare-commit-msg` in your git repository (make sure the
file is executable). If you want it to be added to reposiories
automatically, you need to use a [template
directory](https://coderwall.com/p/jp7d5q/create-a-global-git-commit-hook):

    $ mkdir -p ~/.git-templates/hooks
    $ cp preparechangelog.py ~/.git-templates/hooks/prepare-commit-msg
    $ chmod +x ~/.git-templates/hooks/prepare-commit-msg
    $ git config --global init.templatedir '~/.git-templates'

The default changelog filename is `CHANGES`, you can configure this in
your `~/.gitconfig` as follows:

    [changelog]
    filename = CHANGES.txt

For some simple preprocessing, you can configure a callable that receives the
extracted changelog diff as its argument, like this:

    [changelog]
    preprocess = lambda msg: msg.upper()

You can use the `re` module in the `preprocess` callable, so for a more
realistic example, to transform "Updated flux compensator (TICKET-123)" into
"Re TICKET-123: Updated flux compensator", you could use this (note that
backslashes need to be escaped in the `.gitconfig` file):

    [changelog]
    preprocess = lambda x: re.sub('(^.*) ?\\(([A-Z]+-[0-9]+)\\)\\.?$', r'Re \\2: \\1', x)

