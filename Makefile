start:
	python manage.py runserver 0.0.0.0:4243

shell:
	python manage.py shell

mm:
	python manage.py migrate

flake:
	flake8

patch:
	npm version patch
	git push --tags origin master

test:
	python manage.py test -v 2

loc:
	python manage.py makemessages --ignore build -l en -l fr && python manage.py compilemessages

deploy:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*
