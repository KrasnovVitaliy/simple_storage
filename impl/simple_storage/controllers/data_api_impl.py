import logging
from fastapi import HTTPException, status

import simple_storage.libs.encryption as encryption
from simple_storage.libs.storage import Storage
import simple_storage.libs.config_loader as config_loader
from simple_storage.libs.tokens import token_is_valid

logger = logging.getLogger(__name__)
config = config_loader.Config()
storage = Storage()


async def get_item_by_key(key: str, token: str):
    if config.get(config_loader.USE_AUTH) and not token_is_valid(token):
        logger.warning(f"Incorrect token: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    item = storage.get_data(key)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    if config.get(config_loader.USE_ENCRYPTION):
        return encryption.decrypt(item, config.get(config_loader.ENCRYPTION_KEY).encode())

    return item


async def create_item(key: str, data: str, token: str) -> None:
    if config.get(config_loader.USE_AUTH) and not token_is_valid(token):
        logger.warning(f"Incorrect token: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if config.get(config_loader.USE_ENCRYPTION):
        data = encryption.encrypt(data, config.get(config_loader.ENCRYPTION_KEY).encode())
        storage.put_data(key, data)
    else:
        storage.put_data(key, data.encode())


async def delete_item(key: str, token: str) -> None:
    if config.get(config_loader.USE_AUTH) and not token_is_valid(token):
        logger.warning(f"Incorrect token: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    storage.delete_data(key)
