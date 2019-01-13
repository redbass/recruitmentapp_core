Recruitment-App-Core
====================

Setup
-----
First of all create a python virtual env and then create the a link, called 
`.virtualenv` in the root of the project. Example:

```bash
ln -s ~/.virtualenvs/APP .virtualenv
```

Then setup `Git` hooks

```bash
make setup_git_hooks 
```

Development Environment
-----------------------

To run locally the app the following environment variable is required:

```bash
APP_ENV=local
```

2. To run the local database:
```bash
docker-compose up
```
