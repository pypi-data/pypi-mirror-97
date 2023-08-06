.. _contribution:

============
Contribution
============

Any kind of contribution (not limit to what is mentioned in this document) is
appreciated in order to make Nitrate better. Anyone who is interested in
Nitrate is able to contribute in various areas, whatever you are good at
coding, organizing or writing documentation, or a normal user to share ideas
and suggestions.


Testing
-------

Testing, testing, and testing. Testing is the most important way to ensure the
high quality of Nitrate to serve users. There are many areas to test, such as
the features, documentation, translation, and any other aspects you may focus
on. Once you find a problem, please search it in the `Issues`_ to see whether
it has been reported by other people. If no one reported there yet, you are
encouraged to file one with detailed and descriptive description.


Documentation
-------------

Documentation has been provided along with the source code within ``docs/``
directory. You could go through the documentation to find any potential
problems, e.g. typos or out-of-date content.

Documentation is built using Sphinx. All content must be written in
reStructuredText format. You can use any your favourite text editor to edit it.

To generate the HTML content and review::

    (cd docs; make html)

To test the changes::

    tox -e docs


Translation
-----------

We are willing to make our contribution to benefit the world. To translate
Nitrate to usual languages in the universe is a critical task. Your
contribution is so important to everyone. Picking up and editing the PO file of
specific language you are skilled in.

Before making pull request, make sure your translation have no grammatical
mistakes and semantic errors. Feel free the look into to translation issues by
consulting language experts around you when you hesitant.


Package
-------

RPM packages are available from Fedora Copr already. You are encouraged to
package for other package system, e.g. the DEB package or others.


Development
-----------

If you are interested in writing code or would like to learn how to develop a
website using Python and Django, contributing patch to fix specific problems
would be a good way. Please don't be hesitated to contact maintainer to discuss
your ideas and implement it.

For easily to get started, you may want to go through `easyfix issues`_ or
`help-wanted issues`_ and take one.

.. _easyfix issues: https://github.com/Nitrate/Nitrate/issues?q=is%3Aissue+is%3Aopen+label%3Aeasyfix
.. _help-wanted issues: https://github.com/Nitrate/Nitrate/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22

Get the code
~~~~~~~~~~~~

Code is hosted in Github. Following the guide in Github to fork and clone
code to your local machine. For example, I have forked Nitrate, then I can
clone it::

    git clone git@github.com:tkdchen/Nitrate.git


Setup development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow up the steps in either of the following documents to setup your own
development environment. The steps should be doable on other platforms.

.. toctree::
   :maxdepth: 1

   set_dev_env
   set_dev_env_with_vagrant


Confirm the problem
~~~~~~~~~~~~~~~~~~~

Before making any changes to code, you should search in `Issues`_ to see
whether someone else is working on the issue you want to fix. This is helpful
to avoid duplicated work of you. Also, this is a good chance to communicate
with the owner to share what you are thinking of.

If no issue there, create one and give detailed information as much as
possible. If there is already an issue filed, and nobody takes it, then you can
take it if you would like to fix it.


Hack, hack and hack
~~~~~~~~~~~~~~~~~~~

Happy hacking.

#. create local branch based on the ``develop`` branch.

#. hacking, hacking and hacking. Please do remember to write unit tests.

#. test, test and test ...

   ::

       tox

#. when your code is ready, commit your changes and sign-off the commit, push to
   your cloned repository, and make a pull request to ``develop`` branch.


Commit message format
~~~~~~~~~~~~~~~~~~~~~

A good commit message will help us to understand your contribution as easily
and correctly as possible. Your commit message should follow this format::

    summary to describe what this commit does (#XXX)

    Arbitrary text to describe why you commit these code in detail

Generally, the length of summary line should be limited within range 70-75. The
remaining text should be wrapped at 79 character.


Sign-off commit
~~~~~~~~~~~~~~~

Every commit must be signed off with your name and email address. This can be
done by specifying option ``-s`` to ``git commit``, for example::

    git commit -s -m "commit message"

The sign-off means you have read and agree to `Developer Certificate of Origin`_.
Nitrate uses version 1.1::

    Developer Certificate of Origin
    Version 1.1

    Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
    1 Letterman Drive
    Suite D4700
    San Francisco, CA, 94129

    Everyone is permitted to copy and distribute verbatim copies of this
    license document, but changing it is not allowed.


    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.

.. _Developer Certificate of Origin: https://developercertificate.org/

Review & Acceptance
~~~~~~~~~~~~~~~~~~~

Till now, congratulations, you have contributed to Nitrate. Please be patient
to wait for our review.

.. _Issues: https://github.com/Nitrate/Nitrate/issues
