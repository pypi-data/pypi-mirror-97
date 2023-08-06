.. See LICENSE for details

.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://gitlab.com/incoresemi/utils/repomanager/issues.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://gitlab.com/incoresemi/utils/repomanager/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `repomanager` for local development.

1. Fork the `repomanager` repo on GitLab.
2. Clone your fork locally::

    $ git clone https://gitlab.com/incoresemi/utils/repomanager.git

3. Create an issue and WIP merge request that creates a working branch fro you

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. When you're done making changes, check that your changes pass pytest
   tests, including testing other Python versions with tox::

    $ cd tests
    $ pytest test_repomanager.py -v 


5. Commit your changes and push your branch to GitLab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a merge request through the GitLab website.

Merge Request Guidelines
------------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should include tests.
2. If the merge request adds functionality, the docs should be updated. 
3. The merge request should work for Python 3.6, 3.7 and 3.8, and for PyPy. 
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::


    $ python -m unittest tests.test_repomanager

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed.
Then run::

$ bumpversion --config-file setup.cfg patch # possible: major / minor / patch
$ git push origin name-of-your-branch

