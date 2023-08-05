import boto3
import os
import json

from enum import Enum

from properly_util_python.properly_logging import ProperLogger


class ProperlyEvents(str, Enum):
    USER_CREATED = 'userCreated'
    STAGE_CHANGED_OFFER = 'stageChangedOffer'
    USER_ENTERED_ALL_OFFER_INFO = 'userEnteredAllOfferInfo'
    SHOWING_UPDATED_OR_CREATED = 'userShowingUpdatedOrCreated'
    HUBSPOT_DEAL_CHANGED = 'hubspotDealChanged'
    DEAL_CHANGED_STAGE = 'dealChangedStage'
    ACCEPTED_OFFER = 'userAcceptedOffer'
    SEARCH_RESULTS_CHANGED = 'searchResultsChanged'
    PPR_FEEDBACK = 'pprFeedback'
    FAVOURITE_ADDED = 'favouriteAdded'
    FAVOURITE_REMOVED = 'favouriteRemoved'
    USER_DEAL_STAGES_CHANGED = 'userDealStagesChanged'
    BEHAVIOUR_TRACK_EVENT = 'behaviourTrackEvent'
    COGNITO_ACCOUNT_MESSAGE = 'cognitoAccountMessage'


class EventBusBase:
    def send_event(self, properly_user_id: str, event_name: ProperlyEvents, data_block_name: str, data_block: dict):
        raise NotImplementedError


class PropertyEvents(str, Enum):
    PROPERTY_VERIFIED_INFO_UPDATED = 'propertyVerifiedInfoUpdated'
    PPR_ESTIMATE_UPDATE = 'pprEstimateUpdated'


class HistoricalPropertyEvents(str, Enum):
    HISTORICAL_PROPERTY_UPDATED = "historicalPropertyUpdated"


class NamedEventBus(EventBusBase):
    def __init__(self, stream_name, kinesis=None, logger=None):
        stage = os.environ.get("PROPERLY_STAGE", "staging")
        self.kinesis = kinesis or boto3.client("kinesis")
        self.stream_name = f"{stage}-{stream_name}"
        self.logger = logger if logger else ProperLogger("NamedEventBus")

    def send_event(self, partition_key: str, event_name: str, data_block_name: str, data_block: dict):
        event_to_send = {
            "eventName": event_name,
            data_block_name: data_block
        }
        self.logger.debug("Sending event", {"event": event_to_send})

        event_as_json = json.dumps(event_to_send)
        event_as_bytes = event_as_json.encode('utf-8')

        # Kinesis data payloads are in bytes in base64 encoded
        self.logger.debug("Event as bytes", {"event_as_bytes": event_as_bytes})
        self.kinesis.put_record(
            StreamName=self.stream_name,
            Data=event_as_bytes,
            PartitionKey=partition_key,
        )


class PropertyEventBus(NamedEventBus):
    """
    This the wrapped up implementation of the event bus for Property records.
    """
    def send_event(self, property_id: str, event_name: PropertyEvents, data_block_name: str, data_block: dict):
        """
        The send event for the Property related buses.
        :param property_id: The Property ID of the record. This is used as the bus partition key.
        :param event_name: The name of the bus event.
        :param data_block_name: The attribute name of the data block.
        :param data_block: The block of data put on the bus.
        """
        super().send_event(
            partition_key=property_id,
            event_name=event_name,
            data_block_name=data_block_name,
            data_block=data_block)


class EventBus(NamedEventBus):
    def __init__(self, kinesis=None, logger=None):
        """
        The default generic event bus handler for "events-002" Kinesis stream.
        """
        super().__init__(stream_name="events-002", kinesis=kinesis, logger=logger)

    def send_event(self, properly_user_id: str, event_name: ProperlyEvents, data_block_name: str, data_block: dict):
        """
        The send event for the default user related buses.
        :param properly_user_id: The user ID of the record.  This is used as the partition key.
        :param event_name: The name of the bus event.
        :param data_block_name: The attribute name of the data block.
        :param data_block: The block of data put on the bus.
        """
        super().send_event(
            partition_key=properly_user_id,
            event_name=event_name,
            data_block_name=data_block_name,
            data_block=data_block)
