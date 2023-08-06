#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import asyncio
import logging
import ssl
from contextlib import suppress
from typing import Dict, List, Optional
from uuid import uuid4

from betterproto.grpc.util.async_channel import AsyncChannel
from grpclib.client import Channel

from .onos_api.onos.e2sub.endpoint import E2RegistryServiceStub, TerminationEndpoint
from .onos_api.onos.e2sub.subscription import (
    Action,
    ActionType,
    E2SubscriptionServiceStub,
    Encoding,
    EventTrigger,
    Payload,
    ServiceModel,
    Subscription,
    SubscriptionDetails,
    SubsequentAction,
    SubsequentActionType,
    TimeToWait,
)
from .onos_api.onos.e2sub.task import E2SubscriptionTaskServiceStub, EventType
from .onos_api.onos.e2t.admin import E2TAdminServiceStub
from .onos_api.onos.e2t.e2 import (
    ControlAckRequest,
    ControlResponse,
    E2TServiceStub,
    EncodingType,
    RequestHeader,
    ServiceModel as E2TServiceModel,
    StreamRequest,
)


class TaskEvent:
    def __init__(self, app_id: str, subscription_id: str, queue: asyncio.Queue) -> None:
        self.app_id = app_id
        self.subscription_id = subscription_id
        self.queue = queue
        self.task: Optional[asyncio.Task] = None
        self.prev_stream: Optional[asyncio.Task] = None

    async def process(self, e2sub_channel: Channel) -> None:
        endpoint_client = E2RegistryServiceStub(e2sub_channel)
        task_client = E2SubscriptionTaskServiceStub(e2sub_channel)

        prev_endpoint_id = None
        async for response in task_client.watch_subscription_tasks(
            subscription_id=self.subscription_id
        ):
            event = response.event
            if event.task.subscription_id != self.subscription_id:
                # Only interested in tasks related to this subscription
                continue
            if event.task.endpoint_id == prev_endpoint_id:
                # Skip if the stream is already open for the associated E2 endpoint
                continue

            if event.type == EventType.NONE or event.type == EventType.CREATED:
                if self.prev_stream is not None:
                    self.prev_stream.cancel()

                prev_endpoint_id = event.task.endpoint_id
                termination = await endpoint_client.get_termination(id=prev_endpoint_id)
                self.prev_stream = asyncio.create_task(
                    self.stream(termination.endpoint)
                )
            elif event.type == EventType.REMOVED:
                prev_endpoint_id = None
                if self.prev_stream is not None:
                    self.prev_stream.cancel()
                    self.prev_stream = None

    async def stream(self, endpoint: TerminationEndpoint) -> None:
        try:
            async with Channel(
                endpoint.ip, endpoint.port, ssl=E2._ssl_context
            ) as channel:
                e2t_client = E2TServiceStub(channel)
                requests: AsyncChannel = AsyncChannel()
                await requests.send_from(
                    [
                        StreamRequest(
                            app_id=self.app_id,
                            subscription_id=self.subscription_id,
                        )
                    ],
                    close=True,
                )
                async for response in e2t_client.stream(requests):
                    await self.queue.put(response.indication_message)
        except Exception:
            logging.exception(f"E2T stream on '{endpoint.ip}:{endpoint.port}' failed")

    async def cancel(self) -> bool:
        if self.task is None or not self.task.cancel():
            return False
        with suppress(asyncio.CancelledError):
            await self.task
            self.task = None

        if self.prev_stream is not None:
            self.prev_stream.cancel()
            with suppress(asyncio.CancelledError):
                await self.prev_stream
                self.prev_stream = None

        return True


class E2:
    _app_id: Optional[str] = None
    _e2t_endpoint: Optional[str] = None
    _e2sub_endpoint: Optional[str] = None
    _e2t_channel: Optional[Channel] = None
    _e2sub_channel: Optional[Channel] = None
    _ssl_context: Optional[ssl.SSLContext] = None
    _subscriptions: Dict[str, TaskEvent] = {}

    @classmethod
    def configure(
        cls,
        app_id: str,
        e2t_endpoint: str,
        e2sub_endpoint: str,
        ca_path: Optional[str] = None,
        cert_path: Optional[str] = None,
        key_path: Optional[str] = None,
        skip_verify: bool = True,
    ) -> None:
        cls._app_id = app_id
        cls._e2t_endpoint = e2t_endpoint
        cls._e2sub_endpoint = e2sub_endpoint

        if ca_path is not None and cert_path is not None and key_path is not None:
            cls._ssl_context = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH, cafile=ca_path
            )
            cls._ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
            cls._ssl_context.check_hostname = not skip_verify

    @classmethod
    async def start(cls) -> None:
        if cls._e2t_endpoint is None or cls._e2sub_endpoint is None:
            raise Exception("E2 client has not been configured")

        e2t_ip, e2t_port = cls._e2t_endpoint.rsplit(":", 1)
        e2sub_ip, e2sub_port = cls._e2sub_endpoint.rsplit(":", 1)
        cls._e2t_channel = Channel(e2t_ip, int(e2t_port), ssl=cls._ssl_context)
        cls._e2sub_channel = Channel(e2sub_ip, int(e2sub_port), ssl=cls._ssl_context)

    @classmethod
    async def stop(cls) -> None:
        if cls._e2t_channel is None or cls._e2sub_channel is None:
            raise Exception("E2 client has not been started")

        cls._e2t_channel.close()
        cls._e2sub_channel.close()
        cls._e2t_channel = None
        cls._e2sub_channel = None

    @classmethod
    async def list_nodes(cls) -> List[str]:
        if cls._e2t_channel is None:
            raise Exception("E2 client has not been started")

        admin_client = E2TAdminServiceStub(cls._e2t_channel)
        return [conn.id async for conn in admin_client.list_e2_node_connections()]

    @classmethod
    async def send_control(
        cls,
        e2_node_id: str,
        service_model_id: str,
        header: bytes,
        message: bytes,
        ack_request: ControlAckRequest = ControlAckRequest.ACK,
    ) -> ControlResponse:
        if cls._e2t_channel is None:
            raise Exception("E2 client has not been started")

        e2t_client = E2TServiceStub(cls._e2t_channel)
        request_header = RequestHeader(
            encoding_type=EncodingType.PROTO,
            service_model=E2TServiceModel(id=service_model_id),
        )
        return await e2t_client.control(
            header=request_header,
            e2_node_id=e2_node_id,
            control_header=header,
            control_message=message,
            control_ack_request=ack_request,
        )

    @classmethod
    async def subscribe(
        cls,
        e2_node_id: str,
        service_model_id: str,
        trigger: bytes,
        queue: asyncio.Queue,
    ) -> str:
        if cls._e2sub_channel is None or cls._app_id is None:
            raise Exception("E2 client has not been started")

        subscription_client = E2SubscriptionServiceStub(cls._e2sub_channel)
        subscription = Subscription(
            id=str(uuid4()),
            app_id=cls._app_id,
            details=SubscriptionDetails(
                e2_node_id=e2_node_id,
                service_model=ServiceModel(id=service_model_id),
                event_trigger=EventTrigger(
                    payload=Payload(encoding=Encoding.ENCODING_PROTO, data=trigger)
                ),
                actions=[
                    Action(
                        id=10,  # unique action ID for this subscription ID
                        type=ActionType.ACTION_TYPE_REPORT,
                        subsequent_action=SubsequentAction(
                            type=SubsequentActionType.SUBSEQUENT_ACTION_TYPE_CONTINUE,
                            time_to_wait=TimeToWait.TIME_TO_WAIT_ZERO,
                        ),
                    )
                ],
            ),
        )

        await subscription_client.add_subscription(subscription=subscription)
        task_event = TaskEvent(cls._app_id, subscription.id, queue)
        cls._subscriptions[subscription.id] = task_event
        task_event.task = asyncio.create_task(task_event.process(cls._e2sub_channel))
        return subscription.id

    @classmethod
    async def unsubscribe(cls, subscription_id: str) -> bool:
        if cls._e2sub_channel is None:
            raise Exception("E2 client has not been started")
        if subscription_id not in cls._subscriptions:
            return False
        subscription = cls._subscriptions[subscription_id]
        if not subscription.cancel():
            return False

        subscription_client = E2SubscriptionServiceStub(cls._e2sub_channel)
        try:
            await subscription_client.remove_subscription(id=subscription_id)
            del cls._subscriptions[subscription_id]
            return True
        except Exception:
            logging.exception(f"Failed to unsubscribe on {subscription_id}")
            return False
