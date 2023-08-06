from __future__ import annotations
from ehelply_bootstrapper.integrations.integration import Integration
from typing import TYPE_CHECKING
from ehelply_microservice_library.integrations.fact import get_fact_endpoint

from ehelply_bootstrapper.utils.state import State

if TYPE_CHECKING:
    from ehelply_microservice_library.routers.router_service_monitor import Heartbeat

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json


class UsageMQ(BaseModel):
    project_uuid: str
    usage_key: str
    quantity: int


class Monitor(Integration):
    """
    Note integration is used to talk to the ehelply-notes microservice
    """

    def __init__(self) -> None:
        super().__init__("monitor")

        self.m2m = State.integrations.get("m2m")
        self.sqs = State.aws.make_client("sqs")

    def init(self):
        super().init()

    def load(self):
        super().load()

    def get_base_url(self) -> str:
        return get_fact_endpoint('ehelply-monitors')

    def register_service(self):
        """
        Register a new running service/process/thread with the monitor service
        :return:
        """
        pass

    def heartbeat(self, heartbeat: Heartbeat):
        """
        Send a heartbeat over REST
        In general, use the AWS SQS ehelply-monitoring queue to send heartbeats. This is only here in case we need
          to send one manually for some reason
        :param heartbeat:
        :return:
        """
        pass

    def minor_alarm(self):
        """
        Alert the monitoring service to a minor alarm on this microservice
        :return:
        """
        pass

    def major_alarm(self):
        """
        Alert the monitoring service to a major alarm on this microservice
        :return:
        """
        pass

    def critical_alarm(self):
        """
        Alert the monitoring service to a critical alarm on this microservice
        :return:
        """
        pass

    def warning(self):
        """
        Alert the monitoring service to a warning on this microservice
        :return:
        """
        pass

    def clear_alarm(self):
        """
        Alert the monitoring service to a clear alarm on this microservice
        :return:
        """
        pass

    def add_usage(self, usage: UsageMQ) -> bool:
        """
        Add usage to a project

        NOTE: Quantity formats represented by a x10000000 integer. Precision to the millonth

        :return:
        """
        if usage.project_uuid == 'ehelply-resources' or usage.project_uuid == 'ehelply-cloud':
            return False

        self.sqs.send_message(
            QueueUrl=get_fact_endpoint("mq-usage"),
            MessageBody=json.dumps(jsonable_encoder(usage.dict()))
        )

        return True
