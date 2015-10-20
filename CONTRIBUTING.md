# Contributing to Hypatia

Read this *before* you make a pull request. _Hopefully_ everything a Python dev would want to know about contributing to Hypatia, e.g., style, guidelines, requirements, testing.

Before you continue, read:

  * `LICENSE`
  * `README.md`: Everything the user needs to know
  * `CODE-OF-CONDUCT.md`: Be compassionate and respectful

## Social

Hypatia has strives to be a safe place for all. Please read the `CODE-OF-CONDUCT.md`.

### Contact and Communication

Please communicate with our lovely team:

  * IRC: Freenode #hypatia
  * Twitter: @hypatia_engine
  * Email: hypatia.engine@gmail.com

Lily, project mommy:

  * Email: lillian.lynn.lemmer@gmail.com
  * Twitter: @LilyLemmer

### Letter to Women

Hey you!

It's Lily, the project mommy. I just wanna say that this project is especially for you as a developer; you come first. I'm a woman who's openly lesbian and trans, I hope that reassures you that Hypatia has a welcoming, open, and safe culture.

I'd like to offer you free one-on-one sessions, where I'll teach you software engineering! I'll teach you until you're making quality contributions to Hypatia! My hope is to help women develop a portfolio for a career in software engineering.

I'd also like to invite you to the official, invite-only, Hypatia developer chat. We use a service called Slack to chat; you don't need to download anything. Send an email to lillian.lynn.lemmer@gmail.com requesting an invite!

Let me know if you need anything.

Warm Regards,
Lillian Lynn Lemmer

## Quick Info

  * Branch from, pull request to develop
  * Use descriptive branch names
  * We're strict about documentation (docstrings, commit messages, comments)
  * Use test.sh to test before you commit!
  * You'll probably want to pip install --user requirements/testing.txt
  * This repo's etc/ directory contains additional/optional tools to assist contributors

## Git

Branch from `develop`, pull requests against `develop`.

  * Try to avoid large/huge commits
  * Try to avoid imlementing multiple concepts in one commit
  * A branch should only implement what its name describes, e.g., "add-display-settings-and-tools"

### Git Flow

The general git flow of the project follows [A Successful git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/). Please branch from the `develop` branch.

### Git Messages

Commit messages **must** begin with single line summarizing the patch, followed by a blank line, and then the rest of the message.  The blank line is mandatory because without the output of many Git commands become messy to read, e.g. `git shortlog`.

Commit messages must be as explanatory as possible.  Any developer should be able to understand *why* a change was made just by reading the commit message for that change.  This means that commit messages that cotain only `"Fixes a bug"` or `"Updates to sprite code"` are unacceptable.  When writing a commit message ask yourself, *"Why is this change necessary?"*  Your message must answer that question.  [Here is an example commit](https://github.com/hypatia-engine/hypatia/commit/fdbfc5f3e62eb4f5d04ca23f5705e4e97a5e89bf) which answers that question.

If your commit is a bug-fix then try to find the commit which introduced the bug and reference that in your message.  The preferred format is `first eight digits of the SHA-1 (The Commit's First Line)`.  [Here is an example](https://github.com/hypatia-engine/hypatia/commit/b52c3345ae8e312017c2a1cf21793fdbc63b2493) demonstrating how to refer to previous commits.  Note well that GitHub automatically creates links to commits you reference in this way.

If your commit relates to a GitHub issue then reference that issue in the message by writing `GitHub-Issue: #NNN` where `NNN` is the issue number.  [Here is an example](https://github.com/hypatia-engine/hypatia/commit/04d64aa1c76d1958d934c9d64e72a6928ab6466f) of such references.  Again, note well that GitHub turns these references into links.  The threads for those issues will also receive a link back to the commit.

## General Documentation Rules

  * Always explain what everything is and how it works, to the best of your understanding!
  * Amazing docstrings are a must!
  * Always use gender neutral pronouns in all documentation, including code comments, e.g., they, them, their.
 
## Code Style

  * [PEP8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

### Docstrings

You are required to write _amazing docstrings_. The docstring convention used is [Google Style Docstrings](http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html).

All of the following must have *thorough docstrings*:

  * Modules
  * Functions
  * Classes
  * Methods (yes, even __init__)

A *thorough docstring*:

  * Has more than a brief description
  * Justifies the existence of whatever its describing
  * A module-level docstring with a section for constants, where the module's constants are thoroughly explained.
  * If for a function or method, describes possible return value, and describes arguments with more than a brief description. Try including doctest examples in your argument elaboration.
  * Has a doctest

The following code snippet exemplifies everything described in this section (_Docstrings_):

```python
example
```

Use four spaces to indent within docstrings:

```python
def dummy(dumb):
    """One-line description.

    Elaborative description.

    Args:
        dumb (int): A dumb number. Remember we
            said we use four spaces to indent?

    """

    pass
```

### Doctests

Doctests are *required* in docstrings for the following, as to provide a proof-of-concept:

  * Classes
  * Methods
  * Functions

Here are some relevant resources on doctests:

  * [Official Python guide on doctests](https://docs.python.org/2/library/doctest.html)
  * [A wonderful, more thorough guide on doctests](http://pymotw.com/2/doctest/)

Our doctests are verified by Travis CI. You can avoid embarassment by running the `test.sh` supplied in the repo to test your changes.

### Whitespace

Whitespace is important. You use whitespace to make stuff stand out. You use whitespace to set relation. See: [The Law of Proximity](http://study.com/academy/lesson/law-of-proximity-examples-lesson-quiz.html).

The following effect major events to logic, and thus require whitespace (blank line) above and below:

  * `return`
  * `break`
  * `continue`
  * `yield`
  * `raise`


```python
if x == 2:

    continue

elif x == 3:

    return None

elif x == 4:
    x += 1
elif x == 6:

    break

elif x == 10:

    raise Exception("Whoops!")
```

It's keen to add a blank line below if/else/elif blocks which exceed one line, as to separate it from the next else/elif block. For example:

```python
if user_input == EAT_TACO:
    player.eat(taco)
    player.satisfied = True

elif user_input == PLAY_GAME:
    player.play_game(castlevania)
    player.satisfied = True

elif user_input == CHOOSE_TO_BE_SATISFIED:
    player.satisfied = True
else:
    player.satisfied = False
```

Always add a blank line above and below the terminating quote for the docstring. For example:

```python
def dummy():
    """Fake description of function.

    """

    pass


def another_dummy():
    """A fake description of this other
    fake function.

    Only designed for you to understand
    code style guidelines.

    """

    pass
```

The following must have a blank line above:

  * `except`: when the respective try block exceeds one line
  * `else`, `elif`: when the previous `else`, `elif`, or `if` block exceeded one line

Example of what must have a blank line above:

```python
try:
    d = {}
    d['lol no such key']

except KeyError:
    print("what a horrible example")

if x == 3:
    x += 5
    y -= 3
    a = x - y

elif x == 5:
    x -= 4
elif x == 6:
    x += 8
    y -= 9

else:
    x = 5
```

## tests

* Hypatia uses pytest for automated testing. To set up your Hypatia repository for testing, run the following:

  ```
  cd /path/to/hypatia-repository
  pip install -r requirements/testing.txt
  ```

  You can now run the tests by running `test.sh`.

* Reference `tests/test_tiles.py` for an example on how to structure your tests. See [official pytest usage examples](http://pytest.org/latest/example) for more generic samples. 
  * Avoid creating classes in your tests.
  * The following try/except block is needed:

    ```
    try:
        os.chdir('demo')
    except OSError:
        pass
    ```

## File and Directory Notes

### distrib.sh

This script is used for distributing A NEW RELEASE to PyPi.

### demo/

This directory hosts `game.py`, which is a demo of Hypatia. It also hosts the demo's editable resources.

### docs/

Sphinx docs source. Use the custom `make-sphinx.sh` to build the sphinx documentation from the docstrings.

The *built* Sphinx docs are published to the official Hypatia website, at the following URI: http://lillian-lemmer.github.io/hypatia/api

### etc/

*OPTIONAL* configurations/configuration scripts, helper files, etc. Worth checking out! Has a `objecttypes.xml` for Tiled editor!

### hypatia/

The actual Python package source.

### media/

Media, namely pictures, officially related to Hypatia as a project, e.g., logos, icons.

### requirements/

The requirements files installable by `pip`. Notes on the files:

|Requirements File|You'd want to use if...                        |
|-----------------|-----------------------------------------------|
|base.txt         |ALWAYS!                                        |
|python2.txt      |You use Python 2.x!                            |
|testing.txt      |You want to test and/or contribute to the code!|
|travis.txt       |NEVER                                          |

### tests/

Unit tests for py.test and Travis Continuous Integration. These files are for assuring Hypatia's API remains consistent, reproducible, functional, etc. They are in part what determines build success/fail according to Travis CI. See our `build` badge.

See also: `test.sh`, it's the official script to run when testing any changes.
