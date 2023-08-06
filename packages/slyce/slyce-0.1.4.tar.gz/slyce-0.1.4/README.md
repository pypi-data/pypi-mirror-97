## Slyce

Client for calling Slyce API.

#### Quickstart

```python
import asyncio
import os

from slyce import SlyceClient
from slyce.exception import SlyceError

os.environ['SLYCE_APPLICATION_CREDENTIALS'] = '/some/path/to/creds'

FINGERPRINT= 'UNIQUE_USER_IDENTIFIER'  # Optional
IMAGE_PATH = '/some/path/to/image'
WORKFLOW_ID = 'WORKFLOW_ID'

async def main(loop):
    with SlyceClient(fingerprint=FINGERPRINT) as slyce:
        try:
            image_id = await slyce.upload_image(IMAGE_PATH)
            res = await slyce.execute_workflow(WORKFLOW_ID, image_id=image_id)
            if res.get('data'):
                data = res['data']
                print(f"Type: {data['type']}")
                print(f"Operation: {data['operation']}")
                if data.get('results'):
                    print(f"First Result: {json.dumps(data['results'][0], indent=2)}")
        except SlyceError as e:
            print(e)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
```