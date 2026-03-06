.PHONY: test lint clean run dashboard

test:
	pytest tests/

lint:
	black src tests
	flake8 src tests
	mypy src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/

run:
	training-bot --help

dashboard:
	streamlit run src/training_bot/interfaces/dashboard.py
