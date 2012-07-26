#Professors
A Professors repository built on top of [PopIt](https://github.com/mysociety/popit).


## How to install Professors

…

## Requirements
This webapp fully relies on [PopIt](https://github.com/mysociety/popit) as the provider fo the data. 

## Run the tests

	python setup.py nosetests
	
This command will also print the test coverage. 

## Some notes for developers

There is a libs folder in `/profs/` which contains a git submodule with a reference to the python wrapper for the popit API. The original repository can be found on [github](https://github.com/domoritz/popit-python).