db-setup:
	make init && make migrate && make upgrade

init:
	flask db init

migrate:
	flask db migrate

upgrade:
	flask db upgrade

test:
	export PYTHONPATH=$(pwd) && pytest -v

seed:
	export DB_USERNAME=postgres && export DB_PASSWORD=postgres python ./scripts/seed-db.py
