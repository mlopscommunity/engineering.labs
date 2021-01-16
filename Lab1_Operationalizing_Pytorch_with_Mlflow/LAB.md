# Operationalizing Pytorch Model with Mlflow

## Context

PyTorch is one of the main machine learning library used for applications such as computer vision and 
natural language processing. It is catching up with TensorFlow accelerating the path from research 
prototyping to production deployment. Recently, Pytorch community announced a number of technical 
contributions to enable end-to-end support for MLflow usage with PyTorch. 

MLflow is an open source platform to manage the ML lifecycle, including experimentation, reproducibility, deployment, and a central model registry. One may interact with its components by command line interface
or well-known APIs (Python, R, Java and REST), building a workflow capable of handling development and
production activies.

In this lab, MLOps community wants to test them and provide feasible ways to build end-to-end model 
lifecycles of Pytorch assets using Mlflow.

## Repo Organization

Following list describes the most relevant folders in which this lab is organized. Some folders in 
this repo are self-explanatory (like [_imgs_](imgs/)) and therefore aren'r mentioned in the list.

* [src](src/): Main source code folder. It comprises all software produced during this lab. _Src_ 
itself is organized into subfolders according to which components it belongs to;
* [docs](docs/): Binary documentation, drawings and reports produced during this lab;
* [infra](infra/): Infrastrucuture creation and definition code.

## Proposal

Our team intend to orchestrate common unix management toolkits (shell commands, ssh, etc), MLFlow
CLI and MLFlow components to build a seamless end-to-end pipeline. It should comprehend 
[Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) (CI), 
[Continuous Delivery](https://en.wikipedia.org/wiki/Continuous_delivery) (CD) and 
[Continuous Traning](https://cloud.google.com/solutions/machine-learning/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) (CT). 
The following figure depicts the proposed architecture.

![Proposed architecture](imgs/arch.svg)

**Nodes** are bare-metal or virtual machines that host a part of the pipeline process. **ML components** 
are ML-based code that should be trained, tested and deployed by end-to-end pipeline.They must be 
packaged as [MLFlow projects](https://mlflow.org/docs/latest/projects.html). **Training nodes**
host the training process which runs in **Training containers**, running dockerized images built 
with MLFlow and necessary libs to train ML components. Each ML component defines its needs, that is, 
libs and external dependencies. To ensure traceability, provenance and model configuration management, 
one may track hyperparameters, training steps, test results, extra data and the model itself into 
_MLFlow Tracking Server_ hosted in the **Tracking Node**. All these items, metadata and trained models, 
are stored in external resources: RDBMS and Cloud Storage Services. Trained models are embedded into 
dockerized **Serving Instances**, containers running [Torchserve](https://pytorch.org/serve/) providing 
web access to the models. Serving instances are hosted by **Serving Nodes**.

In order to provide feedback loop, a **Monitor Node** checks the status and performance meters, issuing 
new training cycles or a full rebuild process. Some structures traverses through Development and Production perimeters. Serving, Training and Monitor nodes are key elements that communicate between those zones.

### Scenarios

TBD

## References
TBD