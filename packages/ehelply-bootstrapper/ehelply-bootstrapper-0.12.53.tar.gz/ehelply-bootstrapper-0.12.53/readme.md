# Bootstrapper
Bootstrapper is used to quickly establish generic microservices.

## What does it do

Bootstrapper takes care of several tedious and menial microservice tasks including:
* Handles the loading process of microservices including a hand off back to the business logic
* Abstracts away common integrations (referred to as drivers) such as MySQL, AWS (boto3), MongoDB, Redis, Sentry, SocketIO, FastAPI
    * Each driver has varying levels of abstraction and completeness
* Abstracts away environments. The bootstrapper treats the loading process differently depending on whether the service is in prod, qa, test, or dev
* Exposes an API to the developer for creating integrations between microservices which are part of the same application. These are referred to as integrations.
* Loads default and developer defined configuration files depending on the environment the service is in.
* Exposes a singleton state manager to the microservice
* Contains a small library of useful models, functions, and code for development of microservices.
* Installs many common PyPi dependencies which are used across most microservices

## What is isn't
* Bootstrapper is not a microservice template, however, it can and should be used within microservice templates.
    * Due to proprietary nature of microservice templates, eHelply has chosen not to offer one publicly at the moment. This decision may change in the future.
* Perfect. There are many drivers which could be added or improved. Feel free to submit PRs to add new drivers.

## Is this stable and production ready?
The quick and dirty answer is probably. eHelply is using Bootstrapper to power all of our microservices. For this reason, this project continues to mature and evolve over time. At this point, we would consider it to be reasonably stable. By no means is it feature complete, and it is possible for breaking changes to be introduced in the near or long term, but we don't expect the Bootstrapper to fail in production scenarios at this time.

In addition to this information, eHelply plans to launch microservices into production in late 2020 or early 2021, so we would expect this project to be officially production ready at that point in time.

## Contributing
The goal of Bootstrapper is to be a generic microservice bootstrapper. This means that it should provide value to any company, organization, or individual that wishes to utilize it. For this reason, all contributions must also be generic and refrain from opinionated choices.

Since eHelply is sponsoring the development of this project, it is unlikely that breaking changes would be accepted and merged in from third parties. However, we always welcome new (non-breaking) additions and bug fixes. And, who knows, if your breaking change is necessary, it will be merged in.

## Commands
* Run tests: `pytest`
* Run tests with coverage report: `pytest --cov=ehelply_bootstrapper`
