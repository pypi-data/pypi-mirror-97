# coding: utf-8
import logging
from pathlib import Path
from importlib import import_module

from fastapi import FastAPI

from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from sqlalchemy import create_engine
import pprint

from modularapi.settings import get_setting
from modularapi.db import db

logger = logging.getLogger()


if get_setting().LOG_TO_STDOUT:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s",
    )


def get_app():
    app = FastAPI()

    modules = tuple(Path().glob("modules/*"))
    if modules:
        for path in modules:
            if path.is_dir():
                # "modules/<module_name>/" -> "modules.<module_name>"
                module_path = ".".join(path.parts)
                logger.info(f"loading module [{module_path}]")

                try:
                    module = import_module(".".join([module_path, "main"]))
                    try:
                        getattr(module, "on_load")(app)
                        # load "db.py" if it exists and it's a file
                        if (path / "db.py").is_file():
                            import_module(".".join([module_path, "db"]))

                    except AttributeError:
                        logger.error(
                            f"Could not load module {module_path} ! missing entrypoint !"
                        )

                except ModuleNotFoundError:
                    logger.error(f"Could not load module {module_path} missing main.py!")
    else:
        logger.warning("There is no modules folder !")

    # ensure the database is up to date
    engine = create_engine(get_setting().PG_DNS)
    mc = MigrationContext.configure(engine.connect())
    diff = compare_metadata(mc, db)
    if diff:
        logger.critical(
            f"The database is not up to date ! use the Modular cli to update the database schema {pprint.pformat(diff)}"
        )
        exit(1)

    db.init_app(app)
    return app
