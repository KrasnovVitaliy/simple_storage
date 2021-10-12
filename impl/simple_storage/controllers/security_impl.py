import logging
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
import simple_storage.libs.config_loader as config_loader

config = config_loader.Config()

logger = logging.getLogger(__name__)


def get_token_bearerAuth(authorization_credentials: HTTPAuthorizationCredentials) -> bool:
    logger.info(f"Received authorization credentials: {authorization_credentials}")
    if authorization_credentials.credentials != config.get(config_loader.MASTER_KEY):
        logger.error(f"Incorrect master key: {authorization_credentials}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
