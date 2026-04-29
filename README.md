# ai-workspace
Personal AI monorepo for blogs, apps, experiments, and tools, powered by Pants. An all-in-one AI workspace for personal projects, blogs, experiments, and developer tools.
Contains AI/ML code utilising NLP, Machine Learning, related technologies

# General Development And Release Rules

These rules apply to this repository and day-to-day development:

- `live` is the production release branch.
- `qa` must contain all code planned for release.
- Feature branches are cut from `qa`.
- Pull requests from feature branches merge into `qa`.
- At release time, `qa` is merged into `live`.
- Rebase should be done before opening/updating a PR.
- No merge commits are allowed (keep history linear).

## Branch Flow

```text
live  <-  qa  <-  feature/<name>
```

## Git Command Examples

### 1) Start a feature branch from `qa`

```sh
git checkout qa
git pull --ff-only origin qa
git checkout -b feature/my-change
```

### 2) Keep your feature branch updated with `qa` using rebase

```sh
git fetch origin
git rebase origin/qa
```

If conflicts happen:

```sh
git add <resolved-files>
git rebase --continue
```

### 3) Push your rebased branch and create PR to `qa`

First push of a new feature branch:

```sh
git push -u origin feature/my-change
```

If you already pushed the branch and then rebased it:

```sh
git push --force-with-lease origin feature/my-change
```

Open a PR:

- Base branch: `qa`
- Compare branch: `feature/my-change`

### 4) Release process: promote `qa` to `live`

```text
all the release procedures would be handles by one person
```

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


