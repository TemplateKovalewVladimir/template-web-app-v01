# Kerberos

## Keytab

Данные команды связаны с настройкой Kerberos аутентификации, используя утилиты ktpass и setspn.

### Создание Keytab файла с помощью ktpass.exe:

```bash
ktpass.exe -princ HTTP/api.app.local.ru@LOCAL.RU -mapuser user-test -pass PassW0rd -ptype KRB5_NT_PRINCIPAL -out api_app_local_ru.keytab
```

В этой команде:

- ktpass.exe - инструмент командной строки для настройки ключевых ресурсов для использования с сервисами Kerberos.
- -princ указывает принципал Kerberos, который ассоциирован с учетной записью службы.
- -mapuser указывает локальный или доменный пользователь, который будет отображаться на данный принципал.
- -pass это пароль пользователя, который отображается на принципал.
- -ptype устанавливает тип принципала.
- -out определяет путь к файлу, в котором будет создан keytab файл для аутентификации.

### Вспомогательные команды

Регистрация SPN для учётной записи с помощью setspn:

```bash
setspn -A HTTP/api.app.local.ru user-test
```
В этой команде:

- setspn - инструмент командной строки для управления SPN (Service Principal Names).
- -A добавляет новый SPN для указанной учетной записи.
- HTTP/api.app.local.ru имя SPN, которое будет связано с пользователем user-test.

---

Проверка SPN в домене и учётной записи:

```bash
setspn -Q */api.app.local.ru
```

- -Q выполняет поиск в Active Directory для SPN, соответствующих предоставленному шаблону.

```bash
setspn -L user-test
```

- -L отображает все SPN, которые зарегистрированы для указанной учетной записи.

---

Удаление SPN из учётной записи:

```bash
setspn -d HTTP/api.app.local.ru user-test user-test
```

- -d удаляет указанный SPN из учетной записи user-test.


## /etc/krb5.conf

Пример файла конфигурации `/etc/krb5.conf`

```conf
[logging]
# default = FILE:/var/log/krb5libs.log
# kdc = FILE:/var/log/krb5kdc.log
# admin_server = FILE:/var/log/kadmind.log

[libdefaults]
 dns_lookup_realm = false
 ticket_lifetime = 24h
 renew_lifetime = 7d
 forwardable = true
 rdns = false
 default_realm = LOCAL.RU
# default_ccache_name = KEYRING:persistent:%{uid}

[realms]
 LOCAL.RU = {
  kdc = dc.local.ru
  admin_server = dc.local.ru
 }

[domain_realm]
 .local.ru = LOCAL.RU
 local.ru = LOCAL.RU
```

# Alembic

Alembic - это библиотека для миграций базы данных, которая является частью инструментария SQLAlchemy. Она позволяет управлять изменениями в схеме базы данных, вставлять и удалять таблицы, а также создавать и изменять столбцы и индексы без написания SQL кода напрямую. Использование Alembic особенно полезно в разработке приложений, в которых схема базы данных постоянно изменяется по мере разработки.

## Alembic Helper

Здесь описаны команды для работы с инструментом Alembic в асинхронном режиме (-t async) в контексте проекта, использующего FastAPI и базу данных PostgreSQL, на примере кода, взятого из репозитория по ссылке.

Инициализация Alembic:

```bash
alembic init -t async alembic
```

Эта команда создает новую структуру директории для миграций Alembic и генерирует файл конфигурации alembic.ini вместе с шаблоном окружения, который поддерживает асинхронные операции.

---

Создание новой ревизии:

```bash
alembic revision --autogenerate -m 'First test'
```

Команда revision с параметром --autogenerate создает новую ревизию (версию изменений схемы базы данных) и называет ее 'First Test'. Alembic автоматически обнаруживает изменения между текущей схемой базы данных и моделью данных в приложении и создает сценарий миграции для их применения.

---

Применение миграций:

```bash
alembic upgrade head
```

Эта команда применяет последнюю созданную ревизию (или ревизии, если их несколько) к базе данных. "head" указывает на последнее состояние схемы базы данных в рамках системы миграции.


# Заимствовал код

Код заимствован из проекта "full-stack-fastapi-postgresql", который является шаблоном для создания полноценных веб-приложений с использованием FastAPI и PostgreSQL. Репозиторий содержит примеры работы с Alembic для миграции схемы базы данных, что упрощает процесс разработки и обеспечивает более удобное управление изменениями в базе данных. https://github.com/tiangolo/full-stack-fastapi-postgresql