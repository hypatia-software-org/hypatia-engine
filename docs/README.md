The +sphinx-source+ directory of this project is for Sphinx. I'm using
autodoc and Napoleon for Google-style docstrings. See:
http://sphinxcontrib-napoleon.readthedocs.org/en/latest/

I had to do the following to get setup:

. +pkg install py27-sphinx+ . +pip install --user
sphinxcontrib-napoleon+ . +sphinx-apidoc -f -F -o sphinx-source/
hypatia+ . edit +config.py+ and add +'sphinxcontrib.napoleon'+
and +'sphinx.ext.autosummary'+ to the +extensions+ list . +sphinx-build
sphinx-source api+

Then I added a +.nojekyll+ to the root of the +gh-pages+ branch, so I
can use directories beginning with an underscore (which sphinx needs).

What you'll wanna do is use the +make-sphinx.sh+ script whenever you
update the docstrings.
