# Britsa Inc. All Rights Reserved (c) 2021
# service-stash PyPI package

from firebase_admin import credentials, firestore, initialize_app
import logging
import ast

logger = logging.getLogger(__name__)

LOGGER_PREFIX: str = 'Britsa (service-stash): '


def connect_firestore_with_key(collection_name: str, firestore_key: str or dict):
    try:
        logger.debug(
            f"{LOGGER_PREFIX}Establishing connection to Firebase's Firestore")
        cred = credentials.Certificate(ast.literal_eval(firestore_key))
        initialize_app(cred)
    except ValueError:
        logger.info(f"{LOGGER_PREFIX}Firebase's firestore app is initialized already")
    finally:
        database = firestore.client()
        logger.info(f"{LOGGER_PREFIX}Firebase's firestore app is successfully connected")
        document_reference = database.collection(collection_name)
        return document_reference
