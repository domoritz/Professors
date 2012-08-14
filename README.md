#Professors
A Professors repository built on top of [PopIt](https://github.com/mysociety/popit).

## Status

This project in a very early stage of development. 

## How to install Professors

…

## Demo

Try the live demo on [http://gsoc12-profs.devtation.de/](http://gsoc12-profs.devtation.de/).

## Requirements
This webapp fully relies on [PopIt](https://github.com/mysociety/popit) as the provider fo the data. This means you need to have a running PopIt installation or use a provided installation. 

Apart from that you'll need the following software on your server (for deployment) or computer (for development).

* Python
* (optional) Virtualenv with virtualenvwrapper
* 

## Installation

Make sure you have instaled the required software. 

* `git clone git://github.com/domoritz/Professors.git`
* `cd Professors`
* `git submodule init`
* `git submodule update`
* At this point you might want to create a virtual environment (developers should prefer virtualenvwrapper)
  * `virtualenv --distribute venv`
  * `source venv/bin/activate`
* `python setup.py develop`

Contiue here for production setup

* `pip install gunicorn`
* Change the `production.ini` file to your needs.
* `pserve --daemon production.ini`

Contiue here for development setup

* Change the `development.ini` file to your needs.
* `pserve --reload development.ini`

## Recommended Schema

Make sure that you use the right case. 

* __name__: The professors name.
* __summary__: A short summary of the professors field of study and other things that do not match the attributes below.
* __other.University__: The university where the professor works.
* __other.Study__: The professor's field of study.
* __other."Place of Birth"__: The place of birth will be linked to the place.
* __other."Nationality"__: The place of birth will be linked to the place.
* __links__: An array of link items consisting of a comment and an url
* __contact_details__: An array of contact details consisting of a kind and a value

## Notes for developers

### Submodule

There is a libs folder in `/profs/` which contains a git submodule with a reference to the python wrapper for the popit API. The original repository can be found on [github](https://github.com/domoritz/popit-python). So don't forget to init and update the submodule.

## Run the tests

	python setup.py nosetests
	
This command will also print the test coverage. 