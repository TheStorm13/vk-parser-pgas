.PHONY: mypy flake8 pylint lint pyinstaller

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
lint:
	black mypy flake8 pylint

# Build the application
build_linux:
	pyinstaller --onefile --windowed src/main.py --add-data "data/description_app.md:data"

build_windows:
	pyinstaller --onefile --windowed src/main.py --add-data "data;data"