==========
Commands
==========

.. contents::
   :local:


**hop-client** provides a command line interface for various tasks:

* :code:`hop configure`: Authentication utilities
* :code:`hop publish`: Publish messages such as GCN circulars and notices
* :code:`hop subscribe`: Listen to messages such as GCN circulars and notices
* :code:`hop version`: Show version dependencies of :code:`hop-client`

:code:`hop configure`
~~~~~~~~~~~~~~~~~~~~~~

This command allows a user to handle auth-based configuration.

.. program-output:: hop configure --help
   :nostderr:

:code:`hop publish`
~~~~~~~~~~~~~~~~~~~~~~

This command allows a user to publish various structured and unstructured messages, including:

* `RFC 822 formatted GCN circular <https://gcn.gsfc.nasa.gov/gcn3_circulars.html>`_
* An XML formatted `GCN/VOEvent notice <https://gcn.gsfc.nasa.gov/tech_describe.html>`_
* Unstructured messages such as JSON-serializable data.

Structured messages such as GCN circulars and VOEvents are published as JSON-formatted text.

Unstructured messages may be piped to this command to be published. This mode of operation
requires JSON input with individual messages separated by newlines, and the Blob format
(`-f BLOB`) to be selected. 

.. program-output:: hop publish --help
   :nostderr:


:code:`hop subscribe`
~~~~~~~~~~~~~~~~~~~~~~

This command allows a user to subscribe to messages and print them to stdout.

.. program-output:: hop subscribe --help
   :nostderr:

:code:`hop version`
~~~~~~~~~~~~~~~~~~~~~~

This command prints all the versions of the dependencies

.. program-output:: hop version --help
   :nostderr:
