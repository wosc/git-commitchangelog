git-commitchangelog
===================

This is a git hook that prefills the commit message with the diff to the
changelog file. It is inspired by the mercurial extension
[hgchangelog](https://bitbucket.org/birkenfeld/hgchangelog).

The hook is written in Python and requires at least Python 2.7 or Python
3.3.

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
