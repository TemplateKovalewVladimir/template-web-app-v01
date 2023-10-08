
alembic init -t async alembic
alembic revision --autogenerate -m 'First test'
alembic upgrade head