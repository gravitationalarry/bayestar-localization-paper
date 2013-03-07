bayestar-localization-paper
===========================

bayestar-localization technical paper

Attention Mac users
-------------------

In order to build a PDF from this manuscript, make sure that you have installed the
following packages with MacPorts:

    $ sudo port install texlive-bibtex-extra texlive-humanities

Git submodules
--------------

Some of the LaTeX files for this manuscript are in Git submodules <http://git-scm.com/book/en/Git-Tools-Submodules>.
After you clone this repository, grab the submodules with the following two commands:

    $ git submodule init
    $ git submodule update

Then, when you pull the repository, to update the submodules, run

    $ git submodule update
