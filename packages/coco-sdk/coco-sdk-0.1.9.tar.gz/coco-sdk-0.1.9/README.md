# CoCoHub SDK to use components in python code

https://www.conversationalcomponents.com

[![asciicast](https://asciinema.org/a/291261.svg)](https://asciinema.org/a/291261)

## Installation
```bash
pip install coco-sdk
```
#### With async support
```bash
pip install coco-sdk[async]
```

## Usage
```python
import coco
import uuid

session_id = str(uuid.uuid4()) # generate a random session id

# directly calling exchange:
response = coco.exchange("namer_vp3", session_id, user_input="hello") # namer_vp3 is CoCoHub component

# using ConversationalComponent API
comp = coco.ConversationalComponent("namer_vp3")
response = comp(session_id, "hello")

# using ComponentSession API
session_with_component = coco.ComponentSession("namer_vp3") 
response = session_with_component("hello")
```

#### Async
```python
import coco.async_api as coco

# directly calling exchange:
response = await coco.exchange("namer_vp3", session_id, user_input="hello") # namer_vp3 is CoCoHub component

# using ConversationalComponent API
comp = coco.ConversationalComponent("namer_vp3")
response = await comp(session_id, "hello")

# using ComponentSession API
session_with_component = coco.ComponentSession("namer_vp3") 
response = await session_with_component("hello")
```