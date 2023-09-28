# HackYeah Project Backend README

Welcome to the backend repository for our "HackYeah" project! This backend is built using Python, Django, and Django Rest Framework.


# Prerequisites

## Native way with virtualenv
- [Python3.10](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)

## Docker way
- [Docker](https://docs.docker.com/engine/install/)  
- [Docker Compose](https://docs.docker.com/compose/install/)

# Local Development

## Native way with virtualenv

First create postgresql database:

```sql
create user hackyeah with createdb;
alter user hackyeah password 'hackyeah';
create database hackyeah owner hackyeah;
```
Now you can setup virtualenv and django:
```bash
virtualenv venv
source venv/bin/activate
pip install pip-tools
make bootstrap
```

## Docker way

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
