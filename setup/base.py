import locale
import os
import sys
from configparser import ConfigParser
from pathlib import Path

from exceptions import SectionNotFoundError

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

BASE_DIR = Path(__file__).parent.parent


def load_config(filename: Path, section: str):
    parser = ConfigParser()
    parser.read(str(filename))

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        msg = f"Section {section} not found in the {filename} file"
        raise SectionNotFoundError(msg)

    return config


CONFIG_PATH = BASE_DIR / ".envs"

APP_TYPE = os.getenv("APP_TYPE", "dev")

if APP_TYPE not in ["dev", "production"]:
    msg = "APP_TYPE must be  set to 'dev' or 'production'"
    raise ValueError(msg)

if APP_TYPE == "dev":
    CONFIG_PATH = CONFIG_PATH / ".local"
    postgres_config = load_config(CONFIG_PATH / "local.ini", "postgresql")
    mail_config = load_config(CONFIG_PATH / "local.ini", "mail")
if APP_TYPE == "production":
    CONFIG_PATH = CONFIG_PATH / ".production"
    postgres_config = load_config(CONFIG_PATH / "production.ini", "postgresql")
    mail_config = load_config(CONFIG_PATH / "production.ini", "mail")

# postgres database
POSTGRES_HOST = postgres_config["host"]
POSTGRES_PORT = postgres_config["port"]
POSTGRES_DB = postgres_config["database"]
POSTGRES_USER = postgres_config["user"]
POSTGRES_PASSWORD = postgres_config["password"]

# references for brazilian ids
CEP_LEN = 8
CNPJ_LEN = 14
CPF_LEN = 11

# mail
MAIL_HOST = mail_config["host"]
MAIL_PORT = mail_config["port"]
MAIL_USER = mail_config["user"]
MAIL_PWD = mail_config["password"]
MAIL_FROM = mail_config["from"]
MAIL_TIMEOUT = mail_config["timeout"]
MAIL_USE_TLS = bool(mail_config["use_tls"])
MAIL_FAIL_SILENTLY = bool(mail_config["fail_silently"])
EMAIL_SSL_KEYFILE = mail_config.get("ssl_keyfile", None)
EMAIL_SSL_CERTFILE = mail_config.get("ssl_certfile", None)
MAIL_ADMIN = mail_config["admin"]


sys.path.append(str(Path(__file__).parent.parent / "config"))
