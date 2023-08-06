State service tools

    Need STATE_SERVICE_URL & STATE_SERVICE_TOKEN (opt) in env.
    Use var STATE_SERVICE_MOCK to emulate state service

Usage:

```python
import uuid
from state_service_utils import utils, enums


async def test_f(*, order_action: utils.OrderAction, node: str, action_type: enums.ActionSubType, **kwargs):
    print(f"New event: {kwargs}")
    await utils.add_event(
        action=order_action,
        item_id=str(uuid.uuid4()),
        type=enums.EventType.VM.value,
        subtype=enums.EventSubType.CONFIG.value,
        data={'ip': '10.36.134.123', 'flavor': 'large'}
    )
    return {'success': True}


if __name__ == '__main__':
    utils.EventsReceiver(test_f, mq_addr='amqp://guest:guest@localhost/', mq_input_queue='test-queue').run()
```