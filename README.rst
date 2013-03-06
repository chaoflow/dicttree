Get dicttree and metachao, dicttree expects metachao to be in a
sibling directory:

    % mkdir dt
    % cd dt
    % git clone git://github.com/chaoflow/metachao
    % git clone git://github.com/chaoflow/dicttree

Bootstrap (needs $NIX_PATH to be set)

    % make bootstrap

Run tests and coverage::

    $ make check

