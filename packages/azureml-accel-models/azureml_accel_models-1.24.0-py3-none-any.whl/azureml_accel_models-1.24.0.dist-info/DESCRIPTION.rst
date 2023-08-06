##########################################################################################
Microsoft Azure Machine Learning Hardware Accelerated Models Service
##########################################################################################

Easily create and train a model using various deep neural networks (DNNs) as a featurizer for deployment to Azure or a Data Box Edge device for ultra-low latency inference. These models are currently available:

- ResNet 50
- ResNet 152
- DenseNet-121
- VGG-16
- SSD-VGG

*****************
Setup
*****************
Follow these `instructions <https://docs.microsoft.com/en-us/azure/machine-learning/service/quickstart-create-workspace-with-python>`_ to install the Azure ML SDK on your local machine, create an Azure ML workspace, and set up your notebook environment, which is required for the next step.

Once you have set up your environment, install the Azure ML Accel Models SDK:

.. code-block:: python

  pip install azureml-accel-models

Note:``*`` This package requires you to install tensorflow >= 1.6. This can be done using:

.. code-block:: python

  pip install azureml-accel-models[cpu]

If your machine supports GPU, then you can leverage the tensorflow-gpu functionality using:

.. code-block:: python

  pip install azureml-accel-models[gpu]

********************
AzureML-Accel-Models
********************
- Create a featurizer using the Accelerated Models
- Convert tensorflow model to ONNX format using AccelOnnxConverter
- Create a container image with AccelContainerImage for deploying to either Azure or Data Box Edge
- Use the sample PredictionClient for inference on a Accelerated Model Host or create your own GRPC client

*********
Resources
*********
- `Read more about FPGAs <https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-accelerate-with-fpgas>`_.



