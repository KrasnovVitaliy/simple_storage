import logging
import simple_storage.libs.encryption as encryption
from simple_storage.libs.storage import Storage
from fastapi import HTTPException, status
import simple_storage.libs.config_loader as config_loader
import uuid

logger = logging.getLogger(__name__)
config = config_loader.Config()
storage = Storage()


def __upload_preconfigured_access_tokens():
    logger.info("Upload preconfigured token")
    for t in config.get(config_loader.PRECONFIGURED_ACCESS_TOKENS):
        __save_token_in_db(t)


def __save_token_in_db(token: str):
    logger.info(f"Save token: {token} to DB")
    if config.get(config_loader.USE_ENCRYPTION):
        logger.info("Encrypt token")
        enc_token = encryption.encrypt(token, config.get(config_loader.ENCRYPTION_KEY).encode())
        storage.put_access_token(enc_token.decode())
    else:
        storage.put_access_token(token)


async def create_token(is_authenticated: bool) -> str:
    logger.info("Create new access token")
    token = uuid.uuid1().hex
    logger.info(f"Generated token: {token}")
    __save_token_in_db(token=token)
    return token


async def delete_token(token: str, is_authenticated: bool) -> None:
    logger.info(f"Delete access token: {token}")
    if config.get(config_loader.USE_ENCRYPTION):
        logger.info("Encrypt token")
        enc_token = encryption.encrypt(token, config.get(config_loader.ENCRYPTION_KEY).encode())
        storage.delete_access_token(enc_token)
    else:
        storage.delete_access_token(token)


__upload_preconfigured_access_tokens()
