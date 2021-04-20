# Lab #2 : Feature store for ML

## Scenario

Production data systems aren’t new. However, operazionalizing ML models to production introduces new requirements for our data tools. A new kind of ML-specific data infrastructure is needed. The Feature Store. 
A feature store is an ML-specific data system that:

* Runs data pipelines that transform raw data into feature values
* Stores and manages the feature data itself, and
* Serves feature data consistently for training and inference purposes

## Content

Imagine to be a member of the Data Science team for an e-commerce company. The company invested a lot to improve its internal systems. And now it is able to collect real time data containing actual transactions. 

Business requires 

* a daily report on product and customers categories insights (in batch)
* a way to classify customer based on the content of its basket as soon as its first visit (in real time)

During the meeting with CTO and all parts involved in the project, team realizes that you need to build

* a system that, given the same inputs, computes daily features and serves them online at the same time. It should have an identical set up if you were to bring an offline model to an online production environment.

That’s where the **Feature Store** comes into play. 

Teams can decide to build their own feature store service or adopting an existing solution (ex. Feast)

We provide data and model based on [e-commerce Kaggle Data](https://www.kaggle.com/carrie1/ecommerce-data)

## Teams

Teams involved in this scenario are:

- TEAM 1: Ish, xin, Korri Jones, wwymak
- TEAM 2: Godwin Ekainu, Artem Glazkov, Artem Yushkovsky, PierPaolo Ippolito
- TEAM 3: arshdeep, jjmachan, rajatgupta, Andrew Poulton
- TEAM 4: Rohan, Sai Krishna, Aahan, nghiaht
- TEAM 5: Oleg Polivin, Sascha Heyer, Semendiak, Chris Smith-Clarke
- TEAM 6: AlmogBaku, Alexey Naiden, Boyan, Paulo Maia
- TEAM 7: Gabriela Melo, Sath, jeff katz, Mark Peters
- TEAM 8: Sandeep, Ruthvik Chowdary, Shi Shu, Sai Thatigotla

## Final Deliverables

LOADING...


## Contributing
If you want to join the initiative, please join the MLOps Community on [Slack](https://mlops-community.slack.com/join/shared_invite)

## License
[MIT](https://choosealicense.com/licenses/mit/)