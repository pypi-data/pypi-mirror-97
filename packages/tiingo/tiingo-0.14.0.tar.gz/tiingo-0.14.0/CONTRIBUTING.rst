.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/hydrosquall/tiingo-python/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Tiingo Python could always use more documentation, whether as part of the
official Tiingo Python docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/hydrosquall/tiingo-python/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `tiingo` for local development.

1. Fork the `tiingo` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/tiingo-python.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv tiingo-python
    $ cd tiingo-python/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 tiingo tests
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.6, and 3.7. These will be checked for you when you open your PR via Github Action checks.

Release Procedure
-----------------------

See RELEASE.rst .

Tips
----

To run a subset of tests::

$ py.test tests.test_tiingo


To regenerate fixture remove it from tests/fixtures and run tests again::

    $ rm tests/fixtures/NAME.yaml
    $ py.test

In order for py.test to run, you will have had to create an environment variable containing a valid tiingo API key so that the test runner can make a valid api call.  One way to do that is to::

    $ export TIINGO_API_KEY='...insert api key here...'

However, now this api key will become embedded in the test fixture file that is created per the prior procedure.  In order to remove this api key from the new test fixtures, run the following from the top level directory::

    $ ./tools/api_key_tool.py
