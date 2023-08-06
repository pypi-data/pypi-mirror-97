===========
Description
===========

Mayan EDMS app to migrate files from external sources.


=======
License
=======

This project is open sourced under the `Apache 2.0 License`_.

.. _`Apache 2.0 License`: https://gitlab.com/mayan-edms/importer/raw/master/LICENSE


============
Installation
============

#. Install from PyPI in the same ``virtualenv`` where you installed Mayan EDMS.
   Or if using the Docker image, pass ``mayan-importer`` to the
   ``MAYAN_PIP_INSTALLS`` environment variable.

   .. code-block:: console

       pip install mayan-importer

#. Add ``importer`` to the ``COMMON_EXTRA_APPS`` setting, either as an
   environment variable, from a Python settings modules, or from the UI
   via the ``config.yaml`` configuration file.

   Python settings module example:

   .. code-block:: console

       INSTALLED_APPS += (
           'importer',
       )

#. Run the migrations for the app (not required for the Docker image):

   .. code-block:: console

       mayan-edms.py migrate


============
Requirements
============

- **dropbox** - Dropbox Python SDK (https://www.dropbox.com/developers/documentation/python#install)
- **Mayan EDMS version 3.4**


=====
Usage
=====

- Create an app in Dropbox's App Console (https://www.dropbox.com/developers/apps/).
- Generate an Access Token with no expiration.
- Create a credential instance in the Mayan EDMS Importer app and enter the Access Token.
- Create an Import Setup that will filter the files to fetch from Dropbox.
- Click the "Populate" button and check that the item count is correct.
- Click the "Process" button to start the import process.
