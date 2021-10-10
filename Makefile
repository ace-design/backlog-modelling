# Makefile to support the artefact

export PIPENV_VERBOSITY=-1

init:
	pipenv install

scenario_1:
	pipenv run ./main.py scenario_1

scenario_2:
	pipenv run ./main.py scenario_2

scenario_3:
	pipenv run ./main.py scenario_3

scenario_4:
	pipenv run ./main.py scenario_4

scenario_5:
	pipenv run ./main.py scenario_5

load:
	pipenv shell

python:
	pipenv run python3