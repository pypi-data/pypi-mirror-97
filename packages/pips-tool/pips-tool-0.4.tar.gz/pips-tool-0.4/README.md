# Pips 
## pip wrapper for new requirements handling

https://www.kennethreitz.org/essays/a-better-pip-workflow

`pips install flask`

1. run pip install flask
2. add flask to requirements.txt
3. run pip freeze > requirements.lock

`pips uninstall flask`

1. run pipdeptree
2. run pip uninstall for all dependencies
3. remove flask from requirements.txt
4. run pip freeze > requirements.lock

`pips install`
1. run pip install -r requirements.lock

`pips update`
1. run pip install -r requirements.txt
2. run pip freeze > requirements.lock

## Setup Project
pip install requirements-dev.txt

## Build and Deployment
python setup.py sdist bdist_wheel
twine upload dist/*

