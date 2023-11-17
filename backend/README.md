
alembic init -t async alembic
alembic revision --autogenerate -m 'First test'
alembic upgrade head

# Заимствовал отсюда
https://github.com/tiangolo/full-stack-fastapi-postgresql