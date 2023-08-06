Microsoft Azure Machine Learning Tracking server plugin for Python
==================================================================

The azureml-mlflow package contains the integration code of AzureML with MLflow.
MLflow (https://mlflow.org/) is an open-source platform for tracking machine learning experiments and managing models.
You can use MLflow logging APIs with Azure Machine Learning so that metrics and artifacts are logged to your Azure
machine learning workspace.

Usage
-----

Within an `AzureML Workspace <https://docs.microsoft.com/python/api/overview/azure/ml/intro?view=azure-ml-py>`_,
add the code below to use MLflow.

.. code-block:: python

   import mlflow
   from azureml.core import Workspace

   workspace = Workspace.from_config()

   mlflow.set_tracking_uri(workspace.get_mlflow_tracking_uri())

More examples can be found at https://aka.ms/azureml-mlflow-examples.




