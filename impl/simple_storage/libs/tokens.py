import logging
from typing import List
from simple_storage.libs.storage import Storage
import simple_storage.libs.encryption as encryption
import simple_storage.libs.config_loader as config_loader

logger = logging.getLogger(__name__)
config = config_loader.Config()
storage = Storage()


def get_all_tokens() -> List[str]:
    tokens = storage.get_all_tokens()
    logger.info(f"Tokens list: {tokens}")
    if config.get(config_loader.USE_ENCRYPTION):
        logger.info("Decrypt tokens")
        tokens = [encryption.decrypt(t, config.get(config_loader.ENCRYPTION_KEY).encode()).decode() for t in tokens]
        logger.info(f"Decrypted tokens: {tokens}")
    return tokens


def token_is_valid(token: str) -> bool:
    logger.info(f"Is token {token} exists in token list")
    if token in get_all_tokens():
        logger.info("Token found")
        return True
    logger.info("Incorrect token")
    return False
# a2740fec295d11ecb557acde48001122
