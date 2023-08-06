import asyncio
import os
import traceback
from dataclasses import dataclass
from functools import partial
from logging import LoggerAdapter

import aiohttp
import simplejson as json
from aio_pika import connect_robust, IncomingMessage, Exchange, Message, DeliveryMode

from .enums import ActionType, ActionStatus, ActionDeploy, EventType, EventSubType
from .exceptions import StateServiceException
from .logging import logger

STATE_SERVICE_URL = os.getenv('STATE_SERVICE_URL')
STATE_SERVICE_TOKEN = os.getenv('STATE_SERVICE_TOKEN')
STATE_SERVICE_MOCK = os.getenv('STATE_SERVICE_MOCK')


@dataclass
class OrderAction:
    order_id: str
    action_id: str
    graph_id: str


if not STATE_SERVICE_URL and not os.getenv('DEBUG'):
    raise StateServiceException('Configuration error, STATE_SERVICE_URL required')


async def _make_request(url, data: dict):
    headers = {}
    if STATE_SERVICE_TOKEN:
        headers['Authorization'] = f'Token {STATE_SERVICE_TOKEN}'

    if STATE_SERVICE_MOCK:
        return {}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=data, ssl=False) as response:
            if response.status == 400:
                raise StateServiceException(await response.json())
            elif response.status != 201:
                raise StateServiceException(f'State service request error ({response.status}): {await response.text()}')


async def add_action_event(*, action: OrderAction, type: ActionType, subtype: ActionDeploy, status='', data=None):
    data = {
        'type': type,
        'subtype': subtype,
        'status': status,
        'data': data
    }
    data.update(action.__dict__)
    await _make_request(
        url=f'{STATE_SERVICE_URL}/actions/',
        data=data
    )


async def add_event(*, action: OrderAction, item_id: str,
                    type: EventType, subtype: EventSubType, status='', data=None):
    data = {
        'item_id': item_id,
        'type': type,
        'subtype': subtype,
        'status': status,
        'data': data
    }
    data.update(action.__dict__)
    await _make_request(
        url=f'{STATE_SERVICE_URL}/events/',
        data=data
    )


def state_action_decorator(func):
    async def wrapper(*, order_action: OrderAction, node, action_type=ActionDeploy.RUN_NODE.value, task_logger,
                      **kwargs):
        await add_action_event(
            action=order_action,
            type=ActionType.DEPLOY.value,
            subtype=action_type,
            status=f'{node}:{ActionStatus.STARTED.value}',
            data=kwargs
        )
        try:
            if action_type not in ActionDeploy._value2member_map_.keys():
                raise StateServiceException(f'Invalid action type: {action_type}')
            result = await func(
                **kwargs,
                order_action=order_action,
                node=node,
                action_type=action_type,
                task_logger=task_logger
            )
            status = f'{node}:{ActionStatus.COMPLETED.value}'
        except Exception as e:
            tb = traceback.format_exc()
            result = {
                'error': str(e),
                'traceback': tb}
            status = f'{node}:{ActionStatus.ERROR.value}'
            task_logger.error(
                f"Error in action ({status}): {tb}")
        await add_action_event(
            action=order_action,
            type=ActionType.DEPLOY.value,
            subtype=action_type,
            status=status,
            data=result
        )
        return result

    return wrapper


class EventsReceiver:
    def __init__(self, fn, mq_addr, mq_input_queue):
        self.mq_addr = mq_addr
        self.input_queue = mq_input_queue
        self.fn = state_action_decorator(fn)
        self.logger = logger

    async def on_message(self, message: IncomingMessage, exchange: Exchange):

        with message.process():
            data = json.loads(message.body)

            if not isinstance(data, dict):
                raise StateServiceException('Invalid message (need struct): %s', data)

            order_action = OrderAction(
                order_id=data.pop('_order_id'),
                action_id=data.pop('_action_id'),
                graph_id=data.pop('_graph_id'))
            node = data['_name']
            action_type = data.get('_type')

            task_logger = LoggerAdapter(logger, extra={
                'order_action': order_action.__dict__,
                'node': node,
                'action_type': action_type,
                'orchestrator_id': data.get('_id')
            })

            response = await self.fn(
                order_action=order_action,
                node=node,
                action_type=action_type,
                task_logger=task_logger,
                **data,
            )
            await exchange.publish(
                Message(body=json.dumps(response).encode(), content_type="application/json",
                        correlation_id=message.correlation_id, delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=message.reply_to,
            )

    async def _receive(self, loop, addr, queue_name, queue_kwargs, prefetch_count=None):
        connection = await connect_robust(addr, loop=loop)
        channel = await connection.channel()
        if prefetch_count:
            await channel.set_qos(prefetch_count=prefetch_count)
        queue = await channel.declare_queue(queue_name, **(queue_kwargs or {}), durable=True)
        await queue.consume(partial(self.on_message, exchange=channel.default_exchange))

    def run(self, queue_kwargs: dict = None, prefetch_count: int = None):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._receive(
            loop, addr=self.mq_addr, queue_name=self.input_queue,
            queue_kwargs=queue_kwargs,
            prefetch_count=prefetch_count
        ))
        loop.run_until_complete(task)
        logger.info('Awaiting events')
        try:
            loop.run_forever()
        except (SystemExit, KeyboardInterrupt):
            logger.info('Sever stopped')


def items_from_events(events, serializer=None):
    items = {}

    # ASC to DESC
    events_for_source = events.copy()
    events_for_source.reverse()
    for event in events_for_source:
        if not serializer:
            # event is dict
            if (item_id := str(event['item_id'])) not in items:
                items[item_id] = event
        else:
            if (item_id := str(event.item_id)) not in items:
                items[item_id] = serializer(instance=event).data

    for event in events:
        if serializer:
            # we can use separate serializer, but it's overhead
            item_id = str(event.item_id)
            key = event.subtype
            status = event.status
            data = event.data
        else:
            item_id = event['item_id']
            key = event['subtype']
            status = event.pop('status', None)
            data = event.pop('data', None)
        if status and data:
            # items[item_id][f'{key}_status'] = status
            # items[item_id][f'{key}_data'] = data
            raise Exception(f'Event has both keys: status & data')
        else:
            items[item_id][key] = status or data

    return list(items.values())
