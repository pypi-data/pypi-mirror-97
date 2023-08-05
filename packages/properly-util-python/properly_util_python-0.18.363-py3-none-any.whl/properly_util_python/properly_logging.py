import logging
import os
from typing import Any, Dict, Optional, Union

import orjson


STANDARD_OFFER_ID = "offer_id"
STANDARD_USER_ID = "user_id"
STANDARD_PROPERTY_ID = "property_id"
STANDARD_LISTING_ID = "listing_id"
STANDARD_GOOGLE_PLACE_ID = "google_place_id"

STANDARD_FORMAT_MAPPER = {
    "offerID": STANDARD_OFFER_ID,
    "offerId": STANDARD_OFFER_ID,
    "userID": STANDARD_USER_ID,
    "userId": STANDARD_USER_ID,
    "propertyID": STANDARD_PROPERTY_ID,
    "propertyId": STANDARD_PROPERTY_ID,
    "listingID": STANDARD_LISTING_ID,
    "listingId": STANDARD_LISTING_ID,
    "placeID": STANDARD_GOOGLE_PLACE_ID,
    "placeId": STANDARD_GOOGLE_PLACE_ID,
    "place_id": STANDARD_GOOGLE_PLACE_ID,
    "googlePlaceID": STANDARD_GOOGLE_PLACE_ID,
    "location_place_id": STANDARD_GOOGLE_PLACE_ID,
}

KeyTypes = Union[int, str]


def _standardize_tags(tags: Optional[Dict[KeyTypes, Any]]) -> Dict[str, Any]:
    standardized_tags = {}
    if not tags:
        return standardized_tags

    for key, value in tags.items():
        string_key = key
        if isinstance(key, int):
            string_key = str(key)

        if string_key in STANDARD_FORMAT_MAPPER:
            standardized_tags[STANDARD_FORMAT_MAPPER[string_key]] = value
        else:
            standardized_tags[string_key] = value

    return standardized_tags


def orjson_default(obj):
    return str(obj)


class ProperLogger:

    def __init__(self, log_location: str, common_tags: Dict[KeyTypes, Any] = None, logger=None):
        """
        Initialize the logger with the basic tags we want logged in every message
        :param log_location: a name for the logical area of code where the log messages are
        being made from. Often this will be the class name like ProperLogger or the filename.
        This isn't auto-generated because the idea is that this is human understandable. The caller
        could pass in __name__ if they so wish.
        :param common_tags: any extra tags that will be added to any subsequent logs
        :param logger: rather than instantiate the logger you can pass one in
        """
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(log_location)

        try:
            level = int(os.environ.get('PROPERLY_LOG_LEVEL', logging.INFO))
        except ValueError:
            level = logging.INFO
        self.logger.level = level

        properly_env = os.environ.get('PROPERLY_STAGE', 'local')
        # Sorting has a performance hit so we only do it outside of prod for test consistency and easier debugging
        self.json_option = orjson.OPT_SORT_KEYS

        self.base_tags = {"log_location": log_location}
        if common_tags:
            self.base_tags = {
                **_standardize_tags(common_tags),
                **self.base_tags
            }

    def _log_with_base_tags(self, level: int, log: Dict[str, Any]):
        self.logger.log(level, orjson.dumps({
            **self.base_tags,
            **log,
        }, option=self.json_option, default=orjson_default))

    def add_common_tags(self, common_tags: Dict[KeyTypes, Any]):
        """
        Add common tags that will continue to be added to subsequent logs
        Replaces any existing tags with the same key
        :param common_tags: extra tags that will be added to any subsequent logs
        """
        self.base_tags = {
            **self.base_tags,
            **_standardize_tags(common_tags),
        }

    def clear_common_tags(self):
        """
        Clears all common tags except log_location
        """
        self.base_tags = {
            "log_location": self.base_tags.get("log_location"),
        }

    def debug(self, message: str, extra_tags: Dict[KeyTypes, Any] = None):
        """
        Log a message along with any tags at a level that will default to being
        ignored in production
        :param message: the message
        :param extra_tags: any extra tags to attach to the log
        """
        extra_tags = _standardize_tags(extra_tags)

        self._log_with_base_tags(logging.DEBUG, {
            **extra_tags,
            "message": message,
        })

    def info(self, message: str, extra_tags: Dict[KeyTypes, Any] = None):
        """
        Log a message along with any tags
        Because of the unstructured nature of this log be considerate about the
        frequency of messages or consider using debug level logging to make it easier
        to silence
        :param message: the message
        :param extra_tags: any extra tags to attach to the log
        """
        extra_tags = _standardize_tags(extra_tags)

        self._log_with_base_tags(logging.INFO, {
            **extra_tags,
            "message": message,
        })

    def metric(self, name: str, value: Any, extra_tags: Dict[KeyTypes, Any] = None):
        """
        Log a metric that can easily be monitored in cloudwatch insights
        :param name: the metric name
        :param value: the metric value
        :param extra_tags: any extra tags to attach to the log
        """
        extra_tags = _standardize_tags(extra_tags)

        self._log_with_base_tags(logging.INFO, {
            **extra_tags,
            "metric_name": name,
            "metric_value": value,
        })

    def warning(self, name: str, message: str, extra_tags: Dict[KeyTypes, Any] = None):
        """
        Log a warning in a structure format that makes it easy to count warnings
        Warnings should be used instead of errors when the severity of the issue is
        smaller but still useful to track
        :param name: the warning name
        :param message: the warning message
        :param extra_tags: any extra tags to attach to the warning log
        """
        extra_tags = _standardize_tags(extra_tags)

        self._log_with_base_tags(logging.WARNING, {
            **extra_tags,
            "warning_name": name,
            "warning_message": message,
        })

    def error(self, name: str, message: str, extra_tags: Dict[KeyTypes, Any] = None):
        """
        Log an error in a structure format that makes it easy to count errors
        :param name: the error name
        :param message: the error message
        :param extra_tags: any extra tags to attach to the error log
        """
        extra_tags = _standardize_tags(extra_tags)

        self._log_with_base_tags(logging.ERROR, {
            **self.base_tags,
            **extra_tags,
            "error_name": name,
            "error_message": message,
        })

    def exception(self, name: str, message: str, extra_tags: Dict[KeyTypes, Any] = None):
        """
        Log an exception in a structured format which will also include a stack trace
        :param name: the exception name
        :param message: the exception message
        :param extra_tags: any extra tags to attach to the exception log
        """
        extra_tags = _standardize_tags(extra_tags)

        self.logger.exception(orjson.dumps({
            **self.base_tags,
            **extra_tags,
            "exception_name": name,
            "exception_message": message,
        }, option=self.json_option, default=orjson_default))
