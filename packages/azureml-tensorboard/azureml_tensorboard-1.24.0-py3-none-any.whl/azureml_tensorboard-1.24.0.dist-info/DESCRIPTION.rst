Microsoft Azure Machine Learning TensorBoard API for Python
===========================================================

This package has been tested with Python 3.6 and 3.7.
=====================================================

The SDK is released with backwards compatibility guarantees.

The Azure Machine Learning *azureml-tensorboard* package combines the AzureML SDK with TensorBoard visualization.

It can be used to:

- Export run history to TensorBoard logs directory. You can run TensorBoard against the directory to view metrics.
- Launch TensorBoard from run history. TensorFlow logs can be written to a specified logs directory and then automatically loaded in real-time from Azure Blob Storage.

*****************
Setup
*****************

Follow these `instructions <https://docs.microsoft.com/azure/machine-learning/how-to-configure-environment#local>`_ to install the Azure ML SDK on your local machine, create an Azure ML workspace, and set up your notebook environment, which is required for the next step.
Once you have set up your environment, install the AzureML TensorBoard package:

.. code-block:: python

   pip install azureml-tensorboard



