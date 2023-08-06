Microsoft Azure Machine Learning Interpret API for Python
=============================================================

This package has been tested with Python 3.6 and 3.7.
=====================================================

The SDK is released with backwards compatibility guarantees.

Machine learning (ML) interpret package is used to interpret black box ML models.

The azureml-interpret package interfaces with explainers to allow users to upload and download explanations from Azure.

The explainers come from the interpret-community package.

 * The TabularExplainer can be used to give local and global feature importances
 * The best explainer is automatically chosen for the user based on the model
 * Local feature importances are for each evaluation row
 * Global feature importances summarize the most importance features at the model-level
 * The API supports both dense (numpy or pandas) and sparse (scipy) datasets
 * For more advanced users, individual explainers can be used
 * The KernelExplainer and MimicExplainer are for BlackBox models
 * The MimicExplainer is faster but less accurate than the KernelExplainer
 * The TreeExplainer is for tree-based models
 * The DeepExplainer is for DNN tensorflow or pytorch models

*****************
Setup
*****************

Follow these `instructions <https://docs.microsoft.com/azure/machine-learning/how-to-configure-environment#local>`_ to install the Azure ML SDK on your local machine, create an Azure ML workspace, and set up your notebook environment, which is required for the next step.
Once you have set up your environment, install the AzureML Interpret package:

.. code-block:: python

   pip install azureml-interpret



