# ai-workspace
Personal AI monorepo for blogs, apps, experiments, and tools, powered by Pants. An all-in-one AI workspace for personal projects, blogs, experiments, and developer tools.
Contains AI/ML code utilising NLP, Machine Learning, related technologies

# Repo Structure

```sh
ai/
├── core
│   ├── loggers
│   ├── exception
│   │   ├── text_processing
│   │   └── tokenizer
│   │   └── triton
|   |   ....
│   └── utils
├── sentiment
│   ├── src
│   │   ├── app
│   │   │   └── service
│   │   │       ├── constants
│   │   │       ├── endpoints
│   │   │       ├── classification
│   │   │       ├── dto
│   │   │       └── utils
│   │   ├── cli
│   │   ├── data
│   │   └── notebooks
```

# AI/ML Ops

## Creating Docker image from pants

#### Steps

- copy .envrc.sample and set values

```sh
cp .envrc.sample .envrc
```
```shell package generation to dist folder
SCRS => pants package ai/sentiment:app-srcs@parametrize=cpu
DEPS => pants package ai/sentiment:app-deps@parametrize=cpu
```

- Create builder base image by running

```sh
sh ./ops/tools/build_bootstrap_cache_image.sh <MODULE_NAME>
```

This will build cache image for the first time

- Run `build_ai_image` with srcs and deps pex target and tag the image

```sh
sh ops/tools/build_ai_image.sh <MODULE_NAME> ai/sentiment:app-deps@parametrize=cpu   ai/sentiment:app-srcs@parametrize=cpu -t ai-sentiment:latest
```

This will create two images

- ai-<MODULE_NAME>:cache
- ai-sentiment:latest

# How to run app locally using docker

- Taking Sentiment classification app as example

# How to run in local?

- copy .envrc.sample and set values

```sh
cp .envrc.sample .envrc
``` 

- Start kafka

```shell
docker compose -f deploy/docker/kafka.docker-compose.yml up --build -d
open 'http://localhost:58080' # to open kafka ui
```

- Run below commands to start app

```shell
pants package ai/sentiment:app-deps@parametrize=cpu && \
pants package ai/sentiment:app-srcs@parametrize=cpu && \
docker-compose -f deploy/docker/sentiment.docker-compose.yml up --build
```


