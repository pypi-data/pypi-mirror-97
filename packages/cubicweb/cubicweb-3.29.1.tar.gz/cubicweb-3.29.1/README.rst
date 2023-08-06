CubicWeb semantic web framework
===============================

CubicWeb is a entities / relations based knowledge management system
developped at Logilab.

This package contains:

- a repository server
- a RQL command line client to the repository
- an adaptative modpython interface to the server
- a bunch of other management tools

|pipeline status| |pypi downloads| |pypi license| |docker pulls|

.. |pipeline status| image:: https://forge.extranet.logilab.fr/cubicweb/cubicweb/badges/branch/default/pipeline.svg
   :target: https://forge.extranet.logilab.fr/cubicweb/cubicweb/-/commits/branch/default
.. |pypi downloads| image:: https://img.shields.io/pypi/dm/cubicweb
   :alt: PyPI - Downloads
   :target: https://pypi.org/project/cubicweb/
.. |pypi license| image:: https://img.shields.io/pypi/l/cubicweb
   :alt: PyPI - License
   :target: https://pypi.org/project/cubicweb/
.. |docker pulls| image:: https://img.shields.io/docker/pulls/logilab/cubicweb
   :alt: Docker Pulls
   :target: https://hub.docker.com/r/logilab/cubicweb

Intranet links to internal Sonarqube :  https://sonarqube.k.intra.logilab.fr/dashboard?id=cubicweb-cubicweb

|Quality Gate Status| |Reliability Rating| |Security Rating| |Technical Debt| |Vulnerabilities|

.. |Quality Gate Status| image:: https://sonarqube.k.intra.logilab.fr/api/project_badges/measure?project=cubicweb-cubicweb&metric=alert_status
   :target: https://sonarqube.k.intra.logilab.fr/dashboard?id=cubicweb-cubicweb
.. |Reliability Rating| image:: https://sonarqube.k.intra.logilab.fr/api/project_badges/measure?project=cubicweb-cubicweb&metric=reliability_rating
   :target: https://sonarqube.k.intra.logilab.fr/dashboard?id=cubicweb-cubicweb
.. |Security Rating| image:: https://sonarqube.k.intra.logilab.fr/api/project_badges/measure?project=cubicweb-cubicweb&metric=security_rating
   :target: https://sonarqube.k.intra.logilab.fr/dashboard?id=cubicweb-cubicweb
.. |Technical Debt| image:: https://sonarqube.k.intra.logilab.fr/api/project_badges/measure?project=cubicweb-cubicweb&metric=sqale_index
   :target: https://sonarqube.k.intra.logilab.fr/dashboard?id=cubicweb-cubicweb
.. |Vulnerabilities| image:: https://sonarqube.k.intra.logilab.fr/api/project_badges/measure?project=cubicweb-cubicweb&metric=vulnerabilities
   :target: https://sonarqube.k.intra.logilab.fr/dashboard?id=cubicweb-cubicweb

Install
-------

More details at https://cubicweb.readthedocs.io/en/latest/book/admin/setup

Getting started
---------------

Execute::

 python3 -m venv venv
 source venv/bin/activate
 pip install 'cubicweb[pyramid]' cubicweb-blog
 cubicweb-ctl create blog myblog
 # read how to create your ~/etc/cubicweb.d/myblog/pyramid.ini file here:
 # https://cubicweb.readthedocs.io/en/latest/book/pyramid/settings/#pyramid-settings-file
 # then start your instance:
 cubicweb-ctl pyramid -D myblog
 sensible-browser http://localhost:8080/

Details at https://cubicweb.readthedocs.io/en/latest/tutorials/base/blog-in-five-minutes

You can also look at the latest builds on Logilab's forge:
https://forge.extranet.logilab.fr/cubicweb/cubicweb

Test
----

Simply run the `tox` command in the root folder of this repository:

    tox

How to install tox: https://tox.readthedocs.io/en/latest/install.html

Documentation
-------------

Look in the doc/ subdirectory or read https://cubicweb.readthedocs.io/en/latest/


CubicWeb includes the Entypo pictograms by Daniel Bruce — http://www.entypo.com

Contributing
------------

Patches can be submitted on Logilab's forge (https://forge.extranet.logilab.fr).
If you do not have a write-access, please contact us at contact@logilab.fr

If you have any questions you can also come on Logilab's public XMPP room using
a XMPP client: public@conference.jabber.logilab.org

--

Alternatively, patches could be submitted by email at the
cubicweb-devel@lists.cubicweb.org mailing list in order to get reviewed by
project integrators or any community member.  The simplest way of send patches
is to use the ``hg email`` command available through the *patchbomb* extension
of Mercurial. Preferably, patches should be *in the message body* of emails.
When submitting a revised version of a patch series, a prefix indicating the
iteration number ``<n>`` of the series should be added to email subject
prefixes; this can be achieved by specifying a ``--flag v<n>`` option to ``hg
email`` command. If needed you can also use the --in-reply-to option.

Examples:

    hg email --to cubicweb-devel@lists.cubicweb.org --intro -r <start>::<end>
    hg email --flag V2 --to cubicweb-devel@lists.cubicweb.org -r <start>::<end>

Mailing list: https://lists.cubicweb.org/mailman/listinfo/cubicweb-devel
Patchbomb extension: https://www.mercurial-scm.org/wiki/PatchbombExtension
Good practice on sending email patches: https://www.mercurial-scm.org/wiki/ContributingChanges#Emailing_patches
