start: FORCE
	env/bin/python -m snake.main

deps: env FORCE
	env/bin/pip install -r requirements.txt

env:
	virtualenv -p python3 env/

FORCE:
