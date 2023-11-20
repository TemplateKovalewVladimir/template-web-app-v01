# Run

### Файлы переменных окружений

Эти файлы должны быть настроены соответственно вашему окружению и требованиям проекта. Они помогают обеспечивать гибкость и безопасность, так как чувствительные данные, такие как пароли и секретные ключи, могут быть изолированы от кода.

---

Файл содержит переменные окружения, необходимые для работы базы данных PostgreSQL.

**.env-db**
```
POSTGRES_USER=template_app
POSTGRES_PASSWORD=template_app
POSTGRES_DB=template_app
```

---

Файл содержит данные для входа в pgAdmin, графический интерфейс для управления базами данных PostgreSQL.

**.env-pgadmin**
```
PGADMIN_DEFAULT_EMAIL=admin@test.ru
PGADMIN_DEFAULT_PASSWORD=PassW0rd
```

---

Файл предназначен для конфигурации backend-части приложения.

**.env-backend** (дополнительные переменные см в backend/app/core/config.py)
```
APP_ENVIRONMENT=PRODUCTION

HTTP_ALLOW_ORIGINS=http://test.ru

DB_HOST=db
DB_PORT=5432
DB_USER=template_app
DB_PASS=template_app
DB_NAME=template_app
```

---

Файл предназначен для конфигурации frontend-части веб-приложения.

**frontend/.env**
```
APP_BASE_API_URL=http://api.test.ru
```