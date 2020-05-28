default: install test style
test:
	@pytest --ff --nf tests --durations=2 --testmon -x --suppress-no-test-exit-code

style:
	@mypy src main.py --strict --show-error-context --pretty
	@./venv/bin/pylint src main.py -f colorized -j 4 --ignore-patterns='test*'
	@flake8 --max-line-length=100 --max-doc-length=100 --show-source --statistics --jobs 4 --doctests src main.py
coverage:
	@pytest --cov=src --ff --nf tests --durations=2 --cov-report term-missing:skip-covered -x
run:
	./main.py
	stty sane
install:
	pip install -r requirements.txt
init: install test run
