mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

super:
	python3 manage.py createsuperuser

message:
	python manage.py makemessages -l zh
	python manage.py makemessages -l uz
	python manage.py makemessages -l ru
	python manage.py makemessages -l en
compile:
	python manage.py compilemessages --ignore=.venv