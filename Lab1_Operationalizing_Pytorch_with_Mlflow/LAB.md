# Operationalizing Pytorch Model with Mlflow

## Context

PyTorch is one of the main machine learning library used for applications such as computer vision and 
natural language processing. It is catching up with TensorFlow accelerating the path from research 
prototyping to production deployment. Recently, Pytorch community announced a number of technical 
contributions to enable end-to-end support for MLflow usage with PyTorch. 

MLflow is an open source platform to manage the ML lifecycle, including experimentation, reproducibility, deployment, and a central model registry. One may interact with its components by command line interface
or well-known APIs (Python, R, Java and REST), building a workflow capable of handling development and
production activies.

In this lab, [MLOps community](https://mlops.community/) wants to test them and provide feasible ways 
to build end-to-end model lifecycles of Pytorch assets using Mlflow.

## Repo Organization

Following list describes the most relevant folders in which this lab is organized. Some folders in 
this repo are self-explanatory (like [_imgs_](imgs/)) and therefore aren'r mentioned in the list.

* [src](src/): Main source code folder. It comprises all software produced during this lab. _Src_ 
itself is organized into subfolders according to which components it belongs to;
* [docs](docs/): Binary documentation, drawings and reports produced during this lab;
* [infra](infra/): Infrastrucuture creation and definition code.

## Proposal
### Design Overview

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
**Control or Operator Machine** is the VM used by Configuration Manager or Operation Engineer to follow up
the process or issue commands to the nodes in the pipeline. This process may run through many different 
perimeters, however this solution comprises _Development_ and _Production_ stages only.

### Architectural Components and Decisions

In this section, we record the (most relevant) design decisions, components selection and the rationale around them.

| # | Subject | Description | Affected Items | Solution | Rationale |
|---|---------|-------------|----------------|----------|-----------|
| 1 | Computing | ML needs processing power as well as GPU. Our architecure relies on distributed elements, thus needing a reasonable number of physical or virtual machines (some with GPU-power) | All Nodes and Machines | GCP Compute Service | It provides $ 300,00 of (enough) free services and we can also spin some gpu-powered machines |
| 2 | Durable Data Storage | Every serious solution needs to store durable data | Tracking Server | SQLite | Simplest and Fastest Relational Database tha fits our needs |
| 3 | Large and Binary Data Storage | ML projects eventually need to store models and extra large files, This type of data doesn't fit in RDBMS | Tracking Server<br>Artifact Store | Google Cloud Storage | Same as #1 |
| 4 | Shipment and Deployment | There are many deployable assets as well as acessory tools that need specific environment and SO libraries to run. Just installing them into a machine isn't a viable option | Training and Serving Nodes<br>Artifact Storage | Docker | It's the _de facto_ pattern for shipping and deploying things |
| 5 | Lib Management | Python has a powerful but sometimes confusing and conflicting library ecossystem. Our components may depend on conflicting libs and that will lead to problems in Production | All Nodes and Machines | Conda<br>Pip | Both are heavily used by Python community. They also work quite well with isolation provided by Docker images |
| 6 | Remote Access | Sometimes we need to issue remote commands or operate a remote machine | All Nodes and Machines | SSH | Hey... It's SSH. There's no need to rationale :-P |
| 7 | CI/CD & Workflow Management | We need to seamlessly integrate and deploy ML stuff. We also have to coordinate the process between nodes | All Items | Github Actions | We're using GitHub, it's heavily used by community and comes off-the-shelf |
| 8 | Scheduler | Some activities are triggered by clock | All Nodes and Machines | CRON | We are using Unix like machines |
| 9 | Project Metadata | We need to describe the ML Component, its structure and how it should run | Source Code Repository<br>Training and Serving Nodes | MLFlow Project Definition | Non-functional Requirement we must adhere |
| 10 | ML Lifecycle Management | We must track the ML Process | All Nodes and Machines | MLFlow |  Non-functional Requirement we must adhere |
| 11 | ML Framework | We are building ML Components. Therefore, we must use a ML framework to train our models | Training and Serving Nodes | Pytorch | Non-functional Requirement we must adhere |


### Workflow

[DevOps](https://en.wikipedia.org/wiki/DevOps) tools heavily relies on actions triggered by changes
and other events regarding application's source code. MLOps goes beyond this assumption since any reasonable
solution must deal with assets like ML Models, datasets, features, etc. Therefore, a simples ML 
application may turn into a complex workflow in order to ensure the best model runs in Production. The
following workflow depicts a common development scenario where a production web application uses a ML
Model to provide business value. 

![Solution Workflow](imgs/workflow.svg)

The first stage is Development Workflow. It concerns the continuous integration of new ML code and Dataset 
changes into a Development Server. Here follows the steps:

1. Commited code or changes in the Dataset fires a training execution. These events trigger Github actions;
 
 1. ML pipeline starts. we are considering that previous data activities (Extraction, Validation and
 Preparation) were already executed. In _Training Node_, a Github runner checks out the ML Component 
 and \ or updates the training dataset. The ML Component itself describes its structure (_MLFlow project file_) 
 and how it should be run (_Dockerfile_). The runner starts the training process using MLFlow CLI 
 features: ```mlflow run```. The training happens in a GPU-powered Docker container configured with the 
 _Tracking Server_ (```MLFLOW_TRACKING_URI```) . At the end of this step, there's a new trained model 
 with its respective metadata;
 
 1. The Training Node sends the trained model, its extra files, and metadata to the Model Registry
 and Tracking Server respectively. In fact, these assets are physically stored in an external Cloud
 Storage Service acessible from Internet;
 
 1. The development workflow ends by deploying the trained model in a _Serving Node_. The runner creates
 and registers a new Docker image capable running the model. The runner starts a container  
 (```docker run```) which downloads and packs the trained model through command 
 ```mlflow create deployment```.

In our scenario, the decision to go to Production must be triggered through MLFlow Tracking Server. Here
are the steps:

5. The Operator promotes the model to Production in the Tracking Server. It triggers a new _Deploy_ event.
The Production Flow Orchestrator _(?)_ pulls the docker image and runs it configuring the environment
variables properly;

5. The Monitor node tracks how model is performing and periodically starts a local training pipeline
with Production data in order to avoid _Model Erosion_;

5. The model realizes the model doesn't perform anymore (_Model Erosion_) or there are significant 
changes in the data (changes in the data semantic, new relevant fields, etc). It start a feedback
loop triggering a full model rebuild process.

## References
TBD