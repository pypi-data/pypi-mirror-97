Cinder Library
==============

.. image:: https://img.shields.io/pypi/v/cinderlib.svg
   :target: https://pypi.python.org/pypi/cinderlib

.. image:: https://img.shields.io/pypi/pyversions/cinderlib.svg
   :target: https://pypi.python.org/pypi/cinderlib

.. image:: https://img.shields.io/:license-apache-blue.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0


Introduction
------------

The Cinder Library, also known as cinderlib, is a Python library that leverages
the Cinder project to provide an object oriented abstraction around Cinder's
storage drivers to allow their usage directly without running any of the Cinder
services or surrounding services, such as KeyStone, MySQL or RabbitMQ.

* Free software: Apache Software License 2.0
* Documentation: https://docs.openstack.org/cinderlib/latest/

The library is intended for developers who only need the basic CRUD
functionality of the drivers and don't care for all the additional features
Cinder provides such as quotas, replication, multi-tenancy, migrations,
retyping, scheduling, backups, authorization, authentication, REST API, etc.

The library was originally created as an external project, so it didn't have
the broad range of backend testing Cinder does, and only a limited number of
drivers were validated at the time.  Drivers should work out of the box, and
we'll keep a list of drivers that have added the cinderlib functional tests to
the driver gates confirming they work and ensuring they will keep working.

Features
--------

* Use a Cinder driver without running a DBMS, Message broker, or Cinder
  service.
* Using multiple simultaneous drivers on the same application.
* Basic operations support:

  - Create volume
  - Delete volume
  - Extend volume
  - Clone volume
  - Create snapshot
  - Delete snapshot
  - Create volume from snapshot
  - Connect volume
  - Disconnect volume
  - Local attach
  - Local detach
  - Validate connector
  - Extra Specs for specific backend functionality.
  - Backend QoS
  - Multi-pool support

* Metadata persistence plugins:

  - Stateless: Caller stores JSON serialization.
  - Database: Metadata is stored in a database: MySQL, PostgreSQL, SQLite...
  - Custom plugin: Caller provides module to store Metadata and cinderlib calls
    it when necessary.

Demo
----

.. raw:: html

  <a href="https://asciinema.org/a/TcTR7Lu7jI0pEsd9ThEn01l7n?autoplay=1"
  target="_blank"><img
  src="https://asciinema.org/a/TcTR7Lu7jI0pEsd9ThEn01l7n.png"/></a>

.. _GIGO: https://en.wikipedia.org/wiki/Garbage_in,_garbage_out
.. _official project documentation: https://readthedocs.org/projects/cinderlib/badge/?version=latest
.. _OpenStack's Cinder volume driver configuration documentation: https://docs.openstack.org/cinder/latest/configuration/block-storage/volume-drivers.html
