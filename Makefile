test:
	PYTHONPATH=. pytest tests

install-deps:
	pip install -r requirements.txt
