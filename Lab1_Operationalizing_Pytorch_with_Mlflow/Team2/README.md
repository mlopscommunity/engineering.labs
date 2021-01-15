
## Approach
The base project is [this](https://colab.research.google.com/github/jonad/pytorch_mlflow/blob/master/textclassification_with_mlflow.ipynb) notebook. 
In this notebook, a Pythorch NLP model is build to detect toxicity, obscene, insults in comments 
(so, given a sentence, or several sentences, how are they toxic, etc..).

The general plan is to build a ML-driven REST API service, 
which will accept some POST request with a text (sentence, or a couple of sentences),
use a model to make a prediction on the level of all of [those](https://colab.research.google.com/github/jonad/pytorch_mlflow/blob/master/textclassification_with_mlflow.ipynb#scrollTo=gkDa6Mo5d21P)
sentence properties and send it as a JSON response.


## Implementation structure
###### (might be changed)
- Load data: download (if needed) a [dataset](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data?select=train.csv), 
    preprocess (leave only some minor part of it, for instance, 5%, perform sentence tokenisation, 
    build embedding matrix, store all those artifacts for later use).

- MLFlow infra: to track experiments and models. 
Here we should have artifact store (bucket / local folder / FTP, whatever to store the models themselves) 
and backend store (to store runs metadata) - [docs](https://www.mlflow.org/docs/latest/tracking.html#storage).

- Train model: [build](https://colab.research.google.com/github/jonad/pytorch_mlflow/blob/master/textclassification_with_mlflow.ipynb#scrollTo=61NQKrIW9fTQ) 
a NN, let’s use hyper-parameters defined in notebook (hard-coded as for now). 
Train the model afterwards on the artifacts from previous step. 
During the training, we could replace [this](https://colab.research.google.com/github/jonad/pytorch_mlflow/blob/master/textclassification_with_mlflow.ipynb#scrollTo=MMmpqfeMV076) 
process tracking with the defined by [MLFlow](https://www.mlflow.org/docs/latest/tracking.html#pytorch-experimental).

- Deploy model: by using an MLFlow PythonAPI we could ask MLFlow server, 
which model is considered to be in “Production” and using this info we could load if from 
artefact store and use it to serve the API. Here we might develop some primitive Flask sever, 
or use MLFlow [facilities](https://www.mlflow.org/docs/latest/models.html#deploy-mlflow-models) to serve the model.