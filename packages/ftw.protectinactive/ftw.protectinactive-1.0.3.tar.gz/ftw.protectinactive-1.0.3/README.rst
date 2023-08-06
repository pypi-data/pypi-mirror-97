ftw.protectinactive
===================

``ftw.protectinactive`` protects inactive content from unauthorized access.

Plone provides fields to set publication and expiration dates.
If the publication date is in the future or the expiration date is in the past the content is inactive.
This inactive state determines if the content should appear on the site or not.

**The problem is that this check is only performed on the catalog.**

It works for listings and all other instances where catalog queries are used.
But it does not protect the content from beeing accessed directly via the url.
An unauthorized user is able to access the content whether it is inactive or not.
This behaviour is highly unintuitive and is often met with incomprehension.

``ftw.protectinactive`` was created to protect inactive content and provide the expected behaviour.
It performs the check for inactive content in a ``IPubAfterTraversal`` hook.
If the content is inactive and the user has no permission to see it, ``ftw.protectinactive``
raises an exception.


Features
--------
* check if content is inactive
* supports Archetypes and Dexterity content
* respects ``Access inactive portal content`` and ``Access future portal content`` permissions (on site root)
* configurable exception type


Installation
------------
- Add ``ftw.protectinactive`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.protectinactive

- Install the generic import profile.


Configuration
-------------

The exception raised by ``ftw.protectinactive`` can be configured in the plone registry.
It will raise an ``Unauthorized`` exception by default. This, however, confirms the
existence of the content, which is a potential unwanted information disclosure.
To avoid this the exception can be changed to a ``NotFound`` exception in the registry.

In addition you can also completaly disable the hook via the plone registry.


Installation local development-environment
------------------------------------------

.. code:: bash

    $ git clone git@github.com:4teamwork/ftw.protectinactive.git
    $ cd ftw.protectinactive
    $ ln -s development.cfg buildout.cfg
    $ python2.7 bootstrap.py
    $ bin/buildout
    $ bin/test



Compatibility
-------------

Runs with `Plone <http://www.plone.org/>`_ `4.3.9`.


Links
-----

- Github: https://github.com/4teamwork/ftw.protectinactive
- Issues: https://github.com/4teamwork/ftw.protectinactive/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.protectinactive

Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.protectinactive`` is licensed under GNU General Public License, version 2.
