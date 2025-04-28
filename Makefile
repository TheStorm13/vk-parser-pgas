.PHONY: mypy flake8 pylint lint

# formater black
black:
	black src/

# linter mypy
mypy:
	mypy src/

# linter flake8
flake8:
	flake8 src/

# linter pylint
pylint:
	pylint src/

# Run linter and formater
lint: black mypy flake8 pylint