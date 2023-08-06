# Mythic Payload Type Container

The `mythic_payloadtype_container` package creates an easy way to get everything set up in a new PayloadType container for a Mythic supported Payload Type. Mythic is a Command and Control (C2) framework for Red Teaming. The code is on GitHub (https://github.com/its-a-feature/Mythic) and the Mythic project's documentation is on GitBooks (https://docs.mythic-c2.net). This code will be included in the default Mythic Payload Type containers, but is available for anybody making custom containers as well.

## Installation

You can install the mythic scripting interface from PyPI:

```
pip install mythic-payloadtype-container
```

## How to use

Version 0.0.3 of the `mythic_payloadtype_container` package supports version 2.2.* of the Mythic project.

For the main execution of the heartbeat and service functionality, simply import and start the service:
```
from mythic_payloadtype_container import mythic_service
mythic_service.start_service_and_heartbeat()
```

For a Payload types Profile's code to leverage the PayloadType or RPC functionality:
```
from mythic_payloadtype_container import PayloadBuilder
# optionally - from mythic_payloadtype_container.PayloadBuilder import *
from mythic_payloadtype_container import MythicResponseRPC
```
