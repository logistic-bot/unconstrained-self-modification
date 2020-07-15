default: test style
test:
	@pytest --ff --nf tests --durations=2 --testmon -x --suppress-no-test-exit-code

style:
	@mypy src main.py --strict --show-error-context --pretty
	@flake8 --max-line-length=100 --max-doc-length=100 --show-source --statistics --jobs 4 --doctests src main.py --ignore=E261,W503
	@./venv/bin/pylint src main.py -f colorized -j 1 --ignore-patterns='test*' --disable=C0330,R0913,W1116,R0903,W0511,R0914,E1111,R0801
coverage:
	@pytest --cov=src --ff --nf tests --durations=2 --cov-report term-missing:skip-covered -x
run:
	./main.py
	stty sane
install:
	python -m pip install -r requirements.txt
init: install test
