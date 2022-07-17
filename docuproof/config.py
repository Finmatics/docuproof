from docuproof.app import application

DEFAULT_CONFIG = {
    "DATABASE_URL": "sqlite:///sqlite.db",
    "BATCH_TIME": 1,
    "BATCH_TIME_UNIT": "hours",
}

application.config.update(DEFAULT_CONFIG)
config = application.config
