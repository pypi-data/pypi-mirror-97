AzureML Contrib Notebook package
================================

This is a preview feature for AzureML Python SDK that allows you to submit jupyter notebook as a run.

To get started with AzureML Python SDK follow these `instructions <https://docs.microsoft.com/en-us/python/api/overview/azure/ml/intro>`_ 

Please install azureml-contrib-notebook to submit jupyter notebook as a run:

.. code-block:: python

  pip install azureml-contrib-notebook

For local run please install papermill package, along with nbconvert:

.. code-block:: python

  pip install "papermill<2" "nbconvert<6"

To enable metrics update from local run in user managed environment please install nteract-scrapbook package:

.. code-block:: python

  pip install nteract-scrapbook




