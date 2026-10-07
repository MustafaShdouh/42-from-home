PYTHON = python3
CONFIG = config.txt

.PHONY: install run debug clean lint

install:
	$(PYTHON) -m pip install -e ".[dev]"

run:
	$(PYTHON) a_maze_ing.py $(CONFIG) || True

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	rm -rf __pycache__ app/__pycache__ maze_generator/__pycache__
	rm -rf .mypy_cache build dist *.egg-info

lint:
	-flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs
