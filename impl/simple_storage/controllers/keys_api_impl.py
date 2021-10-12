import logging
from typing import List
from fastapi import HTTPException, status
from simple_storage.libs.storage import Storage
from simple_storage.libs.tokens import token_is_valid
import simple_storage.libs.config_loader as config_loader

logger = logging.getLogger(__name__)
config = config_loader.Config()
storage = Storage()


async def get_available_keys(token: str) -> List:
    if config.get(config_loader.USE_AUTH) and not token_is_valid(token):
        logger.warning(f"Incorrect token: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return storage.get_data_keys()
