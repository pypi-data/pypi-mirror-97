# Jolly Python Client

Python client for [Jolly](https://github.com/whittlbc/jolly) (Janus Orchestration Layer) that adds a layer of 
abstraction around a scalable Janus cluster. It provides load balancing to the Janus instances, can scale up 
the Janus cluster when needed, and keeps track of which sessions are on which instances, and creates resources on 
the most appropriate Janus instance based on the current load of each.

# Requirements

* Python 3+
* A running [Jolly](https://github.com/whittlbc/jolly) cluster

# Installation

```
$ pip install jolly
```

# Setup

Ensure the following environment variables are set and available:

```
export AWS_DEFAULT_REGION="<your-region>"
export AWS_ACCESS_KEY_ID="<your-access-key-id>"
export AWS_SECRET_ACCESS_KEY="<your-secret-access-key>"
```

# Usage

```python
import jolly

# Register a new message against the janus cluster. This will return 
# the IP of the janus instance that Jolly selected to handle this message.
selected_instance_ip = jolly.create_message('<message_id>')

print(selected_instance_ip) # => 1.2.3.4
```

# License

MIT