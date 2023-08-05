# RCP - Random Checksum Protocol

## How to implement
- Have a dict
- Sort alphanumerical
- Concat its keys and values: `key1value1key2value2...`
- Append shared secret
- Append current utc timestamp
- Optional: Add a salt: `saltkey1value1...`
- Hash with SHA512
- Represent the hash as hex

## How to use

**Get checksum**

```python
from rc_protocol import get_checksum

SHARED_SECRET = "s3cr3t_p@ssw0rd"

my_dict = {
    "key1": "value1",
    "key2": "value2"
}

my_dict["checksum"] = get_checksum(my_dict, SHARED_SECRET)
```

**Validate checksum**

```python
from rc_protocol import validate_checksum

SHARED_SECRET = "s3cr3t_p@ssw0rd"

my_dict = {
    "key1": "value1",
    "key2": "value2",
    "checksum": "d0690e3c924e18bad866e2867698be75f64bdc6e809b76ffedb5c5095c9fbe15d36636b2df1fc47d2a3f348aea272ffc2fed4dc8ee08e0d13631ef646e1648c4"
}

if validate_checksum(my_dict, SHARED_SECRET):
    do_random_things()
else:
    print("You shall not pass.")
```

