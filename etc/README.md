Additional Scripts
==================

This directory contains ancillary scripts and tools which are not
necessary for using or developing Hypatia, but which may be useful to
people working on the project.


Git Hooks
---------

General information about Git hooks: http://githooks.com/

### pre-push

The `pre-push` script in this directory will automatically run
`test.sh`, i.e. the Hypatia test suite, and will reject any attempt to
run `git push` when the test suite fails.  See the note at the very
top of the script for notes on how to install and activate it.

Even with the script in place, it is always possible to push without
triggering the hook by running `git push --no-verify ...`, for
situations where it’s considered acceptable to push something that is
breaking the test suite.
