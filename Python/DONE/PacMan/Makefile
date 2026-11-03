PYTHON ?= $(shell which python3 2>/dev/null || which python 2>/dev/null || echo python3)
CONFIG ?= config.json

.PHONY: all install run debug clean fclean re lint lint-strict package

all: run

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) pac-man.py $(CONFIG)

debug:
	$(PYTHON) -m pdb pac-man.py $(CONFIG)

lint:
	@status=0; \
	echo "Running flake8"; \
	$(PYTHON) -m flake8 . || status=1; \
	echo "Running mypy"; \
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs || status=1; \
	exit $$status

lint-strict:
	@status=0; \
	$(PYTHON) -m flake8 . || status=1; \
	$(PYTHON) -m mypy . --strict || status=1; \
	exit $$status

package:
	$(PYTHON) -m pip install pyinstaller
	@test -f "$(CONFIG)" || { echo "Missing config: $(CONFIG)"; exit 1; }
	$(PYTHON) -m PyInstaller --clean --noconfirm PacMan.spec
	$(PYTHON) -c "from shutil import copy2; copy2('$(CONFIG)', 'dist/config.json'); copy2('README.md', 'dist/README.md')"
	@printf '%s\n' '#!/bin/sh' 'cd "$$(dirname "$$0")" || exit 1' 'exec ./PacMan config.json' > dist/run-pacman.sh
	@chmod +x dist/run-pacman.sh

clean:
	rm -rf __pycache__ .mypy_cache
	rm -rf core/__pycache__ core/states/__pycache__ core/ai/__pycache__
	rm -rf ui/__pycache__
	rm -rf build dist
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

fclean: clean
	rm -rf build dist PacMan PacMan.exe
	rm -rf .venv venv env

re: fclean all
