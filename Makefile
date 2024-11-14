mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

super:
	python3 manage.py createsuperuser