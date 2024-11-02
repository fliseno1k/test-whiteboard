start:
	python src/main.py
	
install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

lint:
	flake8 src/

format:
	black src/
