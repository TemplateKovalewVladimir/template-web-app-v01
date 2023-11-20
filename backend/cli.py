import logging
import sys
from datetime import datetime
from os import path

import click
from sh import (  # pylint: disable=no-name-in-module
    ErrorReturnCode,
    gunzip,
    gzip,
    pg_dump,
    psql,
)

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logging.getLogger("sh.command").setLevel(logging.ERROR)

logger = logging.getLogger("CLI")


@click.group()
def cli():
    pass


@cli.command("dump", help="Дамп БД")
def dump_db():
    try:
        logger.info("Старт дамп БД")
        date_time = datetime.now().strftime("%Y.%m.%d_%H_%M")
        filename = f"{date_time}.sql.gz"
        path_file_backup = path.join(settings.BACKUP_FOLDER, filename)
        logger.info("Дамп в файл: %s", path_file_backup)

        database_uri = settings.database_url
        # sh: pg_dump '--dbname=[uri]' | gzip > file.slq.gz
        gzip(
            _in=pg_dump("-c", f"--dbname={database_uri}", _piped=True),
            _out=path_file_backup,
        )

        logger.info("Успешно")
    except ErrorReturnCode as e:
        logger.error("Ошибка (ErrorReturnCode): %s", str(e))
        sys.exit(1)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Ошибка (Exception): %s", str(e))
        sys.exit(1)


@cli.command("restore", help="Восстановление БД из бэкапа")
@click.option("--name_backup", help="Имя файла бэкапа 2023.11.16_03_00.sql.gz")
def restore_db(name_backup):
    logger.info('Старт "восстановление БД из бэкапа"')
    path_file_backup = path.join(settings.BACKUP_FOLDER, name_backup)
    logger.info("Восстановление из файла: %s", path_file_backup)
    if path.isfile(path_file_backup):
        try:
            database_uri = settings.database_url

            logger.info("Очистка БД перед восстановлением")
            psql(
                "--command=DROP SCHEMA public cascade;CREATE SCHEMA public;",
                f"--dbname={database_uri}",
            )

            logger.info("Восстановление")
            psql(
                gunzip("-c", path_file_backup, _piped=True),
                f"--dbname={database_uri}",
            )

            logger.info("Успешно")
        except ErrorReturnCode as e:
            logger.error("Ошибка (ErrorReturnCode): %s", str(e))
            sys.exit(1)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Ошибка (Exception): %s", str(e))
            sys.exit(1)

    else:
        logger.error("Ошибка: %s не существует", path_file_backup)
        sys.exit(1)


if __name__ == "__main__":
    cli()
