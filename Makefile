makemigrations:
	cd src && alembic revision --autogenerate -m "$(MIGRATION_NAME)"

migrate:
	cd src && alembic upgrade head

