

import base64
import logging
import json

logger = logging.getLogger()
logger.level = logging.INFO


class KinesisProperlyFormatError(Exception):
    pass


class KinesisHelper:

    def get_data_objects_from_event(self, kinesis_event: dict):
        data_objects_array = []
        records_array = kinesis_event.get('Records', None)
        if not records_array:
            raise RuntimeError('Incorrect event passed to kinesis processing')

        for record in records_array:
            kinesis_block = record.get('kinesis', None)
            if not kinesis_block:
                raise KinesisProperlyFormatError('Invalid Kinesis record')
            data_string = kinesis_block.get('data', None)
            if not data_string:
                raise KinesisProperlyFormatError('Empty Kinesis event')

            data_bytes = base64.standard_b64decode(data_string)

            data_as_decoded_string = data_bytes.decode("utf-8")

            data_as_object = json.loads(data_as_decoded_string)

            data_objects_array.append(data_as_object)

        return data_objects_array


