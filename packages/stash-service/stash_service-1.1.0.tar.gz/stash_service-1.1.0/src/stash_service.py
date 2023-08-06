# Britsa Inc. All Rights Reserved (c) 2021
# service-stash PyPI package

from firebase_admin import credentials, firestore, initialize_app
from enum import Enum
import ast

from rest_framework.response import Response
import os
import logging
from dotenv import load_dotenv

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


class HttpStatusCode(Enum):

    # INFORMATIONAL RESPONSES (100–199)
    CONTINUE =(100, 'Information Response - Continue')
    SWITCHING_PROTOCOL =(101, 'Information Response - Switching protocol')
    PROCESSING = (102, 'Information Response - Processing')
    EARLY_HINTS = (103, 'Information Response - Early hints')

    # SUCCESSFUL RESPONSES (200–299)
    OK = (200,'Successful Responce - Ok')
    CREATED = (201,'Successful Responce - Created')
    ACCEPTED = (202,'Successful Responce - Accepted')
    NON_AUTHORITATIVE_INFORMATION = (203,'Successful Responce - Non authoritative information')
    NO_CONTENT = (204,'Successful Responce - No content')
    RESET_CONTENT = (205,'Successful Responce - Reset content')
    PARTIAL_CONTENT = (206,'Successful Responce - Partial content')
    MULTI_STATUS = (207,'Successful Responce - Multi status')
    ALREADY_REPORTED = (208,'Successful Responce - Already reported')
    IM_USED = (226,'Successful Responce - Im used')

    # REDIRECTS (300–399)
    MULTIPLE_CHOICE = (300,'Redirects - Multiple choice')
    MOVED_PERMANENTLY = (301,'Redirects - Moved permanently')
    FOUND = (302,'Redirects - Found')
    SEE_OTHER = (303,'Redirects - See other')
    NOT_MODIFIED = (304,'Redirects - Not modified')
    USE_PROXY = (305,'Redirects - Use proxy')
    UNUSED = (306,'Redirects - Unused')
    TEMPORARY_REDIRECT = (307,'Redirects - Temporary redirect')
    PERMANENT_REDIRECT = (308,'Redirects - Permanent redirect')

    # CLIENT ERRORS (400–499)
    BAD_REQUEST = (400,'Client Error - Bad request')
    UNAUTHORIZED = (401,'Client Error - Unauthorized')
    PAYMENT_REQUIRED = (402,'Client Error - Payment required')
    FORBIDDEN = (403,'Client Error - Forbidden')
    NOT_FOUND = (404,'Client Error - Not found')
    METHOD_NOT_ALLOWED = (405,'Client Error - Method not allowed')
    NOT_ACCEPTABLE = (406,'Client Error - Not acceptable')
    PROXY_AUTHENTICATION_REQUIRED = (407,'Client Error - Proxy authentication required')
    REQUEST_TIMEOUT = (408,'Client Error - Request timeout')
    CONFLICT = (409,'Client Error - Conflict')
    GONE = (410,'Client Error - Gone')
    LENGTH_REQUIRED = (411,'Client Error - Length required')
    PRECONDITION_FAILED = (412,'Client Error - Precondition failed')
    PAYLOAD_TOO_LARGE = (413,'Client Error - Payload too large')
    URI_TOO_LONG = (414,'Client Error - URI too long')
    UNSUPPORTED_MEDIA_TYPE = (415,'Client Error - Unsupported Media type')
    REQUESTED_RANGE_NOT_SATISFIABLE = (416,'Client Error - Requested range not satisfiable')
    EXPECTATION_FAILED = (417,'Client Error - Expectation failed')
    IM_A_TEAPOT = (418,'Client Error - Im a teapot')
    MISDIRECTED_REQUEST = (421,'Client Error - Misdirected request')
    UNPROCESSABLE_ENTITY = (422,'Client Error - Unprocessable entity')
    LOCKED = (423,'Client Error - Locked')
    FAILED_DEPENDENCY = (424,'Client Error - Failed dependency')
    TOO_EARLY = (425,'Client Error - Too early')
    UPGRADE_REQUIRED = (426,'Client Error - Upgrade required')
    PRECONDITION_REQUIRED = (428,'Client Error - Precondition required')
    TOO_MANY_REQUESTS = (429,'Client Error - Too many requests')
    REQUEST_HEADER_FIELDS_TOO_LARGE = (431,'Client Error - Request header fields too large')
    UNAVAILABLE_FOR_LEGAL_REASONS = (451,'Client Error - Unavailable for legal reasons')

    # SERVER ERRORS (500–599)
    INTERNAL_SERVER_ERROR = (500,'Server Error - Internal server error')
    NOT_IMPLEMENTED = (501,'Server Error - Not implemented')
    BAD_GATEWAY = (502,'Server Error - Bad gateway')
    SERVICE_UNAVAILABLE = (503,'Server Error - Service unavailable')
    GATEWAY_TIMEOUT = (504,'Server Error - Gateway timeout')
    HTTP_VERSION_NOT_SUPPORTED = (505,'Server Error - Http version not supported')
    VARIANT_ALSO_NEGOTIATES = (506,'Server Error - Variant also negotiates')
    INSUFFICIENT_STORAGE = (507,'Server Error - Insufficient storage')
    LOOP_DETECTED = (508,'Server Error - Loop detected')
    NOT_EXTENDED = (510,'Server Error - Not extended')
    NETWORK_AUTHENTICATION_REQUIRED = (511,'Server Error - Network authentication required')

    def status_code(self) -> int:
        return self.value[0]

    def status_message(self) -> str:
        return self.value[1]
# AppResponseCodes
class AppResponseCodes(Enum):
    ERROR_OCCURRED = (1000, 'Some error occurred in the code')
    REQUIRED_PARAMETER_NOT_FOUND = (1001, 'Required parameter not found in the request')
    UNAUTHORIZED_REQUEST = (1002, 'Unauthorized request found')

    # App Utils error codes
    ENVIRONMENT_NOT_FOUND = (1010, 'Required environment not found.')
    VERSION_NOT_AVAILABLE = (1011, 'Requested version is not available.')

    def log(self) -> str:
        log_format: str = '{0} - {1}'
        return log_format.format(self.error_code(), self.error_message())

    def error_code(self) -> int:
        return self.value[0]

    def error_message(self) -> str:
        return self.value[1]


class App_Exception(Exception):
    def _init_(self, app_response_code: AppResponseCodes, message: str or None = None,
                   validation_error: bool = False) -> None:
            super(App_Exception, self)._init_(app_response_code.error_message())

            if not message:
                message = ''
            else:
                message = f' [msg= {message}]'

            self.__app_response_statement: str = f'{app_response_code.error_message()}{message} ({app_response_code.error_code()})'
            logger.error(f'Exception raised on {self.__app_response_statement}')

            if validation_error:
                self.__http_code: HttpStatusCode = HttpStatusCode.INVALID_INPUT_PARAMETERS
            else:
                self.__http_code: HttpStatusCode = HttpStatusCode.INTERNAL_SERVER_ERROR

    def response(self) -> Response:
            logger.error(
                f'{self._http_code.status_code()} {self.http_code.status_message()} error response out for {self._app_response_statement})')
            error_response_object: dict = {
                'error_description': self.__http_code.status_message(),
            }
            return Response(error_response_object, status=self.__http_code.status_code())


def get_env(key: str) -> str or App_Exception:
        response_value: str or None = os.environ.get(key)
        if response_value:
            response_value = str(response_value)
            return response_value
        else:
            logger.warning('Application loading .env file')
            load_dotenv()
            logger.info('.env loaded successfully.')
            response_value = os.environ.get(key)
            if response_value:
                response_value = str(response_value)
                return response_value
        raise App_Exception(AppResponseCodes.ENVIRONMENT_NOT_FOUND, message=key, validation_error=False)

class Logger(object):
    def __init__(self, LOG_TAG: str) -> None:
        self.__tag = LOG_TAG

    def debug(self, new_tag: str, message: str) -> None:
        logging.getLogger(new_tag).debug(message)

    def debug(self, message: str) -> None:
        self.debug(new_tag=self.__tag, message=message)

    def info(self, new_tag: str, message: str) -> None:
        logging.getLogger(new_tag).info(message)

    def info(self, message: str) -> None:
        self.info(new_tag=self.__tag, message=message)

    def warn(self, new_tag: str, message: str) -> None:
        logging.getLogger(new_tag).warning(message)

    def warn(self, message: str) -> None:
        self.warn(new_tag=self.__tag, message=message)

    def error(self, new_tag: str, message: str) -> None:
        logging.getLogger(new_tag).error(message)

    def error(self, message: str) -> None:
        self.error(new_tag=self.__tag, message=message)