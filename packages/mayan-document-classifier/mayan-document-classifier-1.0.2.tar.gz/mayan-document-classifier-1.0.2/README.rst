===========
Description
===========

Mayan EDMS machine learning document classifier.


=======
License
=======

This project is open sourced under the `Apache 2.0 License`_.

.. _`Apache 2.0 License`: https://gitlab.com/mayan-edms/dropbox/raw/master/LICENSE


============
Installation
============

#. Install from PyPI in the same ``virtualenv`` where you installed Mayan EDMS.
   Or if using the Docker image, pass ``mayan-document-classifier`` to the
   ``MAYAN_PIP_INSTALLS`` environment variable.

   .. code-block:: console

       pip install mayan-document-classifier

#. Add ``document_classifier`` to the ``COMMON_EXTRA_APPS`` setting, either as an
   environment variable, from a Python settings modules, or from the UI
   via the ``config.yaml`` configuration file.

   Python settings module example:

   .. code-block:: console

       INSTALLED_APPS += (
           'document_classifer',
       )

#. Run the migrations for the app (not required for the Docker image):

   .. code-block:: console

       mayan-edms.py migrate


============
Requirements
============

- **Mayan EDMS version 3.4**
