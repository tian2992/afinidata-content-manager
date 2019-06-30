# Afinidata Content Manager


[![Build Status](https://travis-ci.com/afinidata2019/afinidata-content-manager.svg?branch=master)](https://travis-ci.com/afinidata2019/afinidata-content-manager)
[![Documentation Status](https://readthedocs.org/projects/afinidata-content-manager/badge/?version=latest)](https://afinidata-content-manager.readthedocs.io/en/latest/?badge=latest)


## Overview


The Afinidata Content Manager handles the content for Afinidata. This features Users who create Posts, which can be Reviewed by Special Users.

The Content Manager is built using Python3, Django, and a small set of extra dependencies. The directory layout is quite standard for Django projects. The main apps are: **content_manager**, **messenger_users**, **posts** and **upload**.


## Installation / Running

1. Install Python 3.6 or more as suggested by your OS.
2. Install dependencies, a suggested way is to use virtualenv: ```virtualenv -p python3 venv/; source venv/bin/activate; pip install -r requirements.txt```
3. Run ```manage.py``` and build and execute db migrations. MySQL is used in production, while a stub config exists for running using SQLite. 
4. Ready to go! Use the WSGI app exposed as content_manager

## Contributing

The Afinidata Content Manager is a Free Software Product created by Afinidata and available under the AGPL Licence. 

To contribute, read our [Code of Conduct](CODE_OF_CONDUCT.md), our [Docs at Read The Docs](https://afinidata-content-manager.readthedocs.io/en/latest/) and code away.
Create a pull request and contact us in order to merge your suggested changes. We suggest the use of git flow in order to provide a better contributing experience.

